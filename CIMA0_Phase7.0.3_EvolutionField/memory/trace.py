import numpy as np



class TraceMemory:


    def __init__(
        self,
        n
    ):

        self.trace=np.zeros(n)



    def add(
        self,
        idx,
        value
    ):

        self.trace[idx]+=value



    def decay(self):

        self.trace*=0.9999



    def probability(
        self,
        ids
    ):

        values=np.abs(
            self.trace[ids]
        )


        if values.sum()==0:

            return None


        return (
            values /
            values.sum()
        )