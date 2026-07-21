from core.network import OscillatorNetwork
from runtime.scheduler import Scheduler
from observer.statistics import snapshot



net=OscillatorNetwork(
    n=1000,
    degree=6,
    coupling=0.12
)


scheduler=Scheduler(
    n=1000,
    budget=100
)



print("=== CIMA0 Phase2 ===")


for step in range(200000):


    active=scheduler.tick()


    net.step(active)


    if step%10000==0:

        print(
            step,
            snapshot(net)
        )