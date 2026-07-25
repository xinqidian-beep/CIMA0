import numpy as np


class Observer:


    """
    Passive observer.

    Cannot affect world.
    """


    def observe(self,universe):


        sample=np.array(
            [
                c.state
                for c in universe.cells[:64]
            ]
        )


        return {

            "mean":
                float(
                    np.mean(sample)
                ),

            "std":
                float(
                    np.std(sample)
                ),

            "active":
                int(
                    np.sum(
                        np.linalg.norm(
                            sample,
                            axis=1
                        )>1
                    )
                )
        }