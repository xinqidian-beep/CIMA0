import math


class Cell:


    def __init__(
        self,
        omega,
        x=0.0,
        v=0.0
    ):

        self.x=x
        self.v=v

        self.omega=omega



    def force(self):

        return -(self.omega**2)*self.x



    def energy(self):

        return (
            0.5*self.x*self.x+
            0.5*self.v*self.v
        )



    def step(
        self,
        dt,
        external=0.0
    ):


        f=self.force()


        f+=external


        self.v += f*dt


        self.x += self.v*dt