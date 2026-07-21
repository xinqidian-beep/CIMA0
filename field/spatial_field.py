import numpy as np


class SpatialField:

    def __init__(
        self,
        organs,
        radius=1.0,
        coupling=0.0001
    ):

        self.organs = organs
        self.radius = radius
        self.coupling = coupling


    def step(self):

        n = len(self.organs)


        for i in range(n):

            for j in range(i+1,n):


                a=self.organs[i]
                b=self.organs[j]


                distance=np.linalg.norm(
                    a.position -
                    b.position
                )


                if distance < self.radius:


                    force = (
                        self.coupling *
                        (
                            b.state -
                            a.state
                        )
                    )


                    a.velocity += force
                    b.velocity -= force