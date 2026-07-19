import numpy as np


class OscillatorOrgan:

    def __init__(self, name):

        self.name = name

        self.state = np.random.normal(
            0,
            0.01
        )

        self.activity = 0

        self.history = []



    def receive(self, field):

        value = np.mean(field)

        self.state += value * 0.01

        self.activity += 1



    def step(self):

        # 自然衰减

        self.state *= 0.995

        self.history.append(
            self.state
        )

        if len(self.history) > 100:

            self.history.pop(0)



    def emit(self):

        return self.state



    def snapshot(self):

        return {

            "name": self.name,

            "state":
                round(
                    float(self.state),
                    5
                ),

            "activity":
                self.activity
        }