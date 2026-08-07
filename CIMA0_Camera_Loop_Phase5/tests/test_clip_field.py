import os
import sys
import numpy as np


# project root
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

    print("=" * 60)
    print("CIMA0 Phase5 CLIPField Test")
    print("=" * 60)



    #
    # create field
    #

    clip_field = CLIPField(
        weight_path=CLIP_WEIGHT,
        device="cpu"
    )


    print("CLIPField loaded")



    #
    # synthetic byte input
    #
    # simulate camera packet
    #

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )


    # add simple structure
    frame[100:300, 200:400, 0] = 255
    frame[200:350, 300:500, 1] = 128



    packet = {

        "bytes":
            frame.tobytes(),

        "shape":
            frame.shape,

        "dtype":
            str(frame.dtype)

    }



    #
    # send
    #

    clip_field.receive(
        packet
    )


    #
    # compute
    #

    clip_field.step()



    #
    # inspect
    #

    snapshot = clip_field.snapshot()


    print("-" * 60)

    print(
        "age:",
        snapshot["age"]
    )


    print(
        "output_shape:",
        snapshot["output_shape"]
    )


    print(
        "layers:"
    )


    for name, shape in snapshot["layers"].items():

        print(
            " ",
            name,
            shape
        )



    print("-" * 60)



    if clip_field.output is not None:

        print(
            "output dtype:",
            clip_field.output.dtype
        )

        print(
            "output min:",
            clip_field.output.min()
        )

        print(
            "output max:",
            clip_field.output.max()
        )

        print(
            "output sample:",
            clip_field.output[0][:10]
        )


    else:

        print(
            "NO OUTPUT"
        )



    print("=" * 60)
    
    print(
        "snapshot:",
        clip_field.snapshot()
    )


    if clip_field.output is not None:

        print(
            "output shape:",
            clip_field.output.shape
        )

        print(
            "output dtype:",
            clip_field.output.dtype
        )

        print(
            "output first 10:",
            clip_field.output[0][:10]
        )

    else:

        print(
            "output is None"
        )
    
    
    print("CLIPField test finished")



if __name__ == "__main__":

    main()