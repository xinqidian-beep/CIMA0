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

        # 当前活动势
        # 不是累计记忆
        # 是短时间尺度状态
        self.activity_memory = 0.0

        # 外部扰动场
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


        # 扰动消费
        self.field = 0.0


        self.update_slow()



    def update_slow(self):

        activity = abs(self.x)



        #
        # 自然耗散活动势
        #
        # 没有奖励
        # 没有惩罚
        # 没有竞争
        #
        self.activity_memory = (

            0.999 *
            self.activity_memory

            +

            0.001 *
            activity

        )



        #
        # 慢变量
        #
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

            "x":
                float(self.x),

            "v":
                float(self.v),

            "g":
                float(self.g),

            "activity":
                float(
                    self.activity_memory
                ),

            "energy":
                float(
                    self.energy
                )
        }