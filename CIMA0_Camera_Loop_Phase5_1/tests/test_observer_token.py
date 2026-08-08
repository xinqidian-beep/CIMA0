import sys
import os


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)


import numpy as np

from core.internal_dynamics_observer import InternalDynamicsObserver



def create_token_layer():

    tokens = {}


    for i in range(50):

        tokens[f"token{i}"] = (
            np.random.randn(
                768
            )
            .astype(
                np.float32
            )
        )


    return tokens



def print_tree(
    data,
    indent=0
):

    space = " " * indent


    if isinstance(data, dict):

        for k,v in data.items():

            if isinstance(v, dict):

                print(
                    space + k
                )

                print_tree(
                    v,
                    indent + 2
                )

            else:

                print(
                    space +
                    k +
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
        "CIMA0 Phase5.1 Observer Token Test"
    )


    #
    # fake cloud
    #

    snapshot = {

        "cloud":

        {

            "layer7":

            create_token_layer()

        }

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
        "first activity:"
    )

    print_tree(
        request
    )



    #
    # change one token
    #

    snapshot["cloud"]["layer7"]["token23"] += (
        np.random.randn(
            768
        )
        .astype(
            np.float32
        )
        *
        0.8
    )



    request2 = observer.observe(
        snapshot
    )


    print()

    print(
        "after token23 change:"
    )


    print_tree(
        request2
    )



if __name__ == "__main__":

    main()