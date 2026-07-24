import numpy as np



class CoarseObserver:


    def __init__(
        self,
        n,
        sample
    ):

        self.n=n
        self.sample_size=sample



    def scan(self):


        return np.random.choice(
            self.n,
            self.sample_size,
            replace=False
        )