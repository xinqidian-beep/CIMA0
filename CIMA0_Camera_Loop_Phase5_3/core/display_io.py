import numpy as np



class DisplayIO:
    """
    Pure display port.


    Input:

        field/media packet


    Output:

        RGB uint8 framebuffer



    Knows:

        packet format


    Does NOT know:

        camera meaning

        planet meaning

        feature meaning

        semantic meaning

    """



    def __init__(
        self,
        height=240,
        width=320
    ):

        self.height = height

        self.width = width



    def encode(
        self,
        packet
    ):


        if packet is None:

            return None



        data = self._decode(
            packet
        )


        if data is None:

            return None



        fmt = packet.get(
            "format",
            "field"
        )



        #
        # media stream
        #

        if fmt == "BGR":

            image = self._bgr_to_rgb(
                data
            )



        #
        # internal numeric field
        #

        else:

            image = self._field_to_rgb(
                data
            )



        if image is None:

            return None



        image = self._resize(
            image
        )


        return image.astype(
            np.uint8
        )



    def _decode(
        self,
        packet
    ):


        try:


            raw = np.frombuffer(

                packet["bytes"],

                dtype=np.dtype(
                    packet["dtype"]
                )

            )


            data = raw.reshape(

                packet["shape"]

            )


        except Exception:


            return None



        return data



    def _bgr_to_rgb(
        self,
        data
    ):


        if data.ndim != 2:

            return None



        if data.shape[1] != 3:

            return None



        #
        # restore pixel structure

        #
        # if original shape information exists,
        # prefer it
        #

        return data.reshape(

            -1,

            1,

            3

        )[:, :, ::-1]



    def _field_to_rgb(
        self,
        data
    ):


        if data.ndim == 2:

            img = data[:, :, None]

            img = np.repeat(

                img,

                3,

                axis=2

            )


        elif data.ndim == 3:


            if data.shape[2] == 3:

                img = data


            else:

                img = np.repeat(

                    data[:, :, :1],

                    3,

                    axis=2

                )


        else:

            return None



        minimum = img.min()

        maximum = img.max()



        if maximum > minimum:


            img = (

                img - minimum

            ) / (

                maximum - minimum

            )

        else:


            img = np.zeros_like(
                img
            )



        return (

            img * 255

        ).astype(
            np.uint8
        )



    def _resize(
        self,
        img
    ):


        h,w,c = img.shape



        ys = np.linspace(

            0,

            h-1,

            self.height

        ).astype(
            np.int32
        )


        xs = np.linspace(

            0,

            w-1,

            self.width

        ).astype(
            np.int32
        )


        return img[

            np.ix_(

                ys,

                xs,

                np.arange(c)

            )

        ]