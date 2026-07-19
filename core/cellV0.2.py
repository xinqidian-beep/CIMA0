import numpy as np


class Cell:

    def __init__(self, id, dim=512):

        self.id=id

        # 当前状态
        self.state=np.random.normal(
            0,
            0.1,
            dim
        )


        # 状态变化速度
        self.velocity=np.zeros(dim)


        # 局部历史痕迹
        self.trace=np.zeros(dim)


        # 局部能量
        self.energy=1.0


        # 活动次数
        self.activity=0



    def stimulate(
        self,
        vector,
        strength
    ):

        impulse = vector * strength * 0.05


        # 输入改变速度
        self.velocity += impulse


        # 输入改变能量
        self.energy += strength*0.01


        self.activity+=1



    def step(self):


        # 1. 惯性运动

        self.state += self.velocity



        # 2. 速度自然衰减

        self.velocity *= 0.95



        # 3. 状态阻尼

        self.state *= 0.999



        # 4. 热涨落

        self.state += np.random.normal(
            0,
            0.001,
            self.state.shape
        )



        # 5. trace残留

        self.trace *=0.98

        self.trace += self.state*0.02



        # 6. 能量消耗

        self.energy*=0.999



    def similarity(self,vector):

        return (
            np.dot(
                self.state,
                vector
            )
            /
            (
                np.linalg.norm(self.state)
                *
                np.linalg.norm(vector)
                +
                1e-8
            )
        )