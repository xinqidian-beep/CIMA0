from core.cell import Cell
from core.coupling import LocalCoupling


def main():

    a = Cell(
        x=1.0,
        v=0.0
    )


    b = Cell(
        x=-0.5,
        v=0.3
    )


    coupling = LocalCoupling(
        strength=0.01
    )


    steps = 200000


    for i in range(steps):


        coupling.connect(
            a,
            b
        )


        a.step()
        b.step()



        if i % 20000 == 0:

            distance = (
                a.x-b.x
            )


            print(
                i,
                {
                    "A":a.snapshot(),
                    "B":b.snapshot(),
                    "distance":round(distance,6)
                }
            )



if __name__ == "__main__":
    main()