import cv2
import time


from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem
from core.display_io import DisplayIO


from core.camera_planet import CameraPlanet
from core.clip_region import ClipRegion

CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"

def main():

    print("=" * 60)
    print("CIMA0 Internal Dynamics Loop")
    print("")
    print("ESC : exit")
    print("=" * 60)



    #
    # local modules
    #

    planet = CameraPlanet()


    CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


    clip = ClipRegion(
        CLIP_WEIGHT
    )



    #
    # lifecycle
    #

    internal = InternalDynamics(
        planet,
        clip
    )



    #
    # observer
    #

    observer = InternalDynamicsObserver()



    #
    # compute
    #

    compute = ComputeSystem(
        capacity=100
    )



    #
    # output
    #

    display = DisplayIO()



    while True:


        #
        # camera byte input
        #

        if hasattr(
            planet,
            "camera_bytes"
        ):

            data = planet.camera_bytes()

            if data is not None:

                internal.receive(
                    data
                )



        #
        # internal evolution
        #

        internal.step()



        #
        # snapshot
        #

        snapshot = internal.snapshot()



        #
        # local observation
        #

        request = observer.observe(
            snapshot
        )



        #
        # resource allocation
        #

        allocation = compute.allocate(
            request
        )



        #
        # display
        #

        frame = display.encode(
            snapshot
        )



        if frame is not None:

            cv2.imshow(
                "CIMA0",
                frame
            )



        #
        # ESC
        #

        key = cv2.waitKey(1) & 0xff


        if key == 27:

            print(
                "CIMA0 stopped"
            )

            break



        time.sleep(
            0.03
        )



    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()