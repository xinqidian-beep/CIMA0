import numpy as np

from core.cell import Cell



class Universe:


    def __init__(
        self,
        n,
        avg_neighbors,
        dt,
        omega_min,
        omega_max,
        seed
    ):

        np.random.seed(seed)

        self.n=n
        self.dt=dt

        self.time=0


        self.cells=[]


        for i in range(n):

            self.cells.append(
                Cell(
                    omega=np.random.uniform(
                        omega_min,
                        omega_max
                    ),
                    x=np.random.normal(
                        0,
                        0.01
                    ),
                    v=np.random.normal(
                        0,
                        0.01
                    )
                )
            )


        self.neighbors=[]


        for i in range(n):

            ids=np.random.choice(
                n,
                avg_neighbors,
                replace=False
            )

            self.neighbors.append(ids)



    def event(self):


        i=np.random.randint(
            self.n
        )


        cell=self.cells[i]


        coupling=0.0


        for j in self.neighbors[i]:

            coupling += (
                self.cells[j].x
                -
                cell.x
            )


        coupling*=0.02



        cell.step(
            coupling,
            self.dt
        )


        self.time+=1



    def run(
        self,
        steps
    ):

        for _ in range(steps):

            self.event()



    def snapshot(self):

        energies=np.array(
            [
                c.energy()
                for c in self.cells
            ]
        )


        return {

            "time":
                self.time,

            "cells":
                self.n,

            "energy_mean":
                float(
                    energies.mean()
                ),

            "energy_std":
                float(
                    energies.std()
                ),

            "x_std":
                float(
                    np.std(
                        [
                            c.x
                            for c in self.cells
                        ]
                    )
                )
        }