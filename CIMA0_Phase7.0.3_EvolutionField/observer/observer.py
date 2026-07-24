import numpy as np


class Observer:


    def __init__(self):

        self.interest=None



    def observe(self,state):

        diff=np.abs(state)


        # 稀疏发现
        ids=np.random.choice(
            len(state),
            64,
            replace=False
        )


        scores=diff[ids]


        self.interest=ids[
            np.argmax(scores)
        ]


        return self.interest