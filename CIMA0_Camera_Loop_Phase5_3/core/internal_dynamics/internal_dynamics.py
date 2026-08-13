import numpy as np



class InternalDynamics:
    """
    CIMA0 Internal Dynamics Interface.


    Responsibility:


        external disturbance

                |

                v

        disturbance field


                |

                v

        Planet evolution



    Knows:

        packet conversion
        disturbance forwarding
        evolution clock


    Does NOT know:

        camera meaning
        color meaning
        cloud meaning
        display
        observer
    """



    def __init__(
        self,
        planet
    ):

        self.planet = planet

        self.last_snapshot = None



    def receive(
        self,
        raw
    ):
        """
        Receive external disturbance.


        Only:

            bytes
            reshape
            type conversion


        No semantic interpretation.
        """


        disturbance = self._prepare_disturbance(
            raw
        )


        if disturbance is None:

            return



        #
        # forward disturbance
        #

        if hasattr(
            self.planet,
            "receive"
        ):

            self.planet.receive(
                disturbance
            )



        #
        # fallback:
        #
        # some pure Planet rules
        # only expose state
        #

        elif hasattr(
            self.planet,
            "state"
        ):

            field = disturbance["field"]


            state = self.planet.state


            if state.shape == field.shape:

                self.planet.state += field



    def _prepare_disturbance(
        self,
        packet
    ):
        """
        Universal byte unpacking.


        Input:

            media packet


        Output:

            disturbance packet


        No:

            camera logic

            feature extraction

            semantic conversion
        """


        if packet is None:

            return None



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



        #
        # external field projection
        #
        # media -> disturbance
        #

        if data.ndim == 3:


            #
            # collapse channels
            #
            # not semantic
            #
            # just create scalar disturbance field
            #

            data = data.astype(
                np.float32
            ).mean(
                axis=2
            )


        elif data.ndim != 2:


            return None



        data = data.astype(
            np.float32
        )


        #
        # normalize disturbance magnitude
        #

        if data.max() > 1.0:

            data = (

                data / 255.0

                -

                0.5

            )



        return {


            "field":

                data,


            "shape":

                data.shape,


            "dtype":

                "float32",



            "type":

                "disturbance",



            "source":

                packet.get(
                    "source",
                    "external"
                ),



            "origin":

                packet.get(
                    "format",
                    "unknown"
                )

        }



    def step(
        self
    ):

        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()



        self.last_snapshot = {


            "planet":

                self._snapshot_planet()

        }



    def _snapshot_planet(
        self
    ):


        if hasattr(
            self.planet,
            "snapshot"
        ):

            return self.planet.snapshot()



        if hasattr(
            self.planet,
            "state"
        ):

            return self.planet.state.copy()



        return None



    def snapshot(
        self
    ):


        if self.last_snapshot is None:

            return {

                "planet":

                    self._snapshot_planet()

            }


        return self.last_snapshot.copy()