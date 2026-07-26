import numpy as np


class CloudMatrix:
    """
    Persistent external cloud field.

    Cloud has its own dynamics.

    No:
        control Cell
        store Cell state
        optimize

    Only:
        exist
        decay
        disappear
    """


    def __init__(
        self,
        size,
        decay=0.995,
        lifetime=5000
    ):

        self.size = size

        # NaN = no cloud
        self.field = np.full(
            size,
            np.nan
        )

        self.age = np.zeros(
            size,
            dtype=np.int32
        )

        self.decay = decay

        self.lifetime = lifetime



    def clear(self):

        self.field.fill(
            np.nan
        )

        self.age.fill(
            0
        )



    def deposit_random(
        self,
        count=4,
        strength=1.0
    ):

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

            self.age[cid] = 0



    def step(self):

        """
        Cloud internal evolution.

        Not Cell.
        """

        active = ~np.isnan(
            self.field
        )


        # decay
        self.field[active] *= self.decay


        # age
        self.age[active] += 1



        # disappear

        expired = (
            active
            &
            (
                self.age
                >
                self.lifetime
            )
        )


        self.field[expired] = np.nan

        self.age[expired] = 0



    def contact(self, cid):

        value = self.field[cid]


        if np.isnan(value):

            return None


        return float(value)