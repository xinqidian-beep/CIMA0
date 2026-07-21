import numpy as np

from organs.oscillator_organ import OscillatorOrgan


np.random.seed(42)



organ = OscillatorOrgan(
    "test",
    dim=16
)



TOTAL = 200000



print("=== BASELINE ===")


for i in range(50000):

    organ.step()



print(
    organ.snapshot()
)



# ==========================
# apply perturbation
# ==========================

print("\n=== PERTURBATION ===")


def perturb(
    organ,
    strength=0.05
):

    """
    Environment influence.

    Not command.

    Only changes velocity.

    """

    force = (
        np.random.randn(
            organ.dim
        )
        *
        strength
    )


    organ.velocity += force



perturb(
    organ,
    strength=0.05
)



print(
    "after perturb"
)

print(
    organ.snapshot()
)



# ==========================
# recovery / transition
# ==========================

print("\n=== AFTER ===")


for i in range(150000):


    organ.step()



    if i % 20000 == 0:

        print(
            i,
            organ.snapshot()
        )



print("\nFINAL")


print(
    organ.snapshot()
)