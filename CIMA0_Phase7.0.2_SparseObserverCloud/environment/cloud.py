import numpy as np



class CloudField:


    def __init__(self,n):

        self.field=np.zeros(n)


        self.memory=np.zeros(n)



    def deposit(
        self,
        idx,
        value
    ):


        self.memory[idx]+=value*0.001



    def evolve(self):


        self.memory*=0.99999



    def get(self,i):


        return self.memory[i]