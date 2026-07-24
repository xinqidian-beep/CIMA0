import numpy as np
from core.cell import Cell


class Universe:


    def __init__(
        self,
        n=4096,
        seed=42
    ):

        np.random.seed(seed)

        self.time = 0

        self.cells=[]

        for _ in range(n):

            self.cells.append(
                Cell(
                    x=np.random.normal(0,0.01),
                    v=0.0,
                    omega=np.random.uniform(
                        0.95,
                        1.05
                    )
                )
            )


        # 固定局部连接
        self.edges=[]

        for i in range(n):

            self.edges.append(
                np.random.choice(
                    n,
                    4,
                    replace=False
                )
            )



    def step(self, events):

        dt=0.01


        for _ in range(events):

            for i,c in enumerate(self.cells):

                ids=self.edges[i]

                neighbors=[
                    self.cells[j].x
                    for j in ids
                ]

                c.step(
                    neighbors,
                    dt
                )


            self.time+=1



    def snapshot(self):

        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        energy=x*x*0.5


        return {

            "time":self.time,

            "cells":len(self.cells),

            "energy_mean":
                float(
                    energy.mean()
                ),

            "energy_std":
                float(
                    energy.std()
                ),

            "x_std":
                float(
                    x.std()
                )
        }


    def state_view(self):

        # 只提供副本

        return np.array(
            [
                c.x
                for c in self.cells
            ]
        )