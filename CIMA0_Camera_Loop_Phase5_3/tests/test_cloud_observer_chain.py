
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import numpy as np

from core.internal_dynamics.cloud.cloud_field import CloudField
from core.internal_dynamics_observer import InternalDynamicsObserver

def main():

    print("=" * 60)
    print("CIMA0 Cloud -> Observer Chain Test")
    print("=" * 60)


    #
    # cloud
    #

    cloud = CloudField(
        capacity=32
    )


    #
    # inject fake field
    #
    # 模拟内部已经形成32个cell
    #

    data = np.linspace(
        -1.0,
        1.0,
        32
    )


    packet = {

        "type":
            "field",

        "source":
            "test",

        "bytes":
            data.astype(
                np.float32
            ).tobytes(),

        "shape":
            data.shape,

        "dtype":
            "float32"

    }


    cloud.receive(
        packet
    )


    snapshot = cloud.snapshot()



    print("\n[CLOUD SNAPSHOT]")
    print(snapshot)



    #
    # observer
    #

    observer = InternalDynamicsObserver()


    read_state = observer.read(
        {
            "cloud":
                snapshot
        },
        {
            "cloud":
                32
        }
    )



    print("\n[OBSERVER READ]")
    print(read_state)



    #
    # encode
    #

    display_packet = observer.encode_field(
        read_state,
        source="test"
    )


    print("\n[DISPLAY PACKET]")


    if display_packet:

        print(
            display_packet.keys()
        )

        print(
            "shape:",
            display_packet["shape"]
        )

        print(
            "dtype:",
            display_packet["dtype"]
        )

        print(
            "bytes:",
            len(display_packet["bytes"])
        )


    else:

        print(
            "None"
        )



if __name__ == "__main__":

    main()