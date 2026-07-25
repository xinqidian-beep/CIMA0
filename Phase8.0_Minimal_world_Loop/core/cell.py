import numpy as np


class Cell:
    """
    Minimal autonomous individual.

    Cell only cares about itself.

    No:
        global state
        other cells
        reward
        target
        optimizer

    Dynamics:
        self-sustained nonlinear oscillator
    """

    def __init__(self, cid, seed=None):

        self.cid = cid

        rng = np.random.default_rng(seed)

        # position
        self.x = rng.uniform(-1.0, 1.0)

        # velocity
        self.v = rng.uniform(-1.0, 1.0)

        # personal parameters
        self.omega = rng.uniform(
            0.95,
            1.05
        )

        self.mu = 0.8

        self.dt = 0.02


        # memory only belongs to itself
        self.history = []



    def step(self, perturb=0.0):
        """
        One local evolution step.

        perturb:
            outside world influence

        It is not control.
        """

        accel = (
            self.mu *
            (1 - self.x*self.x)
            *
            self.v

            -
            self.omega*self.omega*self.x

            +
            perturb
        )


        self.v += accel * self.dt

        self.x += self.v * self.dt



        # local boundary only
        # prevent numerical explosion
        if abs(self.x) > 10:

            self.x = np.tanh(
                self.x
            )


        self.history.append(
            self.x
        )


        if len(self.history) > 100:

            self.history.pop(0)



    def state(self):

        return {

            "id":
                self.cid,

            "x":
                float(self.x),

            "v":
                float(self.v),

            "energy":
                float(
                    0.5 *
                    (
                        self.x*self.x
                        +
                        self.v*self.v
                    )
                )
        }