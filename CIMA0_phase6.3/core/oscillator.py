import numpy as np


class Oscillator:
    """
    CIMA0 Phase6.3

    Pure local dynamics.

    State:
        x
        v

    No:
        reward
        energy control
        competition
        adaptation
    """

    def __init__(
        self,
        x,
        v,
        omega=1.0,
        mu=0.6,
        dt=0.02
    ):

        self.x=x
        self.v=v

        self.omega=omega
        self.mu=mu
        self.dt=dt


    def step(
        self,
        external=0.0
    ):

        accel = (

            self.mu
            *
            (1-self.x*self.x)
            *
            self.v

            -

            self.omega*self.omega*self.x

            +

            external
        )


        self.v += accel*self.dt

        self.x += self.v*self.dt



    def phase(self):

        return np.arctan2(
            self.v,
            self.x
        )