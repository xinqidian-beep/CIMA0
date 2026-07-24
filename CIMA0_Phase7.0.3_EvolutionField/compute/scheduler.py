import numpy as np


class ComputeScheduler:


    def __init__(self):

        self.depth=1



    def allocate(self,observer_signal):


        if observer_signal is None:

            return []


        # 局部展开

        center=observer_signal


        region=np.arange(
            max(0,center-8),
            min(center+8,4096)
        )


        return region