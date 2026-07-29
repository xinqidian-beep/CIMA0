import numpy as np


class Observer:

    """
    Sparse observation system.

    Does not control.
    Only samples and projects.

    """

    def __init__(
        self,
        observer_threshold=0.5
    ):

        self.observer_threshold = (
            observer_threshold
        )

        self.sample_ephemeral_value = 0.0



    def sample_ephemeral_state(
        self,
        kin_x
    ):

        """
        Local sampling only.

        """

        self.sample_ephemeral_value = abs(
            kin_x
        )



    def evaluate_ephemeral_raised(
        self
    ):

        """
        Raised signal.

        Relative simple projection.

        """

        return {

            "raised":

                self.sample_ephemeral_value
                >
                self.observer_threshold,


            "activity":

                self.sample_ephemeral_value

        }