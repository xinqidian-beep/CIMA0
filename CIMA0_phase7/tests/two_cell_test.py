import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


from core.cell import Cell
from core.coupling import diffusive_coupling


a = Cell(
    x=1.0,
    v=0.0
)

b = Cell(
    x=0.3,
    v=0.7
)


steps = 200000


phase=[]


for i in range(steps):

    fa, fb = diffusive_coupling(
        a,
        b,
        strength=0.01
    )

    a.step(fa)
    b.step(fb)


    if i % 20000 == 0:

        dx = a.x-b.x

        print(
            i,
            {
                "a":a.state(),
                "b":b.state(),
                "distance":dx
            }
        )