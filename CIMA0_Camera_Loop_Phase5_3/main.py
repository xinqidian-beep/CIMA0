import cv2

from core.camera_planet import CameraPlanet
from core.internal_dynamics import InternalDynamics
from core.display_io import DisplayIO

from archive.planet import Planet



def main():

    print("=" * 60)
    print("CIMA0 Planet internal packet test")
    print("=" * 60)



    #
    # internal world
    #

    dynamics = InternalDynamics()


    #
    # planet organ
    #

    planet = Planet()


    dynamics.register(
        "planet",
        planet
    )



    #
    # display
    #

    display = DisplayIO()



    #
    # camera
    #

    cap = cv2.VideoCapture(0)


    if not cap.isOpened():

        print(
            "camera open failed"
        )

        return



    camera_planet = CameraPlanet()



    while True:



        #
        # camera
        #

        ret, frame = cap.read()


        if not ret:

            continue



        #
        # CameraPlanet
        #

        packet = camera_planet.step(
            frame
        )


        if packet is None:

            continue



        print(
            "\n[CAMERA]"
        )

        print(
            packet.keys()
        )


        print(
            packet["shape"],
            packet["dtype"],
            len(packet["bytes"])
        )



        #
        # enter internal world
        #

        dynamics.receive(
            packet
        )



        #
        # evolve
        #

        dynamics.step()



        #
        # snapshot
        #

        snapshot = dynamics.snapshot()



        print(
            "[SNAPSHOT]"
        )


        print(
            snapshot.keys()
        )



        planet_state = snapshot.get(
            "planet"
        )


        if planet_state is None:

            print(
                "planet missing"
            )

            continue



        print(
            "[PLANET STATE]"
        )


        print(
            type(planet_state)
        )



        #
        # packet check
        #

        if isinstance(
            planet_state,
            dict
        ):


            print(
                planet_state.keys()
            )


            shape = planet_state.get(
                "shape"
            )


            dtype = planet_state.get(
                "dtype"
            )


            data = planet_state.get(
                "bytes"
            )


            print(
                shape,
                dtype,
                len(data) if data else None
            )



        #
        # display
        #

        frame_out = display.encode(
            planet_state
        )


        if frame_out is not None:


            cv2.imshow(
                "CIMA0",
                frame_out
            )



        if cv2.waitKey(1) & 0xff == 27:

            break



    cap.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()