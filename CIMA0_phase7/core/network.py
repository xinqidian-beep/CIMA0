import numpy as np

from core.cell import Cell
from core.coupling import LocalCoupling
from core.topology import AdaptiveTopology



class CellNetwork:


    def __init__(
        self,
        n=32,
        degree=4
    ):

        self.n=n

        self.cells=[]

        self.edges=[]


        for i in range(n):

            self.cells.append(
                Cell(
                    np.random.uniform(-1,1),
                    np.random.uniform(-0.5,0.5)
                )
            )


        self._create_graph(
            degree
        )


        self.topology=AdaptiveTopology(
            n,
            self.edges
        )


        self.coupling=LocalCoupling()



    def _create_graph(
        self,
        degree
    ):

        for i in range(self.n):

            ns=np.random.choice(
                [
                    j for j in range(self.n)
                    if j!=i
                ],
                degree,
                replace=False
            )


            for j in ns:

                if i<j:
                    self.edges.append(
                        (i,j)
                    )



    def step(
        self,
        step_count
    ):


        # local dynamics

        for c in self.cells:
            c.step()



        # relations

        for a,b in self.edges:

            w=self.topology.weight(
                a,b
            )


            self.coupling.connect(
                self.cells[a],
                self.cells[b],
                w
            )



        self.coupling.apply()



        if step_count%100==0:

            self.topology.update(
                [
                    c.x
                    for c in self.cells
                ]
            )



    def snapshot(self):

        xs=np.array(
            [
                c.x for c in self.cells
            ]
        )

        gs=np.array(
            [
                c.g for c in self.cells
            ]
        )


        return {

            "cells":self.n,

            "edges":len(self.edges),

            "x_std":float(xs.std()),

            "g_mean":float(gs.mean()),

            "g_std":float(gs.std()),

            "active":int(
                np.sum(abs(xs)>0.1)
            )
        }