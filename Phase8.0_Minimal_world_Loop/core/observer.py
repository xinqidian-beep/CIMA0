import numpy as np


class ObserverSystem:
    """
    Observer system.

    Only samples.

    No:
        control
        optimization
        feedback
    """

    def __init__(self, sample_size=32):

        self.sample_size = sample_size


    def sample(self, cells):

        ids = np.random.choice(
            len(cells),
            size=min(
                self.sample_size,
                len(cells)
            ),
            replace=False
        )


        states = [
            cells[i].state()
            for i in ids
        ]


        xs = np.array(
            [s["x"] for s in states]
        )

        vs = np.array(
            [s["v"] for s in states]
        )


        return {

            "sample":
                len(states),

            "x_mean":
                float(np.mean(xs)),

            "x_std":
                float(np.std(xs)),

            "v_mean":
                float(np.mean(vs)),

            "v_std":
                float(np.std(vs))

        }