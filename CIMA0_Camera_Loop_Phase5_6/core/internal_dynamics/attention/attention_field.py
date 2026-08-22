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


        self.fields = {}


        if shape is not None:

            self.fields["default"] = np.zeros(
                shape,
                dtype=np.float32
            )



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


        source = signal.get(
            "source",
            "unknown"
        )
        
        #
        # old spatial mode
        #

        delta = signal.get(
            "delta"
        )
        
        if delta is not None:

            intensity = self._extract_intensity(
                delta
            )


            self._update_source(
                source,
                intensity
            )

            return

        #
        # new envelope mode
        #

        activity = signal.get(
            "signal",
            0.0
        )


        if activity <= 0:

            return


        self._update_scalar(
            source,
            activity
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

        result = {}

        for name, field in self.fields.items():

            result[name] = np.copy(
                field
            )

        return result



    def clear(
        self
    ):

        for field in self.fields.values():

            field.fill(
                0.0
            )



    #
    # internal
    #

    def _update_source(
        self,
        source,
        intensity
    ):

        self._ensure_shape(
            source,
            intensity.shape
        )


        field = self.fields[source]


        field *= self.decay_rate


        active = (
            intensity
            >
            self.threshold
        )
        
        field[active] += (
            intensity[active]
            *
            self.growth_rate
        )
        
        self.fields[source] = np.clip(
            field,
            0.0,
            1.0
        )
        
    def _update_scalar(
        self,
        source,
        value
    ):

        if source not in self.fields:

            self.fields[source] = np.zeros(
                1,
                dtype=np.float32
            )


        field = self.fields[source]


        field *= self.decay_rate


        field[0] += (
            value *
            self.growth_rate
        )


        self.fields[source] = np.clip(
            field,
            0.0,
            1.0
        )    

    def decay(
        self
    ):

        for source in self.fields:

            self.fields[source] *= (
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
        source,
        shape
    ):

        if source not in self.fields:

            self.fields[source] = np.zeros(
                shape,
                dtype=np.float32
            )


        elif self.fields[source].shape != shape:
            
            #
            # source changed shape
            # recreate only this source
            #

            self.fields[source] = np.zeros(
                shape,
                dtype=np.float32
            )