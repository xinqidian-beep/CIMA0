import time

from core.cell import Cell
from core.cloud import CloudMatrix
from core.topology import Topology
from core.observer import Observer



def main():


    print(
        "=== CIMA0 Core ==="
    )


    N=4096


    cells=[
        Cell(i)
        for i in range(N)
    ]


    cloud=CloudMatrix(
        N
    )


    topology=Topology(
        N
    )


    observer=Observer()



    steps=200000



    start=time.time()


    for t in range(steps):


        # external event

        if t % 10000 ==0:

            cloud.deposit_random(
                count=4,
                strength=1.0
            )

            print(
                "cloud event",
                t
            )



        for cell in cells:


            signal = cloud.contact(
                cell.cid
            )


            if signal is None:

                perturb=0.0

            else:

                perturb=signal



            # local symmetric coupling

            coupling=0.0


            neighbors = topology.get(
                cell.cid
            )


            for nid in neighbors:

                coupling += (
                    cells[nid].x
                    -
                    cell.x
                )


            coupling *= 0.01



            cell.step(

                perturb=perturb,

                coupling=coupling

            )



        if t % 10000 ==0:


            print(
                {
                    "time":t,
                    **observer.sample(
                        cells
                    )
                }
            )


    print(
        "finished",
        time.time()-start
    )



if __name__=="__main__":

    main()