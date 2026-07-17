import numpy as np

from .cell import Cell
from .attractor import AttractorGraph



class Cloud:


    def __init__(
        self,
        cells=64,
        dim=512
    ):

        self.dim=dim

        self.cells=[

            Cell(i, dim=dim)

            for i in range(cells)

        ]


        self.attractor=AttractorGraph(dim=dim)



        self.step_count=0

        self.last_kind="none"




    def receive(
        self,
        stimulus
    ):


        self.last_kind=stimulus.kind


        vector=stimulus.vector



        # 找局部响应

        for cell in self.cells:

            s=cell.similarity(
                vector
            )

            if s>0.1:

                cell.stimulate(
                    vector,
                    stimulus.intensity
                )



        self.attractor.update(
            vector
        )



    def step(self):


        for c in self.cells:

            c.step()


        self.step_count+=1



    def snapshot(self):


        active=sum(

            1

            for c in self.cells

            if c.activity>0

        )


        return {

            "step":
            self.step_count,


            "input":
            self.last_kind,


            "attractor":
            self.attractor.last_index,


            "stability":
            round(
                self.attractor.last_score,
                4
            ),


            "active_cells":
            active

        }