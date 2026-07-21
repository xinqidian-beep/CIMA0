import numpy as np



class ComputeField:


    """
    Resource environment.

    Only decides computation opportunity.

    Does not modify organism.

    """


    def __init__(
        self,
        organs,
        capacity=8
    ):

        self.organs=organs
        self.capacity=capacity

        self.rng=np.random.default_rng(42)



    def step(self):


        scores=[]


        for o in self.organs:

            score=(

                abs(o.prediction_error)

                +

                o.uncertainty

                +

                0.01*self.rng.random()

            )


            scores.append(score)



        scores=np.array(scores)


        prob=(
            scores
            /
            (scores.sum()+1e-12)
        )


        active=self.rng.choice(
            len(self.organs),
            self.capacity,
            replace=False,
            p=prob
        )


        return list(active)