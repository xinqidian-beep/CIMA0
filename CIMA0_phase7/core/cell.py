import numpy as np

from core.oscillator import Oscillator


class Cell:

    def __init__(
        self,
        x,
        v,
        energy=1.0
    ):

        self.oscillator = Oscillator(
            x,
            v
        )

        # slow memory trace
        self.g = 0.0

        # internal resources
        self.energy = energy

        # accumulated fatigue
        self.fatigue = 0.0

        # temporary field
        self.field = 0.0



    @property
    def x(self):
        return self.oscillator.x


    @property
    def v(self):
        return self.oscillator.v



    def add_field(self,value):

        self.field += value



    def activity(self):

        return abs(self.x)+abs(self.v)



    def step(self):

        activity = self.activity()


        # ------------------
        # energy metabolism
        # ------------------

        consume = (
            0.00005 *
            activity
        )


        recover = (
            0.00001 *
            (1.0-self.energy)
        )


        self.energy += recover
        self.energy -= consume


        # boundary only physical limit
        self.energy = np.clip(
            self.energy,
            0.05,
            2.0
        )


        # ------------------
        # fatigue
        # ------------------

        self.fatigue += (
            0.0001 *
            activity
        )


        self.fatigue -= (
            0.00005 *
            self.fatigue
        )


        self.fatigue=max(
            0.0,
            self.fatigue
        )


        # ------------------
        # effective drive
        # ------------------

        drive = (
            self.energy /
            (1.0+self.fatigue)
        )


        self.oscillator.step(
            self.field * drive
        )


        self.field=0.0


        self.update_slow()



    def update_slow(self):

        activity=self.activity()


        self.g += (
            0.00001*
            (
                activity-
                self.g
            )
        )



    def snapshot(self):

        return {

            "x":
            round(float(self.x),5),

            "v":
            round(float(self.v),5),

            "g":
            round(float(self.g),5),

            "energy":
            round(float(self.energy),5),

            "fatigue":
            round(float(self.fatigue),5)
        }