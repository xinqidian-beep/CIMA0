import numpy as np


class Cell:

    def __init__(self, cid):

        self.cid = cid

        # 自己的状态
        self.x = np.random.uniform(
            -0.01,
            0.01
        )

        self.v = np.random.uniform(
            -0.01,
            0.01
        )


        # 自己的能量
        self.energy = 0.001


        # 自己时间
        self.age = 0



    def step(
        self,
        local_env
    ):

        self.age += 1


        #
        # 行星式动力
        #
        # 不追求收敛
        # 不追求目标
        #

        force = (
            -0.1*self.x
            +
            0.05*np.sin(self.age*0.001)
        )


        # 环境只产生微扰

        force += (
            local_env
            *
            0.001
        )


        noise = np.random.normal(
            0,
            0.0001
        )


        self.v += force + noise

        self.x += self.v



        #
        # 能量只是自身状态
        #

        self.energy = (
            abs(self.x)
            *
            0.1
            +
            0.001
        )


        #
        # 给环境留下痕迹
        #

        residue = (
            self.x
            *
            0.0001
        )


        return residue



    def state(self):

        return {
            "id":self.cid,
            "x":self.x,
            "energy":self.energy
        }