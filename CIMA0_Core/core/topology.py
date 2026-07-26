import numpy as np


class Topology:


    def __init__(
        self,
        size,
        degree=4
    ):

        self.size=size

        self.neighbors={}


        for i in range(size):

            choices=list(
                range(size)
            )

            choices.remove(i)


            self.neighbors[i]=list(
                np.random.choice(
                    choices,
                    degree,
                    replace=False
                )
            )


    def get(
        self,
        cid
    ):

        return self.neighbors[cid]