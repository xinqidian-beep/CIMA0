import time

from core.network import AsyncEvolutionNetwork


def main():


    print(
        "=== CIMA0 Phase7.8 Minimal Async Scale ==="
    )


    net = AsyncEvolutionNetwork(
        cells=1024,
        avg_degree=4
    )


    EVENTS = 10_000_000


    interval = 1_000_000


    start=time.time()



    for i in range(
        0,
        EVENTS,
        interval
    ):


        net.step(
            interval
        )


        print(
            net.snapshot()
        )


    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":
    main()