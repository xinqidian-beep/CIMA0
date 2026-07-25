import numpy as np



class Observer:


    def observe(
        self,
        universe
    ):


        x=universe.state()


        return {

            "mean":
                float(
                    np.mean(x)
                ),

            "std":
                float(
                    np.std(x)
                ),

            "active":
                int(
                    np.sum(
                        np.abs(x)>1e-3
                    )
                )
        }