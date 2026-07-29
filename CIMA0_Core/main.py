import numpy as np

from core.planet import PlanetEngine
from core.cloud import Cloud
from core.observer import Observer
from core.compute import ComputeSystem
from core.interface import ByteInterface



def bytes_to_disturbance(
    data,
    size
):
    """
    IO bytes -> cloud disturbance

    No semantic decoding.

    Only numerical mapping.
    """

    values = np.frombuffer(
        data,
        dtype=np.uint8
    )


    if len(values) == 0:

        return np.zeros(
            (
                size,
                size
            )
        )


    values = values.astype(
        float
    )


    values = (
        values
        -
        128.0
    ) / 128.0


    disturbance = np.zeros(
        (
            size,
            size
        )
    )


    count = min(
        values.size,
        size * size
    )


    disturbance.flat[:count] = (
        values[:count]
    )


    return disturbance




def main():

    print(
        "=== CIMA0 minimal core ==="
    )


    # IO

    io = ByteInterface()



    # Cloud

    cloud_size = 16

    cloud = Cloud(
        cloud_size,
        cloud_size
    )



    # Primitive dynamic

    planet = PlanetEngine(
        x=1.0,
        v=0.0,
        omega=1.0,
        dt=0.01
    )



    # Observer

    observer = Observer()



    # Compute

    compute = ComputeSystem()



    # simulate external byte input

    io.push(
        b"CIMA0"
    )



    for step in range(100000):


        # -----------------
        # IO
        # -----------------

        raw = io.read()



        disturbance = bytes_to_disturbance(
            raw,
            cloud_size
        )


        # -----------------
        # Cloud
        # -----------------

        cloud.receive(
            disturbance
        )


        cloud.evolve()



        # -----------------
        # Planet
        # -----------------

        local_force = np.mean(
            cloud.matrix
        )


        planet.step(
            external_force=local_force
        )



        # -----------------
        # Observer
        # -----------------

        signal = abs(
            planet.x
        )


        observation = observer.observe(
            signal
        )


        # -----------------
        # Compute
        # -----------------

        steps = compute.allocate(
            observation["raised"]
        )


        result = compute.compute(
            signal,
            steps
        )


        if step % 100 == 0:

            print(
                {
                    "step": step,

                    "raised":
                        observation["raised"],

                    "activity":
                        signal,

                    "baseline":
                        observation["baseline"],

                    "compute_steps":
                        steps,

                    "result":
                        result
                }
            )



if __name__ == "__main__":

    main()