import numpy as np


class ObserverSystem:
    """
    Observer only samples.

    No:
        control
        optimization
        feedback
        memory of world

    Snapshot is temporary.
    """


    def __init__(
        self,
        min_sample=16,
        max_sample=128,
        observation_probability=0.01
    ):

        self.min_sample = min_sample
        self.max_sample = max_sample

        self.observation_probability = (
            observation_probability
        )

        self.snapshot = {}



    def should_observe(self, t):

        """
        Random time window.

        Observer has no clock control.
        """

        return (
            np.random.random()
            <
            self.observation_probability
        )



    def sample(self, cells, t):

        """
        Random quantity sampling.

        Snapshot only.
        """

        size = np.random.randint(
            self.min_sample,
            self.max_sample + 1
        )


        size = min(
            size,
            len(cells)
        )


        ids = np.random.choice(
            len(cells),
            size=size,
            replace=False
        )


        states = [
            cells[i].state()
            for i in ids
        ]


        xs = np.array(
            [
                s["x"]
                for s in states
            ]
        )


        vs = np.array(
            [
                s["v"]
                for s in states
            ]
        )


        self.snapshot = {

            "time":
            t,

            "observed":
            size,

            "x_mean":
            float(np.mean(xs)),

            "x_std":
            float(np.std(xs)),

            "v_mean":
            float(np.mean(vs)),

            "v_std":
            float(np.std(vs))

        }


        return self.snapshot



    def summary(self):

        return self.snapshot