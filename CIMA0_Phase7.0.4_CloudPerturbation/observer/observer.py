import numpy as np
import random


class Observer:
    """
    局部观察者

    只观察状态变化
    不控制动力
    不寻找目标
    不判断智能
    """

    def __init__(self):

        self.history = []


    def observe(self, universe):

        n = len(
            universe.cells
        )


        # 稀疏观察
        sample_size = min(
            64,
            n
        )


        ids = random.sample(
            range(n),
            sample_size
        )


        values = np.array(
            [
                universe.cells[i].x
                for i in ids
            ]
        )


        obs = {

            "sample":
                sample_size,


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
                        values * values
                    )
                )
        }


        self.history.append(
            obs
        )


        return obs