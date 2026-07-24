import random


class Observer:


    def __init__(
        self,
        sample_size=64
    ):

        self.sample_size=sample_size



    def sample(self, universe):


        ids=random.sample(

            range(len(universe.cells)),

            self.sample_size

        )


        result=[]


        for i in ids:


            result.append(

                (
                    i,
                    universe.local_state(i)

                )

            )


        return result