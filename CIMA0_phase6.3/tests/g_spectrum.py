import numpy as np


data=np.load(
    "data/phase6_observation.npz"
)


g=data["g"]


g=g-np.mean(g)


fft=np.abs(
    np.fft.rfft(g)
)


freq=np.fft.rfftfreq(
    len(g),
    d=0.02*5
)


index=np.argmax(
    fft[1:]
)+1


print(
    "dominant frequency:",
    freq[index]
)


print(
    "amplitude:",
    fft[index]
)