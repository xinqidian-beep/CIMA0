class InternalDynamics:

    def __init__(
        self,
        core=None
    ):

        self.core = core

        self.external_bytes = b""


    def receive(
        self,
        data
    ):

        if data is not None:

            self.external_bytes = data



    def step(
        self
    ):

        if self.core is None:
            return


        self.core.receive(
            self.external_bytes
        )


        self.core.step()



    def snapshot(
        self
    ):

        if self.core is None:

            return None


        return self.core.snapshot()