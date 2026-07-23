import numpy as np

from core.oscillator import Oscillator
from core.topology import LocalTopology



class OscillatorNetwork:


    def __init__(
        self,
        n=128,
        avg_degree=4,
        coupling=0.01
    ):

        np.random.seed(42)


        self.n=n

        self.time=0

        self.coupling=coupling



        self.cells=[]


        for i in range(n):

            self.cells.append(

                Oscillator(

                    x=np.random.uniform(
                        -1.5,
                        1.5
                    ),

                    v=np.random.uniform(
                        -0.8,
                        0.8
                    ),

                    omega=np.random.uniform(
                        0.97,
                        1.03
                    ),

                    mu=np.random.uniform(
                        0.55,
                        0.65
                    )

                )

            )



        self.topology=LocalTopology(
            n,
            avg_degree
        )




    def local_force(
        self,
        idx
    ):

        force=0.0


        for a,b in self.topology.edges:


            if a==idx:

                other=self.cells[b]

                force += (
                    self.coupling*
                    np.sin(
                        other.x-
                        self.cells[idx].x
                    )
                )


            elif b==idx:

                other=self.cells[a]

                force += (
                    self.coupling*
                    np.sin(
                        other.x-
                        self.cells[idx].x
                    )
                )



        return force




    def step(
        self,
        events=1
    ):


        for _ in range(events):


            # no global clock

            i=np.random.randint(
                self.n
            )


            force=self.local_force(
                i
            )


            self.cells[i].step(
                force
            )


            self.time+=1




    def snapshot(self):


        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        energy=np.array(
            [
                c.energy
                for c in self.cells
            ]
        )



        return {


            "time":
                self.time,


            "cells":
                self.n,


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
                )

        }