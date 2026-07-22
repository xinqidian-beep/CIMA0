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


        # slow variables

        self.g = 0.0

        self.fatigue = 0.0


        # external perturbation

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



    def step(self):


        #
        # fatigue changes sensitivity
        #
        effective_field = (
            self.field
            /
            (1.0 + self.fatigue)
        )


        self.oscillator.step(
            effective_field
        )


        #
        # consume perturbation
        #

        self.field = 0.0


        #
        # slow evolution
        #

        self.update_slow()



    def update_slow(self):


        activity = abs(self.x)



        #
        # local history trace
        #

        self.g += (

            0.00001 *

            (
                activity
                -
                self.g
            )

        )



        #
        # activity creates fatigue
        #

        self.fatigue += (

            0.00005 *
            activity

        )



        #
        # natural recovery
        #

        self.fatigue -= (

            0.00001 *
            self.fatigue

        )



        if self.fatigue < 0:

            self.fatigue = 0.0



    def snapshot(self):


        return {

            "x":
                round(self.x,6),

            "v":
                round(self.v,6),

            "g":
                round(self.g,6),

            "energy":
                round(self.energy,6),

            "fatigue":
                round(self.fatigue,6)

        }