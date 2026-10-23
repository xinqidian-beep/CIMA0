import os
import sys
import json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cv2

from archive.planet import Planet
from core.internal_dynamics.cloud import PlanetField
from core.internal_dynamics.internal_dynamics import InternalDynamics
from core.observer.internal_dynamics_observer import InternalDynamicsObserver
from core.internal_dynamics.cache.observation_cache import ObservationCache
from core.internal_dynamics.attention.attention_field import AttentionField
from core.compute_system.compute_system import ComputeSystem
from core.compute_system.sampling.sampler import Sampler
from core.internal_dynamics.cloud_collision import CloudCollision
from core.io.display_io import DisplayIO
from core.io.transport import TransportRouter
from core.terminal.camera import CameraPlanet, CameraObserver
from core.io.camera_io import CameraIO
from core.internal_dynamics.organs.clip_field import CLIPField


LOG_DIR = r"C:\temp\cima0_spark_test"
CLIP_WEIGHT = os.path.join(ROOT, "models", "open_clip_pytorch_model.bin")
TOTAL_STEPS = 1000


def main():
    os.makedirs(LOG_DIR, exist_ok=True)

    #
    # init (copied from main.py)
    #
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
    display = DisplayIO()
    clip_field = CLIPField(weight_path=CLIP_WEIGHT, sampler=sampler)
    dynamics.register("clip", clip_field)

    transport.subscribe("camera_raw", dynamics)
    transport.subscribe("camera_observation", dynamics)
    transport.subscribe("visual", display)

    camera_io = CameraIO()
    camera_observer = CameraObserver()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera_available = cap.isOpened()

    if not camera_available:
        print("camera open failed, running without camera")

    #
    # record
    #
    records = []

    for step in range(TOTAL_STEPS):
        if camera_available:
            ret, frame = cap.read()
            if ret and frame is not None:
                camera_state = {"field": frame}
                raw_packet = camera_io.encode(camera_state)
                if raw_packet is not None:
                    observation_packet = camera_observer.observe(raw_packet)
                    if observation_packet is not None:
                        transport.publish(observation_packet)

        dynamics.step()

        snapshot = dynamics.snapshot()

        #
        # extract four indicators
        #
        collision_result = getattr(collision, "last_result", None) or {}
        response_count = 0
        if isinstance(collision_result, dict):
            response_count = collision_result.get("collision_result", {}).get("count", 0)

        clip_act = 0.0
        clip_state = clip_field.activity() if hasattr(clip_field, "activity") else {}
        if isinstance(clip_state, dict):
            clip_act = float(clip_state.get("activity", 0.0))

        planet_delta = 0.0
        if hasattr(planet, "previous_state") and planet.previous_state is not None:
            planet_delta = float(np.mean(np.abs(planet.state - planet.previous_state)))

        winner_layer = getattr(clip_field, "winner_layer", None)

        cloud_count = len(dynamics.cloud_state.snapshot())

        records.append({
            "step": step,
            "response_count": response_count,
            "clip_activity": clip_act,
            "planet_delta": planet_delta,
            "winner_layer": winner_layer,
            "cloud_count": cloud_count,
        })

    if camera_available:
        cap.release()
    cv2.destroyAllWindows()

    #
    # save records
    #
    with open(os.path.join(LOG_DIR, "records.json"), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    #
    # analysis
    #
    analyze(records)


def analyze(records):
    results = {}

    #
    # 1. power-law avalanches
    #
    response_counts = [r["response_count"] for r in records if r["response_count"] > 0]
    if response_counts:
        from collections import Counter
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
            plt.savefig(os.path.join(LOG_DIR, "avalanche.png"))
            plt.close()
        except Exception as e:
            print("avalanche plot failed:", e)

    #
    # 2. dynamic coupling
    #
    try:
        from scipy.stats import spearmanr
        clip_acts = [r["clip_activity"] for r in records]
        planet_deltas = [r["planet_delta"] for r in records]
        if len(clip_acts) > 2:
            corr, p = spearmanr(clip_acts, planet_deltas)
            results["coupling"] = {"spearman": float(corr), "p": float(p)}
    except Exception as e:
        print("spearman failed:", e)

    #
    # 3. history path dependence (markov)
    #
    winners = [r["winner_layer"] for r in records if r["winner_layer"] is not None]
    if winners:
        from collections import defaultdict
        transitions = defaultdict(lambda: defaultdict(int))
        for a, b in zip(winners[:-1], winners[1:]):
            transitions[a][b] += 1
        results["markov"] = {str(k): dict(v) for k, v in transitions.items()}

    #
    # 4. nonlinear resilience
    #
    cloud_counts = [r["cloud_count"] for r in records]
    results["cloud_counts"] = cloud_counts

    #
    # save
    #
    with open(os.path.join(LOG_DIR, "analysis.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("analysis saved to", LOG_DIR)


if __name__ == "__main__":
    main()