import numpy as np

from organs.oscillator_organ import OscillatorOrgan

# ==========================
# 参数
# ==========================

NUM_ORGANS = 64

DIM = 16

TOTAL_STEPS = 500_000
field = np.random.normal(0,1,512)
SNAPSHOT_INTERVAL = 20_000


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