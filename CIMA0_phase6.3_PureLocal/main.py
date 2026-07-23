import time

from core.network import LocalUniverse



def main():


    print(
        "=== CIMA0 Phase6.3 Pure Local ==="
    )


    universe=LocalUniverse(
        n=1024,
        degree=6
    )


    start=time.time()


    total=10_000_000


    report=1_000_000



    for i in range(total):

        universe.step()


        if i%report==0:

            print(
                universe.snapshot()
            )



    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()