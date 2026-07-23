import numpy as np


class LocalField:

    """
    Only local interaction field.

    No global state.
    """

    def __init__(self,n):

        self.field=np.zeros(n)


    def update(
        self,
        x,
        edges_from,
        edges_to
    ):

        self.field.fill(0)


        diff = (
            x[edges_to]
            -
            x[edges_from]
        )


        np.add.at(
            self.field,
            edges_from,
            diff
        )


        np.add.at(
            self.field,
            edges_to,
            -diff
        )


        return self.field