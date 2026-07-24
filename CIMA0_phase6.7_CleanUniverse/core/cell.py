import numpy as np


class Cell:

    """
    Minimal autonomous oscillator.

    Only owns:

        x
        v
        omega

    No:
        global state
        memory
        reward
        energy control

    """


    def __init__(
        self,
        x,
        v,
        omega,
        dt
    ):

        self.x = x
        self.v = v

        self.omega = omega

        self.dt = dt



    def force(self):

        return (
            -self.omega *
            self.omega *
            self.x
        )



    def step(
        self,
        external_force=0.0
    ):

        f = (
            self.force()
            +
            external_force
        )


        # semi implicit Euler
        self.v += f*self.dt

        self.x += self.v*self.dt