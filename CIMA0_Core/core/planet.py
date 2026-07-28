import numpy as np


class PlanetEngine:
    """
    Minimal autonomous dynamic engine.

    Only owns:

        x
        v
        omega
    """


    def __init__(
        self,
        x=1.0,
        v=0.0,
        omega=1.0,
        dt=0.01
    ):

        self.x = float(x)

        self.v = float(v)

        self.omega = float(omega)

        self.dt = float(dt)



    def force(self):

        return (
            -self.omega
            *
            self.omega
            *
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


        self.v += (
            f
            *
            self.dt
        )


        self.x += (
            self.v
            *
            self.dt
        )



    def sample(self):

        return (
            self.x,
            self.v,
            self.omega
        )