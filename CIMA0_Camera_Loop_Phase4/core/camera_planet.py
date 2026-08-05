import numpy as np


class CameraPlanet:
    """
    External camera source.

    Responsibility:

        hardware frame acquisition

    Output:

        byte stream package

    No:

        sampling
        compression
        observation
        computation
    """


    def __init__(self):

        self.shape = None
        self.dtype = None



    def step_planet(self, frame):

        if frame is None:
            return None


        array = np.asarray(
            frame
        )


        self.shape = array.shape
        self.dtype = str(array.dtype)


        return {

            "frame":
                frame,

            "shape":
                array.shape,

            "dtype":
                self.dtype
        }



    def snapshot(self):

        return {

            "shape":
                self.shape,

            "dtype":
                self.dtype

        }