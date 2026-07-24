import numpy as np


class Observer:


    def read(
        self,
        universe
    ):


        x,v = universe.raw_state_sample(
            512
        )


        energy = (
            0.5*
            (
                x*x+
                v*v
            )
        )


        return {

            "time":
                universe.time,


            "cells":
                len(universe.cells),


            "x_std":
                float(
                    x.std()
                ),


            "energy_mean":
                float(
                    energy.mean()
                ),


            "energy_std":
                float(
                    energy.std()
                )

        }