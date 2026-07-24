import random
import numpy as np


class Compute:

    """
    稀疏计算系统

    不控制动力系统
    不修改cell

    只负责:
    采样
    压缩统计
    精算局部
    """

    def __init__(
        self,
        sample_size=64
    ):

        self.sample_size = sample_size



    def process(
        self,
        universe,
        observation=None
    ):

        n = len(
            universe.cells
        )


        #
        # 稀疏采样
        #
        ids = random.sample(
            range(n),
            min(
                self.sample_size,
                n
            )
        )


        values = np.array(
            [
                universe.cells[i].x
                for i in ids
            ]
        )


        #
        # 压缩统计
        #
        result = {

            "sample":
                len(values),


            "mean":
                float(
                    np.mean(values)
                ),


            "std":
                float(
                    np.std(values)
                ),


            "energy":
                float(
                    np.mean(
                        values*values
                    )
                )
        }


        return result