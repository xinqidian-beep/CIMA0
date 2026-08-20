import numpy as np


class AttentionField:
    """
    CIMA0 Phase5_4

    Dynamic attention field.

    Input:

        observation signal
                |
                v
        attention update


    Responsibility:

        - maintain attention strength
        - accumulate repeated changes
        - decay inactive regions
        - provide attention state


    Does NOT:

        - observe
        - compare snapshots
        - understand meaning
        - control dynamics


    """

    def __init__(
        self,
        shape=None,
        decay=0.95,
        growth=0.2,
        threshold=0.0
    ):

        self.decay_rate = decay

        self.growth_rate = growth

        self.threshold = threshold


        if shape is not None:

            self.field = np.zeros(
                shape,
                dtype=np.float32
            )

        else:

            self.field = None



    def receive(
        self,
        signal
    ):
        """
        Receive observation result.

        Expected:

        {
            "changed": bool,
            "delta": ndarray,
            "signal": float
        }

        """

        if signal is None:

            return


        delta = signal.get(
            "delta"
        )


        if delta is None:

            self.decay()

            return



        intensity = self._extract_intensity(
            delta
        )


        self._ensure_shape(
            intensity.shape
        )


        self._update(
            intensity
        )



    def step(
        self
    ):
        """
        Attention evolution step.
        """

        self.decay()



    def snapshot(
        self
    ):
        """
        Read-only output.
        """

        if self.field is None:

            return None


        return np.copy(
            self.field
        )



    def clear(
        self
    ):

        if self.field is not None:

            self.field.fill(
                0.0
            )



    #
    # internal
    #

    def _update(
        self,
        intensity
    ):

        self.field *= self.decay_rate


        active = (
            intensity
            >
            self.threshold
        )


        self.field[active] += (
            intensity[active]
            *
            self.growth_rate
        )


        self.field = np.clip(
            self.field,
            0.0,
            1.0
        )



    def decay(
        self
    ):

        if self.field is None:

            return


        self.field *= (
            self.decay_rate
        )



    def _extract_intensity(
        self,
        delta
    ):
        """
        Convert change into attention strength.

        Keep spatial structure.
        """

        arr = np.asarray(
            delta
        )


        if arr.ndim == 3:

            # BGR/RGB

            intensity = np.mean(
                np.abs(arr),
                axis=2
            )

        else:

            intensity = np.abs(
                arr
            )


        return intensity.astype(
            np.float32
        )



    def _ensure_shape(
        self,
        shape
    ):

        if self.field is None:

            self.field = np.zeros(
                shape,
                dtype=np.float32
            )


        elif self.field.shape != shape:

            self.field = np.zeros(
                shape,
                dtype=np.float32
            )