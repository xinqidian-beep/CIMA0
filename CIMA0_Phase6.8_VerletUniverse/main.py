import time


from config import *

from core.universe import Universe
from core.observer import Observer



def main():


    print(
        "=== CIMA0 Phase6.7.1 Observer Upgrade ==="
    )


    u=Universe(

        n=N_CELLS,

        avg_neighbors=AVG_NEIGHBORS,

        dt=DT,

        omega_min=OMEGA_MIN,

        omega_max=OMEGA_MAX,

        seed=SEED

    )


    obs=Observer()



    start=time.time()



    while True:


        u.step(
            EVENTS_PER_REPORT
        )


        print(
            obs.read(u)
        )


        if u.time>=MAX_EVENTS:

            break



    print(
        "runtime:",
        time.time()-start
    )




if __name__=="__main__":

    main()