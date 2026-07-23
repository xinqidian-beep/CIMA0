import random
import numpy as np

from core.cell import Cell
from core.topology import AdaptiveTopology


class NaturalAsyncNetwork:


    def __init__(
        self,
        n=128
    ):

        self.n = n


        self.cells = [
            Cell(
                x=np.random.uniform(-1,1),
                v=np.random.uniform(-0.5,0.5)
            )
            for _ in range(n)
        ]


        self.topology = AdaptiveTopology(
            n
        )


        self.time = 0



    def local_field(
        self,
        i
    ):

        """
        只允许局部信息
        """

        field = 0.0


        neighbors = self.topology.neighbors(i)


        for j in neighbors:

            dx = (
                self.cells[j].x
                -
                self.cells[i].x
            )


            w = self.topology.weight(
                i,
                j
            )


            field += (
                w * dx
            )


        return field



    def update_cell(
        self,
        i
    ):

        cell = self.cells[i]


        field = self.local_field(i)


        # 局部扰动直接进入振子
        cell.oscillator.step(
            field
        )


        # 慢变量自己演化
        cell.update_slow()



    def step(
        self,
        events=1
    ):

        """
        异步事件

        没有全局同步
        """

        for _ in range(events):

            i = random.randrange(
                self.n
            )


            self.update_cell(i)


            self.time += 1



    def snapshot(self):


        xs=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        energy=np.array(
            [
                c.energy
                for c in self.cells
            ]
        )


        activity=np.abs(xs)


        return {

            "time":
                self.time,


            "cells":
                self.n,


            "edges":
                self.topology.edge_count(),


            "x_std":
                float(xs.std()),


            "activity_mean":
                float(activity.mean()),


            "activity_std":
                float(activity.std()),


            "energy_mean":
                float(energy.mean())

        }