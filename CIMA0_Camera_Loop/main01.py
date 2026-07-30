from hardware.usb_camera import USBCamera
from hardware.display_device import DisplayDevice


from core.camera_io import CameraIO
from core.camera_planet import CameraPlanet
from core.camera_observer import CameraObserver
from core.camera_compute import CameraCompute
from core.projection import Projection
from core.display_io import DisplayIO



def main():


    #
    # hardware
    #

    camera = USBCamera()

    display_device = DisplayDevice()



    #
    # boundary / core
    #

    camera_io = CameraIO()

    display_io = DisplayIO()


    camera_planet = CameraPlanet()

    observer = CameraObserver()

    compute = CameraCompute(
        capacity_slots=10000
    )

    projection = Projection()



    try:


        while True:


            #
            # hardware input
            #

            frame = camera.read()


            if frame is None:

                continue



            #
            # input boundary
            #

            external_frame = (
                camera_io.input_frame(
                    frame
                )
            )



            #
            # external world mapping
            #

            current_state = (
                camera_planet.capture_state(
                    external_frame
                )
            )



            #
            # observer self comparison
            #

            delta_ephemeral = (
                observer.evaluate_change(
                    current_state
                )
            )



            #
            # temporary demand
            #

            request_ephemeral = (
                observer.evaluate_sampling_request(
                    delta_ephemeral
                )
            )



            #
            # compute resource response
            #

            compute.step_compute()


            compute_result = (
                compute.evaluate_compute_slots(
                    request_ephemeral
                )
            )


            compute_slots = (
                compute_result[
                    "compute_slots"
                ]
            )



            #
            # sparse projection
            #

            sample_ephemeral = (
                observer.project_sampling(
                    current_state,
                    delta_ephemeral,
                    compute_slots
                )
            )



            #
            # reconstruct output
            #

            output_state = (
                projection.project_ephemeral_frame(
                    current_state,
                    sample_ephemeral
                )
            )



            #
            # output boundary
            #

            display_frame = (
                display_io.output_frame(
                    output_state
                )
            )



            #
            # hardware display
            #

            display_device.show(
                display_frame
            )


            key = (
                display_device.poll_device()
            )


            if key == 27:

                break



    finally:


        camera.release()

        display_device.release()




if __name__ == "__main__":

    main()