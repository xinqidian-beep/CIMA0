import numpy as np


class InternalDynamicsObserver:
    """
    Internal dynamics observer.


    Responsibility:

        internal snapshot
              |
              v
        temporal comparison
              |
              v
        observation snapshot


    Does:

        read
        compare with history
        expose change


    Does not:

        evolve internal state
        control internal dynamics
        interpret meaning
        allocate computation
    """


    def __init__(self):

        self.previous = None



    def step_observe(
        self,
        snapshot
    ):
        """
        Observe internal state.

        Only compare state change.
        """


        if snapshot is None:

            return {

                "active": False,

                "delta": 0.0

            }



        current = self._extract_state(
            snapshot
        )



        if current is None:

            return {

                "active": False,

                "delta": 0.0

            }



        if self.previous is None:


            delta = np.zeros_like(
                current
            )


        else:


            delta = (

                current

                -

                self.previous

            )



        self.previous = (
            current.copy()
        )



        return {

            "active": True,

            "state": current,

            "delta": delta,

            "activity":

                float(
                    np.mean(
                        np.abs(delta)
                    )
                )

        }



    def _extract_state(
        self,
        snapshot
    ):
        """
        Extract observable field.

        No interpretation.

        Only find numerical state.
        """


        if isinstance(
            snapshot,
            np.ndarray
        ):

            return snapshot



        if isinstance(
            snapshot,
            dict
        ):


            #
            # prefer raw field
            #

            if "field" in snapshot:

                return np.asarray(
                    snapshot["field"],
                    dtype=np.float32
                )



            #
            # future internal modules
            #

            for value in snapshot.values():


                if isinstance(
                    value,
                    np.ndarray
                ):

                    return np.asarray(
                        value,
                        dtype=np.float32
                    )



        return None



    def snapshot(self):

        return {

            "module":
                "InternalDynamicsObserver",

            "state":
                "observing"

        }