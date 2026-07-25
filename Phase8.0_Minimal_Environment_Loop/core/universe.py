import numpy as np

from core.cell import Cell



class Universe:


    def __init__(
        self,
        n=4096
    ):

        self.cells = [
            Cell()
            for _ in range(n)
        ]

        self.time = 0



    def state(self):

        return np.array(
            [
                c.x
                for c in self.cells
            ]
        )



    def step(
        self,
        perturb={}
    ):

        n = len(self.cells)


        # 异步局部事件
        idx = np.random.randint(
            0,
            n
        )


        force = perturb.get(
            idx,
            0.0
        )


        self.cells[idx].step(
            force
        )


        self.time += 1



    def stats(self):

        x = self.state()


        energy = np.array(
            [
                c.energy
                for c in self.cells
            ]
        )


        return {

            "time":
                self.time,

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