from .cloud.cloud_field import CloudField
from .cloud.cell import Cell



class InternalDynamics:
    """
    CIMA0 Phase5_3

    Internal organ container.

    Does NOT know:

        camera
        image
        clip
        meaning
        display
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

        for organ in self.organs.values():

            if hasattr(
                organ,
                "receive"
            ):

                organ.receive(raw)



    def request_compute(
        self
    ):

        requests = {}

        for name, organ in self.organs.items():

            if hasattr(
                organ,
                "request_compute"
            ):

                requests[name] = organ.request_compute()


        return requests



    def execute_compute(
        self,
        allocation
    ):

        for organ in self.organs.values():

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



__all__ = [
    "InternalDynamics",
    "CloudField",
    "Cell",
]