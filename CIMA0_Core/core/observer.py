import numpy as np


class Observer:


    def __init__(
        self,
        sample_size=64
    ):

        self.sample_size=sample_size



    def sample(
        self,
        cells
    ):


        n=len(cells)

        k=min(
            self.sample_size,
            n
        )


        ids=np.random.choice(
            n,
            k,
            replace=False
        )


        xs=np.array(
            [
                cells[i].x
                for i in ids
            ]
        )


        vs=np.array(
            [
                cells[i].v
                for i in ids
            ]
        )


        return {

            "sampled":k,

            "x_std":
            float(np.std(xs)),

            "v_std":
            float(np.std(vs))

        }