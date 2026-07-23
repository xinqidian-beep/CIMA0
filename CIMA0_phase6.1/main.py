import time

from core.network import OscillatorNetwork
from core.observer import Observer



def main():


    print(
        "=== CIMA0 Phase6.1 Natural Evolution ==="
    )


    net=OscillatorNetwork(
        n=128
    )


    obs=Observer()


    start=time.time()


    total=1000000


    for i in range(total):

        net.step()


        if i%100000==0:

            print(
                obs.snapshot(net)
            )


    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()