import numpy as np

from core.cell import Cell


class Edge:


    def __init__(
        self,
        a,
        b,
        weight=0.5
    ):

        self.a=a
        self.b=b

        self.weight=weight

        self.activity=0.0

        self.age=0



    def update(
        self,
        signal
    ):

        self.activity += (
            0.001 *
            (
                abs(signal)
                -
                self.activity
            )
        )


        self.weight += (
            0.00001 *
            (
                self.activity
                -
                0.05
            )
        )


        self.weight *= 0.999999


        if self.weight < 0:
            self.weight=0



        self.age += 1



    def alive(self):

        return self.weight > 0.05






class CellNetwork:



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


        for i in range(n):

            self.cells.append(

                Cell(
                    x=np.random.uniform(-1,1),
                    v=np.random.uniform(-0.5,0.5)
                )

            )



        self.edges=[]


        self._create_graph(
            degree
        )



        self.coupling_strength=coupling_strength



    def _create_graph(
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

                        Edge(
                            i,
                            j,
                            np.random.uniform(
                                0.3,
                                0.7
                            )
                        )

                    )



    def step(
        self,
        step_count
    ):



        fields=np.zeros(
            self.n
        )



        # ----------------
        # edge interaction
        # ----------------

        for e in self.edges:


            a=self.cells[e.a]

            b=self.cells[e.b]



            diff=b.x-a.x



            force=(
                diff*
                e.weight*
                self.coupling_strength
            )



            fields[e.a]+=force

            fields[e.b]-=force



            e.update(
                force
            )




        # apply field


        for i,c in enumerate(self.cells):

            c.add_field(
                fields[i]
            )



        # cell evolution


        for c in self.cells:

            c.step()



        # slow topology evolution

        if step_count % 5000 == 0:


            self.edges=[

                e
                for e in self.edges
                if e.alive()

            ]




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


        weights=np.array(

            [
                e.weight
                for e in self.edges
            ]

        )



        degree=np.zeros(
            self.n
        )


        for e in self.edges:

            degree[e.a]+=1

            degree[e.b]+=1



        return {


            "cells":
                self.n,


            "edges":
                len(self.edges),


            "x_std":
                float(xs.std()),


            "g_mean":
                float(gs.mean()),


            "g_std":
                float(gs.std()),



            "energy_mean":
                float(
                    np.mean(
                        [
                            c.energy
                            for c in self.cells
                        ]
                    )
                ),



            "weight_mean":
                float(
                    weights.mean()
                )
                if len(weights)
                else 0,



            "active":
                int(
                    np.sum(
                        abs(xs)>0.1
                    )
                ),



            "degree_mean":
                float(
                    degree.mean()
                )

        }