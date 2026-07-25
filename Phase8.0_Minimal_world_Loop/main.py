import time
import numpy as np

from core.cell import Cell
from core.compute import ComputeSystem
from core.observer import ObserverSystem



def main():

    print(
        "=== Phase8.0 Minimal World ==="
    )


    N = 4096


    cells = [
        Cell(i)
        for i in range(N)
    ]


    compute = ComputeSystem(
        cells
    )


    observer = ObserverSystem(
        sample_size=64
    )


    steps = 1000000


    start = time.time()


    for t in range(steps):

        compute.step()


        if t % 100000 == 0:

            obs = observer.sample(
                compute.get_cells(),
                t
            )

            summary = observer.summary()


            print(
                {
                    "time": t,
                    "snapshot": summary
                }
            )


    print(
        "finished",
        time.time()-start
    )



if __name__ == "__main__":
    main()