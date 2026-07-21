import numpy as np


class ComputeField:

    def __init__(
        self,
        organs,
        capacity=8
    ):

        self.organs = organs
        self.capacity = capacity

        self.rng = np.random.default_rng(42)


    def step(self):

        scores=[]

        for i,o in enumerate(self.organs):

            # 这里只读取动力学状态
            # 不改变 organ
            score = (
                abs(o.prediction_error)
                +
                o.uncertainty
                +
                0.01*self.rng.random()
            )

            scores.append(score)



        scores=np.array(scores)


        # soft selection
        # 不是排名治理
        prob=scores/(scores.sum()+1e-12)


        active=self.rng.choice(
            len(self.organs),
            size=self.capacity,
            replace=False,
            p=prob
        )


        return list(active)