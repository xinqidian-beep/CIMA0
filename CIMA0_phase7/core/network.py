import numpy as np

from core.cell import Cell
from core.coupling import LocalCoupling


class CellNetwork:


    def __init__(
        self,
        n=128,
        degree=4
    ):

        np.random.seed(42)


        self.n=n


        self.cells=[]

        self.edges=[]


        self.coupling=LocalCoupling(
            strength=0.01
        )


        for i in range(n):

            self.cells.append(

                Cell(

                    x=np.random.uniform(-1,1),

                    v=np.random.uniform(
                        -0.5,
                        0.5
                    )

                )

            )


        self.create_graph(
            degree
        )



    def create_graph(self,degree):


        for i in range(self.n):

            neighbors=np.random.choice(

                [
                    j
                    for j in range(self.n)
                    if j!=i
                ],

                size=degree,

                replace=False
            )


            for j in neighbors:

                if i<j:

                    self.edges.append(
                        (i,j)
                    )



    def step(self):


        self.coupling.clear()


        for a,b in self.edges:


            self.coupling.connect(

                self.cells[a],

                self.cells[b]

            )


        self.coupling.apply()



        for c in self.cells:

            c.step()



    def snapshot(self):


        activity=np.array(

            [
                c.activity()
                for c in self.cells
            ]

        )


        energy=np.array(

            [
                c.energy
                for c in self.cells
            ]

        )


        fatigue=np.array(

            [
                c.fatigue
                for c in self.cells
            ]

        )


        top=int(
            np.argmax(activity)
        )


        return {


            "cells":self.n,

            "edges":len(self.edges),


            "activity_mean":
            float(activity.mean()),


            "activity_std":
            float(activity.std()),


            "energy_mean":
            float(energy.mean()),


            "fatigue_mean":
            float(fatigue.mean()),


            "top_cell":
            top,


            "top_activity":
            float(activity[top])

        }