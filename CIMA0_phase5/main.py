from core.network import OscillatorNetwork
from core.scheduler import Scheduler
from core.disturbance import CloudPerturbation
from observer import Observer



print("=== CIMA0 Phase5 ===")


network = OscillatorNetwork(
    n=1000
)


scheduler = Scheduler(
    n=1000
)


cloud = CloudPerturbation(
    strength=0.05,
    probability=0.002
)


observer = Observer()



TOTAL_STEPS = 500000


for step in range(TOTAL_STEPS):


    active = scheduler.select()


    network.step(
        active
    )


    # 云扰动
    disturbance_events = cloud.apply(
        network
    )


    if step % 10000 == 0:

        data = observer.record(
            network,
            scheduler,
            step
        )


        data["cloud_events"] = (
            cloud.total_events
        )


        print(
            step,
            data
        )



print("=== FINAL ===")

print(
    {
        "cloud_events":
            cloud.total_events,

        "update_min":
            scheduler.update_count.min(),

        "update_max":
            scheduler.update_count.max(),

        "update_mean":
            scheduler.update_count.mean()
    }
)