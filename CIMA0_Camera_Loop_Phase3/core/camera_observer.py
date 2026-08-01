import numpy as np


class CameraObserver:
    """
    External camera observation boundary.

    Responsibility:

        raw camera frame
            |
            v
        spatial sampling
            |
            v
        external state


        temporal comparison
            |
            v
        delta ephemeral


    Does not:

        understand image
        classify
        predict
        control dynamics
        allocate compute
        select importance
        modify internal rules
    """



    def __init__(
        self,
        camera_size=32
    ):

        #
        # pixels per cell
        #
        self.camera_size = camera_size


        #
        # previous instantaneous state
        #
        self.previous_state = None



    def sample(
        self,
        frame
    ):
        """
        Raw camera frame -> external state


        Input:

            BGR frame


        Output:

            cell state matrix
        """


        if frame is None:
            return None



        h, w, _ = frame.shape


        size = self.camera_size


        grid_h = int(
            np.ceil(
                h / size
            )
        )


        grid_w = int(
            np.ceil(
                w / size
            )
        )


        state = np.zeros(
            (
                grid_h,
                grid_w
            ),
            dtype=np.float32
        )



        for y in range(grid_h):

            for x in range(grid_w):


                y0 = y * size
                y1 = min(
                    y0 + size,
                    h
                )


                x0 = x * size
                x1 = min(
                    x0 + size,
                    w
                )


                block = frame[
                    y0:y1,
                    x0:x1
                ]


                if block.size == 0:
                    continue



                #
                # only spatial aggregation
                #
                # no meaning
                #

                state[y, x] = (
                    block.mean()
                    /
                    255.0
                )


        return state



    def step_observe(
        self,
        current_state
    ):
        """
        Temporal self comparison.


        Output:

            delta_ephemeral


        No:

            judgement
            filtering
            selection
        """


        if current_state is None:
            return None



        if self.previous_state is None:

            self.previous_state = (
                current_state.copy()
            )

            return None



        delta_ephemeral = (
            current_state
            -
            self.previous_state
        )



        #
        # overwrite only
        #

        self.previous_state = (
            current_state.copy()
        )


        return delta_ephemeral



    def snapshot(
        self
    ):
        """
        Read-only external observation snapshot.
        """


        if self.previous_state is None:
            return None



        return {

            "shape":
                self.previous_state.shape,

            "mean":
                float(
                    self.previous_state.mean()
                ),

            "std":
                float(
                    self.previous_state.std()
                )

        }