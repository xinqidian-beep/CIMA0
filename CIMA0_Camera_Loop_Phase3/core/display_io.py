import numpy as np


class DisplayIO:
    """
    Display IO interface.

    Responsibility:

        InternalDynamics snapshot
                |
                v
        display data


    No:

        internal interpretation
        state analysis
        control
    """


    def __init__(
        self,
        width=640,
        height=480
    ):

        self.width = width
        self.height = height



    def encode(
        self,
        snapshot
    ):
        """
        Convert internal snapshot
        into display frame.

        Only format conversion.
        """

        if snapshot is None:

            return np.zeros(
                (
                    self.height,
                    self.width,
                    3
                ),
                dtype=np.uint8
            )


        #
        # snapshot only provides state
        #

        value = snapshot.get(
            "value",
            0.0
        )


        value = float(value)

        value = max(
            0.0,
            min(
                1.0,
                abs(value)
            )
        )


        level = int(
            value * 255
        )


        frame = np.full(
            (
                self.height,
                self.width,
                3
            ),
            level,
            dtype=np.uint8
        )


        return frame