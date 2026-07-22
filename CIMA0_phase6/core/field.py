import numpy as np


class LocalField:


    def __init__(
        self,
        n
    ):

        self.n=n

        self.field=np.zeros(n)


        self.noise=np.random.normal(
            0,
            0.01,
            n
        )



    def update(
        self,
        x,
        edges_from,
        edges_to
    ):


        field=np.zeros(
            self.n
        )


        diff=(
            x[edges_from]
            -
            x[edges_to]
        )


        influence=np.sin(
            diff
        )


        np.add.at(
            field,
            edges_from,
            influence
        )


        np.add.at(
            field,
            edges_to,
            -influence
        )


        self.field=field / (
            len(edges_from)+1
        )


        return self.field