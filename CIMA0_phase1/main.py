from network import OscillatorNetwork
from observer import Observer


if __name__ == "__main__":


    net = OscillatorNetwork(
        n=1000,
        coupling=0.12,
        avg_degree=6
    )


    obs = Observer()


    STEPS = 500000


    print(
        "=== CIMA0 Phase1 ==="
    )


    for step in range(STEPS):

        net.step()


        if step % 5000 == 0:

            data = obs.measure(net)

            print(
                step,
                data
            )