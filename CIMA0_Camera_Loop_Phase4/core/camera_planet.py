import numpy as np


class CameraPlanet:


    def __init__(self):

        self.previous_state = None
        self.current_state = None



    def step(
        self,
        frame
    ):

        if frame is None:
            return



        self.previous_state = self.current_state


        self.current_state = {

            "bytes":
                frame.tobytes(),

            "shape":
                frame.shape,

            "dtype":
                str(frame.dtype)

        }



    def state(
        self
    ):

        return self.current_state