import numpy as np

from core.cell import Cell
from core.cloud import CloudField
from core.interaction import LocalInteraction



class Universe:


    def __init__(
        self,
        n,
        avg_neighbors,
        dt,
        omega_min,
        omega_max,
        cloud_size,
        cloud_strength,
        seed
    ):


        np.random.seed(seed)


        self.dt=dt

        self.time=0



        self.cells=[

            Cell(
                np.random.uniform(
                    omega_min,
                    omega_max
                )
            )

            for _ in range(n)

        ]


        self.edges=[]


        for i in range(n):

            ids=np.random.choice(
                n,
                avg_neighbors,
                replace=False
            )

            self.edges.append(ids)



        self.cloud=CloudField(
            cloud_size,
            cloud_strength,
            seed
        )


        self.interaction=LocalInteraction()



    def event(self):


        i=np.random.randint(
            len(self.cells)
        )


        cell=self.cells[i]


        neighbors=[

            self.cells[j]

            for j in self.edges[i]

        ]


        f=self.interaction.force(
            cell,
            neighbors
        )


        cloud_force=self.cloud.sample(i)


        cell.step(
            self.dt,
            f+cloud_force
        )



    def step(
        self,
        events
    ):


        for _ in range(events):


            self.cloud.step()


            self.event()


            self.time+=1



    def snapshot(self):


        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        e=np.array(
            [
                c.energy()
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
                float(e.mean()),

            "energy_std":
                float(e.std())

        }