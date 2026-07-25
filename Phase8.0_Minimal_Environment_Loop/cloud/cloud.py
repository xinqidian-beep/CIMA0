import numpy as np



class Cloud:


    def __init__(
        self,
        n_cells,
        strength=0.05
    ):

        self.n_cells=n_cells

        self.strength=strength



    def contact(self):

        result={}


        count=np.random.randint(
            1,
            6
        )


        ids=np.random.choice(
            self.n_cells,
            count,
            replace=False
        )


        for i in ids:

            value=np.random.normal(
                0,
                self.strength
            )

            result[int(i)] = value


        return result