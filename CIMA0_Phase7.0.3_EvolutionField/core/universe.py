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



    def tick(self):

        """
        动力系统自己的时间推进

        不知道observer
        不知道compute
        """

        for c in self.cells:

            c.step()


        self.time+=1



    def local_state(self, idx):

        return self.cells[idx].observe()