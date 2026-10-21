
import copy
import numpy as np


class InternalDynamicsObserver:

    """
    Read-only internal observer.

    Responsibilities:
        1. describe current internal state
        2. compare current observation with previous observation
        3. return structured observation/change

    Does NOT:
        - select
        - allocate compute
        - modify Planet
        - modify AttentionField
        - interpret semantic meaning
        - discard original observation structure
    """

    def __init__(self):

        pass

    #
    # ---------------------------------------------------------
    # observe
    # ---------------------------------------------------------
    #

    def observe(
        self,
        snapshot
    ):

        if snapshot is None:

            return None

        #
        # Keep the complete current observation.
        #
        current = self._copy(
            snapshot
        )

        #
        # Describe current state.
        #
        description = self.describe(
            current
        )

        return {
            "observation": current,
            "description": description,
            
        }

    #
    # ---------------------------------------------------------
    # describe
    # ---------------------------------------------------------
    #

    def describe(
        self,
        snapshot
    ):

        if snapshot is None:

            return None

        state = {}

        #
        # Planet
        #
        planet = snapshot.get(
            "planet"
        )

        if planet is not None:

            #
            # ndarray planet state
            #
            if isinstance(
                planet,
                np.ndarray
            ):

                state["planet"] = {
                    "shape": planet.shape,
                    "mean": float(
                        np.mean(
                            planet
                        )
                    ),
                    "energy": float(
                        np.mean(
                            np.abs(
                                planet
                            )
                        )
                    )
                }

            #
            # Structured planet observation
            #
            elif isinstance(
                planet,
                dict
            ):

                state["planet"] = (
                    self._describe_dict(
                        planet
                    )
                )

            else:

                state["planet"] = {
                    "type": type(
                        planet
                    ).__name__
                }

        return state


    #
    # ---------------------------------------------------------
    # description helpers
    # ---------------------------------------------------------
    #

    def _describe_dict(
        self,
        value
    ):

        result = {}

        for key, item in value.items():

            #
            # nested dictionary
            #

            if isinstance(
                item,
                dict
            ):

                result[key] = self._describe_dict(
                    item
                )

                continue


            #
            # numpy array
            #

            if isinstance(
                item,
                np.ndarray
            ):

                if np.issubdtype(
                    item.dtype,
                    np.number
                ):

                    result[key] = {
                        "shape": item.shape,
                        "mean": float(
                            np.mean(item)
                        ),
                        "energy": float(
                            np.mean(
                                np.abs(item)
                            )
                        )
                    }

                else:

                    result[key] = {
                        "shape": item.shape,
                        "dtype": str(
                            item.dtype
                        )
                    }

                continue


            #
            # numeric scalar
            #

            if isinstance(
                item,
                (int, float, np.integer, np.floating)
            ):

                result[key] = float(item)

                continue


            #
            # list
            #
            # Do not interpret its internal meaning.
            # Preserve structure and only describe its container.
            #

            if isinstance(
                item,
                list
            ):

                result[key] = {
                    "type": "list",
                    "length": len(item)
                }

                continue


            #
            # tuple
            #
            # Important:
            # region is a tuple such as
            # (64, 0, 128, 64)
            #
            # It is structural information,
            # not a field to calculate mean().
            #

            if isinstance(
                item,
                tuple
            ):

                result[key] = {
                    "type": "tuple",
                    "length": len(item)
                }

                continue


            #
            # everything else
            #

            result[key] = {
                "type": type(item).__name__
            }

        return result

    #
    # ---------------------------------------------------------
    # copy helpers
    # ---------------------------------------------------------
    #

    def _copy(
        self,
        value
    ):

        if isinstance(
            value,
            dict
        ):

            return {
                key: self._copy(
                    item
                )
                for key, item in value.items()
            }

        if isinstance(
            value,
            list
        ):

            return [
                self._copy(
                    item
                )
                for item in value
            ]

        if isinstance(
            value,
            tuple
        ):

            return tuple(
                self._copy(
                    item
                )
                for item in value
            )
            
        if isinstance(value, np.ndarray):

            return np.copy(value)    

        
        return value
            
        

    def _scalar_or_copy(
        self,
        value
    ):

        try:

            array = np.asarray(
                value
            )

            if array.ndim == 0:

                return float(
                    array
                )

        except Exception:

            pass

        return self._copy(
            value
        )