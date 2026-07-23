import sys
import os
import numpy as np


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)


from core.oscillator import Oscillator



STEPS = 5000


def create_system(g):

    return Oscillator(
        x=1.0,
        v=0.0,

        omega=1.0,
        mu=0.6,
        dt=0.02,

        g=g,

        tau_g=50.0,
        alpha_g=0.15
    )



# ==========================
# two identical fast states
# ==========================

system_A = create_system(
    g=0.0
)


system_B = create_system(
    g=1.0
)



distance = []

energy_A = []
energy_B = []


for step in range(STEPS):


    system_A.step()

    system_B.step()



    dx = (
        system_A.x
        -
        system_B.x
    )

    dv = (
        system_A.v
        -
        system_B.v
    )


    d = np.sqrt(
        dx*dx
        +
        dv*dv
    )


    distance.append(d)


    energy_A.append(
        system_A.energy
    )

    energy_B.append(
        system_B.energy
    )



distance = np.array(distance)



print(
    "=== Phase6.1 Slow State Test ==="
)


print(
    "initial distance:",
    distance[0]
)


print(
    "final distance:",
    distance[-1]
)


print(
    "max distance:",
    np.max(distance)
)


print(
    "mean distance:",
    np.mean(distance)
)



print("\nEnergy difference:")


print(
    "final:",
    abs(
        energy_A[-1]
        -
        energy_B[-1]
    )
)


if np.max(distance) > 1e-3:

    print(
        "\nRESULT:"
    )

    print(
        "PASS - g changes future trajectory"
    )

else:

    print(
        "\nRESULT:"
    )

    print(
        "FAIL - g has no observable effect"
    )



np.save(
    "data/slow_state_distance.npy",
    distance
)


print(
    "\nsaved data/slow_state_distance.npy"
)