import numpy as np


class Cell:

    def __init__(
        self,
        x=0.0,
        v=0.0,
        omega=1.0,
        energy=1e-4
    ):

        self.x=x
        self.v=v

        self.omega=omega

        self.energy=energy


    def step(
        self,
        force=0.0,
        perturb=0.0,
        dt=0.01
    ):

        a = (
            -self.omega*self.omega*self.x
            +
            force
            +
            perturb
        )


        self.v += a*dt

        self.x += self.v*dt


        self.energy = (
            0.5*self.v*self.v
            +
            0.5*self.omega*self.omega*self.x*self.x
        )