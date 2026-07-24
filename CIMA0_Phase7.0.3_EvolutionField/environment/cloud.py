import numpy as np


class CloudField:


    def __init__(self,n):

        self.n=n

        self.field=np.zeros(n)



    def receive(
        self,
        idx,
        value
    ):

        self.field[idx]+=value



    def evolve(self):

        self.field*=0.999



    def sample(self,idx):

        return self.field[idx]
