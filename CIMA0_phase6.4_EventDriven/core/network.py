import numpy as np

from core.cell import Cell
from core.scheduler import Scheduler


class Network:


    def __init__(self,n=1024):


        self.cells=[]


        for i in range(n):

            self.cells.append(

                Cell(
                    i,
                    np.random.uniform(-1,1),
                    np.random.uniform(-1,1)
                )

            )



        self.connect()


        self.scheduler=Scheduler()


        for c in self.cells:

            self.scheduler.add(
                c,
                0
            )



    def connect(self):

        for c in self.cells:


            ids=np.random.choice(
                len(self.cells),
                4,
                replace=False
            )


            for i in ids:

                if i!=c.id:

                    c.neighbors.append(
                        (
                            self.cells[i],
                            0.01
                        )
                    )



    def step(self,n):

        self.scheduler.run(n)



    def snapshot(self):

        x=np.array(
            [
                c.oscillator.x
                for c in self.cells
            ]
        )


        e=np.array(
            [
                c.oscillator.energy
                for c in self.cells
            ]
        )


        return {

            "time_events":
                sum(
                    c.local_time
                    for c in self.cells
                ),

            "cells":
                len(self.cells),

            "x_std":
                float(x.std()),

            "energy_mean":
                float(e.mean()),

            "energy_std":
                float(e.std())
        }