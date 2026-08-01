import numpy as np

from core.camera_planet import CameraPlanet
from core.camera_observer import CameraObserver
from core.camera_io import CameraIO

from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver

from core.display_io import DisplayIO

from hardware.usb_camera import USBCamera
from hardware.display_device import DisplayDevice
from archive.planet import Planet
from core.clip_region import ClipRegion

CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


def main():
    camera = USBCamera()
    display = DisplayDevice()

    camera_planet = CameraPlanet()
    camera_observer = CameraObserver()
    camera_io = CameraIO()

    planet = Planet()
    clip = ClipRegion(CLIP_WEIGHT)
    internal = InternalDynamics(planet, clip)
    internal_observer = InternalDynamicsObserver()

    display_io = DisplayIO()

    print("=" * 60)
    print("CIMA0 Camera Loop")
    print(
        """
Camera
  |
CameraPlanet
  |
CameraObserver
  |
CameraIO
  |
InternalDynamics
  |
InternalDynamicsObserver
  |
DisplayIO
  |
Display
"""
    )
    print("=" * 60)

    try:
        while True:
            frame = camera.read()
            if frame is None:
                continue

            camera_state = camera_planet.step_planet(frame)

            sampled_snapshot = camera_observer.step_observe(camera_state)
            if sampled_snapshot is None:
                continue

            sampled_state = sampled_snapshot.get("state", sampled_snapshot)
            data = camera_io.encode(sampled_state)

            internal.receive(data)
            internal.step()

            internal_snapshot = internal.snapshot()

            observe_snapshot = internal_observer.step_observe(internal_snapshot)
            if observe_snapshot is None:
                continue

            print("OBS", observe_snapshot.get("activity", 0.0))

            planet_obs = observe_snapshot.get("planet")
            clip_obs = observe_snapshot.get("clip")

            if planet_obs is not None:
                print(
                    "PLANET",
                    planet_obs.get("activity", 0.0),
                    "STATE",
                    planet_obs.get("state_delta", 0.0),
                    "VEL",
                    planet_obs.get("velocity_delta", 0.0),
                    "ENERGY",
                    planet_obs.get("energy_delta", 0.0),
                    "PHASE",
                    planet_obs.get("phase_delta", 0.0),
                )

            if clip_obs is not None:
                print(
                    "CLIP",
                    clip_obs.get("activity", 0.0),
                    "FOCUS",
                    clip_obs.get("focus_layer", None),
                    "EMB",
                    clip_obs.get("embedding_activity", 0.0),
                    "BASIN",
                    clip_obs.get("basin_movement", 0.0),
                )

            display_frame = display_io.encode(observe_snapshot)
            if display_frame is not None:
                display.show(display_frame)

            if display.step_display() == 27:
                break

    finally:
        camera.release()
        display.close()


if __name__ == "__main__":
    main()