import time

from core.network import NaturalAsyncNetwork



def main():

    print(
        "=== CIMA0 Phase7.7 Minimal Async Evolution ==="
    )


    net = NaturalAsyncNetwork(
        n=128
    )


    start=time.time()


    for step in range(
        1000000
    ):


        net.step(
            events=1
        )


        if step%100000==0:

            print(
                step,
                net.snapshot()
            )


    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":
    main()