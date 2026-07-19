import numpy as np


class Cloud:


    def __init__(
        self,
        cells=64
    ):

        self.cells=[
            Cell(i)
            for i in range(cells)
        ]


        self.edges=[]


        # 随机稀疏连接

        for i in range(cells):

            neighbors=np.random.choice(
                [
                    j for j in range(cells)
                    if j!=i
                ],
                4,
                replace=False
            )

            for j in neighbors:

                if i<j:

                    self.edges.append(
                        (i,j)
                    )


        self.coupling=0.05



    def step(self):


        forces=[
            0
            for _ in self.cells
        ]


        # 相位耦合

        for a,b in self.edges:


            phase_diff=(

                self.cells[a].phase()

                -

                self.cells[b].phase()

            )


            force=self.coupling*np.sin(
                phase_diff
            )


            forces[a]+=force

            forces[b]-=force



        # 更新

        for i,c in enumerate(self.cells):

            c.step(
                forces[i]
            )