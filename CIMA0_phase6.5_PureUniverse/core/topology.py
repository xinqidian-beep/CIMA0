import numpy as np


class Topology:


    def __init__(
        self,
        n,
        degree=6
    ):

        self.n=n

        self.neighbors=[
            []
            for _ in range(n)
        ]


        for i in range(n):

            ids=np.random.choice(
                n,
                degree,
                replace=False
            )


            for j in ids:

                if j!=i:

                    self.neighbors[i].append(j)