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

        # slow variable
        self.g = 0.0

        # natural trace
        self.activity_memory = 0.0

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

        self.oscillator.step(
            self.field
        )


        self.field = 0.0


        self.update_slow()



    def update_slow(self):

        activity = abs(self.x)


        # 极弱历史痕迹
        # 不是奖励
        # 不是竞争
        self.activity_memory += (
            0.001 * activity
            -
            0.00001 * self.activity_memory
        )


        # 慢变量
        self.g += (
            0.00001 *
            (
                activity
                -
                self.g
            )
        )



    def snapshot(self):

        return {
            "x":self.x,
            "g":self.g,
            "memory":self.activity_memory,
            "energy":self.energy
        }