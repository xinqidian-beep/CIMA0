import numpy as np


class InternalDynamicsObserver:

    """
    Read-only observer.

    Does:

        snapshot
        self comparison
        sampling


    No:

        evolution
        control
        interpretation
        resource allocation
    """


    def __init__(
        self,
        sample_size=64
    ):

        self.sample_size = sample_size

        self.history = None



    def step_observe(
        self,
        snapshot
    ):


        if snapshot is None:

            return None



        state = self._flatten(
            snapshot
        )


        delta = self._delta(
            state
        )


        sample = self._sample(
            state,
            delta
        )


        return {

            "state":
                sample,

            "delta":
                delta

        }



    def _flatten(
        self,
        snapshot
    ):

        if isinstance(
            snapshot,
            np.ndarray
        ):

            return snapshot.flatten()



        values=[]


        for v in snapshot.values():

            if isinstance(
                v,
                np.ndarray
            ):

                values.extend(
                    v.flatten()
                )


        if not values:

            return np.zeros(
                1,
                dtype=np.float32
            )


        return np.asarray(
            values,
            dtype=np.float32
        )



    def _delta(
        self,
        state
    ):

        if self.history is None:

            self.history = state.copy()

            return np.zeros_like(
                state
            )


        delta = (
            state
            -
            self.history
        )


        self.history = state.copy()


        return delta



    def _sample(
        self,
        state,
        delta
    ):
        """
        Same principle as camera:

        all state exists

        changed area raises

        """

        n = len(state)


        if n <= self.sample_size:

            output=np.zeros(
                self.sample_size,
                dtype=np.float32
            )

            output[:n]=state

            return output



        #
        # raised score
        #

        score=np.abs(
            delta
        )


        index=np.argsort(
            score
        )[::-1]


        selected=index[
            :self.sample_size
        ]


        return state[
            selected
        ]