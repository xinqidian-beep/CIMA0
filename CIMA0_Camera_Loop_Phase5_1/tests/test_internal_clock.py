import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)

import time
import numpy as np


from archive.planet import Planet
from core.clip_region import ClipRegion
from core.internal_dynamics import InternalDynamics


def fake_camera_bytes(
    width=640,
    height=480
):
    """
    Simulate one camera frame.

    Only produces bytes.
    No camera logic.
    """

    frame = np.zeros(
        (
            height,
            width,
            3
        ),
        dtype=np.uint8
    )


    # simple disturbance
    frame[
        100:200,
        100:200,
        0
    ] = 255


    return frame.reshape(-1).tobytes()



def print_snapshot(
    tag,
    snapshot
):

    planet = snapshot["planet"]["state"]

    clip = snapshot["clip"]


    print()
    print("=" * 40)
    print(tag)

    print(
        "planet mean:",
        float(
            planet.mean()
        )
    )


    if clip is not None:

        print(
            "clip mean:",
            float(
                clip.mean()
            )
        )

        print(
            "clip std:",
            float(
                clip.std()
            )
        )



def main():


    print(
        "Internal autonomous clock test"
    )


    #
    # build internal world
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



    #
    # one external disturbance
    #

    data = fake_camera_bytes()


    internal.receive(
        data
    )


    print(
        "Injected one camera frame"
    )


    #
    # first state
    #

    snap = internal.snapshot()

    print_snapshot(
        "INITIAL",
        snap
    )



    #
    # internal evolution only
    #

    for i in range(100):

        internal.step()


        if i % 20 == 0:

            snap = internal.snapshot()

            print_snapshot(
                f"STEP {i}",
                snap
            )


        time.sleep(
            0.01
        )



    print()
    print(
        "Test finished"
    )



if __name__ == "__main__":

    main()