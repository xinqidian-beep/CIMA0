import numpy as np
import random

from core.cell import Cell


class Universe:


    def __init__(
        self,
        n=4096,
        degree=4,
        coupling=0.01,
        seed=42
    ):

        np.random.seed(seed)
        random.seed(seed)

        self.cells = []

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


        self.time = 0

        self.coupling = coupling


        # 固定局部拓扑

        self.neighbors = {}

        for i in range(n):

            pool = list(range(n))

            pool.remove(i)

            self.neighbors[i] = random.sample(
                pool,
                degree
            )



    def event(
        self,
        perturb=None
    ):

        """
        一个局部动力事件

        不扫描全局

        选择一个cell:
            读取邻居
            产生局部作用
            局部反作用


        """

        if perturb is None:

            perturb = {}



        # 随机局部事件中心

        idx = random.randrange(
            len(self.cells)
        )


        cell = self.cells[idx]


        neighbors = self.neighbors[idx]



        local_force = 0.0



        for j in neighbors:

            neighbor = self.cells[j]


            local_force += (

                neighbor.x
                -
                cell.x

            )


        local_force *= self.coupling



        # =====================
        # 中心cell更新
        # =====================

        cell.step(

            local_force=local_force,

            perturb=perturb.get(
                idx,
                0.0
            )

        )



        # =====================
        # 局部反作用
        #
        # 不扩散
        # 不全局
        # =====================


        if len(neighbors)>0:


            reaction = (

                -local_force
                /
                len(neighbors)

            )


            for j in neighbors:


                self.cells[j].step(

                    local_force=reaction,

                    perturb=0.0

                )



        self.time += 1




    def snapshot(self):


        energies = [

            c.energy()

            for c in self.cells

        ]


        xs = [

            c.x

            for c in self.cells

        ]


        return {


            "time":

            self.time,


            "energy_mean":

            float(
                np.mean(
                    energies
                )
            ),


            "energy_std":

            float(
                np.std(
                    energies
                )
            ),


            "x_std":

            float(
                np.std(
                    xs
                )
            )


        }



    def local_state(
        self,
        idx
    ):

        """
        Observer接口

        只允许读取单个局部状态
        """

        return self.cells[idx].observe()