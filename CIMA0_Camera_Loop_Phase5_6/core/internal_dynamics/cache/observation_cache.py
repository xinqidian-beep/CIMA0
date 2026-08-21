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

        if isinstance(a, dict) and isinstance(b, dict):

            return self._dict_difference(
                a,
                b
            )


        return np.asarray(b) - np.asarray(a)



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

                if len(sub)>0:

                    result[key]=sub


                continue



            #
            # numeric field
            #

            try:

                result[key] = (
                    np.asarray(b[key])
                    -
                    np.asarray(a[key])
                )

            except Exception:

                continue


        return result
        
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
        """
        Defensive copy.

        Prevent external mutation.
        """

        if isinstance(data, dict):

            output = {}


            for k, v in data.items():

                try:

                    output[k] = np.copy(v)

                except Exception:

                    output[k] = v


            return output



        try:

            return np.copy(data)


        except Exception:

            return data