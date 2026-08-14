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
        
        self.last_projection = None

    def receive(
        self,
        packet
    ):

        disturbance = self._prepare_disturbance(
            packet
        )


        if disturbance is None:
            return



        #
        # keep external structure
        #

        self.structure_trace = {

            "external":
            {
                "format":
                    disturbance["format"],

                "shape":
                    disturbance["shape"],

                "dtype":
                    disturbance["dtype"]
            }

        }



        field = disturbance["field"]


        if not hasattr(
            self.planet,
            "state"
        ):
            return



        state = self.planet.state



        projected = self._project(
            field,
            state.shape
        )


        if projected is None:
            return



        #
        # record internal structure
        #

        self.structure_trace["internal"] = {

            "format":
                "field",

            "shape":
                projected.shape,

            "dtype":
                "float32"

        }

        #
        # bounded collision dynamics
        #

        collision_strength = 0.05
        dissipation = 0.05


        # 
        # natural decay of previous internal state
        #

        self.planet.state *= (
            1.0 - dissipation
        )


        #
        # collision with external field
        #

        self.planet.state += (
            projected *
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

        Responsibility:

            resize external disturbance
            into internal state space


        Does NOT:

            semantic reduction
            feature extraction
            hidden channel loss


        Return:

            projected field

        Side effect:

            save projection structure
        """



        if field is None:

            return None



        original_shape = field.shape



        #
        # record original structure
        #

        projection_info = {

            "source":
            {
                "shape":
                    original_shape,

                "ndim":
                    field.ndim,

                "channels":
                    None
            },


            "target":
            {
                "shape":
                    target_shape
            }

        }



        #
        # preserve channel information
        #

        if field.ndim == 3:


            projection_info["source"]["channels"] = field.shape[2]


            #
            # Planet currently uses 2D state
            #
            # Therefore collision needs a scalar projection.
            #
            # This is a structural projection,
            # not semantic interpretation.
            #

            field = np.mean(
                field,
                axis=2
            )


            projection_info["channel_mapping"] = {

                "type":
                    "collapse",


                "input_channels":
                    original_shape[2],


                "output_channels":
                    1,


                "empty_slots":
                    {

                        "B":
                            None,

                        "G":
                            None,

                        "R":
                            None

                    }

            }



        elif field.ndim == 2:


            projection_info["channel_mapping"] = {

                "type":
                    "identity",

                "channels":
                    1
 
            }


        else:

            return None



        #
        # spatial projection
        #

        if field.shape != target_shape:


            if len(target_shape) != 2:

                return None



            h,w = target_shape


            sh,sw = field.shape[:2]


            ys = np.linspace(
                0,
                sh - 1,
                h
            ).astype(
                np.int32
            )


            xs = np.linspace(
                0,
                sw - 1,
                w
            ).astype(
                np.int32
            )


            field = field[
                np.ix_(
                    ys,
                    xs
                )
            ]



        #
        # keep trace
        #

        self.last_projection = projection_info



        return field.astype(
            np.float32
        )
        
        
    def step(
        self
    ):
        """
        Internal evolution tick.

        Planet owns its own dynamics.
        InternalDynamics only schedules and snapshots.

        No semantic processing.
        """



        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()



        self.last_snapshot = {}



        if hasattr(
            self.planet,
            "snapshot"
        ):

            self.last_snapshot["planet"] = (
                self.planet.snapshot()
            )



        #
        # keep disturbance projection structure
        #

        if (
            hasattr(
                self,
                "last_projection"
            )
            and
            self.last_projection is not None
        ):

            self.last_snapshot["projection"] = (
                self.last_projection.copy()
            )



        #
        # keep external/internal structure trace
        #

        if (
            hasattr(
                self,
                "structure_trace"
            )
            and
            self.structure_trace is not None
        ):

            self.last_snapshot["structure"] = (
                self.structure_trace.copy()
            )
        
        
    
    def snapshot(
        self
    ):
        """
        Internal dynamics snapshot.

        Contains:

            internal state

            structure trace

            projection information

        No semantic interpretation.
        """



        if self.last_snapshot is not None:

            return self.last_snapshot.copy()



        snapshot = {}



        if hasattr(
            self.planet,
            "snapshot"
        ):

            snapshot["planet"] = (
                self.planet.snapshot()
            )



        #
        # external -> internal structure
        #

        if hasattr(
            self,
            "last_projection"
        ):

            snapshot["projection"] = (
                self.last_projection
            )



        #
        # input structure
        #

        if hasattr(
            self,
            "structure_trace"
        ):

            snapshot["structure"] = (
                self.structure_trace
            )



        return snapshot