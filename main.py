import numpy as np

class OscillatorOrgan:

    def __init__(
        self,
        name,
        dim=16
    ):

        self.name = name

        self.dim = dim

        self.state = np.random.normal(
            0,
            0.01,
            dim
        )

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


    def receive(self, field):

        pass


    def step(self):

        self.phase += self.frequency * 0.01

        internal = np.sin(self.phase)

        self.state += internal * 0.001

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

            "name": self.name,

            "mean": round(
                float(np.mean(self.state)),
                5
            ),

            "std": round(
                float(np.std(self.state)),
                5
            ),

            "phase_mean": round(
                float(np.mean(self.phase)),
                5
            ),

            "phase_std": round(
                float(np.std(self.phase)),
                5
            ),

            "activity": self.activity
        }


# ==========================
# 参数
# ==========================

NUM_ORGANS = 64

DIM = 16

TOTAL_STEPS = 10_000_000

SNAPSHOT_INTERVAL = 100_000


# ==========================
# 创建系统
# ==========================

organs = []

for i in range(NUM_ORGANS):

    organs.append(
        OscillatorOrgan(
            name=f"organ_{i}",
            dim=DIM
        )
    )



# ==========================
# 初始状态
# ==========================

print("INITIAL")

print(
    [
        o.snapshot()
        for o in organs[:8]
    ]
)



# ==========================
# 演化
# ==========================

for step in range(TOTAL_STEPS):


    # 当前场

    field = np.concatenate(
        [
            o.emit()
            for o in organs
        ]
    )


    # 每个organ接受场

    for o in organs:

        o.receive(field)



    # 内部演化

    for o in organs:

        o.step()



    # 观察窗口

    if step % SNAPSHOT_INTERVAL == 0:


        means = np.array(
            [
                np.mean(o.state)
                for o in organs
            ]
        )


        phases = np.array(
            [
                o.phase
                for o in organs
            ]
        )


        print(
            {
                "step": step,

                "organs":
                    NUM_ORGANS,

                "mean":
                    round(float(np.mean(means)),5),

                "organ_std":
                    round(float(np.std(means)),5),

                "phase_std":
                    round(float(np.std(phases)),5),

                "state_std":
                    round(
                        float(
                            np.mean(
                                [
                                    np.std(o.state)
                                    for o in organs
                                ]
                            )
                        ),
                       5
                    )
            }
        )



# ==========================
# 最终
# ==========================

print("FINAL")

for o in organs[:16]:

    print(
        o.snapshot()
    )