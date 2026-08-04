import numpy as np



class ClipRegion:
    """
    Local structural layer.

    Responsibility:

        external byte stream
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
        allocate resources


    Own state:

        input_state
        local_state
        age
    """



    def __init__(
        self,
        width=64,
        height=64,
        channels=3,
        weight_path=None
    ):
        #
        # compatibility:
        # old call:
        # ClipRegion(weight_path)
        #

        if isinstance(width, str):

            weight_path = width

            width = 64
            height = 64
            channels = 3   
 
    

        self.width = int(width)
        self.height = int(height)
        self.channels = int(channels)


        #
        # external disturbance buffer
        #

        self.input_state = None


        #
        # local layer state
        #

        self.local_state = None


        #
        # internal time
        #

        self.age = 0



        #
        # evolution rate
        #

        self.rate = 0.01



    def receive(
        self,
        data
    ):
        """
        Receive raw bytes.

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

            self.local_state = field



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
        Byte stream
        ->
        local matrix


        No semantic conversion.

        Only structural reconstruction.
        """


        if data is None:
            return None



        if isinstance(
            data,
            bytes
        ):

            arr = np.frombuffer(
                data,
                dtype=np.uint8
            )


        elif isinstance(
            data,
            np.ndarray
        ):

            arr = np.asarray(
                data,
                dtype=np.uint8
            ).reshape(-1)


        else:

            return None



        if arr.size == 0:
            return None



        size = (
            int(self.width) *
            int(self.height) *
            int(self.channels)
        )



        if arr.size < size:

            buf = np.zeros(
                size,
                dtype=np.uint8
            )

            buf[:arr.size] = arr

            arr = buf


        else:

            arr = arr[:size]



        field = arr.reshape(
            self.height,
            self.width,
            self.channels
        )



        #
        # keep numerical range
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
        Raw local layer state.

        Read only.
        """


        if self.local_state is None:

            return None



        return (
            self.local_state
            .copy()
        )



    def state(
        self
    ):
        """
        Observer summary.

        Does not replace snapshot.
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