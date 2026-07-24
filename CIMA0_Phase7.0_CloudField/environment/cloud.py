import numpy as np


class CloudField:

    """
    External perturbation field.

    No:
        memory
        reward
        target
        optimization

    Only:
        stochastic disturbance
    """

    def __init__(
        self,
        strength=0.001,
        seed=0
    ):

        self.strength = strength

        self.rng = np.random.default_rng(seed)



    def perturb(self):

        return self.rng.normal(
            0,
            self.strength
        )