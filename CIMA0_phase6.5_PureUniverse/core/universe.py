import numpy as np

from core.cell import Cell


class Universe:


    def __init__(
        self,
        n=4096,
        avg_degree=4
    ):

        self.n = n

        self.time = 0


        self.cells = []


        np.random.seed(42)


        for _ in range(n):

            self.cells.append(

                Cell(

                    x=np.random.uniform(
                        -1,
                        1
                    ),

                    v=np.random.uniform(
                        -0.5,
                        0.5
                    ),

                    omega=np.random.uniform(
                        0.95,
                        1.05
                    )

                )

            )


        self.build_network(
            avg_degree
        )



    def build_network(
        self,
        avg_degree
    ):

        self.neighbors = [
            []
            for _ in range(self.n)
        ]


        for i in range(self.n):

            choices=np.random.choice(
                self.n,
                avg_degree,
                replace=False
            )


            for j in choices:

                if j != i:

                    self.neighbors[i].append(j)



    def local_force(
        self,
        i
    ):

        force=0.0


        xi=self.cells[i].x


        for j in self.neighbors[i]:


            xj=self.cells[j].x

            force += (
                0.01 *
                np.sin(
                    xj-xi
                )
            )


            


        return force



    def step(
        self,
        events=1
    ):

        """
        asynchronous evolution

        only selected cells update
        """

        for _ in range(events):

            i=np.random.randint(
                self.n
            )


            f=self.local_force(i)


            self.cells[i].step(
                f
            )


            self.time += 1




    def snapshot(self):

        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        energy=np.array(
            [
                c.energy
                for c in self.cells
            ]
        )


        return {

            "time":
                self.time,

            "cells":
                self.n,

            "edges":
                len(self.edges),

            "x_std":
                float(xs.std()),

            "energy_mean":
                float(energies.mean()),

            "energy_std":
                float(energies.std()),
            "active_ratio":
                float(
                    np.mean(
                        energies > 1e-8
                    )
                )

        }