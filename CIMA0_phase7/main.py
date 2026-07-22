import time

from core.network import CellNetwork



def main():

    print(
        "=== CIMA0 Phase7.2 Network Emergence ==="
    )


    net=CellNetwork(
        n=32,
        degree=4
    )


    steps=500000


    start=time.time()


    for i in range(steps):

        net.step(i)


        if i%50000==0:

            print(
                i,
                net.snapshot()
            )


    print()

    print(
        "runtime:",
        round(time.time()-start,3)
    )



if __name__=="__main__":
    main()