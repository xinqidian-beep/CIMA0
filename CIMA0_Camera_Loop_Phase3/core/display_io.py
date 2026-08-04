import numpy as np


class DisplayIO:
    """
    Simple video output port.

    input:
        structured data

    output:
        fixed RGB byte frame

    Does NOT:
        analyze
        interpret
        control
    """


    def __init__(
        self,
        height=240,
        width=320
    ):

        self.height = height
        self.width = width


        self.frame_buffer = np.zeros(
            (
                height,
                width,
                3
            ),
            dtype=np.uint8
        )


    # --------------------------------------------------
    # public output
    # --------------------------------------------------

    def encode(
        self,
        data
    ):

        field = self._find_array(
            data
        )


        if field is None:

            return self.frame_buffer



        frame = self._to_rgb(
            field
        )


        self.frame_buffer[:] = frame


        return self.frame_buffer



    # --------------------------------------------------
    # find display payload
    # --------------------------------------------------

    def _find_array(
        self,
        obj
    ):

        if isinstance(
            obj,
            np.ndarray
        ):

            if obj.size:

                return obj


        if isinstance(
            obj,
            dict
        ):

            for value in obj.values():

                result = self._find_array(
                    value
                )

                if result is not None:

                    return result


        return None



    # --------------------------------------------------
    # ndarray -> RGB bytes
    # --------------------------------------------------

    def _to_rgb(
        self,
        array
    ):

        data = np.nan_to_num(
            array.astype(
                np.float32
            )
        )


        #
        # RGB input
        #

        if (
            data.ndim == 3
            and data.shape[2] >= 3
        ):

            image = data[:, :, :3]


        #
        # scalar field
        #

        elif data.ndim == 2:

            mn = data.min()
            mx = data.max()


            if mx > mn:

                image = (
                    data - mn
                ) / (
                    mx - mn
                ) * 255

            else:

                image = np.zeros_like(
                    data
                )


            image = np.stack(
                [
                    image,
                    image,
                    image
                ],
                axis=2
            )


        else:

            flat = data.reshape(
                -1
            )

            side = int(
                np.sqrt(
                    flat.size
                )
            )


            if side < 1:

                return self.frame_buffer


            image = flat[:side*side].reshape(
                side,
                side
            )


            image = np.stack(
                [
                    image,
                    image,
                    image
                ],
                axis=2
            )


        image = self._resize(
            image
        )


        image = np.clip(
            image,
            0,
            255
        )


        return image.astype(
            np.uint8
        )



    # --------------------------------------------------
    # fixed output size
    # --------------------------------------------------

    def _resize(
        self,
        image
    ):

        h, w = image.shape[:2]


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


        return image[
            np.ix_(
                ys,
                xs,
                np.arange(3)
            )
        ]