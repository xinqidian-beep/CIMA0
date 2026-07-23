from core.network import OscillatorNetwork



def main():


    print(
        "=== CIMA0 Phase6.2 Pure Dynamics ==="
    )


    net=OscillatorNetwork(
        n=128,
        avg_degree=4,
        coupling=0.01
    )


    STEPS=1000000


    for i in range(STEPS):

        net.step(
            events=1
        )


        if i%100000==0:

            print(
                net.snapshot()
            )



if __name__=="__main__":

    main()