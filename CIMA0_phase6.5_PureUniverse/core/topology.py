import numpy as np


class LocalTopology:


    def __init__(
        self,
        cells,
        radius=2.0
    ):

        self.cells=cells

        self.radius=radius


        self.links=[
            []
            for _ in cells
        ]


    def build_local(
        self
    ):

        n=len(self.cells)


        for i in range(n):

            self.links[i]=[]


        # 初始化阶段允许一次

        for i in range(n):

            for j in range(i+1,n):

                d=np.linalg.norm(
                    self.cells[i].pos-
                    self.cells[j].pos
                )

                if d < self.radius:

                    self.links[i].append(j)
                    self.links[j].append(i)



    def neighbors(
        self,
        i
    ):

        return [
            self.cells[j]
            for j in self.links[i]
        ]