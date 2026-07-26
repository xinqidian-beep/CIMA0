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

    def diffuse(
        self,
        strength=0.1
    ):

        new_field = self.field.copy()


        for i in range(1, self.size - 1):

            if np.isnan(self.field[i]):
                continue


            left = self.field[i-1]
            right = self.field[i+1]


            influence = 0.0
            count = 0


            if not np.isnan(left):
                influence += left
                count += 1


            if not np.isnan(right):
                influence += right
                count += 1


            if count > 0:

                avg = influence / count

                new_field[i] += (
                    avg - self.field[i]
                ) * strength


        self.field = new_field

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