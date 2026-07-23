import numpy as np


class Body:

    """
    Minimal physical body

    only:
        position
        velocity
        mass

    no:
        energy
        activity
        memory
        goal
    """

    def __init__(
        self,
        x,
        v,
        mass=1.0
    ):

        self.x=x
        self.v=v
        self.mass=mass



    def kinetic(self):

        return (
            0.5*
            self.mass*
            self.v*self.v
        )