import numpy as np

from core.cell import Cell


class Universe:
    """
    Pure dynamical core.

    Rules:

    1. Cell dynamics is closed.
    2. External field can only perturb state.
    3. No observer.
    4. No ranking.
    5. No global optimization.
    6. No memory inside dynamics.

    Evolution:
        local state
            |
            v
        coupling
            |
            v
        oscillator update

    """

    def __init__(
        self,
        n=4096,
        avg_neighbors=4,
        omega_min=0.95,
        omega_max=1.05,
        dt=0.01,
        seed=42
    ):

        self.n = n
        self.dt = dt

        np.random.seed(seed)


        self.cells=[]


        for _ in range(n):

            self.cells.append(

                Cell(

                    x=np.random.normal(
                        0,
                        0.01
                    ),

                    v=np.random.normal(
                        0,
                        0.01
                    ),

                    omega=np.random.uniform(
                        omega_min,
                        omega_max
                    )

                )

            )


        #
        # fixed random local topology
        #
        self.neighbors=[]


        for i in range(n):

            ids=np.random.choice(
                n,
                avg_neighbors,
                replace=False
            )

            self.neighbors.append(
                ids
            )


        self.time=0



    def step(self, events):

        for _ in range(events):

            self._single_step()

            self.time += 1



    def _single_step(self):


        xs=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        for i,cell in enumerate(self.cells):


            #
            # local coupling only
            #
            neighbor_mean=np.mean(
                xs[
                    self.neighbors[i]
                ]
            )


            coupling = (
                neighbor_mean
                -
                cell.x
            )


            #
            # pure oscillator
            #
            cell.step(
                coupling,
                self.dt
            )



    def snapshot(self):

        xs=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        energy=np.array(
            [
                0.5*c.v*c.v
                +
                0.5*c.omega*c.omega*c.x*c.x
                for c in self.cells
            ]
        )


        return {


            "time":
                self.time,


            "cells":
                self.n,


            "energy_mean":
                float(
                    np.mean(energy)
                ),


            "energy_std":
                float(
                    np.std(energy)
                ),


            "x_std":
                float(
                    np.std(xs)
                )

        }