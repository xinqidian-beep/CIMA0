import numpy as np


class Observer:


    def read(self,u):


        e=np.array(
            [
            c.energy()
            for c in u.cells
            ]
        )


        return {

        "time":u.time,

        "cells":len(e),

        "energy_mean":
            float(e.mean()),

        "energy_std":
            float(e.std()),

        "max_ratio":
            float(
                e.max()/e.mean()
            )

        }