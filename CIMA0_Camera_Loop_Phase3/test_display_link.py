import numpy as np
from core.display_io import DisplayIO
from hardware.display_device import DisplayDevice


def main():
    d = DisplayDevice()
    io = DisplayIO()

    samples = []

    for i in range(50):
        obs = float(i) / 50.0
        planet_act = obs * 0.8
        clip_act = obs * 1.2

        snapshot = {
            "active": True,
            "activity": obs,
            "planet": {
                "activity": planet_act,
                "state_delta": planet_act * 0.9,
                "velocity_delta": 0.0,
                "energy_delta": 0.0,
                "phase_delta": 0.0,
            },
            "clip": {
                "activity": clip_act,
                "layer_activities": [clip_act * 0.3, clip_act * 0.5, clip_act * 0.2],
                "embedding_activity": clip_act * 0.4,
                "basin_movement": 0.01,
                "focus_layer": i % 3,
            },
        }
        samples.append(snapshot)

    while True:
        for s in samples:
            frame = io.encode(s)
            if frame is not None:
                d.show(frame)
            if d.step_display() == 27:
                d.close()
                return


if __name__ == "__main__":
    main()