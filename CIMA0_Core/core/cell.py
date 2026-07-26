import numpy as np


class Cell:

    def __init__(self, cid):

        self.cid = cid

        self.x = np.random.uniform(-1.0, 1.0)
        self.v = np.random.uniform(-0.5, 0.5)

        # locked intrinsic parameter
        self._omega = np.random.uniform(
            0.95,
            1.05
        )

        self.dt = 0.02


    @property
    def omega(self):

        return self._omega


    def local_perturb(self, value):

        self.external = value


    def step(
        self,
        coupling=0.0,
        perturb=0.0
    ):

        force = (

            # harmonic restoring
            -self.omega**2 * self.x

            # nonlinear restoring
            -0.1 * self.x**3

            # damping
            -0.05 * self.v

            # local interaction
            + coupling

            # cloud disturbance
            + perturb
        )


        self.v += force * self.dt

        self.x += self.v * self.dt



    def state(self):

        return {

            "id": self.cid,
            "x": float(self.x),
            "v": float(self.v),
            "omega": float(self.omega)

        }