import numpy as np


class ClipRegion:
    """
    Local structural layer.

    Input:

        external data
        {
            bytes,
            shape,
            dtype
        }


    Flow:

        external byte field
                |
                v
        local structural projection
                |
                v
        local state evolution


    Does NOT:

        understand camera
        understand image
        classify
        control
        allocate


    Own state:

        input_state
        local_state
        age
    """



    def __init__(
        self,
        width=64,
        height=64,
        channels=3
    ):

        self.width = int(width)

        self.height = int(height)

        self.channels = int(channels)



        #
        # external disturbance
        #

        self.input_state = None



        #
        # local field
        #

        self.local_state = None



        #
        # internal time
        #

        self.age = 0



        #
        # evolution speed
        #

        self.rate = 0.01




    def receive(
        self,
        data
    ):
        """
        Receive external data.

        No interpretation.

        Only store.
        """

        self.input_state = data




    def step(
        self
    ):
        """
        Local autonomous evolution.
        """

        self.age += 1


        if self.input_state is None:
            return



        field = self.project(
            self.input_state
        )


        if field is None:
            return



        if self.local_state is None:

            self.local_state = field.copy()


        else:

            self.local_state += (
                self.rate *
                (
                    field -
                    self.local_state
                )
            )




    def project(
        self,
        data
    ):
        """
        External data
            |
            v
        local matrix


        Only structural projection.
        """


        if data is None:

            return None



        if not isinstance(
            data,
            dict
        ):

            return None



        raw = data.get(
            "bytes"
        )


        shape = data.get(
            "shape"
        )


        dtype = data.get(
            "dtype"
        )


        if raw is None:

            return None


        if shape is None:

            return None




        #
        # rebuild external field
        #

        try:

            arr = np.frombuffer(
                raw,
                dtype=np.uint8
            )


            src = arr.reshape(
                shape
            )


        except Exception:

            return None




        #
        # keep spatial relation
        #

        if src.ndim != 3:

            return None



        h,w,c = src.shape



        if c != self.channels:

            return None




        #
        # local sampling
        #

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



        field = src[
            np.ix_(
                ys,
                xs
            )
        ]



        #
        # numerical field
        #

        field = (
            field.astype(
                np.float32
            )
            /
            255.0
        )


        return field




    def snapshot(
        self
    ):
        """
        Raw local field.

        Read only.
        """

        if self.local_state is None:

            return None



        return self.local_state.copy()




    def state(
        self
    ):
        """
        Observer summary.
        """

        if self.local_state is None:

            return {

                "active": False,

                "shape": None

            }



        return {

            "active": True,

            "shape":
                list(
                    self.local_state.shape
                ),

            "mean":
                float(
                    self.local_state.mean()
                ),

            "std":
                float(
                    self.local_state.std()
                ),

            "age":
                self.age
        }