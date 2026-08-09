import numpy as np


class DisplayIO:
    """
    Pure display port.


    Input:

        byte packet

        {
            bytes,
            shape,
            dtype
        }


    Output:

        RGB uint8 frame


    No:

        semantic interpretation
        model knowledge
        feature meaning
        control

    """



    def __init__(
        self,
        height=240,
        width=320
    ):

        self.height = height
        self.width = width
        #
        # latest display state
        #
        
        #self.current_field = None
        #self.current_timestamp = None
        
    
        
    def encode(
        self,
        data
    ):


        if data is None:

            return None
            
        #
        # receive new display state
        #
                
        return self._render(
            data
        )    




    #
    # byte -> array
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


            array = raw.reshape(
                packet["shape"]
            )


            return array.astype(
                np.float32
            )


        except Exception as e:

            print(
                "display decode error:",
                e
            )

            return None





    #
    # dimension adapter only
    #

    def _to_rgb(
        self,
        array
    ):


        if array.ndim == 2:


            return np.repeat(
                array[:, :, None],
                3,
                axis=2
            )



        if array.ndim == 3:


            #
            # already image-like
            #

            if array.shape[2] == 3:

                return array



            #
            # arbitrary feature channels
            #
            # take first 3 channels only
            # no semantic meaning
            #

            if array.shape[2] > 3:

                return array[:, :, :3]



        if array.ndim == 1:


            #
            # vector state
            #
            # reshape as line field
            #

            return array.reshape(
                1,
                -1,
                1
            ).repeat(
                3,
                axis=2
            )


        return None





    #
    # resize
    #

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





    #
    # numeric -> framebuffer
    #

    def _to_uint8(
        self,
        img
    ):


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
        ).astype(
            np.uint8
        )
        
    def _render(
        self,
        data
    ):

        img = data


        #
        # numeric field
        #

        img = self._to_rgb(
            img
        )


        if img is None:

            return None



        #
        # resize to window
        #

        img = self._resize(
            img
        )


        #
        # uint8 framebuffer
        #

        img = self._to_uint8(
            img
        )


        return img