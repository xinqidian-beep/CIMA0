import numpy as np


class InternalDynamicsObserver:


    def describe(
        self,
        snapshot
    ):

        if snapshot is None:

            return None


        state = {}


        planet = snapshot.get(
            "planet"
        )


        if planet is not None:

            state["planet"] = {

                "shape":
                    planet.shape,

                "mean":
                    float(
                        np.mean(
                            planet
                        )
                    ),

                "energy":
                    float(
                        np.mean(
                            np.abs(
                                planet
                            )
                        )
                    )

            }


        return state