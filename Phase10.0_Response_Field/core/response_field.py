import numpy as np


class ResponseField:
    """
    Minimal response field.

    Role:

        impulse
            |
            v
        response memory

    No:
        optimization
        learning
        target
        control


    Field only stores
    and transforms incoming impulse.
    """


    def __init__(
        self,
        size,
        decay=0.995
    ):

        self.size = size

        self.decay = decay

        self.field = np.zeros(
            size,
            dtype=float
        )



    def deposit(
        self,
        cid,
        value
    ):

        """
        External impulse.

        One-way input.
        """

        self.field[cid] += value
        
    def absorb(
        self,
        cid,
        value
    ):
        self.field[cid] += value



    def contact(
        self,
        cid
    ):

        value = self.field[cid]


        if abs(value) < 1e-12:

            return None


        return float(value)



    def step(self):

        """
        Natural fading.

        No reset.
        No erase.
        """

        self.field *= self.decay



    def snapshot(self):

        active = np.sum(
            np.abs(self.field) > 1e-12
        )

        return {

            "active":
            int(active),

            "mean":
            float(
                np.mean(self.field)
            ),

            "std":
            float(
                np.std(self.field)
            ),

            "max":
            float(
                np.max(
                    np.abs(self.field)
                )
            )

        }