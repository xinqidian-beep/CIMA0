import numpy as np
from core.cell import Cell


class Universe:


    def __init__(
        self,
        n=4096,
        seed=42
    ):

        np.random.seed(seed)


        self.cells=[]


        for i in range(n):

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
                        0.95,
                        1.05
                    )

                )

            )


        self.time=0



    def tick(self, perturb=None):


        if perturb is None:

            perturb={}



        for i,c in enumerate(self.cells):


            p = perturb.get(
                i,
                0.0
            )


            c.step(
                perturb=p
            )



        self.time += 1



    def local_state(self, idx):

        return self.cells[idx].observe()