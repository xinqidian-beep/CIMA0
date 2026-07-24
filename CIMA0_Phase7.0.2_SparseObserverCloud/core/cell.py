import numpy as np


class Cell:


    def __init__(self, omega):

        self.x=np.random.randn()*0.1

        self.v=0.0

        self.omega=omega



    def energy(self):

        return 0.5*(

            self.x*self.x
            +
            self.v*self.v

        )



    def step(self, perturb):


        force=(

            -self.omega*self.omega*self.x

            +

            perturb

        )


        self.v += force*0.01

        self.x += self.v*0.01