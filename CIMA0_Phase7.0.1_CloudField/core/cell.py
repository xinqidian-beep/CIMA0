import numpy as np


class Cell:


    def __init__(
        self,
        omega,
        dt,
        seed=None
    ):

        rng=np.random.default_rng(seed)


        self.x=rng.normal(
            0,
            0.5
        )

        self.v=rng.normal(
            0,
            0.5
        )


        self.omega=omega

        self.dt=dt



    def force(self):

        return (
            -self.omega**2
            *
            self.x
        )



    def step(
        self,
        external=0.0
    ):


        f=self.force()


        # 半隐式积分

        self.v += (
            f + external
        ) * self.dt


        self.x += (
            self.v
            *
            self.dt
        )



    def energy(self):

        return (
            0.5*
            (
                self.v**2
                +
                self.omega**2*self.x**2
            )
        )