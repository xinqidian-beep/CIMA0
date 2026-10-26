import os
import sys
import json
import argparse
from collections import Counter, defaultdict

import numpy as np
import cv2

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from archive.planet import Planet
from core.internal_dynamics.cloud import PlanetField
from core.internal_dynamics.internal_dynamics import InternalDynamics
from core.observer.internal_dynamics_observer import InternalDynamicsObserver
from core.internal_dynamics.cache.observation_cache import ObservationCache
from core.internal_dynamics.attention.attention_field import AttentionField
from core.compute_system.compute_system import ComputeSystem
from core.compute_system.sampling.sampler import Sampler
from core.internal_dynamics.cloud_collision import CloudCollision
from core.io.transport import TransportRouter
from core.terminal.camera.camera_observer import CameraObserver
from core.io.camera_io import CameraIO
from core.internal_dynamics.organs.clip_field import CLIPField

CLIP_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLIP_WEIGHT = os.path.join(CLIP_BASE_DIR, "models", "open_clip_pytorch_model.bin")


def build_system():
    planet_rule = Planet(size=128)
    planet = PlanetField(planet_rule)
    observation_cache = ObservationCache()
    sampler = Sampler()
    compute = ComputeSystem(capacity=1024, sampler=sampler)
    collision = CloudCollision()
    observer = InternalDynamicsObserver()
    attention_field = AttentionField()
    transport = TransportRouter()

    dynamics = InternalDynamics(
        planet=planet,
        compute=compute,
        collision=collision,
        observer=observer,
        observation_cache=observation_cache,
        attention_field=attention_field,
    )

    clip_field = CLIPField(weight_path=CLIP_WEIGHT, sampler=sampler)
    dynamics.register("clip", clip_field)

    camera_observer = CameraObserver()
    transport.subscribe("camera_raw", dynamics)
    transport.subscribe("camera_observation", dynamics)
    transport.subscribe("internal_drive", camera_observer)

    camera_io = CameraIO()

    return {
        "planet": planet,
        "compute": compute,
        "collision": collision,
        "transport": transport,
        "dynamics": dynamics,
        "camera_observer": camera_observer,
        "camera_io": camera_io,
        "clip_field": clip_field,
    }


def extract_coordinate(coord):
    if coord is None:
        return None
    if isinstance(coord, dict):
        return (
            coord.get("layer"),
            coord.get("token"),
            coord.get("dimension"),
        )
    return None


def probe(steps=1000, print_every=100, log_dir=r"C:\temp\cima0_spark_test"):
    os.makedirs(log_dir, exist_ok=True)

    system = build_system()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("camera open failed")
        return

    records = []
    zero_state_count = 0
    previous_winner = None
    winner_switch_count = 0

    for step in range(steps):
        ret, frame = cap.read()
        if ret and frame is not None:
            camera_state = {"field": frame}
            raw_packet = system["camera_io"].encode(camera_state)
            if raw_packet is not None:
                obs_packet = system["camera_observer"].observe(raw_packet)
                if obs_packet is not None:
                    system["transport"].publish(obs_packet)

        snapshot, drive_packet = system["dynamics"].step()
        if drive_packet is not None:
            system["transport"].publish(drive_packet)

        collision_result = getattr(system["collision"], "last_result", None) or {}
        collision_count = 0
        if isinstance(collision_result, dict):
            collision_count = collision_result.get("collision_result", {}).get("count", 0)

        clip_act = 0.0
        clip = system["dynamics"].organs.get("clip")
        if clip is not None and hasattr(clip, "activity"):
            c = clip.activity()
            if isinstance(c, dict):
                clip_act = float(c.get("activity", 0.0))

        planet_act = 0.0
        p = system["planet"].activity()
        if isinstance(p, dict):
            planet_act = float(p.get("activity", 0.0))

        cloud_count = len(system["dynamics"].cloud_state.snapshot())

        winner_layer = getattr(system["clip_field"], "winner_layer", None)
        matrix_coordinate = extract_coordinate(
            getattr(system["clip_field"], "matrix_coordinate", None)
        )

        #
        # zero-state
        #
        if winner_layer is None:
            zero_state_count += 1

        #
        # winner switch
        #
        if (
            previous_winner is not None
            and winner_layer is not None
            and winner_layer != previous_winner
        ):
            winner_switch_count += 1

        previous_winner = winner_layer

        records.append({
            "step": step,
            "response_count": collision_count,
            "planet_activity": planet_act,
            "clip_activity": clip_act,
            "collision_count": collision_count,
            "cloud_count": cloud_count,
            "winner_layer": winner_layer,
            "matrix_coordinate": matrix_coordinate,
        })

        if step % print_every == 0:
            print(
                f"step={step} "
                f"planet_activity={planet_act:.6f} "
                f"clip_activity={clip_act:.6f} "
                f"collision_count={collision_count} "
                f"cloud_count={cloud_count} "
                f"winner_layer={winner_layer} "
                f"coord={matrix_coordinate} "
                f"zero={zero_state_count} "
                f"switch={winner_switch_count}"
            )

    cap.release()
    cv2.destroyAllWindows()

    with open(os.path.join(log_dir, "records.json"), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    analyze(records, zero_state_count, winner_switch_count, log_dir)


def analyze(records, zero_state_count, winner_switch_count, log_dir):
    results = {}

    #
    # 1. power-law avalanche
    #
    response_counts = [r["response_count"] for r in records if r["response_count"] > 0]
    if response_counts:
        counter = Counter(response_counts)
        sizes = sorted(counter.keys())
        freqs = [counter[s] for s in sizes]
        results["avalanche"] = {"sizes": sizes, "freqs": freqs}
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            plt.figure()
            plt.loglog(sizes, freqs, "o-")
            plt.xlabel("response_count")
            plt.ylabel("frequency")
            plt.title("Power-law avalanche")
            plt.savefig(os.path.join(log_dir, "avalanche.png"))
            plt.close()
        except Exception as e:
            print("avalanche plot failed:", e)

    #
    # 2. dynamic coupling
    #
    try:
        from scipy.stats import spearmanr
        planet_acts = [r["planet_activity"] for r in records]
        clip_acts = [r["clip_activity"] for r in records]
        if len(planet_acts) > 2:
            corr, p = spearmanr(planet_acts, clip_acts)
            results["coupling"] = {"spearman": float(corr), "p": float(p)}
    except Exception as e:
        print("spearman failed:", e)

    #
    # 3. history path dependence
    #
    winners = [r["winner_layer"] for r in records if r["winner_layer"] is not None]
    if winners:
        transitions = defaultdict(lambda: defaultdict(int))
        for a, b in zip(winners[:-1], winners[1:]):
            transitions[a][b] += 1
        results["markov"] = {str(k): dict(v) for k, v in transitions.items()}
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            labels = sorted(set(winners))
            matrix = np.zeros((len(labels), len(labels)))
            for i, a in enumerate(labels):
                for j, b in enumerate(labels):
                    matrix[i, j] = transitions[a][b]
            plt.figure()
            plt.imshow(matrix, cmap="Blues")
            plt.xticks(range(len(labels)), labels)
            plt.yticks(range(len(labels)), labels)
            plt.title("Markov transition (winner_layer)")
            plt.colorbar()
            plt.savefig(os.path.join(log_dir, "markov.png"))
            plt.close()
        except Exception as e:
            print("markov plot failed:", e)

    #
    # 4. nonlinear resilience
    #
    results["cloud_counts"] = [r["cloud_count"] for r in records]

    #
    # zero-state (one perspective)
    #
    results["zero_state_count"] = int(zero_state_count)
    results["zero_state_ratio"] = float(zero_state_count / max(1, len(records)))

    #
    # clip_activity variance (another perspective)
    #
    clip_acts = [r["clip_activity"] for r in records]
    if clip_acts:
        results["clip_activity_variance"] = float(np.var(clip_acts))
        results["clip_activity_mean"] = float(np.mean(clip_acts))

    #
    # winner switch frequency (another perspective)
    #
    results["winner_switch_count"] = int(winner_switch_count)
    results["winner_switch_rate"] = float(
        winner_switch_count / max(1, len(records))
    )

    with open(os.path.join(log_dir, "analysis.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("analysis saved to", log_dir)
    print("zero_state_count =", zero_state_count)
    print("zero_state_ratio =", results["zero_state_ratio"])
    print("clip_activity_variance =", results.get("clip_activity_variance"))
    print("winner_switch_count =", winner_switch_count)
    print("winner_switch_rate =", results["winner_switch_rate"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--print-every", type=int, default=100)
    parser.add_argument("--log-dir", type=str, default=r"C:\temp\cima0_spark_test")
    args = parser.parse_args()

    probe(
        steps=args.steps,
        print_every=args.print_every,
        log_dir=args.log_dir,
    )


if __name__ == "__main__":
    main()