import numpy as np


class Cell:

    """
    Minimal autonomous unit.

    Only knows:

        own state
        local neighbors

    """

    def __init__(
        self,
        x,
        v,
        omega,
        dt=0.02
    ):

        self.x=x
        self.v=v

        self.omega=omega

        self.dt=dt



    def update(
        self,
        local_force
    ):

        # oscillator dynamics

        accel = (

            -self.omega*self.omega*self.x

            +

            local_force

        )


        self.v += accel*self.dt

        self.x += self.v*self.dt



    def energy(self):

        return 0.5*(
            self.x*self.x
            +
            self.v*self.v
        )