from core.field import FieldDynamics
import numpy as np



field = FieldDynamics(
    size=128
)


for step in range(100000):

    field.step()


    if step % 1000 == 0:

        state = field.snapshot()


        print(
            {
                "step":step,

                "max":
                float(
                    np.abs(state).max()
                ),

                "std":
                float(
                    state.std()
                ),

                "mean":
                float(
                    state.mean()
                )
            }
        )