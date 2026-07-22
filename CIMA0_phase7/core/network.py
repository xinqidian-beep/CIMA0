import numpy as np

from core.cell import Cell
from core.coupling import LocalCoupling
from core.topology import AdaptiveTopology



# 每个节点允许的总连接强度
EDGE_BUDGET = 6.0



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


        # 局部相关
        correlation = (
            ca.x *
            cb.x
        )


        # 局部增强
        self.weight += (
            0.00001 *
            correlation
        )


        # 自然衰减
        self.weight *= 0.999995


        if self.weight < 0:
            self.weight = 0


        self.age += 1



    def alive(self):

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
        # 创建局部主体
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



        #
        # 初始稀疏关系
        #
        self._create_graph(
            degree
        )



        #
        # 拓扑观察层
        #
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

                    if j != i

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






    def _limit_connection_budget(self):


        totals=[

            0.0

            for _ in range(self.n)

        ]



        for e in self.edges:

            totals[e.a]+=e.weight

            totals[e.b]+=e.weight



        #
        # 局部资源竞争
        #
        for i in range(self.n):


            excess = (
                totals[i]
                -
                EDGE_BUDGET
            )


            if excess <= 0:

                continue



            related=[

                e

                for e in self.edges

                if e.a == i
                or e.b == i

            ]



            #
            # 弱边优先减少
            #
            related.sort(

                key=lambda x:x.weight

            )



            for e in related:


                if excess <= 0:

                    break



                reduce=min(

                    e.weight,

                    excess

                )


                e.weight-=reduce


                excess-=reduce







    def step(
        self,
        step_count
    ):


        #
        # 1.
        # 关系自身演化
        #
        for e in self.edges:

            e.update(
                self.cells
            )



        #
        # 2.
        # 资源限制
        #
        if step_count % 100 == 0:

            self._limit_connection_budget()



        #
        # 3.
        # 删除死亡关系
        #
        if step_count % 100 == 0:


            self.edges=[

                e

                for e in self.edges

                if e.alive()

            ]



        #
        # 4.
        # 局部耦合
        #
        for e in self.edges:


            self.coupling.connect(

                self.cells[e.a],

                self.cells[e.b],

                strength=e.weight

            )



        #
        # 5.
        # cell自身动力学
        #
        for c in self.cells:

            c.step()



        #
        # 6.
        # 慢观察
        #
        if step_count % 1000 == 0:


            self.topology.update(

                [

                    c.x

                    for c in self.cells

                ]

            )







    def snapshot(self):


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


        energies=np.array(

            [

                c.energy

                for c in self.cells

            ]

        )


        weights=np.array(

            [

                e.weight

                for e in self.edges

            ]

        )


        degree=np.zeros(

            self.n

        )


        for e in self.edges:

            degree[e.a]+=1

            degree[e.b]+=1



        return {


            "cells":

                self.n,


            "edges":

                len(self.edges),



            "x_std":

                float(xs.std()),



            "g_mean":

                float(gs.mean()),



            "g_std":

                float(gs.std()),



            "energy_mean":

                float(
                    energies.mean()
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
                    degree.mean()
                ),



            "degree_std":

                float(
                    degree.std()
                )

        }