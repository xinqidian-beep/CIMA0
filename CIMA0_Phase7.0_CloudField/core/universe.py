import numpy as np

from core.cell import Cell



class Universe:


    def __init__(
        self,
        n,
        avg_neighbors,
        dt,
        omega_min,
        omega_max,
        seed=0
    ):


        self.rng=np.random.default_rng(seed)

        self.time=0

        self.cells=[]


        for _ in range(n):

            self.cells.append(
                Cell(
                    omega=self.rng.uniform(
                        omega_min,
                        omega_max
                    ),
                    dt=dt
                )
            )


        self.neighbors=[]


        for i in range(n):

            ids=self.rng.choice(
                n,
                avg_neighbors,
                replace=False
            )

            self.neighbors.append(ids)



    def event(
        self,
        disturbance
    ):

        i=self.rng.integers(
            len(self.cells)
        )


        c=self.cells[i]


        coupling=0.0


        for j in self.neighbors[i]:

            coupling += (
                self.cells[j].x
                -
                c.x
            )


        coupling /= len(
            self.neighbors[i]
        )


        c.step(
            coupling,
            disturbance
        )


        self.time += 1



    def step(
        self,
        events,
        cloud
    ):


        for _ in range(events):

            d=cloud.perturb()

            self.event(d)



    def snapshot(self):


        xs=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        es=np.array(
            [
                c.energy()
                for c in self.cells
            ]
        )


        return {

            "time":self.time,

            "cells":len(self.cells),

            "x_std":float(xs.std()),

            "energy_mean":float(es.mean()),

            "energy_std":float(es.std())

        }