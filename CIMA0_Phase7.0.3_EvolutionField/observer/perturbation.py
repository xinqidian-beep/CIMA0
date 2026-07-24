import random


class CloudPerturbation:

    def __init__(self, strength=0.001):
        self.strength=strength


    def inject(self, universe, count=32):

        ids=random.sample(
            range(len(universe.cells)),
            count
        )

        field={}

        for i in ids:
            field[i]=(
                random.uniform(
                    -self.strength,
                    self.strength
                )
            )

        return field