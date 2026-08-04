import numpy as np


class DisplayIO:
    """
    Pure output adapter.

    Responsibility:

        array structure
              |
              v
        display byte stream


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
        # preserve structure
        #

        arr = self._normalize(
            arr
        )



        #
        # scalar field
        #

        if arr.ndim == 2:


            rgb = np.stack(
                [
                    arr,
                    arr,
                    arr
                ],
                axis=2
            )


        #
        # already vector field
        #

        elif arr.ndim == 3:

            rgb = arr



        else:

            return None



        rgb = self._resize(
            rgb
        )


        return (
            rgb * 255
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