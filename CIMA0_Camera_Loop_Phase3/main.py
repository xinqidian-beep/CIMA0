import numpy as np


from core.camera_planet import CameraPlanet
from core.camera_observer import CameraObserver
from core.camera_io import CameraIO

from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver

from core.display_io import DisplayIO


from hardware.usb_camera import USBCamera
from hardware.display_device import DisplayDevice



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

    internal = InternalDynamics()



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
            # external hardware state
            #

            camera_state = camera_planet.step_planet(
                frame
            )



            #
            # external sampling
            #

            sampled_state = camera_observer.step_observe(
                camera_state
            )



            #
            # bytes transport
            #

            data = camera_io.encode(
                sampled_state
            )



            #
            # internal disturbance
            #

            internal.receive(
                data
            )


            internal.step()



            #
            # internal sampling
            #

            internal_snapshot = internal.snapshot()



            observe_snapshot = (
                internal_observer.step_observe(
                    internal_snapshot
                )
            )



            print(
                "OBS",
                observe_snapshot.get(
                    "activity"
                )
            )



            #
            # display projection
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