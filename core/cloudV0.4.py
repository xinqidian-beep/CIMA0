import numpy as np

from .cell import Cell


class Cloud:


    def __init__(
        self,
        cells=64,
        dim=512
    ):

        self.dim=dim

        self.cells=[

            Cell(
                i,
                dim
            )

            for i in range(cells)

        ]


        self.edges=[]


        # 随机局部连接

        for i in range(cells):

            neighbors=np.random.choice(
                [
                    j for j in range(cells)
                    if j!=i
                ],
                size=6,
                replace=False
            )


            for j in neighbors:

                if i<j:

                    self.edges.append(
                        (i,j)
                    )


        self.coupling=0.05

        self.step_count=0



    def receive(
        self,
        stimulus
    ):

        vector=stimulus.vector

        strength=getattr(
            stimulus,
            "intensity",
            1.0
        )


        for c in self.cells:

            c.stimulate(
                vector,
                strength
            )



    def step(self):


        forces=[

            np.zeros(self.dim)

            for _ in self.cells

        ]


        # Kuramoto局部耦合

        for a,b in self.edges:


            diff=(

                self.cells[a].phase()

                -

                self.cells[b].phase()

            )


            f=(
                self.coupling
                *
                np.sin(diff)
            )


            forces[a]+=f

            forces[b]-=f



        for i,c in enumerate(self.cells):

            c.step(
                forces[i]
            )


        self.step_count+=1



    def snapshot(self):


        phases=[

            c.phase()

            for c in self.cells

        ]


        return {

            "step":
            self.step_count,


            "phase_std":
            round(
                float(np.std(phases)),
                5
            ),


            "avg_x":
            round(
                float(
                    np.mean(
                        [
                            np.mean(c.x)
                            for c in self.cells
                        ]
                    )
                ),
                5
            ),


            "activity":
            sum(
                c.activity
                for c in self.cells
            )

        }