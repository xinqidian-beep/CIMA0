import time
import numpy as np

from core.cell import Cell
from core.cloud import CloudMatrix
from core.observer import ObserverSystem



def main():

    print(
        "=== Phase9.0 Cloud Field ==="
    )


    N = 4096


    cells = [
        Cell(i)
        for i in range(N)
    ]


    # =========================
    # Cloud external field
    # =========================

    cloud = CloudMatrix(
        size=N
    )


    # =========================
    # Observer
    # =========================

    observer = ObserverSystem(
        min_sample=32,
        max_sample=128,
        observation_probability=0.02
    )


    steps = 500000


    start = time.time()



    for t in range(steps):


        # ---------------------
        # cloud collision
        # ---------------------

        if t % 100000 == 0:

            cloud.deposit_random(
                count=4,
                strength=1.0
            )

            print(
                {
                    "cloud_event": True,
                    "time": t
                }
            )
            
            for cid in range(N):

                signal = cloud.contact(cid)

                if signal is not None:

                    cells[cid].local_perturb(
                        signal
                    )

                    print(
                        {
                            "cloud_collision":True,
                            "cell":cid,
                            "value":signal,
                            "time":t
                        }
                    )

                


                



        # ---------------------
        # L1 world
        # ---------------------

        for cell in cells:


            value = cloud.contact(
                cell.cid
            )


            if value is not None:
                print(
                    {
                        "cloud_collision": True,
                        "cell": cell.cid,
                        "value": value,
                        "time": t
                    }
                )

                cell.local_perturb(
                    value
                )



            cell.step()



        # ---------------------
        # L2 observer
        # ---------------------

        if observer.should_observe(t):


            snapshot = observer.sample(
                cells,
                t
            )


            print(
                {
                    "snapshot":
                    snapshot
                }
            )



    print(
        "finished",
        time.time()-start
    )



if __name__ == "__main__":

    main()