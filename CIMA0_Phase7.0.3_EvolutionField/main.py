import time
import numpy as np


from core.universe import Universe

from observer.observer import Observer

from compute.field import ComputeField



def main():


    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    universe=Universe(
        n=4096
    )


    observer=Observer()


    compute=ComputeField(
        sample_size=64
    )


    start=time.time()


    last=0


    perturbed=False


    before=None



    while universe.time < 10_000_000:


        universe.event()



        # 云扰动

        if (
            universe.time==5_000_000
            and not perturbed
        ):

            before=universe.snapshot()


            idx=np.random.choice(
                len(universe.cells),
                32,
                replace=False
            )


            perturb={
                int(i):
                np.random.normal(
                    0,
                    0.01
                )
                for i in idx
            }


            for _ in range(1000):

                universe.event(
                    perturb
                )


            after=universe.snapshot()


            response=after-before


            print(
                {
                    "disturb_response":
                    observer.response(
                        response
                    )
                }
            )


            perturbed=True



        if universe.time-last>=100000:


            print(
                universe.stats(),
                "compute=",
                compute.compute(
                    universe
                )
            )


            last=universe.time



    print(
        "finished",
        time.time()-start
    )



if __name__=="__main__":

    main()