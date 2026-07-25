import random
import math


class Cell:
    """
    Minimal autonomous entity.

    Knows only:
        self state
        local environment

    Does not know:
        universe
        other cells
        global state
    """

    def __init__(self, cid):

        self.cid = cid

        # internal existence state
        self.energy = random.uniform(
            0.0005,
            0.0015
        )

        self.x = random.uniform(
            -0.01,
            0.01
        )

        self.age = 0


    def step(
        self,
        local_environment
    ):

        self.age += 1


        # self internal dynamics
        internal = (
            math.sin(
                self.age * 0.0001
                + self.cid
            )
            * 0.00001
        )


        # environment feedback
        env_effect = (
            local_environment
            *
            0.001
        )


        # small unavoidable noise
        noise = (
            random.random()
            -
            0.5
        ) * 0.00001



        self.x += (
            internal
            +
            env_effect
            +
            noise
        )


        # energy follows own existence
        self.energy += (
            abs(self.x)
            *
            0.000001
        )


        # natural decay
        self.energy *= 0.999999


        return self.x



    def state(self):

        return {
            "id": self.cid,
            "x": self.x,
            "energy": self.energy,
            "age": self.age
        }