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
        byte stream


    Resource interaction:

        read compute resource state

        decide own sampling density


    Does not:

        control ComputeSystem
        understand image meaning
        classify
        predict
        control internal dynamics
        allocate resources
    """



    def __init__(self):

        self.camera_size = 32


        self.previous_state = None



    def update_resource(
        self,
        compute_state
    ):
        """
        Adapt own sampling density.

        Input:

            resource state only


        No command.
        No control.
        """


        available = compute_state[
            "available"
        ]


        if available > 0.7:

            self.camera_size = 16


        elif available > 0.3:

            self.camera_size = 32


        else:

            self.camera_size = 64



    def sample(
        self,
        frame
    ):
        """
        Camera frame -> local cell state
        """


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


                state[y,x] = (
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
        Temporal variation.

        delta =
            current
            -
            previous
        """


        if self.previous_state is None:

            self.previous_state = (
                current_state.copy()
            )

            return None



        delta = (
            current_state
            -
            self.previous_state
        )


        self.previous_state = (
            current_state.copy()
        )


        return delta



    def encode_bytes(
        self,
        state
    ):
        """
        External state -> byte stream.

        No meaning.
        Only transport format.
        """


        normalized = np.clip(
            state,
            0.0,
            1.0
        )


        data = (
            normalized
            *
            255
        ).astype(
            np.uint8
        )


        return data.tobytes()



    def snapshot(self):

        if self.previous_state is None:

            return None


        return {

            "camera_size":
                self.camera_size,

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