import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import time
import numpy as np


from archive.planet import Planet
from core.clip_region import ClipRegion
from core.internal_dynamics import InternalDynamics



def fake_camera_bytes(
    width=640,
    height=480
):

    frame = np.zeros(
        (
            height,
            width,
            3
        ),
        dtype=np.uint8
    )


    frame[
        100:200,
        100:200,
        0
    ] = 255


    return frame.reshape(-1).tobytes()



def main():

    print(
        "Phase4 internal clock experiment"
    )


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


    #
    # external disturbance once
    #

    internal.receive(
        fake_camera_bytes()
    )


    print(
        "camera disturbance injected"
    )


    #
    # internal owns time now
    #

    for i in range(200):

        internal.step()


        if i % 20 == 0:

            snapshot = internal.snapshot()


            planet_state = snapshot["planet"]["state"]


            print(
                "step:",
                i,
                "planet mean:",
                float(
                    planet_state.mean()
                )
            )


        time.sleep(
            0.01
        )


    print(
        "finished"
    )



if __name__ == "__main__":

    main()