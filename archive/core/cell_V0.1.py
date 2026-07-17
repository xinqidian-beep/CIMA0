import numpy as np


class Cell:
    """
    CIMA-0 最小物理单元

    不知道全局
    只有自己的状态
    """

    def __init__(self, cid):

        self.id = cid

        # 局部状态
        self.phase = np.random.random() * np.pi * 2
        self.energy = np.random.random()

        # 固有属性
        self.frequency = np.random.uniform(
            0.95,
            1.05
        )

        # 简单局部记忆
        self.memory = 0.0


    def observe(self):

        return {
            "phase": self.phase,
            "energy": self.energy
        }


    def update_memory(self, signal):

        self.memory = (
            self.memory * 0.99
            +
            signal * 0.01
        )