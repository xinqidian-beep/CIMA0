import numpy as np


def local_update(cell, neighbors):

    """
    CIMA-0 三公理：

    只有局部状态变化

    """

    coupling = 0.05

    influence = 0


    for n in neighbors:

        influence += np.sin(
            n.phase-cell.phase
        )


    cell.phase += (
        cell.frequency
        +
        coupling * influence
    ) * 0.02


    cell.energy += (
        np.random.randn()
        *0.005
    )


    # 自然限制
    cell.energy *= 0.999


    if cell.energy < 0:
        cell.energy = 0