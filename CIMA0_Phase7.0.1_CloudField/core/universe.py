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
        seed,
        cloud
    ):


        self.rng=np.random.default_rng(
            seed
        )


        self.time=0


        self.cells=[]


        for _ in range(n):

            omega=self.rng.uniform(
                omega_min,
                omega_max
            )


            self.cells.append(
                Cell(
                    omega,
                    dt,
                    seed=self.rng.integers(999999)
                )
            )


        self.neighbors=[]


        for i in range(n):

            ids=self.rng.choice(
                n,
                avg_neighbors,
                replace=False
            )

            self.neighbors.append(
                ids
            )



        self.cloud=cloud



    def event(self):


        i=self.rng.integers(
            len(self.cells)
        )


        cell=self.cells[i]


        coupling=0



        for j in self.neighbors[i]:

            other=self.cells[j]


            coupling += (
                other.x
                -
                cell.x
            )


        coupling*=0.02



        cloud_force=(
            self.cloud.sample(i)
            *
            0.01
        )


        cell.step(
            coupling+
            cloud_force
        )



        self.time+=1




    def step(
        self,
        events
    ):


        for _ in range(events):

            self.cloud.evolve()

            self.event()



    def snapshot(self):


        xs=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        energies=np.array(
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
                float(xs.std()),


            "energy_mean":
                float(
                    energies.mean()
                ),


            "energy_std":
                float(
                    energies.std()
                ),


            "cloud_std":
                float(
                    self.cloud.field.std()
                )
        }