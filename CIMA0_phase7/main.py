import time

from core.network import NaturalObserverNetwork



def main():


    print(
        "=== CIMA0 Phase7.6 Natural Observer ==="
    )


    net=NaturalObserverNetwork(
        n=128,
        degree=4,
        coupling_strength=0.01
    )


    steps=1000000


    start=time.time()


    for i in range(steps):

        net.step(i)


        if i%100000==0:

            print(
                i,
                net.snapshot()
            )


    print(
        "runtime:",
        round(
            time.time()-start,
            3
        )
    )



if __name__=="__main__":

    main()