import numpy as np


class CameraPlanet:
    """
    External camera hardware.

    Responsibility:

        provide raw camera facts


    Does:

        frame acquisition information


    No:

        sampling
        normalization
        observation
        computation allocation
        semantic processing
    """


    def __init__(self):

        self.height = None
        self.width = None
        self.channels = None



    def step_planet(
        self,
        frame
    ):

        if frame is None:
            return None


        img = np.asarray(
            frame
        )


        h, w = img.shape[:2]


        self.height = h
        self.width = w
        self.channels = (
            img.shape[2]
            if len(img.shape) == 3
            else 1
        )


        return {

            "frame": frame,

            "height":
                self.height,

            "width":
                self.width,

            "channels":
                self.channels

        }



    def snapshot(self):

        return {

            "module":
                "CameraPlanet",

            "resolution":
                (
                    self.height,
                    self.width
                ),

            "channels":
                self.channels

        }