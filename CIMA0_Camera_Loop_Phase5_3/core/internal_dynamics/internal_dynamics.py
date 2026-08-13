import numpy as np


class InternalDynamics:
    """
    CIMA0 Phase5_3

    Bridge between external disturbance
    and Planet dynamics.

    Responsibility:

        packet
          |
          v
        decode
          |
          v
        disturbance field
          |
          v
        collision into Planet

    Does NOT know:

        camera meaning
        color meaning
        display
        sampling
        compute budget
    """


    def __init__(
        self,
        planet
    ):

        self.planet = planet

        self.last_snapshot = None



    def receive(
        self,
        packet
    ):
        """
        Receive external disturbance.

        Only injects disturbance.
        Does not replace Planet state.
        """

        disturbance = self._prepare_disturbance(
            packet
        )


        if disturbance is None:
            return



        field = disturbance["field"]


        if not hasattr(
            self.planet,
            "state"
        ):
            return



        state = self.planet.state



        #
        # project disturbance
        # into Planet state space
        #
        field = self._project(
            field,
            state.shape
        )


        if field is None:
            return



        #
        # small collision
        #
        collision_strength = 0.01


        self.planet.state += (
            field *
            collision_strength
        )



    def _prepare_disturbance(
        self,
        packet
    ):
        """
        Byte packet -> disturbance field

        Keep original structure.

        No semantic reduction.
        """


        if not isinstance(
            packet,
            dict
        ):
            return None



        required = (
            "bytes",
            "shape",
            "dtype"
        )


        if not all(
            key in packet
            for key in required
        ):
            return None



        try:

            data = np.frombuffer(
                packet["bytes"],
                dtype=np.dtype(
                    packet["dtype"]
                )
            )


            data = data.reshape(
                packet["shape"]
            )


        except Exception:

            return None



        data = data.astype(
            np.float32
        )



        #
        # keep channel structure
        #
        if data.ndim not in (
            2,
            3
        ):
            return None



        #
        # normalize only
        #
        if data.max() > 1.0:

            data = (
                data / 255.0
                -
                0.5
            )



        return {

            "type":
                "disturbance",

            "field":
                data,

            "shape":
                data.shape,

            "dtype":
                "float32",

            "source":
                packet.get(
                    "source",
                    "external"
                ),

            "format":
                packet.get(
                    "format",
                    "unknown"
                )

        }



    def _project(
        self,
        field,
        target_shape
    ):
        """
        Spatial projection only.

        No meaning.
        No feature extraction.
        """


        #
        # Planet current state:
        #
        # (H,W)
        #

        if field.ndim == 3:

            #
            # collapse only for collision projection
            #
            # original packet is not changed
            #
            field = field.mean(
                axis=2
            )



        if field.shape == target_shape:

            return field



        if len(target_shape) != 2:

            return None



        h,w = target_shape


        sh,sw = field.shape[:2]


        ys = np.linspace(
            0,
            sh-1,
            h
        ).astype(
            np.int32
        )


        xs = np.linspace(
            0,
            sw-1,
            w
        ).astype(
            np.int32
        )


        return field[
            np.ix_(
                ys,
                xs
            )
        ]



    def step(
        self
    ):

        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()



        if hasattr(
            self.planet,
            "snapshot"
        ):

            self.last_snapshot = {

                "planet":
                    self.planet.snapshot()

            }

        else:

            self.last_snapshot = {}



    def snapshot(
        self
    ):

        if self.last_snapshot is None:

            if hasattr(
                self.planet,
                "snapshot"
            ):

                return {

                    "planet":
                        self.planet.snapshot()

                }


            return None



        return self.last_snapshot.copy()