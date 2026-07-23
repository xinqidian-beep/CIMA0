import time

from core.network import OscillatorNetwork



def main():

    print(
        "=== CIMA0 Phase6.3 Open Universe ==="
    )


    net=OscillatorNetwork(
        n=1024,
        avg_degree=6
    )


    start=time.time()


    total=10_000_000


    report=1_000_000


    for i in range(total):

        net.step(
            events=1
        )


        if i%report==0:

            print(
                net.snapshot()
            )


    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()