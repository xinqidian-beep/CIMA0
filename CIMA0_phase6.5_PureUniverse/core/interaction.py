import numpy as np


def local_force(
    cell,
    neighbors
):

    force=np.zeros(3)


    for n in neighbors:

        delta=n.pos-cell.pos

        r=np.linalg.norm(delta)+1e-6


        force += (
            delta /
            (r*r*r)
        )


    return force