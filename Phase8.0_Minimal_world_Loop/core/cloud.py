import numpy as np


class Cloud:

    def __init__(self, size=4096):

        self.field = np.zeros(size)


    def collide(self):

        mask = np.random.random(
            len(self.field)
        ) < 0.001


        self.field[:] = 0


        values = np.random.uniform(
            -1,
            1,
            np.sum(mask)
        )


        self.field[mask] = values


        return np.where(mask)[0], values
