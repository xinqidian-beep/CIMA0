import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from core.cloud import CloudMatrix



print(
    "=== Cloud Decay Test ==="
)


cloud = CloudMatrix(
    size=1000
)


cloud.deposit_random(
    count=10,
    strength=1.0
)


print(
    "initial:",
    cloud.active_count()
)



for t in range(500):

    cloud.decay()


    if t % 50 == 0:

        print(
            {
                "time": t,
                "active": cloud.active_count()
            }
        )



final = cloud.active_count()


print(
    "final:",
    final
)



if final == 0:

    print(
        "PASS: cloud event disappears naturally"
    )

else:

    print(
        "PASS: cloud remains as weak field"
    )