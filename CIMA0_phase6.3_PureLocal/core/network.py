import numpy as np

from core.cell import Cell



class LocalUniverse:


    def __init__(
        self,
        n=1024,
        degree=6,
        coupling=0.05
    ):


        np.random.seed(42)

        self.n=n

        self.time=0

        self.coupling=coupling



        self.cells=[]


        for i in range(n):

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


        self.neighbors=self.build_network(
            degree
        )



    def build_network(
        self,
        degree
    ):

        neighbors=[
            []
            for _ in range(self.n)
        ]


        for i in range(self.n):

            targets=np.random.choice(
                [
                    j
                    for j in range(self.n)
                    if j!=i
                ],
                degree,
                replace=False
            )


            for j in targets:

                neighbors[i].append(j)



        return neighbors



    def step(self):

        # one local event

        i=np.random.randint(
            self.n
        )


        cell=self.cells[i]


        force=0.0


        # ONLY local information

        for j in self.neighbors[i]:

            other=self.cells[j]


            force += (

                np.sin(
                    other.x-cell.x
                )

            )



        force*=self.coupling


        cell.update(
            force
        )


        self.time+=1



    def snapshot(self):

        # observer only

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
                self.n,

            "x_std":
                float(x.std()),

            "energy_mean":
                float(e.mean()),

            "energy_std":
                float(e.std())

        }