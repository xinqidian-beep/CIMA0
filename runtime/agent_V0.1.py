class CIMA:

    def __init__(self):

        self.cloud = LayeredCloud(
            kinds=[
                "audio",
                "vision",
                "text"
            ]
        )

        self.dev = DevelopmentController(...)


        self.bus = InputBus()


    def run(self):

        while True:

            stimuli=self.bus.poll()

            for s in stimuli:
                self.cloud.receive(s)

            self.cloud.step()

            self.dev.observe(self.cloud)