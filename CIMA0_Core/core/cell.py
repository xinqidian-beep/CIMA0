import numpy as np


class Cell:


    def __init__(self, cid):

        self.cid = cid

        self.x = np.random.uniform(
            -1.0,
            1.0
        )

        self.v = np.random.uniform(
            -0.5,
            0.5
        )


        self._omega = np.random.uniform(
            0.95,
            1.05
        )


        self.dt = 0.02



    @property
    def omega(self):

        return self._omega



    def step(
        self,
        perturb=0.0,
        coupling=0.0
    ):


        self.v += perturb


        self.v += coupling



        acceleration = (
            -self.omega**2 * self.x
            -
            0.1*self.x**3
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

            "id":self.cid,
            "x":float(self.x),
            "v":float(self.v),
            "omega":float(self.omega)

        }