import numpy as np


class Oscillator:

    """
    CIMA0 Phase6.0

    Phase5:
        Van der Pol oscillator

    Phase6 addition:
        endogenous slow variable g


    State:

        fast:
            x
            v

        slow:
            g


    No:
        memory buffer
        reward
        learning
        optimizer
    """


    def __init__(
        self,
        x,
        v,
        omega=1.0,
        mu=0.6,
        dt=0.02,

        # Phase6 slow variable
        g=0.0,
        tau_g=50.0,
        alpha_g=0.15
    ):

        # fast state
        self.x = x
        self.v = v


        self.omega = omega

        # base metabolism
        self.mu = mu

        self.dt = dt



        # =====================
        # slow variable
        # =====================

        self.g = g

        self.tau_g = tau_g

        self.alpha_g = alpha_g



        # diagnostics

        self.activity = 0.0


        self.energy = 0.5 * (
            x*x + v*v
        )



    def step(
        self,
        external_field=0.0
    ):


        # =====================
        # 1. activity measurement
        # =====================

        self.activity = abs(self.x)



        # =====================
        # 2. slow adaptation
        # =====================

        dg = (
            self.activity
            -
            self.g
        ) / self.tau_g


        self.g += dg * self.dt



        # =====================
        # 3. intrinsic modulation
        # =====================

        mu_eff = (
            self.mu *
            (
                1.0
                +
                self.alpha_g *
                np.tanh(self.g)
            )
        )



        # =====================
        # 4. Van der Pol dynamics
        # =====================

        accel = (

            mu_eff *
            (1-self.x*self.x)
            *
            self.v

            -

            self.omega*self.omega
            *
            self.x

            +

            external_field
        )



        # =====================
        # 5. integrate
        # =====================

        self.v += accel*self.dt

        self.x += self.v*self.dt



        # =====================
        # 6. energy
        # =====================

        self.energy = 0.5 * (
            self.x*self.x
            +
            self.v*self.v
        )



    def state(self):

        return {

            "x":
                round(float(self.x),6),

            "v":
                round(float(self.v),6),

            "g":
                round(float(self.g),6),

            "activity":
                round(float(self.activity),6),

            "energy":
                round(float(self.energy),6)
        }