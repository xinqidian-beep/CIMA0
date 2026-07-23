import random


class EventScheduler:


    def __init__(
        self,
        n,
        events_per_step=8
    ):

        self.n=n
        self.events_per_step=events_per_step



    def sample(self):

        return random.sample(
            range(self.n),
            self.events_per_step
        )