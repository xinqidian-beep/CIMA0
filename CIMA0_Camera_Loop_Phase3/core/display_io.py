import numpy as np


class DisplayIO:
    """
    Pure display port.

    Input:
        existing field structure

    Output:
        RGB byte stream


    No:
        interpretation
        semantic mapping
        field selection
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



        #
        # keep spatial relation
        #

        arr = self._normalize(
            arr
        )



        #
        # scalar field
        #

        if arr.ndim == 2:

            rgb = np.zeros(
                (
                    arr.shape[0],
                    arr.shape[1],
                    3
                ),
                dtype=np.float32
            )


            #
            # identical mapping
            #
            # no color creation
            #

            rgb[:,:,0] = arr
            rgb[:,:,1] = arr
            rgb[:,:,2] = arr



        #
        # already RGB
        #

        elif arr.ndim == 3:

            rgb = arr



        else:

            return None



        rgb = self._resize(
            rgb
        )


        return (
            rgb * 255.0
        ).clip(
            0,
            255
        ).astype(
            np.uint8
        )



    def _normalize(
        self,
        arr
    ):

        mn = np.min(
            arr
        )

        mx = np.max(
            arr
        )


        if mx == mn:

            return np.zeros_like(
                arr
            )


        return (
            arr - mn
        ) / (
            mx - mn
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