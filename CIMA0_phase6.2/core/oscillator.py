import numpy as np


class Oscillator:

    """
    CIMA0 Phase6.2

    Pure endogenous dynamics

    State:
        x
        v

    Parameter:
        omega

    No:
        reward
        memory
        adaptation
        energy control
        observer feedback
    """

    def __init__(
        self,
        x,
        v,
        omega=1.0,
        mu=0.6,
        dt=0.02
    ):

        self.x = x
        self.v = v

        self.omega = omega
        self.mu = mu

        self.dt = dt


        # observer only
        self.energy = 0.5*(x*x+v*v)



    def step(
        self,
        external_force=0.0
    ):

        # Van der Pol oscillator

        accel = (

            self.mu *
            (1-self.x*self.x)
            *
            self.v

            -

            self.omega*self.omega*self.x

            +

            external_force
        )


        self.v += accel*self.dt

        self.x += self.v*self.dt



        # only measurement

        self.energy = (
            0.5*
            (
                self.x*self.x
                +
                self.v*self.v
            )
        )



    def state(self):

        return {
            "x":float(self.x),
            "v":float(self.v),
            "omega":float(self.omega),
            "energy":float(self.energy)
        }