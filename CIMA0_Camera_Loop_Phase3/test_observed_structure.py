import numpy as np

from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem

from archive.planet import Planet
from core.clip_region import ClipRegion


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



def inspect_structure(
    obj,
    path=""
):

    if isinstance(obj, dict):

        for key, value in obj.items():

            inspect_structure(
                value,
                path + "." + key
            )


    elif isinstance(obj, np.ndarray):

        print(
            path,
            "shape:",
            obj.shape,
            "dtype:",
            obj.dtype,
            "min:",
            float(np.min(obj)),
            "max:",
            float(np.max(obj))
        )



def main():

    print("=" * 60)
    print("CIMA0 Observed Structure Test")
    print("=" * 60)



    planet = Planet()


    clip = ClipRegion(
        CLIP_WEIGHT
    )


    internal = InternalDynamics(
        planet,
        clip
    )


    observer = InternalDynamicsObserver()


    compute = ComputeSystem(
        capacity=100
    )



    #
    # minimal evolution
    #

    for _ in range(5):

        internal.step()



    #
    # snapshot
    #

    snapshot = internal.snapshot()



    #
    # readonly observe
    #

    request = observer.observe(
        snapshot
    )


    allocation = compute.allocate(
        request
    )


    observed = observer.read(
        snapshot,
        allocation
    )



    print()
    print("Observed structure:")
    print()


    inspect_structure(
        observed,
        "root"
    )



if __name__ == "__main__":

    main()