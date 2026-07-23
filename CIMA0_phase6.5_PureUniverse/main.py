import time

from core.universe import Universe



def main():

    print(
        "=== CIMA0 Phase6.5 Pure Universe ==="
    )


    u=Universe(
        n=40960
    )


    start=time.time()


    for i in range(10):


        u.update(
            1000000
        )


        print(
            u.snapshot()
        )


    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()