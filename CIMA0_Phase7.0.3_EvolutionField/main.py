import time

from core.universe import Universe
from environment.cloud import CloudField
from observer.observer import Observer



def main():


    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    u=Universe(
        n=4096,
        avg_neighbors=4,
        omega_min=0.95,
        omega_max=1.05,
        seed=42
    )


    cloud=CloudField(
        4096
    )


    observer=Observer(
        64
    )


    start=time.time()



    for report in range(100):


        u.step(
            1_000_000
        )


        # 单向信息流
        energy=[
            c.energy()
            for c in u.cells
        ]


        for i,e in enumerate(energy):

            cloud.receive(
                i,
                e*0.000001
            )


        cloud.evolve()


        observer.perceive(
            cloud
        )

        observer.step()



        print(
            u.snapshot(),
            observer.snapshot()
        )



    print(
        "runtime:",
        time.time()-start
    )



if __name__=="__main__":
    main()
