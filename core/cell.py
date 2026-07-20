import numpy as np


class Cell:

    def __init__(
        self,
        id,
        dim=512
    ):

        self.id = id
        self.input_indices = np.random.choice(
            512,
            size=8,
            replace=False
        )
        # 振荡状态
        self.x = np.random.uniform(
            -1.8,
            1.8
        )

        self.v = np.random.uniform(
            -0.8,
            0.8
        )


        # 自然频率微差
        self.omega = np.random.uniform(
            0.97,
            1.03
        )


        # Van der Pol 参数

        self.mu = 0.6


        # 积分步长

        self.dt = 0.02


        # 能量观察量

        self.energy = 1.0


        # 输入活动计数

        self.activity = 0



    def stimulate(
        self,
        vector,
        strength=1.0
    ):

        """
        外部 IO 扰动

        byte field
             |
             v
            Cell
        """

        

        local_value = np.mean(
            vector[self.input_indices]
        )

        

        # 微扰振幅

        self.v += (
            local_value
            *
            strength
            *
            0.02
        )


        self.energy += (
            abs(local_value)
            *
            strength
            *
            0.001
        )


        self.activity += 1



    def step(
        self,
        coupling_force=0.0
    ):

        """
        单个 Cell 自身动力
        """

        # Van der Pol

        accel = (

            self.mu
            *
            (
                1
                -
                self.x**2
            )
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

        self.v += (
            accel
            *
            self.dt
        )


        self.x += (
            self.v
            *
            self.dt
        )


        # 能量自然变化

        self.energy *= 0.999



    def phase(self):

        """
        当前相位
        """

        return np.arctan2(
            self.v,
            self.x
        )



    def state(self):

        """
        对外观察接口

        不参与动力
        """

        return np.array(
            [
                self.x,
                self.v
            ],
            dtype=np.float32
        )
    print(
        self.id,
        self.input_indices
    )   