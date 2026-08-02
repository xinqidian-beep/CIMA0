# core/display_io.py

import numpy as np


class DisplayIO:
    """
    Structural display adapter.

    Responsibility:

        internal snapshot
              |
              v
        display frame


    Does NOT:

        analyze
        interpret
        fuse
        control
        modify internal state
    """


    def __init__(self):
        pass



    def encode(
        self,
        snapshot
    ):

        if snapshot is None:
            return None


        print(
            "DISPLAY SNAPSHOT:",
            snapshot.keys()
        )


        h = 240
        w = 320


        frame = np.zeros(
            (
                h,
                w,
                3
            ),
            dtype=np.uint8
        )


        self._render(
            snapshot,
            frame,
            0,
            0,
            w,
            h
        )


        return frame



    def _render(
        self,
        obj,
        frame,
        x,
        y,
        w,
        h
    ):
        """
        Generic structural renderer.

        Only understands:

            dict
            ndarray
            scalar

        """

        if obj is None:
            return



        if isinstance(
            obj,
            dict
        ):

            items = list(
                obj.items()
            )

            if len(items) == 0:
                return


            step = max(
                1,
                h // len(items)
            )


            for i, (_, value) in enumerate(items):

                self._render(
                    value,
                    frame,
                    x,
                    y + i * step,
                    w,
                    step
                )



        elif isinstance(
            obj,
            np.ndarray
        ):


            if obj.size == 0:
                return


            arr = np.asarray(
                obj,
                dtype=np.float32
            )


            arr = np.nan_to_num(
                arr
            )


            arr = np.abs(
                arr
            )


            mx = np.max(
                arr
            )


            if mx > 0:
                arr = arr / mx


            img = (
                arr * 255
            ).astype(
                np.uint8
            )


            if img.ndim == 2:

                img = np.resize(
                    img,
                    (
                        h,
                        w
                    )
                )


                frame[
                    y:y+h,
                    x:x+w,
                    0
                ] = img



        elif isinstance(
            obj,
            (float, int)
        ):


            value = abs(
                float(obj)
            )


            value = min(
                1.0,
                value
            )


            length = int(
                w * value
            )


            frame[
                y:y+5,
                x:x+length,
                1
            ] = 255