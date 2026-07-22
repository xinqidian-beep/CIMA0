import numpy as np

from core.cell import Cell
from core.coupling import LocalCoupling
from core.topology import AdaptiveTopology



class Edge:


    def __init__(
        self,
        a,
        b,
        weight=0.5
    ):

        self.a = a
        self.b = b

        self.weight = weight

        self.age = 0



    def update(
        self,
        cells
    ):

        ca = cells[self.a]
        cb = cells[self.b]


        # 局部相关性
        correlation = (
            ca.x *
            cb.x
        )


        # Hebbian-like
        self.weight += (
            0.00001 *
            correlation
        )


        # 自然衰减
        self.weight *= 0.999995


        self.age += 1



        # 防止异常
        if self.weight < 0:

            self.weight = 0



    def alive(
        self
    ):

        return self.weight > 0.01





class CellNetwork:



    def __init__(
        self,
        n=128,
        degree=4,
        coupling_strength=0.01,
        seed=42
    ):


        np.random.seed(seed)


        self.n = n


        self.cells = []


        self.edges = []


        self.coupling = LocalCoupling(
            strength=coupling_strength
        )



        #
        # 创建 cell
        #
        for _ in range(n):

            self.cells.append(

                Cell(
                    x=np.random.uniform(
                        -1,
                        1
                    ),

                    v=np.random.uniform(
                        -0.5,
                        0.5
                    )
                )

            )



        self._create_graph(
            degree
        )



        self.topology = AdaptiveTopology(

            n=self.n,

            initial_edges=[
                (
                    e.a,
                    e.b
                )

                for e in self.edges
            ]

        )




    def _create_graph(
        self,
        degree
    ):


        for i in range(self.n):


            neighbors=np.random.choice(

                [
                    j
                    for j in range(self.n)
                    if j!=i
                ],

                size=degree,

                replace=False

            )


            for j in neighbors:


                if i < j:


                    self.edges.append(

                        Edge(
                            i,
                            j,
                            weight=0.5
                        )

                    )





    def step(
        self,
        step_count
    ):


        #
        # 1. 更新边关系
        #
        for e in self.edges:

            e.update(
                self.cells
            )



        #
        # 2. 删除弱关系
        #
        if step_count % 100 == 0:


            self.edges = [

                e

                for e in self.edges

                if e.alive()

            ]



        #
        # 3. 根据当前关系施加扰动
        #
        for e in self.edges:


            self.coupling.connect(

                self.cells[e.a],

                self.cells[e.b],

                strength=e.weight

            )



        #
        # 4. cell自身演化
        #
        for cell in self.cells:

            cell.step()



        #
        # 5. 慢拓扑观察
        #
        if step_count % 1000 == 0:


            self.topology.update(

                [
                    c.x
                    for c in self.cells
                ]

            )





    def snapshot(
        self
    ):


        xs=np.array(

            [
                c.x
                for c in self.cells
            ]

        )


        gs=np.array(

            [
                c.g
                for c in self.cells
            ]

        )


        weights=np.array(

            [
                e.weight
                for e in self.edges
            ]

        )



        return {


            "cells":
                self.n,


            "edges":
                len(self.edges),



            "x_std":
                float(
                    xs.std()
                ),



            "g_mean":
                float(
                    gs.mean()
                ),



            "g_std":
                float(
                    gs.std()
                ),



            "energy_mean":
                float(
                    np.mean(
                        [
                            c.energy
                            for c in self.cells
                        ]
                    )
                ),



            "weight_mean":
                float(
                    weights.mean()
                )
                if len(weights)>0
                else 0.0,



            "weight_std":
                float(
                    weights.std()
                )
                if len(weights)>0
                else 0.0,



            "active":

                int(
                    np.sum(
                        np.abs(xs)>0.1
                    )
                ),



            "degree_mean":

                float(
                    2*
                    len(self.edges)
                    /
                    self.n
                )

        }