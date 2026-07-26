import numpy as np

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from core.cell import Cell
from core.cloud import CloudMatrix


N = 512
STEPS = 5000


def run(seed, use_cloud):

    np.random.seed(seed)


    cells = [
        Cell(i)
        for i in range(N)
    ]


    cloud = CloudMatrix(
        size=N
    )


    if use_cloud:

        cloud.deposit_random(
            count=8,
            strength=1.0
        )


    for t in range(STEPS):


        for cell in cells:


            if use_cloud:

                signal = cloud.contact(
                    cell.cid
                )

                if signal is not None:

                    cell.local_perturb(
                        signal
                    )


            cell.step()


        if use_cloud:

            cloud.decay()


    states = np.array(
        [
            [
                c.x,
                c.v
            ]
            for c in cells
        ]
    )


    return states



def distance(a,b):

    return np.mean(
        np.abs(
            a-b
        )
    )



print(
    "=== Cloud Legacy Test ==="
)



baseline_A = run(
    seed=42,
    use_cloud=False
)


baseline_B = run(
    seed=43,
    use_cloud=False
)


cloud_A = run(
    seed=42,
    use_cloud=True
)



noise_distance = distance(
    baseline_A,
    baseline_B
)


cloud_distance = distance(
    baseline_A,
    cloud_A
)



print(
    {
        "noise_distance":
        noise_distance,

        "cloud_distance":
        cloud_distance
    }
)



if cloud_distance > noise_distance * 2:

    print(
        "PASS: cloud leaves measurable legacy"
    )

else:

    print(
        "FAIL: cloud effect not above noise"
    )