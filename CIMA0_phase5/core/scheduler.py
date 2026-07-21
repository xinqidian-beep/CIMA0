import numpy as np


class Scheduler:

    def __init__(
        self,
        n,
        active_ratio=0.1
    ):

        self.n = n
        self.active_ratio = active_ratio

        self.update_count = np.zeros(
            n,
            dtype=np.int64
        )


    def select(self):

        size = max(
            1,
            int(
                self.n *
                self.active_ratio
            )
        )


        ids = np.random.choice(
            self.n,
            size=size,
            replace=False
        )


        self.update_count[ids]+=1


        return ids