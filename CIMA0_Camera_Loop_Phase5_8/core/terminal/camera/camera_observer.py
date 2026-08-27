import numpy as np



class CameraObserver:
    """
    CIMA0 Camera Observer.


    Input:

        CameraPlanet packet

        {
            bytes,
            shape,
            dtype,
            format,
            channels
        }



    Output:

        camera field observation



    Responsibility:


        maintain BGR field

        calculate change

        raise compute request



    No:


        sampling execution

        compute allocation

        semantic extraction

        image understanding

    """



    def __init__(
        self,
        w_delta=0.5,
        w_age=0.3,
        w_activity=0.2
    ):


        self.previous = None

        self.field = None

        self.age = None



        self.w_delta = w_delta

        self.w_age = w_age

        self.w_activity = w_activity



    def observe(
        self,
        packet
    ):


        pixels = self._decode(
            packet
        )


        if pixels is None:

            return None



        #
        # first frame
        #

        if self.previous is None:


            self.previous = pixels.copy()

            self.field = pixels.copy()


            self.age = np.zeros(

                pixels.shape[0],

                dtype=np.float32

            )


            delta = np.zeros(

                pixels.shape[0],

                dtype=np.float32

            )



        else:


            delta = np.mean(

                np.abs(

                    pixels.astype(
                        np.int16
                    )

                    -

                    self.previous.astype(
                        np.int16
                    )

                ),

                axis=1

            )



            self.previous = pixels.copy()



            self.age += 1



            active = delta > 0


            self.age[active] = 0



            #
            # maintain complete field
            #
            # no sampling here
            #

        activity = delta + 1e-6



        observation = {


            "field":

                self.field.copy(),



            "delta":

                delta.copy(),



            "age":

                self.age.copy(),



            "activity":

                activity.copy(),



            "type":

                "camera_observation",



            "source":

                "camera"

        }



        observation["request"] = self.raise_hand(

            observation

        )



        return observation



    def raise_hand(
        self,
        observation
    ):
        """
        Automatic attention request.

        Only report demand.
        """



        delta = observation["delta"]

        age = observation["age"]

        activity = observation["activity"]



        age_norm = (

            age /

            max(
                np.max(age),
                1.0
            )

        )



        score = (

            self.w_delta * delta

            +

            self.w_age * age_norm

            +

            self.w_activity * activity

        )



        return {


            "type":

                "compute_request",



            "source":

                "camera",



            "score":

                score.astype(
                    np.float32
                ),



            "shape":

                score.shape

        }



    def _decode(
        self,
        packet
    ):


        if packet is None:

            return None



        try:


            raw = np.frombuffer(

                packet["bytes"],

                dtype=np.dtype(
                    packet["dtype"]
                )

            )


            frame = raw.reshape(

                packet["shape"]

            )


        except Exception:


            return None



        #
        # preserve BGR structure
        #

        if frame.ndim != 3:

            return None



        if frame.shape[2] != 3:

            return None



        #
        # pixel field

        #

        return frame.reshape(

            -1,

            3

        )



    def encode_field(
        self,
        observation
    ):


        if observation is None:

            return None



        field = observation["field"]



        return {


            "bytes":

                field.astype(
                    np.uint8
                ).tobytes(),



            "shape":

                field.shape,



            "dtype":

                "uint8",



            #
            # preserve media identity
            #

            "type":

                "field",



            "format":

                "BGR",



            "channels":

                3,



            "source":

                "camera_observer"

        }