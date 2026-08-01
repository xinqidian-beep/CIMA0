import numpy as np
from core.display_io import DisplayIO


def main():
    d = DisplayIO()

    samples = [
        {
            "active": True,
            "activity": 0.05,
            "planet": {
                "activity": 0.05,
                "state_delta": 0.05,
                "velocity_delta": 0.0,
                "energy_delta": 0.0,
                "phase_delta": 0.0,
            },
            "clip": {
                "activity": 0.0,
                "layer_activities": [0.0, 0.0, 0.0],
                "embedding_activity": 0.0,
                "basin_movement": 0.0,
                "focus_layer": None,
            },
        },
        {
            "active": True,
            "activity": 0.20,
            "planet": {
                "activity": 0.12,
                "state_delta": 0.12,
                "velocity_delta": 0.01,
                "energy_delta": 0.0,
                "phase_delta": 0.0,
            },
            "clip": {
                "activity": 0.20,
                "layer_activities": [0.02, 0.08, 0.10],
                "embedding_activity": 0.15,
                "basin_movement": 0.01,
                "focus_layer": 2,
            },
        },
        {
            "active": True,
            "activity": 0.60,
            "planet": {
                "activity": 0.18,
                "state_delta": 0.10,
                "velocity_delta": 0.03,
                "energy_delta": 0.02,
                "phase_delta": 0.03,
            },
            "clip": {
                "activity": 0.60,
                "layer_activities": [0.20, 0.10, 0.30],
                "embedding_activity": 0.25,
                "basin_movement": 0.05,
                "focus_layer": 0,
            },
        },
    ]

    for i, s in enumerate(samples):
        frame = d.encode(s)
        if frame is None:
            print(f"sample {i}: frame=None")
            continue
        print(
            f"sample {i}: shape={frame.shape}, dtype={frame.dtype}, "
            f"min={frame.min()}, max={frame.max()}, mean={frame.mean():.2f}"
        )


if __name__ == "__main__":
    main()