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

        self.local_time = 0
        self.activity = 0.0


    def evolve(self, dt=0.01):

        # 纯动力
        a = -self.omega*self.omega*self.x


        self.v += a * dt
        self.x += self.v * dt


        self.local_time += 1


        self.activity = abs(self.v)+abs(self.x)



    def compress(self):

        return {
            "x":self.x,
            "v":self.v,
            "energy":
                0.5*self.v*self.v
                +
                0.5*self.omega*self.omega*self.x*self.x,
            "time":self.local_time
        }