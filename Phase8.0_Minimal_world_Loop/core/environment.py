import numpy as np


class Environment:

    """
    环境不是控制器

    只是历史残留
    """

    def __init__(self, size):

        self.field = np.zeros(size)



    def read(self, cid):

        return self.field[cid]



    def deposit(self, cid, value):

        """
        个体改变局部环境

        不广播
        不同步
        """

        self.field[cid] *= 0.99

        self.field[cid] += value * 0.0001



    def decay(self):

        self.field *= 0.99999