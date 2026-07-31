import numpy as np


from core.internal_dynamics import InternalDynamics

from archive.observer import Observer
from archive.compute import ComputeSystem
from archive.io import InputField

from hardware.usb_camera import USBCamera
from hardware.display_device import DisplayDevice



CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



def snapshot_to_frame(
    snapshot,
    width=640,
    height=480
):
    """
    IO display projection.

    Only convert data format.

    No:
        judgment
        filtering
        interpretation
    """


    value = snapshot.get(
        "local_signal",
        0.0
    )


    value = abs(
        float(value)
    )


    value = min(
        1.0,
        value
    )


    level = int(
        value * 255
    )


    frame = np.ones(
        (
            height,
            width,
            3
        ),
        dtype=np.uint8
    )


    frame *= level


    return frame




def main():


    camera = USBCamera()


    io = InputField()


    display = DisplayDevice()



    internal = InternalDynamics(
        clip_weight=CLIP_WEIGHT
    )


    observer = Observer()


    compute = ComputeSystem()



    print("=" * 60)
    print("CIMA0 Camera Loop Phase3")
    print()
    print("camera")
    print("  |")
    print("Internal Dynamics")
    print("  |")
    print("  + Planet")
    print("  + ClipRegion")
    print("  |")
    print("Observer(snapshot)")
    print("  |")
    print("IO projection")
    print("  |")
    print("Display")
    print("=" * 60)



    try:

        while True:


            frame = camera.read()


            if frame is None:

                continue



            #
            # external input
            #

            external_state = io.receive(
                frame
            )



            #
            # internal evolution
            #

            internal.update(
                external_state
            )



            #
            # observer only reads
            #

            snapshot = observer.describe(
                internal.observation_state()
            )



            #
            # compute resource
            #

            compute.step()



            #
            # snapshot -> display format
            #

            display_frame = snapshot_to_frame(
                snapshot
            )


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