import numpy as np

from core.cell import Cell
from core.coupling import LocalCoupling



class NaturalObserverNetwork:


    def __init__(
        self,
        n=128,
        degree=4,
        coupling_strength=0.01,
        seed=42
    ):

        np.random.seed(seed)


        self.n=n


        self.cells=[]


        self.edges=[]


        self.coupling=LocalCoupling(
            strength=coupling_strength
        )


        for _ in range(n):

            self.cells.append(

                Cell(
                    x=np.random.uniform(-1,1),
                    v=np.random.uniform(-0.5,0.5)
                )

            )


        self.create_graph(
            degree
        )



        self.top_history=[]



    def create_graph(
        self,
        degree
    ):

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



    def step(
        self,
        step_count
    ):


        #
        # local interaction
        #

        for a,b in self.edges:


            dx=(
                self.cells[b].x
                -
                self.cells[a].x
            )


            force=(
                self.coupling.strength
                *
                dx
            )


            self.cells[a].add_field(
                force
            )


            self.cells[b].add_field(
                -force
            )



        #
        # local evolution
        #

        for cell in self.cells:

            cell.step()



        #
        # observer only
        #

        if step_count % 1000 ==0:

            self.observe()



    def observe(self):


        index=max(

            range(self.n),

            key=lambda i:
                self.cells[i].activity_memory

        )


        value=self.cells[index].activity_memory


        self.top_history.append(
            index
        )


    def snapshot(self):


        xs=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        gs=np.array(
            [
                c.g
                for c in self.cells
            ]
        )


        memories=np.array(

            [
                c.activity_memory
                for c in self.cells
            ]

        )


        top=int(
            np.argmax(
                memories
            )
        )


        return {

            "cells":self.n,

            "edges":len(self.edges),

            "x_std":
                float(xs.std()),

            "g_mean":
                float(gs.mean()),

            "activity_mean":
                float(memories.mean()),

            "activity_std":
                float(memories.std()),

            "top_cell":
                top,

            "top_activity":
                float(memories[top])
        }