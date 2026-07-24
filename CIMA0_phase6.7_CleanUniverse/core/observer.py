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
                
            "tail":
                self.tail_check(
                    energies
                )

        }
        
    def tail_check(self, energies):

        s=np.sort(
            energies
        )


        n=len(s)


        return {

            "median":
                float(
                    np.median(s)
                ),

            "top1":
                float(
                    np.mean(
                        s[-max(1,n//100):]
                    )
                ),

            "top5":
                float(
                    np.mean(
                        s[-max(1,n//20):]
                    )
                ),

            "max_ratio":
                float(
                    s[-1] /
                    np.mean(s)
                )
        }