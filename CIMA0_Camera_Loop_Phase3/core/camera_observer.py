import numpy as np


class CameraObserver:
    """
    Camera sampling module.

    Responsibility:

        frame -> sampled state


    No:

        semantic understanding
        resource allocation
        hardware control
        internal dynamics control
    """


    def __init__(
        self,
        cell_px=20
    ):
        """
        cell_px:
            pixels represented by one sampled cell

        Topology is derived from camera frame size.
        """

        self.cell_px = cell_px

        self.previous = None

        self.last_shape = None



    def sample(
        self,
        frame
    ):
        """
        Full frame deterministic block average.

        BGR preserved.

        frame:
            H,W,3

        return:
            sampled field
        """

        if frame is None:
            return None


        h, w, c = frame.shape


        grid_h = h // self.cell_px
        grid_w = w // self.cell_px


        if grid_h <= 0 or grid_w <= 0:
            return None


        #
        # keep only complete blocks
        # every remaining pixel participates
        #

        usable_h = grid_h * self.cell_px
        usable_w = grid_w * self.cell_px


        trimmed = frame[
            :usable_h,
            :usable_w
        ]


        #
        # BGR block mean
        #

        blocks = trimmed.reshape(
            grid_h,
            self.cell_px,
            grid_w,
            self.cell_px,
            3
        )


        field = blocks.mean(
            axis=(1, 3)
        )


        #
        # normalize
        #

        field = field / 255.0


        return field



    def step_observe(
        self,
        frame
    ):
        """
        Sampling + self comparison.

        δ = current - history
        """


        current = self.sample(
            frame
        )


        if current is None:
            return None



        if self.previous is None:

            delta = np.zeros_like(
                current
            )

        else:

            delta = current - self.previous



        self.previous = current.copy()



        return {

            "state": current,

            "delta": delta,

            "shape": current.shape,

            "activity": float(
                np.mean(
                    np.abs(delta)
                )
            )

        }



    def snapshot(
        self
    ):
        """
        Read only summary.
        """

        if self.previous is None:

            return {
                "active": False
            }


        return {

            "active": True,

            "shape":
                self.previous.shape,

            "mean":
                float(
                    np.mean(
                        self.previous
                    )
                ),

            "std":
                float(
                    np.std(
                        self.previous
                    )
                )

        }