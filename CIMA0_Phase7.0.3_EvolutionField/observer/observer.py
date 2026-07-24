import numpy as np


class Observer:


    def __init__(self,n=64):

        self.state=np.zeros(n)

        self.memory=np.zeros(n)



    def perceive(
        self,
        cloud
    ):

        ids=np.random.choice(
            len(cloud.field),
            self.state.shape[0],
            replace=False
        )


        signal=np.array(
            [
                cloud.sample(i)
                for i in ids
            ]
        )


        self.state += signal



    def step(self):

        self.memory*=0.999

        self.memory+=(
            self.state*0.001
        )

        self.state*=0.95



    def snapshot(self):

        return {
            "observer_activity":
                float(
                    np.std(
                        self.state
                    )
                ),

            "observer_memory":
                float(
                    np.std(
                        self.memory
                    )
                )
        }
