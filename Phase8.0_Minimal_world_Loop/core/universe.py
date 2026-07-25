from core.cell import Cell
from core.environment import Environment



class Universe:


    def __init__(
        self,
        n
    ):

        self.time=0


        self.cells=[
            Cell(i)
            for i in range(n)
        ]


        self.environment=Environment(
            n
        )



    def step(self):


        self.time+=1


        #
        # 每个个体只处理自己
        #

        for c in self.cells:


            local = (
                self.environment
                .interact(
                    c.cid
                )
            )


            residue = c.step(
                local
            )


            self.environment.deposit(
                c.cid,
                residue
            )


        self.environment.decay()



    def stats(self):


        import numpy as np


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


            "x_std":
            float(
                np.std(x)
            ),


            "environment":
            float(
                self.environment.measure()
            )
        }