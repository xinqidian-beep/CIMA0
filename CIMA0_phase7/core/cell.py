import numpy as np

from core.oscillator import Oscillator



class Cell:


    def __init__(
        self,
        x,
        v
    ):

        self.oscillator = Oscillator(
            x,
            v
        )

        self.g = 0.0

        self.field = 0.0



    @property
    def x(self):

        return self.oscillator.x



    @property
    def v(self):

        return self.oscillator.v



    @property
    def energy(self):

        return self.oscillator.energy



    def add_field(
        self,
        value
    ):

        self.field += value



    def apply_field(
        self,
        value
    ):

        self.field += value



    def apply_velocity_field(
        self,
        value
    ):

        self.oscillator.v += value



    def step(self):

        self.oscillator.step(
            self.field
        )


        self.field = 0.0


        self.update_slow()



    def update_slow(self):

        activity = abs(self.x)


        self.g += 0.00001 * (
            activity - self.g
        )



    def state_vector(self):

        return np.array(
            [
                self.x,
                self.v,
                self.g,
                self.energy
            ],
            dtype=float
        )



    def snapshot(self):

        return {

            "x":
                round(
                    float(self.x),
                    6
                ),

            "v":
                round(
                    float(self.v),
                    6
                ),

            "g":
                round(
                    float(self.g),
                    6
                ),

            "energy":
                round(
                    float(self.energy),
                    6
                )

        }