import numpy as np


class Observer:


    def sample(
        self,
        universe,
        size=64
    ):


        ids=np.random.choice(
            len(universe.cells),
            size,
            replace=False
        )


        values=np.array(
            [
                universe.cells[i].x
                for i in ids
            ]
        )


        return {

            "mean":
                float(np.mean(values)),

            "std":
                float(np.std(values)),

            "active":
                int(size)
        }



    def response(
        self,
        data
    ):

        std=np.std(data)


        threshold=std*2


        return {

            "std":
                float(std),

            "active":
                int(
                    np.sum(
                        np.abs(data)>threshold
                    )
                )
        }