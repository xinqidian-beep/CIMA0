import numpy as np



class CameraIO:
    """
    CIMA0 Camera IO.


    Input:

        CameraObserver field


    Output:

        BGR media packet



    Responsibility:


        preserve media stream identity

        bytes packaging



    No:


        sampling

        compute

        image processing

        semantic interpretation

    """



    def __init__(self):

        self.last_packet = None



    def encode(
        self,
        observation
    ):


        if observation is None:

            return None



        if "field" not in observation:

            return None



        field = observation["field"]



        if not isinstance(
            field,
            np.ndarray
        ):

            return None



        #
        # CameraObserver internal form:

        #
        # (pixels,3)

        #

        if field.ndim != 2:

            return None



        if field.shape[1] != 3:

            return None



        packet = {


            "bytes":

                field.astype(
                    np.uint8
                ).tobytes(),



            "shape":

                field.shape,



            "dtype":

                "uint8",



            #
            # media identity
            #

            "type":

                "media",



            "format":

                "BGR",



            "channels":

                3,



            "color_space":

                "BGR",



            "source":

                "camera_io"

        }



        self.last_packet = packet



        return packet



    def state(
        self
    ):

        return self.last_packet