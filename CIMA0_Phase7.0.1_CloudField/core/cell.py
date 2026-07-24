import random


class Cell:

    def __init__(
        self,
        omega=1.0
    ):

        self.x=random.uniform(-0.1,0.1)
        self.v=random.uniform(-0.1,0.1)

        self.omega=omega


    def force(self):

        return -self.omega*self.omega*self.x


    def step(
        self,
        coupling=0.0,
        disturbance=0.0,
        dt=0.01
    ):

        f=self.force()

        f+=coupling
        f+=disturbance


        self.v+=f*dt
        self.x+=self.v*dt



    def energy(self):

        return 0.5*(self.x*self.x+self.v*self.v)