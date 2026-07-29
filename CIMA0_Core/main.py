from core.planet import Planet
from core.input_field import InputField
from core.observer import Observer
from core.compute import ComputeSystem



def main():


    print(
        "=== CIMA0 minimal world ==="
    )


    planet = Planet(
        size=128
    )

    io = InputField()

    observer = Observer()

    compute = ComputeSystem()



    for step in range(100000):


        # 外部偶尔扰动

        if step % 100 == 0:

            disturbance = io.generate()

            planet.receive_disturbance(
                disturbance["position"],
                disturbance["value"]
            )


        # 动力演化

        planet.step()



        # 观察

        snapshot = planet.snapshot()


        signal = observer.scan(
            snapshot
        )


        budget = compute.allocate(
            signal
        )


        budget["center"] = signal["center"]


        local = observer.sample(
            snapshot,
            budget
        )



        if step % 1000 == 0:

            print(
                {
                    "step":step,
                    "activity":
                    signal["deviation"],
                    "center":
                    signal["center"],
                    "sample":
                    local.shape
                }
            )



if __name__=="__main__":

    main()