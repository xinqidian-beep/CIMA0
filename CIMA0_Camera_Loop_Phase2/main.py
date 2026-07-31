from hardware.usb_camera import USBCamera
from hardware.display_device import DisplayDevice


from core.camera_io import CameraIO
from core.display_io import DisplayIO

from core.camera_planet import CameraPlanet
from core.camera_compute import CameraCompute

from core.observer import Observer
from core.clip_region import ClipRegion



CLIP_WEIGHT = (
    r"C:\CIMA0\models\open_clip_pytorch_model.bin"
)



def main():


    #
    # hardware
    #

    camera = USBCamera()

    display = DisplayDevice()



    #
    # boundary
    #

    camera_io = CameraIO()

    display_io = DisplayIO()



    #
    # internal world
    #

    planet = CameraPlanet()

    observer = Observer()

    compute = CameraCompute()



    #
    # local visual basin
    #

    clip_region = ClipRegion(
        CLIP_WEIGHT
    )



    try:


        while True:


            frame = (
                camera.read()
            )


            if frame is None:

                continue



            #
            # input boundary
            #

            input_frame = (
                camera_io
                .input_frame(
                    frame
                )
            )



            #
            # external world mapping
            #

            external_state = (
                planet
                .step_planet(
                    input_frame
                )
            )



            #
            # local clip region
            #
            # first stage:
            # use whole frame
            #
            # later:
            # local region coupling
            #

            clip_state = None



            #
            # observer
            #

            snapshot = (
                observer
                .observe(
                    external_state,
                    clip_state
                )
            )



            #
            # internal computation
            #

            compute.step_compute()



            #
            # output
            #

            output_frame = (
                camera_io
                .output_frame(
                    input_frame
                )
            )


            display_io.output_frame(
                output_frame
            )


            key = (
                display
                .step_display()
            )


            if key == 27:

                break



    finally:

        camera.close()

        display.close()



if __name__ == "__main__":

    main()