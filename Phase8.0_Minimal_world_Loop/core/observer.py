import numpy as np


class Observer:


    def __init__(self, sample_size=32):

        self.sample_size = sample_size



    def look(self, world):

        """
        观察者随机看一小部分

        永远不知道全局
        """

        ids=np.random.choice(
            len(world.cells),
            self.sample_size,
            replace=False
        )


        data=world.sample(ids)


        x=[
            d["x"]
            for d in data
        ]


        return {

            "sample":self.sample_size,

            "mean":
                float(np.mean(x)),

            "std":
                float(np.std(x))
        }