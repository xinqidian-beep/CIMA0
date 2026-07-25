import numpy as np



class Environment:


    def __init__(self):

        self.pressure=0.0



    def receive(
        self,
        response
    ):

        self.pressure += (
            np.mean(
                np.abs(response)
            )
            -
            self.pressure
        )*0.01



    def stimulate(self):

        if self.pressure > 0.02:

            return True

        return False