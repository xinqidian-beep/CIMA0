import random
import numpy as np



class Observer:


    def __init__(
        self,
        sample=64
    ):

        self.sample = sample



    def observe(
        self,
        universe
    ):


        cells = random.sample(
            universe.cells,
            self.sample
        )


        values = np.array(
            [
                c.x
                for c in cells
            ]
        )


        return {

            "mean":
                float(
                    np.mean(values)
                ),

            "std":
                float(
                    np.std(values)
                ),

            "active":
                int(
                    np.sum(
                        np.abs(values)
                        >
                        np.std(values)
                    )
                )
        }