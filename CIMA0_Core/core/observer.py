import numpy as np



class ObserverSystem:


    def __init__(
        self,
        sample_size=64
    ):

        self.sample_size=sample_size



    def sample(
        self,
        cells,
        t
    ):

        n=len(cells)


        ids=np.random.choice(
            n,
            min(
                self.sample_size,
                n
            ),
            replace=False
        )


        xs=[
            cells[i].x
            for i in ids
        ]


        vs=[
            cells[i].v
            for i in ids
        ]



        return {

            "time":t,

            "sampled":len(ids),

            "x_std":float(np.std(xs)),

            "v_std":float(np.std(vs))

        }