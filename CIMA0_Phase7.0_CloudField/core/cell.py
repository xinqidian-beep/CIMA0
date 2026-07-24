import math


class Cell:


    def __init__(
        self,
        omega,
        dt
    ):

        self.x = 0.0
        self.v = 0.0

        self.omega = omega
        self.dt = dt



    def step(
        self,
        coupling,
        disturbance=0.0
    ):


        force = (
            -self.omega*self.omega*self.x
            +
            coupling
            +
            disturbance
        )


        self.v += force*self.dt

        self.x += self.v*self.dt



    def energy(self):

        return 0.5*(
            self.v*self.v
            +
            self.omega*self.omega*self.x*self.x
        )