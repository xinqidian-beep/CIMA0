import numpy as np

from core.cell import Cell


class Population:

    def __init__(
        self,
        n=32,
        coupling=0.005
    ):

        self.n = n
        self.coupling = coupling

        self.cells = []

        for _ in range(n):

            self.cells.append(
                Cell(
                    x=np.random.uniform(-1,1),
                    v=np.random.uniform(-1,1)
                )
            )


    def step(self):

        fields = np.zeros(self.n)


        for i,a in enumerate(self.cells):

            for j,b in enumerate(self.cells):

                if i == j:
                    continue

                fields[i] += (
                    self.coupling *
                    (b.x-a.x)
                )


        for i,c in enumerate(self.cells):

            c.step(
                fields[i]
            )


    def statistics(self):

        energy = np.array(
            [
                c.energy
                for c in self.cells
            ]
        )


        phase = np.array(
            [
                np.arctan2(
                    c.v,
                    c.x
                )
                for c in self.cells
            ]
        )


        return {

            "energy_mean":
                float(
                    energy.mean()
                ),

            "energy_std":
                float(
                    energy.std()
                ),

            "phase_std":
                float(
                    phase.std()
                )
        }