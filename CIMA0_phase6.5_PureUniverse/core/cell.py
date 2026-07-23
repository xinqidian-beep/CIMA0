import numpy as np


class Cell:

    def __init__(
        self,
        pos,
        vel
    ):

        self.pos = np.array(
            pos,
            dtype=np.float64
        )

        self.vel = np.array(
            vel,
            dtype=np.float64
        )


        self.mass = 1.0


    def step(
        self,
        force,
        dt
    ):

        self.vel += force * dt

        self.pos += self.vel * dt



    def energy(self):

        return (
            0.5 *
            np.dot(
                self.vel,
                self.vel
            )
        )