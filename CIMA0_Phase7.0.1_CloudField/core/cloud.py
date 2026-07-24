import random


class Cloud:


    def __init__(
        self,
        strength=0.01
    ):

        self.strength=strength



    def perturb(self):

        """

        返回一次局部扰动

        不知道世界状态

        """

        if random.random()<0.001:

            return random.uniform(
                -self.strength,
                self.strength
            )

        return 0.0