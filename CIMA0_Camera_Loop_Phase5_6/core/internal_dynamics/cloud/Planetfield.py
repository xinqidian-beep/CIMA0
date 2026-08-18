import numpy as np

class PlanetField:


    def __init__(
        self,
        planet
    ):

        self.planet = planet

        self.previous = None



    def receive(
        self,
        disturbance
    ):

        self.planet.receive(
            disturbance
        )



    def step(
        self
    ):

        self.planet.step()


        current = self.planet.snapshot()


        if self.previous is not None:

            delta = np.mean(
                np.abs(
                    current -
                    self.previous
                )
            )

            print(
                "PLANETFIELD DELTA:",
                float(delta)
            )


        self.previous = current.copy()



    def snapshot(
        self
    ):

        return self.planet.snapshot()