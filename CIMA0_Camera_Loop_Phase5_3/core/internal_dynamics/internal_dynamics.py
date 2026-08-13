"""
CIMA0 Phase5_3

Internal Dynamics Interface

Role:

    Transport boundary between external packets
    and Planet dynamics.

Responsible:

    - decode byte payload
    - preserve structural identity
    - forward disturbance

Does NOT know:

    camera
    image
    color
    cloud
    clip
    display
    feature meaning

The internal field keeps its own physics.
"""


import numpy as np



class InternalDynamics:


    def __init__(
        self,
        planet
    ):

        self.planet = planet

        self.last_snapshot = None

        #
        # preserve external identity
        #
        self.last_metadata = None



    def receive(
        self,
        packet
    ):
        """
        Receive external disturbance packet.

        Only transport conversion.

        No interpretation.
        """


        disturbance_packet = self._prepare_disturbance(
            packet
        )


        if disturbance_packet is None:

            return



        field = disturbance_packet["field"]


        #
        # preserve identity side-channel
        #
        self.last_metadata = (
            disturbance_packet.get(
                "metadata"
            )
        )



        if hasattr(
            self.planet,
            "receive"
        ):

            self.planet.receive(
                field
            )



    def _prepare_disturbance(
        self,
        packet
    ):
        """
        bytes -> ndarray

        Preserve:

            shape
            dtype
            metadata

        No:

            conversion
            normalization
            interpretation
        """


        if isinstance(
            packet,
            np.ndarray
        ):

            return {

                "field": packet,

                "shape":
                    packet.shape,

                "dtype":
                    str(packet.dtype),

                "metadata":
                    None
            }



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

            raw = np.frombuffer(
                packet["bytes"],
                dtype=np.dtype(
                    packet["dtype"]
                )
            )


            field = raw.reshape(
                packet["shape"]
            )


        except Exception:

            return None



        return {

            "field":
                field.astype(
                    np.float32,
                    copy=False
                ),

            "shape":
                packet["shape"],

            "dtype":
                packet["dtype"],

            "metadata":
                packet.get(
                    "metadata"
                )

        }



    def step(
        self
    ):
        """
        Advance Planet dynamics.

        No budget.
        No control.
        """


        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()



        self.last_snapshot = (
            self.snapshot()
        )



    def snapshot(
        self
    ):
        """
        Read-only exposure.
        """


        if not hasattr(
            self.planet,
            "snapshot"
        ):

            return None



        state = self.planet.snapshot()



        return {

            "planet":
            {

                "bytes":
                    state.tobytes()
                    if isinstance(
                        state,
                        np.ndarray
                    )
                    else None,


                "shape":
                    state.shape
                    if isinstance(
                        state,
                        np.ndarray
                    )
                    else None,


                "dtype":
                    str(
                        state.dtype
                    )
                    if isinstance(
                        state,
                        np.ndarray
                    )
                    else None,


                "field":
                    state,


                "metadata":
                    self.last_metadata

            }

        }