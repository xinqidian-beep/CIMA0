import numpy as np
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from core.clip_field import CLIPField
from core.internal_dynamics import InternalDynamics



WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



def make_camera():

    img = np.random.randint(
        0,
        255,
        (
            128,
            128,
            3
        ),
        dtype=np.uint8
    )


    return {

        "bytes":
            img.tobytes(),

        "shape":
            img.shape,

        "dtype":
            "uint8"
    }



def main():

    print(
        "CIMA0 Phase5.1 Visual Ingest Test"
    )


    clip = CLIPField(
        WEIGHT
    )


    dynamics = InternalDynamics()


    dynamics.register(
        "visual",
        clip
    )


    camera = make_camera()



    #
    # external byte stream
    #

    dynamics.receive(
        camera
    )


    #
    # local evolution
    #

    for i in range(35):

        dynamics.step()



    snap = dynamics.snapshot()



    visual = snap["visual"]


    print()

    print(
        "age:",
        visual["age"]
    )


    print(
        "field:",
        visual["field"].shape
    )


    print(
        "embedding:",
        visual["embedding"].shape
    )


    print(
        "cloud:",
        len(visual["cloud"])
    )


if __name__ == "__main__":

    main()