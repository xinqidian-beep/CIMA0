import numpy as np


class Cell:

    def __init__(
        self,
        id,
        dim=512
    ):

        self.id=id
        self.dim=dim


        # 状态空间
        self.x=np.random.uniform(
            -1.5,
            1.5,
            dim
        )


        # 速度空间
        self.v=np.random.uniform(
            -0.5,
            0.5,
            dim
        )


        # 每个cell自己的频率
        self.omega=np.random.uniform(
            0.97,
            1.03
        )


        # 内生振荡强度
        self.mu=0.6


        # 历史轨迹
        self.trace=np.zeros(dim)


        # 外部扰动计数
        self.activity=0



    def stimulate(
        self,
        vector,
        strength=1.0
    ):

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
        force=None,
        dt=0.02
    ):

        if force is None:

            force=np.zeros(
                self.dim
            )


        accel=(

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

            force
        )


        self.v += accel*dt

        self.x += self.v*dt


        # 微弱涨落
        self.x += np.random.normal(
            0,
            0.0005,
            self.dim
        )


        # 轨迹残留
        self.trace*=0.98

        self.trace+=(
            self.x*0.02
        )



    def phase(self):

        # 512维相位平均

        return np.arctan2(
            np.mean(self.v),
            np.mean(self.x)
        )