from core.oscillator import Oscillator


class Cell:


    def __init__(
        self,
        x,
        v,
        dt=0.02
    ):

        self.oscillator = Oscillator(
            x,
            v
        )

        self.field = 0.0

        self.energy = 1.0

        self.g = 0.0



    @property
    def x(self):
        return self.oscillator.x


    @property
    def v(self):
        return self.oscillator.v



    def receive(self, value):

        self.field += value



    def step(self):

        # 局部消耗
        self.energy *= 0.99999


        


        # 活动恢复能量
        self.energy += (
            abs(self.x)
            *
            0.00001
        )


        if self.energy > 1:
            self.energy = 1


       



    def update_slow(self):

        self.g += (
            0.00001 *
            (
                abs(self.x)
                -
                self.g
            )
        )



    def activity(self):

        return abs(self.x) * self.energy