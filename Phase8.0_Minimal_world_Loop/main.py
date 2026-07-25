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


    total_steps=10_000_000


    interval=100000



    for i in range(total_steps):


        universe.step()


        if universe.time % interval==0:


            print(
                {
                    **universe.snapshot(),

                    "observer":
                        observer.observe(
                            universe
                        )
                }
            )


    print(
        "finished",
        time.time()-start
    )



if __name__=="__main__":

    main()