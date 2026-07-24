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


        self.n=n

        self.degree=degree

        self.coupling=coupling


        self.time=0



        #
        # 无向局部拓扑
        #

        self.neighbors={

            i:set()

            for i in range(n)

        }



        edges=set()



        while len(edges)<n*degree//2:


            a=random.randrange(n)

            b=random.randrange(n)


            if a==b:
                continue


            if (a,b) in edges or (b,a) in edges:
                continue


            edges.add((a,b))


        for a,b in edges:

            self.neighbors[a].add(b)

            self.neighbors[b].add(a)



    def event(
        self,
        perturb=None
    ):


        if perturb is None:

            perturb={}



        #
        # 一个局部事件
        #

        i=random.randrange(
            self.n
        )


        cell=self.cells[i]



        #
        # 保存局部作用
        #

        interactions=[]



        for j in self.neighbors[i]:


            other=self.cells[j]


            dx = other.x - cell.x


            force = (

                self.coupling *

                dx

            )


            interactions.append(

                (
                    j,
                    force
                )

            )



        #
        # 中心cell受到所有局部边作用
        #

        total_force=sum(

            f

            for _,f in interactions

        )


        cell.step(

            force=total_force,

            perturb=perturb.get(
                i,
                0.0
            )

        )



        #
        # 每条边独立反作用
        #

        for j,force in interactions:


            self.cells[j].step(

                force=-force,

                perturb=0.0

            )



        self.time+=1




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



    def local_state(
        self,
        idx
    ):

        return self.cells[idx].observe()