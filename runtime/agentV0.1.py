from core.cloud import Cloud
class Agent:

    def __init__(self):

        self.cloud = Cloud(
            cells=64,
            dim=512
        )

        self.running=True


    def run(self, steps=1000):

        for _ in range(steps):

            self.cloud.step()

            print(
                self.cloud.snapshot()
            )