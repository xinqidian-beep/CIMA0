import numpy as np


class Oscillator:

    def __init__(
        self,
        x,
        v,
        omega,
        mu=0.6,
        dt=0.02
    ):
        self.x = x
        self.v = v
        self.omega = omega
        self.mu = mu
        self.dt = dt

        self.energy = 0.5 * (
            x*x + v*v
        )


    def step(
        self,
        external_field=0.0
    ):

        # Van der Pol + local field
        accel = (
            self.mu *
            (1-self.x*self.x) *
            self.v
            -
            self.omega*self.omega*self.x
            +
            external_field
        )


        # semi implicit Euler
        self.v += accel*self.dt
        self.x += self.v*self.dt


        self.energy = 0.5 * (
            self.x*self.x +
            self.v*self.v
        )