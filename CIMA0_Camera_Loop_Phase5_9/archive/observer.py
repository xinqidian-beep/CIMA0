import numpy as np


class Observer:
    """
    Local observation system.

    Responsibility:

        local measurement
        local projection
        local description

    Does not:

        control dynamics
        allocate computation
        decide importance
        store history
        modify state

    Output:

        only local observation description
    """


    def __init__(
        self,
        observation_scale=1.0
    ):

        self.observation_scale = observation_scale



    def describe(
        self,
        local_snapshot
    ):
        """
        Describe currently accessible local state.

        Input:

            local_snapshot

        Output:

            temporary local description

        No:

            request
            control
            memory
        """


        abs_state = np.abs(
            local_snapshot
        )


        local_activity = float(
            abs_state.mean()
        )


        local_variation = float(
            abs_state.std()
        )


        local_signal = (
            local_activity +
            local_variation
        ) * self.observation_scale



        return {

            "local_activity":
                local_activity,

            "local_variation":
                local_variation,

            "local_signal":
                float(local_signal)
        }