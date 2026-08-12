
import cv2

from archive.planet import Planet

from core.internal_dynamics import InternalDynamics
from core.internal_dynamics import InternalDynamicsObserver

from core.display_io import DisplayIO

from archive.planet import Planet

from core.terminal.camera import CameraPlanet

def main():

    print("=" * 60)
    print("CIMA0 Phase5_3 Internal Dynamics Loop")
    print("=" * 60)


    planet = Planet(
        size=128
    )


    dynamics = InternalDynamics(
        planet
    )


    observer = InternalDynamicsObserver()


    display = DisplayIO()


    camera_planet = CameraPlanet()


    cap = cv2.VideoCapture(0)


    if not cap.isOpened():

        print(
            "camera open failed"
        )

        return



    while True:


        key = cv2.waitKey(1) & 0xff

        if key == 27:
            break



        ret, frame = cap.read()

        if not ret:
            continue



        packet = camera_planet.step(
            frame
        )



        #
        # external disturbance
        #
        dynamics.receive(
            packet
        )


        #
        # only dynamics evolution
        #
        dynamics.step()



        #
        # observation
        #
        snapshot = dynamics.snapshot()
        
        
        read_state = observer.read(
            snapshot
        )


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
            
if __name__ == "__main__":

    main()            