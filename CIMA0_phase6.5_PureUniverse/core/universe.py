import numpy as np

from core.cell import Cell
from core.topology import Topology
from core.event_queue import EventQueue
from core.oscillator import Oscillator



class Universe:


    def __init__(
        self,
        n=4096
    ):

        np.random.seed(42)


        self.time=0


        self.cells=[]


        for _ in range(n):

            self.cells.append(

                Cell(

                    x=np.random.uniform(
                        -1,1
                    ),

                    v=np.random.uniform(
                        -0.5,0.5
                    ),

                    omega=np.random.uniform(
                        0.95,
                        1.05
                    )

                )

            )


        self.topology=Topology(
            n
        )


        self.events=EventQueue(
            n
        )



    def update(
        self,
        steps
    ):


        for _ in range(steps):

            i=self.events.pop()


            if i is None:
                break


            cell=self.cells[i]


            force=0.0


            for j in self.topology.neighbors[i]:

                force += Oscillator.coupling(
                    cell,
                    self.cells[j]
                )



            cell.step(
                force
            )


            # 局部影响

            self.events.push_neighbors(
                self.topology.neighbors[i]
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
                len(self.cells),

            "x_std":
                float(x.std()),

            "energy_mean":
                float(
                    energy.mean()
                ),

            "energy_std":
                float(
                    energy.std()
                )
        }