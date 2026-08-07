import os
import sys
import numpy as np


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, ROOT)


from core.clip_field import CLIPField



CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



def make_packet(seed):

    rng = np.random.RandomState(seed)

    frame = rng.randint(
        0,
        255,
        (224,224,3),
        dtype=np.uint8
    )


    return {

        "bytes":
            frame.tobytes(),

        "shape":
            frame.shape,

        "dtype":
            str(frame.dtype)

    }



def main():

    print(
        "CIMA0 CLIPField Port Test"
    )


    field = CLIPField(
        CLIP_WEIGHT,
        "cpu"
    )



    packet = make_packet(1)
    
    
    print(
        "input1 first bytes:",
        packet["bytes"][:10]
    )


    packet2 = make_packet(2)


    print(
        "input2 first bytes:",
        packet2["bytes"][:10]
    )
    



    #
    # first input
    #

    field.receive(packet)

    field.step()


    out1 = field.output.copy()



    #
    # same input again
    #

    field.receive(packet)

    field.step()


    out2 = field.output.copy()



    print(
        "output shape:",
        out1.shape
    )

    print(
        "dtype:",
        out1.dtype
    )


    diff = np.abs(
        out1-out2
    ).mean()


    print(
        "repeat difference:",
        diff
    )



    #
    # different input
    #

    field.receive(
        packet2
    )

    field.step()


    out3 = field.output


    diff2 = np.abs(
        out1-out3
    ).mean()


    print(
        "different input difference:",
        diff2
    )



    print(
        "Port test finished"
    )



if __name__ == "__main__":
    main()