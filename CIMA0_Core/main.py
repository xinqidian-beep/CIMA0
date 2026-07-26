import time
import numpy as np


from core.cell import Cell
from core.cloud import CloudMatrix
from core.topology import Topology
from core.observer import ObserverSystem



def main():


    print(
        "=== CIMA0 Core ==="
    )


    N=4096


    cells=[

        Cell(i)

        for i in range(N)

    ]


    topology=Topology(
        N,
        degree=4
    )


    cloud=CloudMatrix(
        N
    )


    observer=ObserverSystem(
        sample_size=64
    )


    steps=200000



    for t in range(steps):


        # -----------------
        # cloud event
        # -----------------

        if t%10000==0:


            cloud.deposit_random(
                count=4,
                strength=1.0
            )


            print(
                "cloud event",
                t
            )



        # -----------------
        # local world
        # -----------------

        for cell in cells:


            coupling=0.0


            neighbors=topology.get(
                cell.cid
            )


            for nid in neighbors:

                coupling += (
                    cells[nid].x
                    -
                    cell.x
                )


            if neighbors:

                coupling/=len(neighbors)


            coupling*=0.05



            signal=cloud.contact(
                cell.cid
            )


            if signal is None:

                signal=0.0



            cell.step(

                coupling=coupling,

                perturb=signal

            )



        cloud.decay()



        if t%10000==0:


            print(
                observer.sample(
                    cells,
                    t
                )
            )



    print(
        "finished"
    )



if __name__=="__main__":

    main()