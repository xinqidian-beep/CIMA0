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


        self.coupling=coupling


        self.neighbors={}


        for i in range(n):

            pool=list(range(n))

            pool.remove(i)


            self.neighbors[i]=random.sample(
                pool,
                degree
            )



    def event(
        self,
        perturb=None
    ):


        if perturb is None:

            perturb={}



        # 异步局部事件

        idx=random.randrange(
            len(self.cells)
        )


        cell=self.cells[idx]


        local_force=0.0



        for j in self.neighbors[idx]:

            neighbor=self.cells[j]


            local_force += (

                neighbor.x
                -
                cell.x

            )


        local_force *= self.coupling



        cell.step(

            local_force=local_force,

            perturb=perturb.get(
                idx,
                0.0
            )

        )


        self.time += 1



    def snapshot(self):


        energies=[

            c.energy()

            for c in self.cells

        ]


        xs=[

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
        
    def local_state(self, idx):

        """
        Observer局部读取接口
        """

        return self.cells[idx].observe()