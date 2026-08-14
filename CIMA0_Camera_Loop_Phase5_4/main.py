import cv2


from archive.planet import Planet


from core.internal_dynamics.internal_dynamics import (
    InternalDynamics
)

from core.internal_dynamics.internal_dynamics_observer import (
    InternalDynamicsObserver
)


from core.compute_system.compute_system import (
    ComputeSystem
)


from core.terminal.camera import (
    CameraPlanet
)


from core.organs.clip_field import (
    CLIPField
)


from core.display_io import (
    DisplayIO
)



def main():


    print("=" * 60)
    print(
        "CIMA0 Phase5_4 Internal Dynamics Loop"
    )
    print("=" * 60)



    #
    # Planet
    #
    # base internal dynamical space
    #

    planet = Planet(
        size=128
    )



    #
    # Compute system
    #
    # independent resource allocator
    #

    compute = ComputeSystem(
        capacity=1024
    )



    #
    # Internal Dynamics
    #

    dynamics = InternalDynamics(
        planet,
        compute
    )



    #
    # Internal organ
    #
    # CLIPField is not vision here.
    #
    # It is an evolved internal organ.
    #

    clip_field = CLIPField(
        weight_path=
        "models/open_clip_pytorch_model.bin"
    )


    dynamics.register(
        "clip",
        clip_field
    )



    #
    # readonly observer
    #

    observer = InternalDynamicsObserver()



    #
    # display port
    #

    display = DisplayIO()



    #
    # external boundary
    #

    camera_planet = CameraPlanet()



    #
    # camera
    #

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )


    camera_available = cap.isOpened()



    if not camera_available:

        print(
            "camera open failed, running without camera"
        )



    while True:


        #
        # window event
        #

        key = cv2.waitKey(
            1
        ) & 0xff


        if key == 27:

            break



        #
        # external packet
        #

        if camera_available:


            ret, frame = cap.read()


            if ret and frame is not None:


                packet = camera_planet.step(
                    frame
                )


                #
                # external disturbance
                #
                # broadcast to organs
                #

                dynamics.receive(
                    packet
                )



        #
        # internal clock
        #

        dynamics.step()



        #
        # snapshot
        #

        snapshot = dynamics.snapshot()



        #
        # observer
        #

        read_state = observer.read(
            snapshot
        )



        #
        # display
        #

        display_packet = observer.encode_field(
            read_state,
            source="internal"
        )



        frame_out = display.encode(
            display_packet
        )



        if frame_out is not None:


            cv2.imshow(
                "CIMA0",
                frame_out
            )



    if camera_available:

        cap.release()


    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()