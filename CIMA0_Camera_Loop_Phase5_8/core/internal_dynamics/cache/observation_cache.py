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

        The relation remains structured:

            TIME
            SPACE
            STATE

        Only STATE produces the change signal.
        """

        if current is None:

            return {

                "changed": False,

                "time": {
                    "previous": None,
                    "current": None,
                    "delta": None
                },

                "space": {
                    "previous": None,
                    "current": None,
                    "changed": False
                },

                "state": {
                    "delta": None,
                    "signal": 0.0,
                    "changed": False
                },

                "signal": 0.0

            }


        #
        # first observation
        #

        if self.previous is None:

            current_space = {
                "level": current.get(
                    "level"
                ),
                "region": self._copy(
                    current.get("region")
                ),
                "path": self._copy(
                    current.get("path")
                )
            }

            return {

                "changed": False,

                "time": {
                    "previous": None,
                    "current": current.get(
                        "age"
                    ),
                    "delta": None
                },

                "space": {
                    "previous": None,
                    "current": current_space,
                    "changed": False
                },

                "state": {
                    "delta": None,
                    "signal": 0.0,
                    "changed": False
                },

                "signal": 0.0

            }


        previous = self.previous


        try:

            #
            # TIME
            #

            previous_age = previous.get(
                "age"
            )

            current_age = current.get(
                "age"
            )

            time_delta = None

            if (
                self._is_numeric(
                    previous_age
                )
                and
                self._is_numeric(
                    current_age
                )
            ):

                time_delta = (
                    np.asarray(current_age)
                    -
                    np.asarray(previous_age)
                )


            #
            # SPACE
            #

            previous_space = {
                "level": previous.get(
                    "level"
                ),
                "region": self._copy(
                    previous.get("region")
                ),
                "path": self._copy(
                    previous.get("path")
                )
            }

            current_space = {
                "level": current.get(
                    "level"
                ),
                "region": self._copy(
                    current.get("region")
                ),
                "path": self._copy(
                    current.get("path")
                )
            }

            space_changed = (
                previous_space
                !=
                current_space
            )


            #
            # STATE
            #

            previous_state = previous.get(
                "exact"
            )

            current_state = current.get(
                "exact"
            )

            state_delta = self._difference(
                previous_state,
                current_state
            )

            state_signal = self._magnitude(
                state_delta
            )

            state_changed = (
                state_signal
                >
                self.threshold
            )


            return {

                "changed": state_changed,

                "time": {
                    "previous": previous_age,
                    "current": current_age,
                    "delta": time_delta
                },

                "space": {
                    "previous": previous_space,
                    "current": current_space,
                    "changed": space_changed
                },

                "state": {
                    "delta": state_delta,
                    "signal": state_signal,
                    "changed": state_changed
                },

                #
                # compatibility / derived signal
                #

                "signal": state_signal

            }


        except Exception:

            return {

                "changed": False,

                "time": {
                    "previous": None,
                    "current": None,
                    "delta": None
                },

                "space": {
                    "previous": None,
                    "current": None,
                    "changed": False
                },

                "state": {
                    "delta": None,
                    "signal": 0.0,
                    "changed": False
                },

                "signal": 0.0

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