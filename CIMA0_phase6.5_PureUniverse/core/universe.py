import numpy as np
from core.cell import Cell


class Universe:


    def __init__(
        self,
        n=4096,
        degree=4
    ):

        self.time=0

        self.dt=0.01


        self.cells=[]


        for i in range(n):

            self.cells.append(
                Cell(
                    x=np.random.normal(
                        0,
                        0.5
                    ),
                    v=np.random.normal(
                        0,
                        0.1
                    ),
                    omega=np.random.uniform(
                        0.95,
                        1.05
                    )
                )
            )


        # 每个个体自己的邻居
        self.neighbors=[]


        for i in range(n):

            ids=np.random.choice(
                n,
                degree,
                replace=False
            )

            ids=[
                x for x in ids
                if x!=i
            ]

            self.neighbors.append(ids)



    def local_interaction(
        self,
        i
    ):


        cell=self.cells[i]


        force=0.0


        for j in self.neighbors[i]:

            other=self.cells[j]


            # 关系偏差
            dx=other.x-cell.x


            # 对称作用
            force += (
                0.01
                *
                dx
            )


        return force



    def event(self):


        i=np.random.randint(
            len(self.cells)
        )


        f=self.local_interaction(i)


        self.cells[i].step(
            f,
            self.dt
        )


        self.time+=1



    def snapshot(self):


        xs=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        energy=np.array(
            [
                0.5*(c.x*c.x+c.v*c.v)
                for c in self.cells
            ]
        )


        return {

            "time":
                self.time,

            "cells":
                len(self.cells),

            "x_std":
                float(xs.std()),

            "energy_mean":
                float(energy.mean()),

            "energy_std":
                float(energy.std())
        }