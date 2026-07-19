import numpy as np


class Cell:

    def __init__(
        self,
        id,
        dim=1
    ):

        self.id = id

        # 状态
        self.x = np.random.uniform(
            -1.5,
            1.5,
            dim
        )

        # 速度
        self.v = np.random.uniform(
            -0.5,
            0.5,
            dim
        )


        # 自身频率
        self.omega = np.random.uniform(
            0.97,
            1.03
        )


        # Van der Pol强度
        self.mu = 0.6


        # 历史痕迹
        self.trace = np.zeros(dim)


        # 活动计数（仅观察）
        self.activity = 0



    def stimulate(
        self,
        vector,
        strength
    ):

        # 外界扰动
        self.v += (
            vector
            *
            strength
            *
            0.05
        )

        self.activity += 1



    def step(
        self,
        coupling_force=None,
        dt=0.02
    ):


        if coupling_force is None:

            coupling_force = 0



        # Van der Pol 动力

        accel = (

            self.mu
            *
            (1-self.x**2)
            *
            self.v

            -

            self.omega**2
            *
            self.x

            +

            coupling_force
        )


        # 积分

        self.v += accel*dt

        self.x += self.v*dt



        # 微弱物理涨落

        self.x += np.random.normal(
            0,
            0.0005,
            self.x.shape
        )


        # 历史

        self.trace *= 0.98

        self.trace += (
            self.x
            *
            0.02
        )



    def phase(self):

        return np.arctan2(
            self.v,
            self.x
        )