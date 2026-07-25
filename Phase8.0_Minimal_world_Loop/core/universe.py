import random

from core.cell import Cell
from core.environment import Environment



class Universe:


    def __init__(
        self,
        n=4096
    ):

        self.time = 0


        self.cells = [
            Cell(i)
            for i in range(n)
        ]


        self.environment = Environment()



    def step(self):

        self.time += 1


        # only a small part acts each event

        idx = random.randrange(
            len(self.cells)
        )


        cell = self.cells[idx]


        local_env = (
            self.environment.local_value()
        )


        x = cell.step(
            local_env
        )


        # cell leaves trace

        self.environment.receive(
            {
                "x":x
            }
        )


        self.environment.decay()



    def statistics(self):

        energy = [
            c.energy
            for c in self.cells
        ]

        xs = [
            c.x
            for c in self.cells
        ]


        return {

            "time":
                self.time,

            "energy_mean":
                sum(energy)
                /
                len(energy),


            "x_std":
                (
                    sum(
                        (
                            x
                            -
                            sum(xs)/len(xs)
                        )**2
                        for x in xs
                    )
                    /
                    len(xs)
                )
                **0.5,


            "environment":
                self.environment.field
        }