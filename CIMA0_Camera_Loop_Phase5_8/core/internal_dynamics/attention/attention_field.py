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

        if signal is None:
            return


        source = signal.get(
            "source",
            "unknown"
        )


        #
        # -------------------------------------------------
        # ObservationCache change envelope
        # -------------------------------------------------
        #

        change = signal.get(
            "change"
        )

        if change is not None:

            delta = change.get(
                "delta"
            )

            if delta is None:
                return

            intensity = self._extract_intensity(
                delta
            )
            
            print(
                "ATTENTION INPUT:",
                source,
                type(intensity),
                getattr(
                    intensity,
                    "shape",
                    None
                ),
                intensity
            )

            self._update_source(
                source,
                intensity
            )

            return


        #
        # -------------------------------------------------
        # old spatial mode
        # -------------------------------------------------
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
        # -------------------------------------------------
        # scalar mode
        # -------------------------------------------------
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

        if delta is None:

            return np.zeros(
                1,
                dtype=np.float32
            )


        #
        # structured data
        #

        if isinstance(delta, dict):

            values = []

            for key, value in delta.items():

                #
                # structural information
                #

                if key == "shape":

                    continue


                #
                # nested structure
                #

                if isinstance(
                    value,
                    dict
                ):

                    nested = self._extract_intensity(
                        value
                    )

                    if nested is not None:

                        values.append(
                            nested
                        )

                    continue


                #
                # numeric information
                #

                try:

                    arr = np.asarray(
                        value,
                        dtype=np.float32
                    )

                except Exception:

                    continue


                if arr.size == 0:

                    continue


                values.append(
                    np.abs(arr)
                )


            #
            # nothing usable
            #

            if not values:

                return np.zeros(
                    1,
                    dtype=np.float32
                )


            #
            # one usable spatial field
            #

            spatial = []

            for value in values:

                arr = np.asarray(
                    value,
                    dtype=np.float32
                )

                if arr.ndim >= 1:

                    spatial.append(
                        arr
                    )


            if spatial:

                reference = spatial[0]

                intensity = np.zeros_like(
                    reference,
                    dtype=np.float32
                )

                for value in spatial:

                    if value.shape == intensity.shape:

                        intensity += np.abs(
                            value
                        )

                return intensity


            #
            # scalar values
            #

            intensity = np.array(
                [
                    float(
                        np.max(
                            np.abs(
                                value
                            )
                        )
                    )
                    for value in values
                ],
                dtype=np.float32
            )

            return intensity


        #
        # ordinary numeric data
        #

        arr = np.asarray(
            delta,
            dtype=np.float32
        )


        if arr.ndim == 3:

            intensity = np.mean(
                np.abs(arr),
                axis=2
            )

        else:

            intensity = np.abs(
                arr
            )


        #
        # scalar → 1D field
        #

        if intensity.ndim == 0:

            intensity = intensity.reshape(
                1
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