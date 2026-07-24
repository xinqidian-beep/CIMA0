import numpy as np



class CoarseObserver:


    def __init__(self,n,size):

        self.n=n

        self.size=size



    def sample(self):


        return np.random.choice(

            self.n,

            self.size,

            replace=False

        )