from core.cell import Cell
from core.environment import Environment


class Universe:


    def __init__(self,n):

        self.time=0

        self.cells=[
            Cell(i)
            for i in range(n)
        ]


        self.environment=Environment(
            n
        )


    def step(self):


        for cell in self.cells:


            local = self.environment.get(
                cell.cid
            )


            state = cell.step(
                local
            )


            self.environment.update(
                cell.cid,
                cell.activity()
            )


        self.time+=1



    def snapshot(self):

        values=[
            c.state
            for c in self.cells
        ]


        import numpy as np


        values=np.array(values)


        return {

            "time":
                self.time,


            "state_std":
                float(
                    np.std(values)
                ),


            "activity_mean":
                float(
                    np.mean(
                        np.linalg.norm(
                            values,
                            axis=1
                        )
                    )
                )
        }