import numpy as np


class DisplayIO:
    """
    CIMA0 Phase5_3

    Pure display port.


    Input:

        packet

        media:

        {
            type: "media",
            format: "BGR",
            bytes,
            shape,
            dtype
        }


        field:

        {
            type: "field",
            representation,
            bytes,
            shape,
            dtype
        }



    Output:

        RGB uint8 framebuffer



    Knows:

        packet structure


    Does NOT know:

        camera meaning
        planet meaning
        field meaning
        semantic meaning
    """



    def __init__(
        self,
        height=240,
        width=320
    ):

        self.height = height

        self.width = width

        #
        # previous complete structure
        #

        self.previous = None

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

        data = self._complete(
            data
        )

        packet_type = packet.get(
            "type"
        )



        #
        # external media stream
        #
        if packet_type == "media":

            image = self._media_to_rgb(
                data,
                packet
            )



        #
        # internal field
        #
        elif packet_type == "field":

            image = self._field_to_rgb(
                data
            )



        else:

            return None



        if image is None:

            return None



        image = self._resize(
            image
        )


        return image.astype(
            np.uint8
        )

    #
    # missing position completion
    #

    def _complete(
        self,
        data
    ):


        if self.previous is None:

            self.previous = data.copy()

            return data



        mask = np.isnan(
            data
        )



        if np.any(mask):

            data = data.copy()

            data[mask] = self.previous[mask]



        self.previous = data.copy()



        return data

    #
    # byte packet decode
    #

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



    #
    # media stream decoder
    #

    def _media_to_rgb(
        self,
        data,
        packet
    ):


        fmt = packet.get(
            "format"
        )


        if fmt != "BGR":

            return None



        #
        # preserve original media structure
        #

        if data.ndim != 3:

            return None



        if data.shape[2] != 3:

            return None



        #
        # BGR -> RGB
        #

        return data[:, :, ::-1]



    #
    # internal field visualization
    #

    def _field_to_rgb(
        self,
        data
    ):


        if data.ndim == 2:


            #
            # scalar field
            #
            # visualization only
            #

            img = data[:, :, None]


            img = np.repeat(

                img,

                3,

                axis=2

            )



        elif data.ndim == 3:


            #
            # already vector field
            #

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



        #
        # normalize framebuffer
        #

        img = img.astype(
            np.float32
        )


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

            img * 255.0

        ).clip(

            0,

            255

        ).astype(

            np.uint8

        )



    #
    # display size adapter
    #

    def _resize(
        self,
        img
    ):


        h,w,c = img.shape



        ys = np.linspace(

            0,

            h - 1,

            self.height

        ).astype(
            np.int32
        )


        xs = np.linspace(

            0,

            w - 1,

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