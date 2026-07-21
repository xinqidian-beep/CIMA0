import numpy as np

from organs.oscillator_organ import OscillatorOrgan



np.random.seed(42)



organ = OscillatorOrgan(
    "test",
    dim=16
)



def perturb(
    organ,
    strength
):

    """
    Environment force.

    Does not overwrite state.

    """

    force = (
        np.random.randn(
            organ.dim
        )
        *
        strength
    )


    organ.velocity += force




def run(
    steps,
    label
):


    for i in range(steps):

        organ.step()


        if i % 20000 == 0:

            print(
                label,
                i,
                organ.snapshot()
            )



print("=== INITIAL STABILIZATION ===")


run(
    50000,
    "BASE"
)



print("\n=== SMALL PERTURBATION ===")


perturb(
    organ,
    0.02
)


run(
    80000,
    "SMALL"
)



print("\n=== MEDIUM PERTURBATION ===")


perturb(
    organ,
    0.05
)


run(
    80000,
    "MEDIUM"
)



print("\n=== LARGE PERTURBATION ===")


perturb(
    organ,
    0.1
)


run(
    80000,
    "LARGE"
)



print("\n=== FINAL ===")


print(
    organ.snapshot()
)