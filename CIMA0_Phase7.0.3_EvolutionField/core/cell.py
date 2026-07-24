import numpy as np


class Cell:

    def __init__(
        self,
        omega,
        x,
        v
    ):

        self.x = x
        self.v = v
        self.omega = omega


    def step(
        self,
        coupling,
        dt
    ):

        # 唯一动力

        force = (
            -self.omega*self.omega*self.x
            +
            coupling
        )


        self.v += force*dt

        self.x += self.v*dt



    def energy(self):

        return (
            0.5*self.v*self.v
            +
            0.5*self.omega*self.omega*self.x*self.x
        )