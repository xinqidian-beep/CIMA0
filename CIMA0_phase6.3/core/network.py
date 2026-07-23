import numpy as np

from core.oscillator import Oscillator
from core.field import LocalField



class OscillatorNetwork:


    def __init__(
        self,
        n=1024,
        avg_degree=6,
        coupling=0.08
    ):

        np.random.seed(42)

        self.n=n

        self.coupling=coupling

        self.time=0


        self.cells=[]


        for i in range(n):

            self.cells.append(

                Oscillator(

                    x=np.random.uniform(
                        -1.8,
                        1.8
                    ),

                    v=np.random.uniform(
                        -0.8,
                        0.8
                    ),

                    omega=np.random.uniform(
                        0.97,
                        1.03
                    )
                )
            )


        self.build_edges(
            avg_degree
        )


        self.field=LocalField(n)



    def build_edges(
        self,
        avg_degree
    ):

        edges=set()


        while len(edges)<self.n*avg_degree//2:

            a=np.random.randint(
                0,
                self.n
            )

            b=np.random.randint(
                0,
                self.n
            )


            if a!=b:

                if a>b:
                    a,b=b,a

                edges.add(
                    (a,b)
                )


        edges=list(edges)


        self.edges_from=np.array(
            [
                e[0]
                for e in edges
            ]
        )


        self.edges_to=np.array(
            [
                e[1]
                for e in edges
            ]
        )



    def step(
        self,
        events=1
    ):


        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        field=self.field.update(
            x,
            self.edges_from,
            self.edges_to
        )


        # asynchronous local evolution

        for _ in range(events):

            i=np.random.randint(
                0,
                self.n
            )


            local_force=(

                self.coupling
                *
                field[i]

            )


            self.cells[i].step(
                local_force
            )


        self.time+=events




    def snapshot(self):

        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        phase=np.array(
            [
                c.phase()
                for c in self.cells
            ]
        )


        energy=0.5*x*x


        return {

            "time":
                self.time,

            "cells":
                self.n,

            "edges":
                len(self.edges_from),

            "x_std":
                float(
                    x.std()
                ),

            "energy_mean":
                float(
                    energy.mean()
                ),

            "energy_std":
                float(
                    energy.std()
                ),

            "phase_std":
                float(
                    phase.std()
                )
        }