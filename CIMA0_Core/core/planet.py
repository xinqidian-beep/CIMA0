import numpy as np


class Planet:

    """
    唯一动力核心

    不知道:
        observer
        compute
        io

    只负责:
        状态演化
        接收瞬时扰动
    """

    def __init__(self, size=128):

        self.size = size

        self.state = np.random.randn(
            size,
            size
        ) * 0.01


    def receive_disturbance(
        self,
        position,
        value
    ):

        x, y = position

        if 0 <= x < self.size and 0 <= y < self.size:

            self.state[x, y] += value



    def step(self):

        old = self.state.copy()

        for x in range(1, self.size-1):
            for y in range(1, self.size-1):

                neighbor = (
                    old[x+1,y] +
                    old[x-1,y] +
                    old[x,y+1] +
                    old[x,y-1]
                ) / 4


                # 最小局部动力规则

                self.state[x,y] += (
                    0.05 *
                    (neighbor-old[x,y])
                )


                # 非线性保持

                self.state[x,y] += (
                    0.001 *
                    np.sin(old[x,y])
                )



    def snapshot(self):

        return self.state.copy()