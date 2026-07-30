import cv2

from hardware.usb_camera import USBCamera

from core.camera_io import CameraIO
from core.display_io import DisplayIO

from core.camera_planet import CameraPlanet
from core.camera_observer import CameraObserver
from core.camera_compute import CameraCompute



def main():


    camera_device = USBCamera()


    camera_io = CameraIO()

    display_io = DisplayIO()


    camera_planet = CameraPlanet()

    camera_observer = CameraObserver()

    camera_compute = CameraCompute()



    step = 0



    while True:


        step += 1


        #
        # hardware input
        #

        frame = camera_device.read()


        if frame is None:

            continue



        #
        # input boundary
        #

        input_frame = (
            camera_io.input_frame(
                frame
            )
        )



        #
        # external world mapping
        #

        external_state = (
            camera_planet.step_planet(
                input_frame
            )
        )



        #
        # temporal observation
        #

        delta_ephemeral = (
            camera_observer.step_observe(
                external_state
            )
        )



        #
        # temporary compute request
        #

        request_ephemeral = (
            camera_observer
            .evaluate_request_ephemeral(
                delta_ephemeral
            )
        )



        #
        # compute resource dynamics
        #

        camera_compute.step_compute()


        compute_result = (
            camera_compute
            .grant_ephemeral_slots(
                request_ephemeral
            )
        )


        compute_slots_ephemeral = (
            compute_result[
                "compute_slots_ephemeral"
            ]
        )



        #
        # temporary sampling
        #

        sampled_ephemeral = (
            camera_planet
            .sample_ephemeral(
                external_state,
                delta_ephemeral,
                compute_slots_ephemeral
            )
        )



        #
        # output boundary
        #

        output_frame = (
            camera_io.output_frame(
                input_frame
            )
        )


        display_io.output_frame(
            output_frame
        )



        #
        # OpenCV event loop
        #

        key = cv2.waitKey(1)


        if key == 27:

            break



        #
        # minimal runtime observation
        #

        if step % 300 == 0:

            print(
                "running",
                step,
                "compute",
                compute_slots_ephemeral,
                "sample",
                len(sampled_ephemeral)
            )



    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()