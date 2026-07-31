import numpy as np


class CameraObserver:
    """
    External camera observer.

    Responsibility:

        temporal self comparison
        ephemeral variation evaluation
        temporary compute request generation


    No:

        image understanding
        sampling allocation
        compute allocation
        priority judgment
        control
        prediction
        long-term memory
    """


    def __init__(self):

        #
        # previous instantaneous state
        #
        # overwritten every frame
        #

        self.previous_ephemeral_state = None



    def step_observe(
        self,
        current_state
    ):
        """
        Compare current external state
        with previous instantaneous state.

        Output:

            delta_ephemeral


        First frame:

            no comparison available

        """

        if (
            self.previous_ephemeral_state
            is None
        ):

            self.previous_ephemeral_state = (
                current_state.copy()
            )

            return None



        delta_ephemeral = (
            current_state -
            self.previous_ephemeral_state
        )


        #
        # overwrite previous state
        #

        self.previous_ephemeral_state = (
            current_state.copy()
        )


        return delta_ephemeral



    def evaluate_request_ephemeral(
        self,
        delta_ephemeral
    ):
        """
        Generate temporary computation request.

        This is only a raise signal.

        It does not decide:

            where to compute
            what is important
            how much is granted

        """

        if delta_ephemeral is None:

            return 0



        variation_ephemeral = np.abs(
            delta_ephemeral
        )



        #
        # collapse local variation
        # into temporary demand
        #

        activity_ephemeral = float(
            variation_ephemeral.mean()
        )


        spread_ephemeral = float(
            variation_ephemeral.std()
        )



        pixel_count = (
            delta_ephemeral.shape[0]
            *
            delta_ephemeral.shape[1]
        )


        request_ephemeral = (

            activity_ephemeral
            +
            spread_ephemeral

        ) * pixel_count



        return int(
            request_ephemeral
        )



    def snapshot(
        self
    ):
        """
        Read-only observation snapshot.
        """

        if (
            self.previous_ephemeral_state
            is None
        ):

            return None


        return {

            "observer_shape":

                self.previous_ephemeral_state.shape

        }