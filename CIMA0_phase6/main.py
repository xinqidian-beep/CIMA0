from core.oscillator import Oscillator
import numpy as np
import time


STEPS = 500000


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


g_history = []

activity_history = []



print("=== CIMA0 Phase6.0 Slow Variable Test ===")


start=time.time()


for step in range(STEPS):

    osc.step()


    g_history.append(
        osc.g
    )

    activity_history.append(
        osc.activity
    )


    if step % 10000 == 0:

        print(
            step,
            osc.state()
        )



g_history=np.array(g_history)

activity_history=np.array(activity_history)



print("\n=== RESULT ===")

print(
    "steps:",
    STEPS
)

print(
    "runtime:",
    round(time.time()-start,3)
)


print(
    "g_mean:",
    float(np.mean(g_history))
)

print(
    "g_std:",
    float(np.std(g_history))
)

print(
    "g_min:",
    float(np.min(g_history))
)

print(
    "g_max:",
    float(np.max(g_history))
)


np.save(
    "phase6_g.npy",
    g_history
)

print(
    "saved phase6_g.npy"
)