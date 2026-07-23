import numpy as np


class Cell:

    """
    Minimal physical individual

    Only knows:
        self state

    No:
        global
        rank
        reward
        memory
        observer
    """

    def __init__(
        self,
        x,
        v,
        omega
    ):

        self.x = x
        self.v = v

        self.omega = omega


        self.energy = 0.5 * (
            x*x + v*v
        )


    def step(
        self,
        local_force
    ):

        dt = 0.02


        accel = (
            -self.omega*self.omega*self.x
            +
            local_force
        )


        self.v += accel * dt

        self.x += self.v * dt


        self.energy = 0.5 * (
            self.x*self.x
            +
            self.v*self.v
        )