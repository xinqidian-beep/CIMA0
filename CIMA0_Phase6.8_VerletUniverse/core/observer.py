import numpy as np



class Observer:



    def read(
        self,
        universe
    ):


        xs=[]

        energies=[]



        for c in universe.cells:


            xs.append(
                c.x
            )


            energies.append(

                0.5*
                (
                    c.x*c.x
                    +
                    c.v*c.v
                )

            )


        xs=np.array(xs)

        energies=np.array(
            energies
        )


        return {


            "time":

                universe.time,


            "cells":

                len(
                    universe.cells
                ),


            "x_std":

                float(
                    xs.std()
                ),


            "energy_mean":

                float(
                    energies.mean()
                ),


            "energy_std":

                float(
                    energies.std()
                ),


            "tail":

                self.tail(
                    energies
                )
        }




    def tail(
        self,
        energies
    ):


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

                    s[
                    -max(
                        1,
                        n//100
                    ):
                    ]

                )

            ),



            "top5":

            float(

                np.mean(

                    s[
                    -max(
                        1,
                        n//20
                    ):
                    ]

                )

            ),



            "max_ratio":

            float(

                s[-1] /
                np.mean(s)

            )
        }