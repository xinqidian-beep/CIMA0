import random
import numpy as np

from .cell import Cell
from .topology import AdaptiveTopology


class AsyncEvolutionNetwork:

    def __init__(
        self,
        cells=1024,
        avg_degree=4,
        seed=42
    ):

        random.seed(seed)
        np.random.seed(seed)

        self.time = 0

        self.cells = [
            Cell(i)
            for i in range(cells)
        ]

        self.topology = AdaptiveTopology(
            cells,
            avg_degree
        )


    def local_field(self, idx):

        """
        只读取邻居
        """

        neighbors = self.topology.neighbors(idx)

        field = 0.0

        for j in neighbors:

            w = self.topology.weight(
                idx,
                j
            )

            field += (
                self.cells[j].x -
                self.cells[idx].x
            ) * w


        return field



    def update_cell(self, idx):

        cell = self.cells[idx]

        field = self.local_field(idx)


        cell.update(
            field
        )



    def step(self, events=1):

        """
        异步事件推进

        一次只更新少量个体
        """

        for _ in range(events):

            idx = random.randrange(
                len(self.cells)
            )

            self.update_cell(
                idx
            )

            self.time += 1



    def snapshot(self):

        x = np.array(
            [
                c.x
                for c in self.cells
            ]
        )

        activity = np.array(
            [
                c.activity
                for c in self.cells
            ]
        )


        return {

            "time":
                self.time,

            "cells":
                len(self.cells),

            "edges":
                self.topology.edge_count(),

            "x_std":
                float(np.std(x)),

            "activity_mean":
                float(np.mean(activity)),

            "activity_std":
                float(np.std(activity)),

            "active_ratio":
                float(
                    np.mean(
                        activity > 0.01
                    )
                )
        }