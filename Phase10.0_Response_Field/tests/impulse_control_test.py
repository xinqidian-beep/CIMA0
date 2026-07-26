import sys
import os
import numpy as np


# 允许从 tests 目录运行
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from core.cell import Cell
from core.response_field import ResponseField



def run(
    seed=42,
    impulse=False
):

    np.random.seed(seed)


    N = 1000


    cells = [
        Cell(i)
        for i in range(N)
    ]


    field = ResponseField(
        size=N
    )


    responses = []


    for t in range(2000):


        # ----------------
        # 单次 impulse
        # ----------------

        if impulse and t == 50:

            cid = np.random.randint(
                0,
                N
            )

            value = 1.0


            field.deposit(
                cid,
                value
            )


            print(
                {
                    "impulse": True,
                    "cell": cid,
                    "time": t
                }
            )


        # ----------------
        # response coupling
        # ----------------

        for c in cells:

            signal = field.contact(
                c.cid
            )

            if signal is not None:

                c.local_perturb(
                    signal
                )


            c.step()



        # field 自身演化

        field.step()



        # ----------------
        # global response
        # ----------------

        r = np.mean(
            [
                abs(c.x)
                for c in cells
            ]
        )


        responses.append(
            r
        )


    return np.array(
        responses
    )





if __name__ == "__main__":


    print(
        "=== Impulse Control Test ==="
    )


    baseline = run(
        seed=42,
        impulse=False
    )


    disturbed = run(
        seed=42,
        impulse=True
    )


    diff = np.mean(
        np.abs(
            baseline - disturbed
        )
    )


    print(
        {
            "mean_difference":
            diff,

            "baseline_final":
            float(
                baseline[-1]
            ),

            "disturbed_final":
            float(
                disturbed[-1]
            )
        }
    )


    if diff > 0.01:

        print(
            "PASS: impulse changes trajectory"
        )

    else:

        print(
            "FAIL: no measurable response"
        )