import random
import numpy as np

from core.cell import Cell



class Universe:


    def __init__(
        self,
        n=4096,
        seed=42
    ):

        np.random.seed(seed)
        random.seed(seed)

        self.time=0


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

                    omega=1.0
                )
            )


        self.neighbors={}


        k=8


        for i in range(n):

            ids=list(range(n))

            ids.remove(i)

            self.neighbors[i]=random.sample(
                ids,
                k
            )



    def event(
        self,
        perturb=None
    ):


        idx=random.randrange(
            len(self.cells)
        )


        cell=self.cells[idx]


        force=0.0


        for j in self.neighbors[idx]:

            other=self.cells[j]


            force += (
                other.x-cell.x
            )*0.01



        p=0.0


        if perturb is not None:

            p=perturb.get(
                idx,
                0.0
            )


        cell.step(
            force=force,
            perturb=p
        )


        self.time+=1



    def stats(self):

        energy=np.array(
            [
                c.energy
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
                    np.std(x)
                )
        }


    def snapshot(self):

        return np.array(
            [
                c.x
                for c in self.cells
            ]
        )