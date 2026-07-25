import time

from core.world import World
from core.observer import Observer



def main():


    print(
        "=== CIMA0 Phase8.0 Minimal_world_Loop ==="
    )


    world=World(
        n=4096
    )


    observer=Observer(
        sample_size=32
    )


    start=time.time()


    TEST_TIME=10_000_000


    for t in range(TEST_TIME):


        world.step()



        if t % 100000 == 0:


            obs=observer.look(
                world
            )


            print(
                {
                    "time":world.time,

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