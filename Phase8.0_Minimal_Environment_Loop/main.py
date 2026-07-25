import numpy as np
import time


from core.universe import Universe
from cloud.cloud import Cloud
from environment.environment import Environment
from observer.observer import Observer



def main():


    print(
        "=== CIMA0 Phase8.0 EnvironmentLoop ==="
    )


    universe=Universe(
        n=4096
    )


    cloud=Cloud(
        n_cells=4096
    )


    env=Environment()


    observer=Observer()



    total=20_000_000


    for step in range(total):


        perturb={}


        # 环境决定是否产生云
        if env.stimulate():

            perturb=cloud.contact()



        universe.step(
            perturb
        )


        if step % 100000 ==0:


            state=universe.state()


            env.receive(
                state
            )


            print(
                {

                **universe.stats(),

                "cloud":
                    len(perturb),

                "environment":
                    env.pressure,

                "observer":
                    observer.observe(
                        universe
                    )

                }
            )


    print(
        "finished"
    )



if __name__=="__main__":

    main()