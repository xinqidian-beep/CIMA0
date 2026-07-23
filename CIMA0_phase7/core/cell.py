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


        # slow trace
        self.g = 0.0


        # metabolic state
        self.energy = 1.0

        self.fatigue = 0.0


        # external perturbation
        self.field = 0.0



    @property
    def x(self):

        return self.oscillator.x



    @property
    def v(self):

        return self.oscillator.v



    def activity(self):

        return abs(self.x)+abs(self.v)



    def add_field(
        self,
        value
    ):

        self.field += value



    def step(self):


        activity=self.activity()


        #
        # metabolism
        #

        consume = (
            0.00001 *
            activity
        )


        recovery = (
            0.00002 *
            (1.0-self.energy)
        )


        self.energy += recovery
        self.energy -= consume


        self.energy=np.clip(
            self.energy,
            0.1,
            2.0
        )


        #
        # fatigue
        #
        # only short memory
        #

        self.fatigue += (
            0.00005 *
            (
                activity-
                self.fatigue
            )
        )


        #
        # energy affects ability
        #

        drive=self.energy



        self.oscillator.step(
            self.field * drive
        )


        self.field=0.0



        self.update_slow()



    def update_slow(self):


        activity=self.activity()


        self.g += (
            0.00001 *
            (
                activity-
                self.g
            )
        )



    def snapshot(self):

        return {

            "x":float(self.x),

            "v":float(self.v),

            "energy":float(self.energy),

            "fatigue":float(self.fatigue),

            "g":float(self.g)

        }