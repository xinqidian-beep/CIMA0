import numpy as np


class InternalDynamicsObserver:
    """
    Read only observer.

    Does NOT:

        modify state
        allocate resource
        control modules
    """


    def __init__(self):

        self.previous = {}



    def observe(
        self,
        snapshot
    ):

        requests = {}


        for name,state in snapshot.items():

            requests[name] = (
                self._measure(
                    name,
                    state
                )
            )


        return requests



    def _measure(
        self,
        name,
        state
    ):

        current = self._extract(
            state
        )


        if current is None:
            return 0.0



        previous = self.previous.get(
            name,
            current
        )


        delta = abs(
            current -
            previous
        )


        self.previous[name] = current


        return float(
            min(
                1.0,
                0.7 * current +
                0.3 * delta
            )
        )



    def _extract(
        self,
        obj
    ):

        values = []

        self._collect(
            obj,
            values
        )


        if values:

            return np.mean(
                np.abs(values)
            )


        return None



    def _collect(
        self,
        obj,
        out
    ):

        if isinstance(
            obj,
            dict
        ):

            for v in obj.values():

                self._collect(
                    v,
                    out
                )


        elif isinstance(
            obj,
            np.ndarray
        ):

            if obj.size:

                out.append(
                    float(
                        np.mean(
                            np.abs(obj)
                        )
                    )
                )


        elif isinstance(
            obj,
            (int,float)
        ):

            out.append(
                float(obj)
            )