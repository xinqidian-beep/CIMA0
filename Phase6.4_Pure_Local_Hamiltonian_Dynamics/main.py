from core.network import LocalHamiltonianNetwork
import time



def main():


    print(
        "=== CIMA0 Phase6.4 Pure Hamiltonian ==="
    )


    net=LocalHamiltonianNetwork(
        n=1024,
        degree=4
    )


    start=time.time()


    total=10_000_000



    for i in range(total):


        net.step()


        if i%1_000_000==0:

            print(
                net.snapshot()
            )



    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":

    main()