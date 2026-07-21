import numpy as np


class ComputeField:


    def __init__(
        self,
        organs,
        capacity=8
    ):

        self.organs=organs

        self.capacity=capacity



    def step(self):


        # 每个 organ 自己产生需求

        demand=[]


        for i,o in enumerate(self.organs):

            d=o.need_compute()

            demand.append(
                (
                    d,
                    i
                )
            )


        # 计算资源自然流向高需求

        demand.sort(
            reverse=True
        )


        active=[
            idx
            for _,idx in demand[:self.capacity]
        ]



        for i,o in enumerate(self.organs):

            if i in active:

                o.full_step()

            else:

                o.compressed_step()



        return active