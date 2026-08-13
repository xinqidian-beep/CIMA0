import cv2


from core.internal_dynamics.planet import Planet
from core.internal_dynamics.internal_dynamics import InternalDynamics
from core.internal_dynamics.internal_dynamics_observer import InternalDynamicsObserver

from core.terminal.camera import CameraPlanet

from core.display.display_io import DisplayIO



def main():

    print("=" * 60)
    print("CIMA0 Phase5_3 Internal Dynamics Loop")
    print("=" * 60)



    #
    # planet
    #
    # base dynamical system
    #

    planet = Planet(
        size=128
    )



    #
    # internal dynamics
    #

    dynamics = InternalDynamics(
        planet
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
    # camera boundary
    #

    camera_planet = CameraPlanet()



    #
    # camera is optional
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
        # ESC handling
        #

        key = cv2.waitKey(1) & 0xff


        if key == 27:

            break



        #
        # external disturbance
        #
        # camera is NOT the clock
        #

        if camera_available:


            ret, frame = cap.read()


            if ret and frame is not None:


                packet = camera_planet.step(
                    frame
                )


                dynamics.receive(
                    packet
                )



        #
        # unconditional planet evolution
        #

        dynamics.step()



        #
        # observation
        #

        snapshot = dynamics.snapshot()


        read_state = observer.read(
            snapshot
        )



        #
        # field packet
        #

        display_packet = observer.encode_field(
            read_state,
            source="internal"
        )



        #
        # framebuffer
        #

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