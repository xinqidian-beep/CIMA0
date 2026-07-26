import numpy as np


class CloudMatrix:


    """
    External disturbance field.

    No:
        Cell reading
        history
        feedback

    Only:
        generate
        decay
        contact
    """


    def __init__(
        self,
        size
    ):

        self.size = size

        self.field = np.full(
            size,
            np.nan
        )



    def clear(self):

        self.field.fill(
            np.nan
        )



    def deposit_random(
        self,
        count=4,
        strength=1.0
    ):

        self.clear()


        ids = np.random.choice(
            self.size,
            count,
            replace=False
        )


        for cid in ids:

            self.field[cid] = np.random.uniform(
                -strength,
                strength
            )



    def contact(
        self,
        cid
    ):

        value = self.field[cid]


        if np.isnan(value):

            return None


        return float(value)