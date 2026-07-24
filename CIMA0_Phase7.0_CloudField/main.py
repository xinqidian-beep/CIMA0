import time


from config import *


from core.universe import Universe

from environment.cloud import CloudField



def main():


    print(
        "=== CIMA0 Phase7.0 Cloud Field ==="
    )


    u=Universe(

        n=N_CELLS,

        avg_neighbors=AVG_NEIGHBORS,

        dt=DT,

        omega_min=OMEGA_MIN,

        omega_max=OMEGA_MAX,

        seed=SEED
    )


    cloud=CloudField(
        strength=CLOUD_STRENGTH,
        seed=SEED
    )


    start=time.time()



    while True:


        u.step(
            EVENTS_PER_REPORT,
            cloud
        )


        print(
            u.snapshot()
        )


        if u.time>=100000000:

            break



    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()