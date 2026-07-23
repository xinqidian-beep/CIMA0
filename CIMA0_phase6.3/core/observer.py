import numpy as np


class Observer:


    def snapshot(
        self,
        net
    ):


        x=np.array(
            [
                c.x
                for c in net.cells
            ]
        )


        g=np.array(
            [
                c.g
                for c in net.cells
            ]
        )


        return {

            "time":
                net.time,

            "cells":
                net.n,

            "x_std":
                float(x.std()),

            "g_mean":
                float(g.mean()),

            "g_std":
                float(g.std())

        }