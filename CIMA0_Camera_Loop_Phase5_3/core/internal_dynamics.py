"""
CIMA0 Phase5_3

Internal Dynamics Container

Only manages local organs.

Does NOT know:

camera
planet
clip
cloud details
meaning
"""


class InternalDynamics:


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

        for organ in self.organs.values():

            if hasattr(
                organ,
                "receive"
            ):

                organ.receive(
                    raw
                )



    def request_compute(
        self
    ):
        """
        Collect compute requests
        from all organs.
        """

        requests = {}


        for name, organ in self.organs.items():

            if hasattr(
                organ,
                "request_compute"
            ):

                requests[name] = (

                    organ.request_compute()

                )


        return requests



    def execute_compute(
        self,
        allocation
    ):
        """
        Dispatch compute budget.
        """

        for name, organ in self.organs.items():

            if hasattr(
                organ,
                "execute_compute"
            ):

                organ.execute_compute(

                    allocation

                )



    def step(
        self
    ):

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

            if hasattr(
                organ,
                "snapshot"
            )

        }



    def snapshot(
        self
    ):

        return self.last_snapshot.copy()



    def output(
        self,
        name
    ):

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