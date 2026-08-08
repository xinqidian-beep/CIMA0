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



def create_tokens():

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



def print_budget(
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

                print_budget(
                    v,
                    indent+2
                )

            else:

                print(
                    space,
                    k,
                    ":",
                    v
                )

    else:

        print(
            space,
            data
        )



def main():

    print(
        "CIMA0 Phase5.1 Observer Budget Test"
    )


    snapshot = {

        "cloud":

        {

            "layer7":

            create_tokens()

        }

    }



    observer = InternalDynamicsObserver()



    #
    # initialize
    #

    observer.observe(
        snapshot
    )



    #
    # create changes
    #

    snapshot["cloud"]["layer7"]["token23"] += (
        np.ones(
            768
        )
        .astype(
            np.float32
        )
        *
        1.0
    )


    snapshot["cloud"]["layer7"]["token10"] += (
        np.ones(
            768
        )
        .astype(
            np.float32
        )
        *
        0.1
    )



    activity = observer.observe(
        snapshot
    )


    print()

    print(
        "activity:"
    )

    print_budget(
        activity
    )



if __name__ == "__main__":

    main()