import numpy as np
import random

from core.cell import Cell



class Universe:


    def __init__(
        self,
        n=4096,
        degree=4,
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


        # 固定局部拓扑

        self.neighbors={}


        for i in range(n):

            choices=list(
                range(n)
            )

            choices.remove(i)


            self.neighbors[i]=random.sample(
                choices,
                degree
            )



    def event(
        self,
        perturb=None
    ):


        if perturb is None:

            perturb={}



        # 随机选择一个局部事件

        i=random.randrange(
            len(self.cells)
        )


        cell=self.cells[i]


        local_force=0.0


        for j in self.neighbors[i]:


            neighbor=self.cells[j]


            local_force += (

                neighbor.x
                -
                cell.x

            )


        local_force *= 0.05



        cell.step(

            local_force=local_force,

            perturb=perturb.get(
                i,
                0.0
            )

        )


        self.time+=1



    def snapshot(self):


        energy=[]


        for c in self.cells:

            energy.append(
                c.observe()["energy"]
            )


        return {

            "time":self.time,

            "energy_mean":
            float(np.mean(energy)),

            "energy_std":
            float(np.std(energy)),

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



    def local_state(self,i):

        return self.cells[i].observe()