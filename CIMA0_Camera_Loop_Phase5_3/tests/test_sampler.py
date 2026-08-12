import numpy as np
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from core.compute_system.sampling import Sampler


sampler = Sampler()


delta = np.array(
    [0.1, 0.8, 0.2, 0.5]
)


age = np.array(
    [10, 1, 20, 3]
)


activity = np.array(
    [0.2, 0.9, 0.1, 0.4]
)


index = sampler.select(
    delta,
    age,
    activity,
    budget=2
)


print(index)