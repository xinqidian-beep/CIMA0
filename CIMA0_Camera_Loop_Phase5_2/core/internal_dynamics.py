"""
CIMA0 Phase5_2

Internal Dynamics

Container only.

Manages:

    registered local organs


Does NOT know:

    camera
    planet
    clip
    image
    meaning


Every organ:

    receive(raw)

    step()

    snapshot()

"""


from .internal_dynamics.cloud import CloudField



class InternalDynamics:
    """
    Internal dynamics container.
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

            if hasattr(
                organ,
                "receive"
            ):

                organ.receive(
                    raw
                )



    def step(
        self
    ):
        """
        Local evolution.

        Each organ owns rules.
        """


        for organ in self.organs.values():

            if hasattr(
                organ,
                "step"
            ):

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
        Read organ output.
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
        Display output only.
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



# compatibility export
__all__ = [

    "InternalDynamics",

    "CloudField",

]