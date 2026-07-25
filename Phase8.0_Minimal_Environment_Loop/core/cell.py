import numpy as np


class Cell:

    def __init__(self):

        self.x = np.random.normal(
            0,
            0.01
        )

        self.energy = (
            self.x *
            self.x
        )


    def step(
        self,
        influence=0.0
    ):

        noise = np.random.normal(
            0,
            0.001
        )

        self.x += (
            influence
            +
            noise
        )

        # natural decay
        self.x *= 0.9999


        self.energy = (
            self.x *
            self.x
        )