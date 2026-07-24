import numpy as np



class CloudField:


    def __init__(
        self,
        size,
        strength,
        seed=None
    ):


        self.size=size

        self.strength=strength


        if seed is not None:
            np.random.seed(seed)


        self.field=np.zeros(size)



    def step(self):


        noise=np.random.normal(
            0,
            1,
            self.size
        )


        mask=np.random.random(
            self.size
        )


        # 空位
        noise[mask<0.2]=0


        # 负扰动
        noise[mask>0.8]*=-1


        self.field += (
            noise*
            self.strength
        )


        # 自然衰减

        self.field*=0.95



    def sample(self,index):


        return self.field[
            index % self.size
        ]