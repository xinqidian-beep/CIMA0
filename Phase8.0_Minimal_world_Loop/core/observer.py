import numpy as np


class Observer:


    def observe(
        self,
        cells
    ):


        x=np.array(
            [
                c.x
                for c in cells
            ]
        )


        return {

            "mean":
            float(np.mean(x)),


            "std":
            float(np.std(x)),


            "active":
            int(
                np.sum(
                    np.abs(x)>0.01
                )
            )
        }