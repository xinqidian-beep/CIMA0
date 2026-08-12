import numpy as np


class CameraPlanet:
    """
    Camera physical boundary.

    Input:

        ndarray BGR frame


    Output:

        byte packet

        {
            bytes,
            shape,
            dtype
        }


    No:

        resize
        sampling
        semantic
        feature
    """



    def __init__(self):

        self.previous_state = None
        self.current_state = None



    def step(
        self,
        frame
    ):


        if frame is None:

            return None



        self.previous_state = (
            self.current_state
        )


        packet = {

            "bytes":
                frame.tobytes(),


            "shape":
                frame.shape,


            "dtype":
                str(frame.dtype)

        }


        self.current_state = packet


        return packet




    def state(
        self
    ):

        return self.current_state