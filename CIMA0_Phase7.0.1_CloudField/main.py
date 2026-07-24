import time

from config import *

from core.universe import Universe
from core.cloud import CloudField
from core.observer import Observer



def main():


    print(
        "=== CIMA0 Phase7.0.1 Cloud Field ==="
    )



    cloud=CloudField(
        n=N_CELLS,
        strength=CLOUD_STRENGTH,
        radius=CLOUD_RADIUS,
        seed=SEED
    )



    u=Universe(

        n=N_CELLS,

        avg_neighbors=AVG_NEIGHBORS,

        dt=DT,

        omega_min=OMEGA_MIN,

        omega_max=OMEGA_MAX,

        seed=SEED,

        cloud=cloud
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



        if u.time>=100_000_000:

            break



    print(
        "runtime:",
        time.time()-start
    )




if __name__=="__main__":

    main()