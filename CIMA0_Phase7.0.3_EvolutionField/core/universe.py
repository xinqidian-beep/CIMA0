import numpy as np
from core.cell import Cell


class Universe:


    def __init__(
        self,
        n=4096,
        seed=42
    ):

        np.random.seed(seed)

        self.cells={}


        for i in range(n):

            self.cells[i]=Cell(
                x=np.random.normal(0,0.01),
                v=np.random.normal(0,0.01),
                omega=np.random.uniform(
                    0.95,
                    1.05
                )
            )


        self.time=0



    def evolve_cells(self, ids):

        """
        只推进被计算系统要求展开的cell
        """

        for i in ids:

            self.cells[i].evolve()



    def snapshot(self):

        energies=[]

        # 这里只是观察接口
        # 后面也会稀疏化

        for c in self.cells.values():

            energies.append(
                c.compress()["energy"]
            )


        return {

            "time":self.time,

            "active":
                len(energies),

            "energy_mean":
                float(np.mean(energies))

        }