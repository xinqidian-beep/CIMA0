import random
import math


class Cell:

    def __init__(self, cid):

        self.cid = cid

        self.x = random.uniform(
            -0.01,
            0.01
        )

        self.energy = (
            self.x*self.x
        )

        self.memory = 0.0


    def step(self, perturb):

        # 外界只是未知变化

        internal = (
            -0.001*self.x
        )


        self.x += (
            internal
            +
            perturb
        )


        self.energy = (
            self.x*self.x
        )


        # 极慢历史

        self.memory = (
            0.999*self.memory
            +
            0.001*self.x
        )



    def state(self):

        return {

            "x":self.x,

            "energy":
                self.energy,

            "memory":
                self.memory

        }