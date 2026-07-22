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


SAMPLE_EVERY = 5



osc = Oscillator(
    x=1.0,
    v=0.0,

    omega=1.0,
    mu=0.6,

    dt=0.02,

    g=0.0,
    tau_g=50.0,
    alpha_g=0.15
)



x=[]
v=[]
g=[]
energy=[]


for step in range(STEPS):

    osc.step()


    if step % SAMPLE_EVERY == 0:

        x.append(osc.x)
        v.append(osc.v)
        g.append(osc.g)
        energy.append(osc.energy)



x=np.array(x)
v=np.array(v)
g=np.array(g)
energy=np.array(energy)



print("=== Phase6 Observation ===")


print(
    "samples:",
    len(x)
)


print(
    "x range:",
    x.min(),
    x.max()
)


print(
    "v range:",
    v.min(),
    v.max()
)


print(
    "energy:",
    energy.min(),
    energy.max()
)


print(
    "g mean:",
    g.mean()
)


print(
    "g std:",
    g.std()
)


np.savez(
    "data/phase6_observation.npz",

    x=x,
    v=v,
    g=g,
    energy=energy
)


print(
    "saved data/phase6_observation.npz"
)