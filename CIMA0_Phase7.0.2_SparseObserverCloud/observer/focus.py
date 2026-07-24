import numpy as np



class FocusObserver:


    def __init__(self,size):

        self.size=size



    def focus(self,ids):


        return np.random.choice(

            ids,

            min(
                self.size,
                len(ids)
            ),

            replace=False

        )