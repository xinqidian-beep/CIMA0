import time


from core.camera_planet import CameraPlanet
from core.camera_compute import CameraComputeSystem
from core.camera_observer import CameraObserver
from core.camera_io import CameraIO

from core.internal_dynamics import InternalDynamics

from core.display_io import DisplayIO

from hardware.usb_camera import USBCamera
from hardware.display_device import DisplayDevice



def main():


    camera = USBCamera()


    planet = CameraPlanet()


    compute = CameraComputeSystem()


    observer = CameraObserver(
        cell_px=20
    )


    camera_io = CameraIO()


    internal = InternalDynamics()


    display_io = DisplayIO()


    display = DisplayDevice()



    print("=" * 60)
    print("CIMA0 Camera Loop")
    print()
    print(
        "Camera"
    )
    print(
        "  |"
    )
    print(
        "CameraPlanet"
    )
    print(
        "  |"
    )
    print(
        "CameraCompute"
    )
    print(
        "  |"
    )
    print(
        "CameraObserver"
    )
    print(
        "  |"
    )
    print(
        "CameraIO"
    )
    print(
        "  |"
    )
    print(
        "InternalDynamics"
    )
    print(
        "  |"
    )
    print(
        "DisplayIO"
    )
    print(
        "  |"
    )
    print(
        "Display"
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
            # hardware information
            #

            planet_state = planet.step_planet(
                frame
            )



            #
            # compute updates own state
            #

            compute_state = compute.step()



            #
            # sampling
            #

            observed = observer.step_observe(
                planet_state["frame"]
                if isinstance(
                    planet_state,
                    dict
                )
                else frame
            )


            if observed is None:
                continue



            #
            # camera -> internal IO
            #

            data = camera_io.encode(
                observed["state"]
            )


            #
            # external perturbation enters
            # internal dynamics
            #

            internal.receive(
                data
            )


            #
            # internal evolution
            #

            internal.step()



            #
            # read-only snapshot
            #

            snapshot = internal.snapshot()



            #
            # internal -> display
            #

            display_frame = display_io.encode(
                snapshot
            )


            display.show(
                display_frame
            )


            if display.step_display() == 27:

                break



            time.sleep(
                0.001
            )



    finally:

        camera.release()

        display.close()



if __name__ == "__main__":

    main()