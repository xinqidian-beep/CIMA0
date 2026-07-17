from .cell import Cell


class Cloud:

    def __init__(self, size=1000):

        self.cells=[
            Cell(i)
            for i in range(size)
        ]


    def step(self,input_field):

        for c in self.cells:

            c.step(input_field)