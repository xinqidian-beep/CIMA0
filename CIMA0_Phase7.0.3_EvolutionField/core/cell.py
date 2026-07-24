import numpy as np


class Cell:

    def __init__(self, x, v, omega):

        self.x = x
        self.v = v
        self.omega = omega


    def step(self, neighbors, dt):

        # 纯局部动力
        coupling = 0.0

        if neighbors:
            avg = sum(neighbors) / len(neighbors)
            coupling = 0.01 * (avg - self.x)


        force = (
            -self.omega*self.omega*self.x
            + coupling
        )


        self.v += force * dt
        self.x += self.v * dt