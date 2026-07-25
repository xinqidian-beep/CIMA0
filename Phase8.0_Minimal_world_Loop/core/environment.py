import random


class Environment:

    """
    World memory.

    Not input.
    Accumulated history.
    """


    def __init__(self):

        self.field = 0.0

        self.events = 0



    def receive(
        self,
        cell_state
    ):

        # world changed by existence

        self.field += (
            cell_state["x"]
            *
            0.000001
        )

        self.events += 1



    def local_value(
        self
    ):

        # local world value

        return self.field



    def decay(self):

        # environment also changes

        self.field *= 0.999999