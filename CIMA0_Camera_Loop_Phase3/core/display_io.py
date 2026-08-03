import numpy as np


class DisplayIO:
    """
    Structural display adapter.

    internal read result -> display frame


    Does NOT:

        analyze
        interpret
        fuse semantics
        control
        modify state


    Only:

        collect structural fields
        project fields into display space
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
        read_result
    ):

        if not read_result:
            return None


        frame = np.zeros(
            (
                self.height,
                self.width,
                3
            ),
            dtype=np.float32
        )


        fields = []


        self._collect(
            read_result,
            fields
        )


        if not fields:
            return None



        #
        # all local fields project into one field
        #

        count = 0


        for field in fields:

            image = self._field_to_image(
                field
            )


            if image is None:
                continue


            image = self._resize(
                image,
                self.height,
                self.width
            )


            if image.ndim == 2:

                image = np.stack(
                    [
                        image,
                        image,
                        image
                    ],
                    axis=2
                )


            frame += image.astype(
                np.float32
            )


            count += 1



        if count > 0:

            frame /= count



        frame = np.clip(
            frame,
            0,
            255
        )


        return frame.astype(
            np.uint8
        )



    # --------------------------------------------------
    # recursive structure traversal
    # --------------------------------------------------

    def _collect(
        self,
        obj,
        fields
    ):

        if obj is None:
            return


        if isinstance(
            obj,
            dict
        ):

            for value in obj.values():

                self._collect(
                    value,
                    fields
                )


            return



        if isinstance(
            obj,
            np.ndarray
        ):

            if obj.size:

                fields.append(
                    obj
                )


            return



    # --------------------------------------------------
    # ndarray -> display field
    # --------------------------------------------------

    def _field_to_image(
        self,
        array
    ):

        arr = np.nan_to_num(
            array.astype(
                np.float32
            )
        )


        #
        # RGB/BGR field
        #

        if (
            arr.ndim == 3
            and arr.shape[2] >= 3
        ):

            value = np.abs(
                arr[:, :, :3]
            )


            mx = value.max()

            if mx > 0:

                value = (
                    value /
                    mx *
                    255
                )


            return value



        #
        # 2D field
        #

        if arr.ndim == 2:

            value = np.abs(
                arr
            )


            mx = value.max()


            if mx > 0:

                value = (
                    value /
                    mx *
                    255
                )


            return value



        #
        # 1D field
        #

        flat = arr.reshape(
            -1
        )


        if flat.size == 0:
            return None


        mx = np.max(
            np.abs(flat)
        )


        if mx > 0:

            flat = (
                np.abs(flat)
                /
                mx *
                255
            )


        side = int(
            np.sqrt(
                len(flat)
            )
        )


        if side > 1:

            usable = side * side

            return flat[:usable].reshape(
                side,
                side
            )


        return flat.reshape(
            1,
            -1
        )



    # --------------------------------------------------
    # simple nearest resize
    # --------------------------------------------------

    def _resize(
        self,
        image,
        height,
        width
    ):

        h, w = image.shape[:2]


        ys = np.linspace(
            0,
            h - 1,
            height
        ).astype(
            np.int32
        )


        xs = np.linspace(
            0,
            w - 1,
            width
        ).astype(
            np.int32
        )


        if image.ndim == 2:

            return image[
                np.ix_(
                    ys,
                    xs
                )
            ]


        return image[
            np.ix_(
                ys,
                xs,
                np.arange(
                    image.shape[2]
                )
            )
        ]