from core.universe import Universe


def main():


    print(
        "=== CIMA0 Phase6.6 Local Interaction ==="
    )


    u=Universe(
        n=4096
    )


    for i in range(
        10_000_000
    ):

        u.event()


        if i%1_000_000==0:

            print(
                u.snapshot()
            )



if __name__=="__main__":
    main()