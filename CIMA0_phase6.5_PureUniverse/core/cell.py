import numpy as np


class Cell:
    """
    Pure physical cell

    Only:
        x
        v
        omega

    No:
        reward
        memory
        ranking
        selection
    """

    def __init__(
        self,
        x,
        v,
        omega=1.0,
        dt=0.02
    ):

        self.x = x
        self.v = v
        self.omega = omega
        self.dt = dt


        self.energy = (
            0.5 *
            (
                x*x +
                v*v
            )
        )


    def step(
        self,
        local_force=0.0
    ):

        # simple oscillator dynamics

        accel = (
            -self.omega*self.omega*self.x
            +
            local_force
        )


        self.v += accel*self.dt

        self.x += self.v*self.dt


        self.energy = (
            0.5 *
            (
                self.x*self.x +
                self.v*self.v
            )
        )


    def observe(self):

        return {
            "x": float(self.x),
            "v": float(self.v),
            "energy": float(self.energy)
        }