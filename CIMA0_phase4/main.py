from core.network import OscillatorNetwork
from scheduler import Scheduler


STEPS = 500000
REPORT = 10000


net = OscillatorNetwork(
    n=1000,
    avg_degree=6,
    coupling=0.12,
    field_strength=0.05
)


scheduler = Scheduler(
    n=1000,
    active_ratio=0.1
)



print(
    "=== CIMA0 Phase4 ==="
)


for step in range(STEPS):


    active = scheduler.select()


    net.step(
        active
    )


    if step % REPORT == 0:

        print(
            step,
            net.snapshot()
        )



print(
    "=== FINAL ==="
)


print(
    {
        "min_updates":
            int(
                scheduler.update_count.min()
            ),

        "max_updates":
            int(
                scheduler.update_count.max()
            ),

        "mean_updates":
            float(
                scheduler.update_count.mean()
            )
    }
)