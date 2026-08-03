# main.py

import time
import cv2


from archive.planet import Planet
from core.clip_region import ClipRegion
from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.display_io import DisplayIO



CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



def main():


    print("=" * 60)
    print("CIMA0 Internal Dynamics Loop")
    print()
    print("ESC : exit")
    print("=" * 60)



    #
    # internal world
    #

    planet = Planet()



    clip = ClipRegion(
        CLIP_WEIGHT
    )



    internal = InternalDynamics(
        planet,
        clip
    )



    observer = InternalDynamicsObserver()



    display_io = DisplayIO()



    #
    # runtime
    #

    running = True



    while running:


        #
        # external byte stream
        #
        # CameraIO will provide this later.
        #
        # Current internal test:
        #

        data = b""



        internal.receive(
            data
        )



        #
        # internal evolution
        #

        internal.step()



        #
        # observation boundary
        #

        snapshot = (
            internal.snapshot()
        )


        observed = (
            observer.observe(
                snapshot
            )
        )



        #
        # output
        #

        frame = (
            display_io.encode(
                observed
            )
        )



        #
        # display
        #

        if frame is not None:


            if isinstance(
                frame,
                dict
            ):

                print(
                    "DISPLAY",
                    frame.keys()
                )


            else:

                cv2.imshow(
                    "CIMA0 Display",
                    frame
                )



        #
        # ESC exit
        #

        key = cv2.waitKey(1) & 0xff


        if key == 27:

            running = False



        time.sleep(
            0.03
        )



    cv2.destroyAllWindows()



    print(
        "CIMA0 stopped"
    )



if __name__ == "__main__":

    main()