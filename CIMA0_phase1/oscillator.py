import numpy as np


class Oscillator:
    """
    最小自治动力单元

    不知道:
        network
        cluster
        observer

    只负责:
        自己的状态演化
    """

    def __init__(
        self,
        omega=1.0,
        mu=0.6,
        x=None,
        v=None,
        energy=1.0
    ):
        self.x = (
            np.random.uniform(-1.8, 1.8)
            if x is None else x
        )

        self.v = (
            np.random.uniform(-0.8, 0.8)
            if v is None else v
        )

        self.omega = omega
        self.mu = mu

        self.energy = energy


    def step(self, force, dt):

        # Van der Pol 动力项
        accel = (
            self.mu * (1 - self.x**2) * self.v
            - self.omega**2 * self.x
            + force
        )

        # Semi-implicit Euler
        self.v += accel * dt
        self.x += self.v * dt


        # 仅记录能量
        # 不参与控制
        self.energy = (
            0.5 * self.v**2
            +
            0.5 * self.omega**2 * self.x**2
        )


    def phase(self):

        return np.arctan2(
            self.v,
            self.x
        )