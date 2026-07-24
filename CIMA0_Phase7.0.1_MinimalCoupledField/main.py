import time
import numpy as np


from config import *


from core.universe import Universe

from environment.cloud import CloudField

from observer.observer import Observer



def main():


    print(
        "=== CIMA0 Phase7.0.1 Minimal Coupled Field ==="
    )


    u=Universe(

        N_CELLS,

        AVG_NEIGHBORS,

        DT,

        OMEGA_MIN,

        OMEGA_MAX,

        SEED

    )


    cloud=CloudField(
        N_CELLS
    )


    obs=Observer(
        N_CELLS
    )


    start=time.time()


    while True:


        u.step(

            cloud.get()

        )


        x=np.array(
            [
                c.x
                for c in u.cells
            ]
        )


        activity=obs.read(x)


        cloud.update(
            activity
        )



        if u.time % EVENTS_PER_REPORT==0:


            e=np.array(

                [
                    c.energy()
                    for c in u.cells

                ]

            )


            print(

                u.snapshot()

            )



        if u.time>=MAX_TIME:

            break



    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()