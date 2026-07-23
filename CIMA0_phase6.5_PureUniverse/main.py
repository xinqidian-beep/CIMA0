import time

from core.universe import Universe
from core.observer import Observer



def main():


    print(
        "=== CIMA0 Phase6.5 Pure Universe ==="
    )


    u=Universe(
        n=40960
    )


    obs=Observer()


    start=time.time()


    target=10_000_000


    report=1_000_000


    while u.time < target:


        u.step(
            events=10000
        )


        if u.time % report == 0:

            print(
                obs.read(u)
            )


    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()