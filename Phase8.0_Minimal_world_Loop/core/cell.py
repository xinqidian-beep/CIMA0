import numpy as np


class Cell:
    """
    最小生命单元

    只知道:
        自己
        附近环境

    不知道:
        世界
        其他cell整体
    """

    def __init__(self, cid):

        self.cid = cid

        # 自己的状态
        self.x = np.random.randn() * 0.01
        self.v = np.random.randn() * 0.01

        # 内部能量
        self.energy = 1.0


    def contact(self, environment):

        """
        局部环境接触

        没有全局信息
        """

        local = environment.read(
            self.cid
        )

        return local * 0.001


    def step(self, environment):

        # 局部扰动
        force = self.contact(environment)


        # 最小动力系统
        self.v += force

        self.x += self.v


        # 自然耗散
        self.energy *= 0.999999


        # 自己留下痕迹
        environment.deposit(
            self.cid,
            self.x
        )


    def state(self):

        return {
            "id": self.cid,
            "x": float(self.x),
            "energy": float(self.energy)
        }