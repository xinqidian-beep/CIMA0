import sys
import os
import numpy as np


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from core.cell import Cell
from core.cloud import CloudMatrix
from core.response import ResponseMonitor



N = 512
STEPS = 2000



np.random.seed(42)



cells = [
    Cell(i)
    for i in range(N)
]


cloud = CloudMatrix(
    N
)


monitor = ResponseMonitor()



for t in range(200):

    for c in cells:
        c.step()


monitor.set_baseline(
    cells
)


print(
    "baseline captured"
)



cloud.deposit_random(
    count=4,
    strength=0.5
)



for t in range(STEPS):


    for c in cells:


        signal = cloud.contact(
            c.cid
        )


        if signal is not None:

            c.local_perturb(
                signal
            )


        c.step()



    cloud.decay()


    if t % 100 == 0:

        print(
            monitor.measure(
                cells,
                t
            )
        )