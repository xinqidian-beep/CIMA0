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
        seed
    ):

        np.random.seed(seed)

        self.n = n
        self.dt = dt
        self.time = 0


        self.cells = []


        for _ in range(n):

            self.cells.append(
                Cell(
                    omega=np.random.uniform(
                        omega_min,
                        omega_max
                    ),

                    # 恢复动力尺度
                    x=np.random.uniform(
                        -1.0,
                        1.0
                    ),

                    v=np.random.uniform(
                        -1.0,
                        1.0
                    )
                )
            )


        self.neighbors=[]


        for i in range(n):

            ids=np.random.choice(
                n,
                avg_neighbors,
                replace=False
            )

            self.neighbors.append(ids)



    def step(self):

        """
        单次完整动力更新

        注意：
        所有cell读取旧状态
        所有cell同时写入新状态

        避免：
        更新顺序成为隐藏扰动
        """


        new_x=np.zeros(
            self.n
        )

        new_v=np.zeros(
            self.n
        )


        for i,cell in enumerate(self.cells):


            coupling=0.0


            for j in self.neighbors[i]:

                coupling += (
                    self.cells[j].x
                    -
                    cell.x
                )


            coupling /= len(
                self.neighbors[i]
            )


            force=(

                -cell.omega *
                cell.omega *
                cell.x

                +

                0.01 *
                coupling
            )


            new_v[i]=(
                cell.v
                +
                force*self.dt
            )


            new_x[i]=(
                cell.x
                +
                new_v[i]*self.dt
            )



        for i,cell in enumerate(self.cells):

            cell.x=new_x[i]
            cell.v=new_v[i]


        self.time+=1



    def run(
        self,
        steps
    ):

        for _ in range(steps):

            self.step()



    def snapshot(self):

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
                self.n,

            "energy_mean":
                float(
                    energies.mean()
                ),

            "energy_std":
                float(
                    energies.std()
                ),

            "x_std":
                float(
                    np.std(
                        [
                            c.x
                            for c in self.cells
                        ]
                    )
                )
        }