import numpy as np

from core.io.transport import BitPacket



class CameraIO:


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



        if field.ndim != 2:

            return None



        if field.shape[1] != 3:

            return None



        packet = BitPacket(

            source="camera",
            
            #
            # external camera stream
            #
            tag="camera_raw",

            data=
                field.astype(
                    np.uint8
                ).tobytes(),


            shape=
                field.shape,


            dtype=
                "uint8",


            schema=
                "media.bgr",


            meta={

                "format":"BGR",

                "channels":3,

                "color_space":"BGR"

            }

        )


        self.last_packet = packet


        return packet