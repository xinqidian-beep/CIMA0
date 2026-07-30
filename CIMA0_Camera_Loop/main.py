from hardware.usb_camera import USBCamera
from core.camera_planet import CameraPlanet
from core.camera_observer import CameraObserver

from core.camera_io import CameraIO
from core.display_io import DisplayIO
from core.camera_compute import CameraCompute





def main():


    #
    # hardware
    #

    camera = USBCamera()



    #
    # boundary IO
    #

    camera_io = CameraIO()

    display_io = DisplayIO()
    camera_planet = CameraPlanet()
    camera_observer = CameraObserver()
    camera_compute = CameraCompute()


    #
    # minimal loop
    #

    while True:


        frame = camera.read()


        if frame is None:

            continue



        #
        # camera input boundary
        #
        
        input_frame = (
            camera_io.input_frame(
                frame
            )
        )

        external_state = camera_planet.step_planet(
        input_frame
        )
        delta_ephemeral = (
            camera_observer.step_observe(
                external_state
            )
        )
 
        request_ephemeral = (
            camera_observer
            .evaluate_request_ephemeral(
                delta_ephemeral
            )
        )


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


        sampled_ephemeral = None
        
        
        #
        # camera output boundary
        #

        output_frame = (
            camera_io.output_frame(
                input_frame
            )
        )



        #
        # display
        #

        display_io.output_frame(
            output_frame
        )



if __name__ == "__main__":

    main()