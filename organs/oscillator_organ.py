import numpy as np


class OscillatorOrgan:

    def __init__(
        self,
        name,
        dim=16
    ):

        self.name = name

        self.dim = dim


        # 内部状态

        self.state = np.random.normal(
            0,
            0.01,
            dim
        )


        # 每个内部单元拥有自己的时间

        self.phase = np.random.uniform(
            0,
            6.28,
            dim
        )


        self.frequency = np.random.uniform(
            0.95,
            1.05,
            dim
        )


        self.activity = 0


        self.history = []



    def receive(
        self,
        field
    ):

        value = np.mean(
            field
        )


        # 外部场扰动

        self.state += (
            np.tanh(value)
            *
            0.001
        )


        self.activity += 1



    def step(self):


        # 内部节律推进

        self.phase += (
            self.frequency
            *
            0.01
        )


        internal = np.sin(
            self.phase
        )


        # 每个维度独立受到内部振荡

        self.state += (
            internal
            *
            0.001
        )


        # 自然衰减

        self.state *= 0.995


        self.history.append(
            self.state.copy()
        )


        if len(self.history) > 100:

            self.history.pop(0)


        self.activity += 1



    def emit(self):

        return self.state



    def snapshot(self):

        return {

            "name":
            self.name,


            "mean":
            round(
                float(
                    np.mean(
                        self.state
                    )
                ),
                5
            ),


            "std":
            round(
                float(
                    np.std(
                        self.state
                    )
                ),
                5
            ),


            "phase_mean":
            round(
                float(
                    np.mean(
                        self.phase
                    )
                ),
                5
            ),


            "phase_std":
            round(
                float(
                    np.std(
                        self.phase
                    )
                ),
                5
            ),


            "activity":
            self.activity

        }