class InternalDynamics:


    def __init__(
        self,
        planet,
        clip
    ):

        self.planet = planet
        self.clip = clip

        self.external_bytes = b""


    def receive(
        self,
        data
    ):

        self.external_bytes = data



    def step(self):

        #
        # byte enters internal boundary
        #
        if hasattr(
            self.planet,
            "inject"
        ):

            self.planet.inject(
                self.external_bytes
            )


        #
        # internal evolution
        #
        self.planet.step()


        self.clip.update(
            self.planet
        )



    def snapshot(self):

        return {

            "planet":
                self.planet.snapshot(),

            "clip":
                self.clip.state()

        }