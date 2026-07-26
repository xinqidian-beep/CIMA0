import numpy as np


class CloudMatrix:
    """
    External cloud field.

    Phase9.0

    Cloud is NOT autonomous.

    It has:
        existence
        value
        decay

    It does NOT have:
        memory
        purpose
        self evolution
    """


    def __init__(self, size):

        self.size = size

        # NaN:
        # no cloud here

        self.field = np.full(
            size,
            np.nan,
            dtype=float
        )



    def clear(self):

        self.field.fill(
            np.nan
        )



    def deposit(
        self,
        cid,
        value
    ):

        """
        External collision.

        value can be:
            positive
            negative
            zero
        """

        self.field[cid] = value



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

            value = np.random.uniform(
                -strength,
                strength
            )

            self.deposit(
                cid,
                value
            )



    def contact(
        self,
        cid
    ):

        """
        Cell reads cloud.

        No feedback.

        Return:

            None
                no cloud

            float
                real signal
        """


        value = self.field[cid]


        if np.isnan(value):

            return None


        return float(value)



    def decay(
        self,
        rate=0.98,
        threshold=1e-3
    ):

        """
        Cloud event disappearance.

        Not death.

        Event loses strength.

        """

        mask = ~np.isnan(
            self.field
        )


        self.field[mask] *= rate



        dead = (
            mask
            &
            (
                np.abs(
                    self.field
                )
                <
                threshold
            )
        )


        self.field[dead] = np.nan



    def active_count(self):

        return int(
            np.sum(
                ~np.isnan(
                    self.field
                )
            )
        )