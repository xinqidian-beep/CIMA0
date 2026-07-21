import numpy as np

from organs.oscillator_organ import OscillatorOrgan
from scheduler.compute_scheduler import ComputeField


np.random.seed(42)


NUM_ORGANS = 64
DIM = 16

TOTAL_STEPS = 500000
SNAPSHOT_INTERVAL = 20000



# ==========================
# create organisms
# ==========================

organs = [
    OscillatorOrgan(
        f"organ_{i}",
        DIM
    )
    for i in range(NUM_ORGANS)
]



# ==========================
# environment resource field
# ==========================

field = ComputeField(
    organs,
    capacity=8
)



print("INITIAL")

for o in organs[:8]:
    print(o.snapshot())



history = {
    i:0
    for i in range(NUM_ORGANS)
}



# ==========================
# runtime
# ==========================

for step in range(TOTAL_STEPS):


    active = field.step()


    for idx in active:

        organs[idx].step()

        history[idx]+=1



    if step % SNAPSHOT_INTERVAL == 0:


        usage=np.array(
            [
                history[i]
                for i in range(NUM_ORGANS)
            ]
        )


        print(
            {
                "step":step,

                "usage_max_mean":
                    round(
                        float(
                            usage.max()
                            /
                            (usage.mean()+1e-9)
                        ),
                        3
                    ),

                "top":
                    sorted(
                        history.items(),
                        key=lambda x:x[1],
                        reverse=True
                    )[:5]
            }
        )



print("FINAL")


for o in organs[:16]:
    print(o.snapshot())