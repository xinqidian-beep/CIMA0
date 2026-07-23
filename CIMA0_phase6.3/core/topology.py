import numpy as np


class LocalTopology:


    def __init__(
        self,
        n,
        avg_degree=4
    ):

        self.n=n


        self.edges=[]


        for i in range(n):

            others=np.delete(
                np.arange(n),
                i
            )


            neighbors=np.random.choice(
                others,
                avg_degree,
                replace=False
            )


            for j in neighbors:

                if i<j:

                    self.edges.append(
                        (i,j)
                    )



    def neighbors(self):

        return self.edges