import numpy as np


class ObservationCache:
    """
    CIMA0 Phase5_4

    Short-lived observation cache.

    Responsibility:

        snapshot(t)
              |
              v
        cache
              |
              v
        snapshot(t+1)
              |
              v
        compare
              |
              v
        change signal


    Does NOT:

        - store history
        - learn
        - select attention
        - modify dynamics
        - become memory


    Lifetime:

        one previous observation only

    """

    def __init__(
        self,
        threshold=0.0
    ):

        self.previous = None

        self.threshold = threshold



    def update(
        self,
        snapshot
    ):
        """
        Store current snapshot.

        Returns:

            previous snapshot

        The caller decides how to compare.
        """

        old = self.previous


        if snapshot is None:

            self.previous = None

            return None


        self.previous = self._copy(snapshot)


        return old



    def compare(
        self,
        current
    ):
        """
        Compare current observation
        with cached previous observation.

        Returns:

        {
            "changed": bool,
            "delta": value,
            "signal": value
        }

        """

        if self.previous is None:

            return {

                "changed": False,

                "delta": None,

                "signal": 0.0

            }



        previous = self.previous



        try:

            delta = self._difference(
                previous,
                current
            )


        except Exception:

            return {

                "changed": False,

                "delta": None,

                "signal": 0.0

            }



        signal = self._magnitude(
            delta
        )



        return {

            "changed":
                signal > self.threshold,

            "delta":
                delta,

            "signal":
                signal

        }



    def step(
        self,
        snapshot
    ):
        """
        One-shot observation cycle.

        1.
        compare with previous

        2.
        replace cache

        3.
        output signal

        """

        result = self.compare(
            snapshot
        )


        self.update(
            snapshot
        )


        return result



    def clear(
        self
    ):
        """
        Destroy current cache.
        """

        self.previous = None



    #
    # internal
    #

    def _difference(
        self,
        a,
        b
    ):

        if (
            isinstance(a, dict)
            and
            isinstance(b, dict)
        ):

            return self._dict_difference(
                a,
                b
            )

        return (
            np.asarray(b)
            -
            np.asarray(a)
        )

    def _dict_difference(
        self,
        a,
        b
    ):

        result = {}

        keys = (
            set(a.keys())
            &
            set(b.keys())
        )

        for key in keys:

            old = a[key]
            new = b[key]

            #
            # recursive structure
            #

            if (
                isinstance(old, dict)
                and
                isinstance(new, dict)
            ):

                sub = self._dict_difference(
                    old,
                    new
                )

                if len(sub) > 0:
                    result[key] = sub

                continue

            #
            # numeric value
            #

            if not self._is_numeric(old):
                continue

            if not self._is_numeric(new):
                continue

            try:

                delta = (
                    np.asarray(new)
                    -
                    np.asarray(old)
                )

                result[key] = delta

            except Exception:

                continue

        return result

    def _is_numeric(
        self,
        value
    ):

        if isinstance(
            value,
            (bool, str, bytes)
        ):
            return False

        if isinstance(
            value,
            (int, float, complex)
        ):
            return True

        if isinstance(
            value,
            np.ndarray
        ):
            return np.issubdtype(
                value.dtype,
                np.number
            )

        if isinstance(
            value,
            np.number
        ):
            return True

        return False

        
    def _magnitude(
        self,
        value
    ):

        if isinstance(
            value,
            dict
        ):

            values=[]

            for v in value.values():

                values.append(
                    self._magnitude(v)
                )

            if len(values)==0:

                return 0.0

            return max(values)


        try:

            return float(
                np.mean(
                    np.abs(value)
                )
            )

        except Exception:

            return 0.0    
        
    def _copy(
        self,
        data
    ):

        if isinstance(
            data,
            dict
        ):

            return {
                k: self._copy(v)
                for k, v in data.items()
            }


        if isinstance(
            data,
            list
        ):

            return [
                self._copy(v)
                for v in data
            ]


        if isinstance(
            data,
            tuple
        ):

            return tuple(
                self._copy(v)
                for v in data
            )


        if isinstance(
            data,
            np.ndarray
        ):

            return np.copy(
                data
            )


        return data