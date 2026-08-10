"""
CIMA0 Phase5_2

Internal Dynamics Container

Only manages local organs.

Does NOT know:

camera
planet
clip
image
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

            organ.receive(raw)



    def step(
        self
    ):

        for organ in self.organs.values():

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

        return self.last_snapshot.copy()



    def output(
        self,
        name
    ):

        organ = self.organs.get(name)

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

        organ = self.organs.get(name)

        if organ is None:
            return None


        if hasattr(
            organ,
            "display_field"
        ):

            return organ.display_field()


        return None