import math
import random


class Cell:


    def __init__(self, cid):

        self.id = cid


        self.x = random.uniform(
            -1,
            1
        )

        self.v = random.uniform(
            -0.1,
            0.1
        )


        self.energy = 1.0


        self.activity = abs(
            self.x
        )



    def update(self, field):


        dt = 0.02


        # 最小振荡动力

        a = (
            -0.15*self.v
            -0.8*self.x
            + field
        )


        self.v += a*dt

        self.x += self.v*dt



        # 能量只是局部物理量

        self.energy += (
            0.001
            -
            0.001*self.activity
        )


        if self.energy < 0:
            self.energy = 0



        self.activity = abs(
            self.x
        )