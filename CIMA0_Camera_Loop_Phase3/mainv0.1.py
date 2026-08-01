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



    #
    # external camera chain
    #

    camera_planet = CameraPlanet()

    camera_observer = CameraObserver()

    camera_io = CameraIO()



    #
    # internal dynamics
    #
    planet = Planet()

    clip = ClipRegion(
        CLIP_WEIGHT
    )

    internal = InternalDynamics(
        planet,
        clip
    )

    internal_observer = InternalDynamicsObserver()



    #
    # display
    #

    display_io = DisplayIO()



    print("=" * 60)

    print(
        "CIMA0 Camera Loop"
    )

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


            #
            # camera hardware
            #

            frame = camera.read()


            if frame is None:

                continue



            #
            # camera hardware state
            #

            camera_state = camera_planet.step_planet(
                frame
            )



            #
            # external sampling
            #
            # CameraObserver only receives image state
            #

            sampled_snapshot = camera_observer.step_observe(
                camera_state
            )


            if sampled_snapshot is None:

                continue



            #
            # extract sampled state
            #
            # IO only transports state
            #

            sampled_state = sampled_snapshot.get(
                "state",
                sampled_snapshot
            )



            #
            # byte transport
            #

            data = camera_io.encode(
                sampled_state
            )



            #
            # disturbance enters internal dynamics
            #

            internal.receive(
                data
            )


            internal.step()



            #
            # internal snapshot
            #

            internal_snapshot = internal.snapshot()



            #
            # internal sampling
            #

            observe_snapshot = (
                internal_observer.step_observe(
                    internal_snapshot
                )
            )



            if observe_snapshot is None:

                continue



            print(
                "OBS",
                observe_snapshot.get(
                    "activity",
                    0.0
                )
            )



            #
            # display format conversion
            #

            display_frame = display_io.encode(
                observe_snapshot
            )


            if display_frame is not None:

                display.show(
                    display_frame
                )



            if display.step_display() == 27:

                break



    finally:

        camera.release()

        display.close()




if __name__ == "__main__":

    main()