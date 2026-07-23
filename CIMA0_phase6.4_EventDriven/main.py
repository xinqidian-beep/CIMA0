from core.network import Network


def main():


    print(
        "=== CIMA0 Phase6.4 Event Driven ==="
    )


    net=Network(
        1024
    )


    for i in range(10):

        net.step(
            10000000
        )


        print(
            net.snapshot()
        )


if __name__=="__main__":

    main()