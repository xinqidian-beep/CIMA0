import numpy as np

from core.cell import Cell
from core.observer import ObserverSystem


N = 4096
STEPS = 200000


def create_cells():

    return [
        Cell(i)
        for i in range(N)
    ]


def collect_stats(cells):

    xs = np.array(
        [
            c.x
            for c in cells
        ]
    )

    vs = np.array(
        [
            c.v
            for c in cells
        ]
    )

    return {

        "x_mean":
            float(xs.mean()),

        "x_std":
            float(xs.std()),

        "v_mean":
            float(vs.mean()),

        "v_std":
            float(vs.std()),

        "activity_mean":
            float(
                np.mean(
                    np.sqrt(
                        xs**2 + vs**2
                    )
                )
            )
    }



def run_without_observer():

    print("\n=== World A : No Observer ===")


    np.random.seed(42)

    cells = create_cells()


    for t in range(STEPS):

        for cell in cells:

            cell.step()


        if t % 50000 == 0:

            print(
                t,
                collect_stats(cells)
            )


    return collect_stats(cells)



def run_with_observer():

    print("\n=== World B : With Observer ===")


    np.random.seed(42)

    cells = create_cells()


    observer = ObserverSystem(
        sample_size=64,
        history_size=8,
        threshold=0.5,
        decay=0.90,
        spread=0.15,
        exploration=0.1
    )


    for t in range(STEPS):

        for cell in cells:

            cell.step()


        if t % 1000 == 0:

            observer.sample(
                cells,
                t
            )


        if t % 50000 == 0:

            print(
                t,
                collect_stats(cells),
                "observer_field=",
                len(
                    observer.observation_field
                )
            )


    return collect_stats(cells)



if __name__ == "__main__":


    a = run_without_observer()

    b = run_with_observer()


    print("\n=== Difference ===")


    for k in a:

        print(
            k,
            "A-B =",
            abs(
                a[k]-b[k]
            )
        )