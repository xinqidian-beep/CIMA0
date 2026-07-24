from core.universe import Universe
from core.observer import Observer


def main():


    print(
    "=== CIMA0 Phase7.0.1 Local Cloud ==="
    )


    u=Universe(
        n=4096
    )


    obs=Observer()



    while True:


        u.step(
            1000000
        )


        print(
            obs.read(u)
        )



if __name__=="__main__":
    main()