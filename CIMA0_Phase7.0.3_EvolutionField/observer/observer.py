import random



class Observer:


    def __init__(
        self,
        sample_size=64
    ):

        self.sample_size=sample_size



    def sample(self, universe):


        ids=random.sample(
            list(universe.cells.keys()),
            self.sample_size
        )


        observations=[]


        for i in ids:

            c=universe.cells[i]


            observations.append(
                (
                    i,
                    abs(c.activity)
                )
            )


        return observations