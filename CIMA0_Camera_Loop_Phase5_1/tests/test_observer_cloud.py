import sys
import os


#
# add project root
#

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(
    ROOT
)


import numpy as np

from core.internal_dynamics_observer import InternalDynamicsObserver



def create_cloud():

    cloud = {}


    for i in range(12):

        cloud[f"layer{i}"] = (
            np.random.randn(
                50,
                768
            )
            .astype(
                np.float32
            )
        )


    return cloud



def print_tree(
    data,
    indent=0
):

    space = " " * indent


    if isinstance(
        data,
        dict
    ):

        for k, v in data.items():

            if isinstance(
                v,
                dict
            ):

                print(
                    space + str(k)
                )

                print_tree(
                    v,
                    indent + 2
                )

            else:

                print(
                    space +
                    str(k) +
                    ": " +
                    str(v)
                )

    else:

        print(
            space +
            str(data)
        )



def main():


    print(
        "CIMA0 Phase5.1 Observer Cloud Test"
    )



    #
    # create fake visual cloud
    #
    
    snapshot = {

        "cloud":
            create_cloud()

    }



    observer = InternalDynamicsObserver()



    #
    # first observation
    #

    request = observer.observe(
        snapshot
    )


    print()

    print(
        "first activity tree:"
    )

    print_tree(
        request
    )



    #
    # read
    #

    allocation = {

        "cloud":
            100

    }


    result = observer.read(
        snapshot,
        allocation
    )


    print()

    print(
        "read result:"
    )


    if "cloud" in result:

        print(
            "layers:",
            len(
                result["cloud"]
            )
        )


        for k,v in result["cloud"].items():

            print(
                k,
                v.shape
            )



    #
    # modify one layer
    #

    snapshot["cloud"]["layer7"] += (
        np.random.randn(
            50,
            768
        )
        .astype(
            np.float32
        )
        *
        0.5
    )



    #
    # second observation
    #

    request2 = observer.observe(
        snapshot
    )


    print()

    print(
        "after layer7 change:"
    )

    print_tree(
        request2
    )



if __name__ == "__main__":

    main()