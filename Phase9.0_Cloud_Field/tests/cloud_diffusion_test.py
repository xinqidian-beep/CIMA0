import sys
import os
import numpy as np

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from core.cloud import CloudMatrix


print(
    "=== Cloud Diffusion Test ==="
)


cloud = CloudMatrix(
    size=100
)


# 单点云

cloud.deposit(
    50,
    1.0
)


print(
    "initial active:",
    cloud.active_count()
)



for t in range(200):

    cloud.diffuse(
        strength=0.2
    )

    cloud.decay(
        rate=0.98
    )


    if t % 20 == 0:

        active = cloud.active_count()

        values = [
            v
            for v in cloud.field
            if not np.isnan(v)
        ]


        print(
            {
                "time": t,
                "active": active,
                "max": max(values)
                if values
                else 0
            }
        )



print(
    "final active:",
    cloud.active_count()
)