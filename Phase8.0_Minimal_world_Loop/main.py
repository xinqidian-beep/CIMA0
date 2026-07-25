import time

from core.universe import Universe
from core.observer import Observer
from core.compression import Compression



def main():


    print(
        "=== CIMA0 Phase8.0 Minimal_world_Loop ==="
    )


    universe = Universe(
        n=4096
    )


    observer = Observer(
        sample=64
    )


    compression = Compression()



    TOTAL_EVENTS = 10_000_000


    REPORT = 100_000



    start=time.time()



    for i in range(
        TOTAL_EVENTS
    ):


        universe.step()



        if universe.time % REPORT ==0:


            obs = observer.observe(
                universe
            )


            compression.record(
                universe
            )


            print(

                universe.statistics()
                |
                {
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