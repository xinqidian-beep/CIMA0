import numpy as np


class Cell:

    def __init__(
        self,
        x,
        v,
        omega=1.0
    ):

        self.x=x
        self.v=v
        self.omega=omega


    def internal_force(self):

        # 自身动力
        return (
            -self.omega
            *
            self.omega
            *
            self.x
        )


    def step(
        self,
        interaction,
        dt
    ):

        force = (
            self.internal_force()
            +
            interaction
        )


        self.v += force * dt

        self.x += self.v * dt