import numpy as np


class LocalField:

    def __init__(self, n):

        self.n = n

        self.field = np.zeros(n)


    def update(
        self,
        x,
        edges_from,
        edges_to
    ):

        total = np.zeros(self.n)
        count = np.zeros(self.n)


        np.add.at(
            total,
            edges_from,
            x[edges_to]
        )

        np.add.at(
            total,
            edges_to,
            x[edges_from]
        )


        np.add.at(
            count,
            edges_from,
            1
        )

        np.add.at(
            count,
            edges_to,
            1
        )


        mask = count > 0


        self.field[:] = 0


        self.field[mask] = (
            total[mask] /
            count[mask]
        )


        return self.field