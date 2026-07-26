import numpy as np


class Cell:
    """
    Minimal autonomous dynamical cell.

    Cell does not know:
        universe
        neighbors
        observer
        purpose

    Cell only:
        maintains its own trajectory
    """

    def __init__(self, cid):

        self.cid = cid

        # state
        self.x = np.random.uniform(
            -1.0,
            1.0
        )

        self.v = np.random.uniform(
            -0.5,
            0.5
        )

        # intrinsic property
        self.omega = np.random.uniform(
            0.95,
            1.05
        )


        self.dt = 0.02


    def local_perturb(self, value):

        """
        External contact.

        Not control.
        Just collision.

        Cell decides nothing about source.
        """

        self.v += value


    def step(self):

        """
        Pure local evolution.

        Nonlinear oscillator.

        No:
            reset
            clamp
            optimize
        """


        # nonlinear planetary-like force

        acceleration = (
            -self.omega**2 * self.x
            -
            0.1 * self.x**3
        )


        self.v += (
            acceleration
            *
            self.dt
        )


        self.x += (
            self.v
            *
            self.dt
        )


    def state(self):

        return {

            "id": self.cid,

            "x": float(self.x),

            "v": float(self.v),

            "omega": float(self.omega)

        }