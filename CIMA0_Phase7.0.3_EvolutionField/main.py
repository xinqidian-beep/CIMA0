import time


from config import *


from core.universe import Universe

from environment.cloud import CloudField

from observer.coarse import CoarseObserver

from observer.focus import FocusObserver



def main():


    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
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


    coarse=CoarseObserver(
        N_CELLS,
        OBSERVER_SIZE
    )


    focus=FocusObserver(
        FOCUS_SIZE
    )


    start=time.time()



    while True:


        # 动力运行

        u.run(
            EVENTS_PER_REPORT
        )



        # 外部观察

        region=coarse.scan()


        ids=focus.focus(
            region,
            u
        )



        # 延迟趋势记录

        cloud.disturb(
            ids,
            u
        )


        cloud.evolve()



        print(
            u.snapshot()
        )



        if u.time>=100_000_000:

            break



    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()