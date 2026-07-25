import time

from core.universe import Universe
from core.observer import Observer



def main():


    print(
        "=== CIMA0 Phase8.0 Minimal_world_Loop ==="
    )


    universe=Universe(
        n=4096
    )


    observer=Observer()


    start=time.time()


    STEPS=10_000_000


    REPORT=100_000



    for i in range(STEPS):


        universe.step()



        if (
            universe.time
            %
            REPORT
            ==
            0
        ):


            obs=observer.observe(
                universe.cells
            )


            print(
                {
                    "time":
                    universe.time,


                    **universe.stats(),


                    "observer":
                    obs
                }
            )



    print(
        "finished",
        time.time()-start
    )



if __name__=="__main__":

    main()