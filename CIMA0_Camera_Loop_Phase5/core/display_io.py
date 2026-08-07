import numpy as np


class DisplayIO:
    """
    Pure display port.

    Input:
        existing field

    Output:
        RGB byte stream

    No:
        interpretation
        normalization
        semantic mapping
        control
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
        field
    ):

        if field is None:
            return None


        arr = np.asarray(
            field,
            dtype=np.float32
        )


        if arr.size == 0:
            return None



        if arr.ndim == 2:


            rgb = np.repeat(
                arr[:,:,None],
                3,
                axis=2
            )


        elif arr.ndim == 3:


            rgb = arr


        else:

            return None



        rgb = self._resize(
            rgb
        )


        return np.clip(
            (rgb + 1.0) * 127.5,
            0,
            255
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