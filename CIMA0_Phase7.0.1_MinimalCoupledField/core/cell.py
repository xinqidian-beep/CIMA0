import numpy as np


class Cell:


    def __init__(self, omega):

        self.x = np.random.randn()*0.1

        self.v = 0.0

        self.omega = omega



    def energy(self):

        return 0.5*(

            self.x*self.x
            +
            self.v*self.v

        )


    def step(self, external):

        """
        外部只能作为微扰
        不改变动力参数
        """

        force = (

            -self.omega*self.omega*self.x

            +

            external

        )


        self.v += force * 0.01

        self.x += self.v * 0.01