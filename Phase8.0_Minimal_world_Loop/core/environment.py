import numpy as np


class Environment:


    def __init__(self,size):

        self.size=size


        #
        # 局部环境
        #
        # 每个位置独立
        #

        self.field=np.zeros(size)



    def interact(
        self,
        cid
    ):

        return self.field[cid]



    def deposit(
        self,
        cid,
        value
    ):


        self.field[cid]+=value



    def decay(self):

        #
        # 世界痕迹自然消退
        #

        self.field*=0.9999



    def measure(self):

        return np.std(
            self.field
        )