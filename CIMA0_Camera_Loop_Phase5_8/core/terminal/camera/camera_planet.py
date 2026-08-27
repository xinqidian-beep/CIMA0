import numpy as np


class CameraPlanet:
    """
    Camera physical boundary.


    Input:

        ndarray BGR frame


    Output:

        media packet

        {
            bytes,
            shape,
            dtype,

            format,
            channels,
            source
        }


    Responsibility:

        preserve camera stream identity


    No:

        resize
        sampling
        compression
        semantic
        feature
        interpretation

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



        #
        # keep previous packet
        #

        self.previous_state = (
            self.current_state
        )



        #
        # preserve original ndarray
        #

        if not isinstance(
            frame,
            np.ndarray
        ):

            return None



        packet = {


            #
            # raw media bytes
            #

            "bytes":
                frame.tobytes(),



            #
            # original tensor structure
            #

            "shape":
                frame.shape,



            #
            # original numeric type
            #

            "dtype":
                str(
                    frame.dtype
                ),



            #
            # identity information
            #

            "format":
                "image",



            "channels":
                "BGR",



            "source":
                "camera"


        }



        self.current_state = packet


        return packet



    def state(
        self
    ):

        return self.current_state