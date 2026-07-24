import numpy as np



class FocusObserver:


    def __init__(
        self,
        size
    ):

        self.size=size



    def focus(
        self,
        ids,
        universe
    ):


        values=np.array(
            [
                abs(
                    universe.cells[i].x
                )
                for i in ids
            ]
        )


        if values.sum()==0:

            return np.random.choice(
                ids,
                self.size
            )


        prob=(
            values /
            values.sum()
        )


        return np.random.choice(
            ids,
            self.size,
            replace=False,
            p=prob
        )