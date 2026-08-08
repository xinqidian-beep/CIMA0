import os
import sys
import numpy as np


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    ROOT
)

from core.clip_field import CLIPField


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


def main():

    print(
        "CIMA0 Phase5.1 CLIP Layer Test"
    )


    clip = CLIPField(
        CLIP_WEIGHT
    )


    dummy = np.zeros(
        (224,224,3),
        dtype=np.uint8
    )


    packet = {

        "bytes":
            dummy.tobytes(),

        "shape":
            dummy.shape,

        "dtype":
            "uint8"
    }


    clip.receive(packet)


    for _ in range(31):

        clip.step()



    snap = clip.snapshot()



    print()

    print(
        "field:",
        snap["field"].shape
    )


    print(
        "embedding:",
        snap["embedding"].shape
    )


    print()


    cloud = snap["cloud"]
    
    print()
    
    print(
        "cloud:",
        len(cloud)
    
    )
    
    for name, value in cloud.items():

        print(
            name,
            value.shape
        )

    stream = clip.read()

    print(
        "stream bytes:",
        len(stream)
    )


if __name__ == "__main__":

    main()