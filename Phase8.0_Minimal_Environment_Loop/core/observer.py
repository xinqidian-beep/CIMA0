import numpy as np


class Observer:


    def observe(self,world):


        values=[

            c.x

            for c in world.cells

        ]


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
                        np.abs(values)>1e-8
                    )
                )

        }