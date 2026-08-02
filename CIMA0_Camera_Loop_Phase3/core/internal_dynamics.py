# core/internal_dynamics.py


class InternalDynamics:
    """
    Internal composite system.

    Responsibility:

        byte stream
             |
             v

        dispatch only

             |
        +----+----+
        |         |
        v         v

     Planet    ClipRegion


        |
        v

     snapshot


    Does NOT:

        decode bytes
        interpret input
        create cloud
        merge states
        control modules
        modify internal rules


    Planet and ClipRegion
    own their own byte interpretation.
    """



    def __init__(
        self,
        planet,
        clip
    ):

        self.planet = planet

        self.clip = clip



    def receive(
        self,
        data
    ):
        """
        Pass external disturbance.

        Raw bytes only.

        No interpretation.
        """


        if hasattr(
            self.planet,
            "receive"
        ):

            self.planet.receive(
                data
            )


        if hasattr(
            self.clip,
            "receive"
        ):

            self.clip.receive(
                data
            )



    def step(
        self
    ):
        """
        Advance internal time.

        Each module evolves independently.
        """


        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()



        if hasattr(
            self.clip,
            "step"
        ):

            self.clip.step()
            
            
    def snapshot(
        self
    ):
        """
        Structural observation.

        No fusion.
        No compression.
        """

        result = {}


        if hasattr(
            self.planet,
            "snapshot"
        ):
 
            result["planet"] = (
                self.planet.snapshot()
            )

        elif hasattr(
            self.planet,
            "state"
        ):

            result["planet"] = {
                "state":
                    self.planet.state
            }



        if hasattr(
            self.clip,
            "snapshot"
        ):

            result["clip"] = (
                self.clip.snapshot()
            )

        elif hasattr(
            self.clip,
            "state"
        ):

            result["clip"] = (
                self.clip.state()
            )



        return result



        
            
            
        
    

    