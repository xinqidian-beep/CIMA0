import numpy as np



class ComputeField:


    def __init__(
        self,
        sample_size=64
    ):

        self.sample_size=sample_size



    def compute(
        self,
        universe
    ):


        ids=np.random.choice(
            len(universe.cells),
            self.sample_size,
            replace=False
        )


        samples=np.array(
            [
                universe.cells[i].x
                for i in ids
            ]
        )


        return {

            "sample":
                self.sample_size,

            "mean":
                float(
                    np.mean(samples)
                ),

            "std":
                float(
                    np.std(samples)
                ),

            "energy":
                float(
                    np.mean(
                        samples*samples
                    )
                )
        }