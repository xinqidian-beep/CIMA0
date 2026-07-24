import numpy as np


class Observer:


    def __init__(
        self,
        sample=256
    ):

        self.sample=sample



    def read(
        self,
        universe
    ):


        ids=np.random.choice(
            universe.size,
            min(
                self.sample,
                universe.size
            ),
            replace=False
        )


        xs=[]
        es=[]


        for i in ids:

            c=universe.cells[i]

            xs.append(
                c.x
            )

            es.append(
                c.energy
            )


        return {

            "time":
                universe.time,

            "sample":
                len(ids),

            "x_std":
                float(
                    np.std(xs)
                ),

            "energy_mean":
                float(
                    np.mean(es)
                ),

            "energy_std":
                float(
                    np.std(es)
                )
        }