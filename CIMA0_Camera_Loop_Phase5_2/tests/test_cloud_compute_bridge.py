"""
CIMA0 Phase5_2

CloudField <-> ComputeSystem bridge test


Verify:

    CloudField request

          |

    ComputeSystem allocate

          |

    CloudField execute


No:
    camera
    clip
    display
    observer

"""


import sys
import os


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)


from core.compute_system import ComputeSystem
from core.internal_dynamics import CloudField





def print_cells(
    cloud,
    title
):

    print()

    print(
        "=" * 60
    )

    print(
        title
    )

    print(
        "=" * 60
    )


    for i,c in enumerate(
        cloud.cells
    ):

        print(

            i,

            "value=",
            c.value,

            "age=",
            c.age,

            "activity=",
            c.activity

        )





def build_request(
    cloud
):

    """
    CloudField reports demand.

    No resource knowledge.
    """


    collision_activity = 0.0

    decay_activity = 0.0



    for c in cloud.cells:


        if not c.empty:


            collision_activity += abs(
                c.value
            )


            decay_activity += c.activity



    return {

        "cloud":

        {

            "collision":
            collision_activity,


            "decay":
            decay_activity

        }

    }





def apply_allocation(
    cloud,
    allocation
):

    """
    Simulated execution.

    This test only checks
    interface connection.

    """


    print()

    print(
        "allocation received:"
    )

    print(
        allocation
    )





def main():


    print(
"""
============================================================
CIMA0 Phase5_2 Cloud Compute Bridge Test

============================================================
"""
    )



    #
    # CloudField
    #

    cloud = CloudField(
        capacity=4
    )



    cloud.cells[0].occupy(
        0.5
    )


    cloud.cells[1].occupy(
        0.3
    )



    print_cells(
        cloud,
        "Initial CloudField"
    )



    #
    # request
    #

    request = build_request(
        cloud
    )


    print()

    print(
        "request:"
    )


    print(
        request
    )



    #
    # compute
    #

    compute = ComputeSystem(
        capacity=100
    )


    allocation = compute.allocate(
        request
    )



    apply_allocation(
        cloud,
        allocation
    )



    #
    # verify
    #

    assert allocation != {}



    total = 0.0


    def walk(
        x
    ):

        nonlocal total


        if isinstance(
            x,
            dict
        ):

            for v in x.values():

                walk(v)


        elif isinstance(
            x,
            (int,float)
        ):

            total += float(x)



    walk(
        allocation
    )



    print()

    print(
        "allocated total:",
        total
    )



    assert total <= 100.0001



    print()

    print(
        "PASS"
    )





if __name__ == "__main__":

    main()