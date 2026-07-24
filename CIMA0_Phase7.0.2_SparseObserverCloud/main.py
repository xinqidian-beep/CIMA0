import time
import numpy as np


from config import *


from core.universe import Universe


from environment.cloud import CloudField


from observer.coarse import CoarseObserver

from observer.focus import FocusObserver




def main():


    print(
        "=== CIMA0 Phase7.0.2 Sparse Observer Cloud ==="
    )


    u=Universe(

        N_CELLS,

        AVG_NEIGHBORS,

        OMEGA_MIN,

        OMEGA_MAX,

        SEED

    )


    cloud=CloudField(
        N_CELLS
    )


    coarse=CoarseObserver(

        N_CELLS,

        COARSE_SIZE

    )


    focus=FocusObserver(

        FOCUS_SIZE

    )



    start=time.time()



    while u.time < MAX_TIME:


        u.run(

            EVENTS_PER_REPORT,

            cloud

        )



        # 第一层观察

        region=coarse.sample()



        # 第二层观察

        ids=focus.focus(region)



        # 产生慢扰动

        for i in ids:


            x=u.cells[i].x


            cloud.deposit(

                i,

                x

            )



        cloud.evolve()



        print(

            u.snapshot()

        )



    print(
        "runtime:",
        time.time()-start
    )




if __name__=="__main__":

    main()