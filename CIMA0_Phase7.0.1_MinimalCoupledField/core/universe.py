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


        self.time=0


        self.cells=[

            Cell(
                np.random.uniform(
                    omega_min,
                    omega_max
                )
            )

            for _ in range(n)

        ]


        self.dt=dt


        self.neighbors=[]


        for i in range(n):

            ids=np.random.choice(
                n,
                avg_neighbors,
                replace=False
            )

            self.neighbors.append(ids)



    def step(self,cloud):


        n=len(self.cells)


        for _ in range(n):


            i=np.random.randint(n)


            cell=self.cells[i]


            local=np.mean(

                [
                    self.cells[j].x
                    for j in self.neighbors[i]

                ]

            )


            coupling=(local-cell.x)*0.05


            env=cloud[i]


            cell.step(

                coupling+env

            )


        self.time+=n



    def snapshot(self):


        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        e=np.array(
            [
                c.energy()
                for c in self.cells
            ]
        )


        return {

            "time":
                self.time,

            "cells":
                len(self.cells),

            "x_std":
                float(np.std(x)),

            "energy_mean":
                float(np.mean(e)),

            "energy_std":
                float(np.std(e))

        }