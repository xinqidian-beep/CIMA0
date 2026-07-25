from core.world import World
from core.environment import Environment
from core.observer import Observer



def main():


    print(
        "=== Phase8.0 Minimal World ==="
    )


    world=World(
        n=4096
    )


    env=Environment()

    obs=Observer()



    for i in range(
        10000000
    ):


        world.step(
            env
        )


        if i%100000==0:


            print(

                world.snapshot(),

                obs.observe(
                    world
                )

            )




if __name__=="__main__":

    main()