import random


class Environment:


    def __init__(self):

        self.phase = 0


    def step(self):

        self.phase += 1



    def cloud(self):

        """
        云进入世界

        不是命令
        只是存在
        """

        if random.random()<0.001:

            return random.gauss(
                0,
                0.05
            )

        return 0.0