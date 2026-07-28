import numpy as np


class Cloud:
    """
    Cloud field.

    Independent dynamic medium.

    Internal state:

        empty
        vacant
        zero
        negative


    Does not know:

        planet
        cell
        observer
        compute
        IO meaning


    Only:

        receive disturbance
        evolve local field
        output compressed state
    """



    def __init__(
        self,
        height,
        width
    ):

        self.height = height
        self.width = width


        # cloud matrix
        #
        # values:
        #   negative
        #   zero
        #   empty(vacant representation)
        #

        self.matrix = np.zeros(
            (
                height,
                width
            ),
            dtype=float
        )



    def receive(
        self,
        disturbance
    ):

        """
        External disturbance.

        Not replacement.

        Only changes local cloud state.
        """


        self.matrix += disturbance



    def evolve(
        self
    ):

        """
        Local cloud evolution.

        Same rule everywhere.

        No special region.
        """


        new_matrix = self.matrix.copy()


        h, w = self.matrix.shape


        for y in range(h):

            for x in range(w):


                local = self.matrix[
                    y,
                    x
                ]


                neighbors = []


                if y > 0:
                    neighbors.append(
                        self.matrix[y-1,x]
                    )

                if y < h-1:
                    neighbors.append(
                        self.matrix[y+1,x]
                    )

                if x > 0:
                    neighbors.append(
                        self.matrix[y,x-1]
                    )

                if x < w-1:
                    neighbors.append(
                        self.matrix[y,x+1]
                    )


                if neighbors:

                    influence = np.mean(
                        neighbors
                    )

                    new_matrix[y,x] = (
                        local
                        +
                        0.01
                        *
                        np.tanh(
                            influence
                        )
                    )


        self.matrix = new_matrix



    def expression(
        self
    ):

        """
        Cloud three-value expression.

        Not predefined meaning.

        Just compression.
        """


        empty_ratio = np.mean(
            self.matrix == 0
        )


        negative_ratio = np.mean(
            self.matrix < 0
        )


        activity = np.std(
            self.matrix
        )


        return np.array(
            [
                empty_ratio,
                negative_ratio,
                activity
            ]
        )