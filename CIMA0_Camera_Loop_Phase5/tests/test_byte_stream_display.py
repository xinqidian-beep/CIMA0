import sys
import os
import time
import cv2
import numpy as np


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)


from archive.planet import Planet
from core.clip_region import ClipRegion
from core.internal_dynamics import InternalDynamics
from core.display_io import DisplayIO



def main():

    print("=" * 60)
    print("Phase4 continuous byte stream display test")
    print("=" * 60)



    #
    # internal world
    #

    planet = Planet()

    clip = ClipRegion(
        64,
        64,
        3
    )


    internal = InternalDynamics(
        planet,
        clip
    )


    display = DisplayIO(
        height=240,
        width=320
    )



    previous = None


    frame_id = 0



    while True:


        #
        # simulate camera byte stream
        #
        # every loop:
        # new external bytes
        #

        camera_frame = (
            np.random.rand(
                64,
                64,
                3
            )
            *
            255
        ).astype(
            np.uint8
        )


        camera_bytes = (
            camera_frame
            .tobytes()
        )


        #
        # external byte enters
        #

        internal.receive(
            camera_bytes
        )



        #
        # internal own step
        #

        internal.step()



        snapshot = internal.snapshot()


        clip_state = snapshot["clip"]


        if clip_state is None:

            continue



        #
        # state -> byte stream
        #

        stream = (
            clip_state
            .astype(
                np.float32
            )
            .tobytes()
        )



        #
        # byte stream restore
        #

        restored = np.frombuffer(
            stream,
            dtype=np.float32
        ).reshape(
            clip_state.shape
        )



        #
        # check byte integrity
        #

        encode_diff = float(
            np.mean(
                np.abs(
                    restored -
                    clip_state
                )
            )
        )



        #
        # temporal change
        #

        if previous is None:

            temporal = 0.0

        else:

            temporal = float(
                np.mean(
                    np.abs(
                        clip_state -
                        previous
                    )
                )
            )


        previous = clip_state.copy()



        print(
            "frame:",
            frame_id,
            "mean:",
            round(
                float(
                    clip_state.mean()
                ),
                6
            ),
            "bytes:",
            len(stream),
            "encode_diff:",
            encode_diff,
            "temporal:",
            temporal
        )


        frame_id += 1



        #
        # display byte reconstructed stream
        #

        frame = display.encode(
            restored
        )


        if frame is not None:

            cv2.imshow(
                "Phase4 byte stream",
                frame
            )


        key = cv2.waitKey(30) & 0xff


        if key == 27:

            break



    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()