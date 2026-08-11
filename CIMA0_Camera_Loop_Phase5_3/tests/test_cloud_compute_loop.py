"""
CIMA0 Phase5_2

CloudField + ComputeSystem loop

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





def count_active(
    cloud
):

    return len(

        [

            c

            for c in cloud.cells

            if c.value is not None

        ]

    )





def main():


    print(
"""
============================================================
CIMA0 Phase5_2 Cloud Compute Loop Test

============================================================
"""
    )


    cloud = CloudField(
        capacity=8
    )


    cloud.cells[0].occupy(
        0.4
    )

    cloud.cells[1].occupy(
        0.45
    )

    cloud.cells[2].occupy(
        -0.3
    )



    compute = ComputeSystem(
        capacity=100
    )


    for step in range(20):


        request = cloud.request_compute()


        allocation = compute.allocate(
            request
        )


        cloud.execute_compute(
            allocation
        )


        print(

            "step:",
            step,

            "active:",
            count_active(
                cloud
            ),

            "allocation:",
            allocation

        )



    print()

    print(
        "FINAL:"
    )


    print(
        cloud.snapshot()
    )


    print()

    print(
        "TEST FINISHED"
    )





if __name__ == "__main__":

    main()