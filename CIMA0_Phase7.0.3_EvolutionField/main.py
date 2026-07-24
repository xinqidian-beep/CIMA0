from core.universe import Universe
from observer.observer import Observer
from compute.scheduler import ComputeScheduler
from environment.field import EvolutionField



def main():

    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    u=Universe()

    obs=Observer()

    compute=ComputeScheduler()

    field=EvolutionField(4096)



    for r in range(100):


        # 动力自己跑

        u.step(
            1_000_000
        )


        state=u.state_view()


        # observer 看

        target=obs.observe(
            state
        )


        # compute 分配

        region=compute.allocate(
            target
        )


        # 环境留下慢影响

        field.update(
            region,
            state
        )


        print(
            u.snapshot()
        )



if __name__=="__main__":
    main()