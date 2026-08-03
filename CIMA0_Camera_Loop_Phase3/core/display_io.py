import numpy as np


class DisplayIO:
    """
    State -> frame

    Pure output.
    """


    def encode(
        self,
        snapshot
    ):

        frame = np.zeros(
            (
                240,
                320,
                3
            ),
            dtype=np.uint8
        )


        return frame