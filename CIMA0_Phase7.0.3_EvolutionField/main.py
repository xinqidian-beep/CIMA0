import time

from core.universe import Universe



EVENTS = 10_000_000

REPORT = 100_000



def main():


    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    u=Universe(

        n=4096,

        degree=4,

        coupling=0.01,

        seed=42

    )



    start=time.time()



    for step in range(EVENTS):


        u.event()



        if step % REPORT == 0:


            print(

                u.snapshot(),

                "compute_field=64"

            )



    print(

        "finished",

        time.time()-start

    )




if __name__=="__main__":

    main()