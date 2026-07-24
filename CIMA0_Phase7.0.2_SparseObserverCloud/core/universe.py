import numpy as np

from core.cell import Cell



class Universe:


    def __init__(
        self,
        n,
        avg_neighbors,
        omega_min,
        omega_max,
        seed
    ):


        np.random.seed(seed)

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



        self.neighbors=[]


        for i in range(n):

            self.neighbors.append(

                np.random.choice(
                    n,
                    avg_neighbors,
                    replace=False
                )

            )



    def event(self,cloud):


        i=np.random.randint(

            len(self.cells)

        )


        cell=self.cells[i]


        local=np.mean(

            [
                self.cells[j].x

                for j in self.neighbors[i]

            ]

        )


        coupling=(

            local-cell.x

        )*0.05



        cell.step(

            coupling
            +
            cloud.get(i)

        )


        self.time+=1



    def run(self,events,cloud):

        for _ in range(events):

            self.event(cloud)



    def snapshot(self):


        e=np.array(

            [
                c.energy()

                for c in self.cells

            ]

        )


        x=np.array(

            [
                c.x

                for c in self.cells

            ]

        )


        return {


            "time":self.time,

            "cells":len(self.cells),

            "x_std":float(np.std(x)),


            "energy_mean":
                float(np.mean(e)),


            "energy_std":
                float(np.std(e))

        }