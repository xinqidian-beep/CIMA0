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


        print(
            "CAMERA IO INPUT:",
            type(observation),
            observation.keys()
        )


        if "field" not in observation:

            return None



        field = observation["field"]


        print(
            "CAMERA FIELD:",
            type(field),
            field.shape,
            field.dtype
        )


        if not isinstance(
            field,
            np.ndarray
        ):

            return None



        #
        # accept BGR field
        #
        # preserve original structure
        #

        if field.shape[-1] != 3:

            return None



        try:


            packet = BitPacket(

                source="camera",

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

                    "format":
                        "BGR",

                    "channels":
                        3,

                    "color_space":
                        "BGR"

                }

            )


        except Exception as e:


            print(
                "BITPACKET ERROR:",
                e
            )


            return None



        self.last_packet = packet


        return packet