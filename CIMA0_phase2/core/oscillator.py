import numpy as np


class Oscillator:
    """
    单动力系统

    不知道：
        集合
        簇
        全局

    只负责自己的状态演化
    """

    def __init__(self, seed=None):

        rng = np.random.default_rng(seed)

        self.x = rng.uniform(-1, 1)
        self.v = rng.uniform(-0.5, 0.5)

        self.omega = rng.uniform(
            0.95,
            1.05
        )

        self.mu = 0.6

        self.energy = (
            self.x*self.x +
            self.v*self.v
        )


    def step(self, force=0.0, dt=0.02):

        accel = (
            self.mu *
            (1-self.x*self.x) *
            self.v
            -
            self.omega*self.omega*self.x
            +
            force
        )


        # semi implicit Euler

        self.v += accel * dt

        self.x += self.v * dt


        self.energy = (
            self.x*self.x +
            self.v*self.v
        )