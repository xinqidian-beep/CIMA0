import numpy as np

from core.snapshot import TemporalSnapshot


class ObserverSystem:
    """
    Observer is only a window.

    It samples the world.

    It does not:
        control
        optimize
        modify

    """

    def __init__(
        self,
        sample_size=64,
        history_size=8,
        threshold=0.5,
        decay=0.90,
        spread=0.15,
        exploration=0.1,
        window_size=32
    ):

        self.sample_size = sample_size
        self.history_size = history_size

        self.threshold = threshold
        self.decay = decay
        self.spread = spread
        self.exploration = exploration

        self.snapshot = TemporalSnapshot(
            window_size
        )


    def observe(self, cells, time):

        ids = np.random.choice(
            len(cells),
            size=min(
                self.sample_size,
                len(cells)
            ),
            replace=False
        )


        states = {}


        for cid in ids:

            s = cells[cid].state()

            states[cid] = {

                "x": s["x"],

                "v": s["v"],

                "omega": s["omega"]

            }


        self.snapshot.push(
            time,
            states
        )


        return self.summary()

    def sample(self, cells, time):
    
        ids = np.random.choice(
            len(cells),
            size=min(
                self.sample_size,
                len(cells)
            ),
            replace=False
        )

        states = {}

        for cid in ids:

            s = cells[cid].state()

            states[cid] = {
                "x": s["x"],
                "v": s["v"],
                "omega": s["omega"]
            }


        # 新增：只保存观察快照
        self.snapshot.push(
            time,
            states
        )

    def summary(self):

        frame = self.snapshot.latest()

        if frame is None:
            return {}


        states = list(
            frame["states"].values()
        )


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


        return {

            "time":
                frame["time"],


            "observed":
                len(states),


            "trajectory_depth":
                self.snapshot.size(),


            "x_mean":
                float(
                    xs.mean()
                ),


            "x_std":
                float(
                    xs.std()
                ),


            "v_mean":
                float(
                    vs.mean()
                ),


            "v_std":
                float(
                    vs.std()
                )

        }