from core.network import OscillatorNetwork

from runtime.scheduler import Scheduler

from observer.statistics import snapshot

from observer.cluster_observer import ClusterObserver

from observer.lifecycle import Lifecycle



net=OscillatorNetwork(
    n=1000,
    degree=6,
    coupling=0.12
)


scheduler=Scheduler(
    n=1000,
    budget=100
)


cluster_observer=ClusterObserver(
    threshold=0.8
)


life=Lifecycle()



print(
    "=== CIMA0 Phase3 ==="
)



TOTAL_STEPS=500000



for step in range(TOTAL_STEPS):


    active=scheduler.tick()


    net.step(active)



    if step % 10000 == 0:


        state=snapshot(net)

        structure=cluster_observer.observe(net)


        result={
            **state,
            **structure
        }


        print(
            step,
            result
        )


        life.update(
            step,
            structure
        )



print("=== FINAL ===")

print(
    life.summary()
)