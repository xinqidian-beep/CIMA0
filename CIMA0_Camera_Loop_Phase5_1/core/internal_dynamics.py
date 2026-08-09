class InternalDynamics:
    """
    Internal dynamics container.


    Only manages:

        registered local organs


    Does NOT know:

        planet
        clip
        camera
        CLIP
        image
        meaning


    Every organ only needs:

        receive(raw)
        step()
        snapshot()
    """



    def __init__(self):

        self.organs = {}

        self.last_snapshot = {}



    def register(
        self,
        name,
        organ
    ):

        self.organs[name] = organ



    def receive(
        self,
        raw
    ):
        """
        External byte stream.

        Broadcast only.

        No interpretation.
        """

        for organ in self.organs.values():

            organ.receive(
                raw
            )



    def step(
        self
    ):
        """
        Local evolution.

        Each organ owns
        its own rule.
        """

        for name,organ in self.organs.items():

            organ.step()



        self.last_snapshot = {

            name:
            organ.snapshot()

            for name, organ
            in self.organs.items()

        }



    def snapshot(
        self
    ):
        """
        Read only export.
        """

        return self.last_snapshot.copy()
        
    def output(
        self,
        name
    ):
        """
        Read one organ snapshot
        as external output source.

        No interpretation.
        """

        organ = self.organs.get(
            name
        )

        if organ is None:
            return None
            
        if hasattr(
            organ,
            "read"
        ):    
            return organ.read()


        


        return None
        
        
    def output_display(
        self,
        name
    ):
        """
        Read one organ display output.

        Convert internal state into display field only.
        """

        organ = self.organs.get(
            name
        )

        if organ is None:
            return None


        if hasattr(
            organ,
            "display_field"
        ):
            return organ.display_field()


        return None