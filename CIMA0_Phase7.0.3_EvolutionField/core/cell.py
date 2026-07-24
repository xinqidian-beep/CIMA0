import math


class Cell:

    def __init__(
        self,
        x,
        v,
        omega
    ):

        self.x = x
        self.v = v
        self.omega = omega

        self.time = 0

        self.activity = 0.0


    def step(self, dt=0.01):

        # 内生动力
        force = -self.omega * self.omega * self.x


        self.v += force * dt

        self.x += self.v * dt


        self.time += 1


        self.activity = (
            abs(self.x)
            +
            abs(self.v)
        )


    def observe(self):

        energy = (
            0.5*self.v*self.v
            +
            0.5*self.omega*self.omega*self.x*self.x
        )

        return {
            "x":self.x,
            "v":self.v,
            "energy":energy,
            "activity":self.activity,
            "time":self.time
        }