"""
CIMA0 Phase5_2

CloudField dynamics loop test


Observe:

    receive

        |

    internal step

        |

    collision

        |

    decay

        |

    snapshot


No external control.

"""


import sys
import os
import random


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)



from core.internal_dynamics import CloudField





def active_count(
    cloud
):

    return len(

        [

            c

            for c in cloud.cells

            if not c.empty

        ]

    )





def dump(
    cloud,
    step
):

    values = [

        round(c.value,4)

        for c in cloud.cells

        if not c.empty

    ]


    print(

        "step:",
        step,

        "active:",
        len(values),

        "values:",
        values,

        "merge:",
        cloud.merge_events

    )





def main():


    print(
"""
============================================================
CIMA0 Phase5_2 CloudField Dynamics Loop Test

============================================================
"""
    )


    cloud = CloudField(
        capacity=8
    )



    #
    # 初始状态注入
    #
    inputs = [

        0.40,
        0.43,
        0.80,
        -0.30,
        0.10

    ]



    print(
        "\nInject initial states\n"
    )


    for v in inputs:

        cloud.receive(
            [v]
        )



    dump(
        cloud,
        0
    )



    #
    # dynamics loop
    #

    for i in range(1,31):


        #
        # occasionally inject
        #
        if i % 5 == 0:


            value = random.choice(

                [

                    0.42,
                    0.44,
                    -0.5,
                    0.7

                ]

            )


            cloud.receive(
                [value]
            )



        cloud.step()



        dump(
            cloud,
            i
        )



    print()


    print(
        "Final snapshot"
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