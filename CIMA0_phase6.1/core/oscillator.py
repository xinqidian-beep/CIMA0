import numpy as np


class Oscillator:

    """
    CIMA0 Phase6.1

    Independent organism.

    State:

        fast:
            x
            v

        slow:
            g

    No:
        reward
        target
        global state
        controller
    """


    def __init__(
        self,
        x,
        v,
        omega=1.0,
        mu=0.6,
        dt=0.02,
        g=0.0,
        tau_g=50.0,
        alpha_g=0.15
    ):

        self.x = x
        self.v = v

        self.omega = omega
        self.mu = mu
        self.dt = dt


        self.g = g
        self.tau_g = tau_g
        self.alpha_g = alpha_g


        self.activity = 0.0


    def step(
        self,
        field=0.0
    ):

        # self observation

        self.activity = abs(self.x)


        # slow internal state

        self.g += (
            (self.activity - self.g)
            /
            self.tau_g
        ) * self.dt


        # self modulation

        mu_eff = (
            self.mu *
            (
                1.0
                +
                self.alpha_g*np.tanh(self.g)
            )
        )


        # local dynamics

        accel = (

            mu_eff
            *
            (1-self.x*self.x)
            *
            self.v

            -

            self.omega*self.omega*self.x

            +

            field
        )


        self.v += accel*self.dt

        self.x += self.v*self.dt



    def energy(self):

        return 0.5*(self.x*self.x+self.v*self.v)