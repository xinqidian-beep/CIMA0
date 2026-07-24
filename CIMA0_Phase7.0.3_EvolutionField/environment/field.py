import numpy as np


class EvolutionField:


    def __init__(self,n):

        self.field=np.zeros(n)



    def drift(self):

        # 自然衰减

        self.field*=0.99999



        noise=np.random.normal(
            0,
            1e-7,
            len(self.field)
        )


        self.field+=noise



    def perturb(
        self,
        ids
    ):

        return self.field[ids]