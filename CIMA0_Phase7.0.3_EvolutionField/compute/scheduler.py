import numpy as np


class Scheduler:


    def __init__(
        self,
        n
    ):

        self.n=n



    def allocate(
        self,
        observer_hint=None
    ):


        # 第一层稀疏采样

        sample=np.random.choice(
            self.n,
            64,
            replace=False
        )


        if observer_hint is None:

            return sample



        # 局部展开

        center=observer_hint


        local=np.arange(
            max(
                0,
                center-8
            ),
            min(
                self.n,
                center+8
            )
        )


        # 少量精算区域

        return np.unique(
            np.concatenate(
                [
                    sample,
                    local
                ]
            )
        )