import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from core.cloud import CloudMatrix


def main():

    print(
        "=== Cloud Persistence Test ==="
    )


    cloud = CloudMatrix(
        size=10,
        decay=0.9,
        lifetime=5
    )


    cloud.field[3] = 1.0


    print(
        "initial:",
        cloud.contact(3)
    )


    for i in range(3):

        cloud.step()

        print(
            "step",
            i,
            cloud.contact(3)
        )


    for i in range(5):

        cloud.step()


    print(
        "after lifetime:",
        cloud.contact(3)
    )


    assert cloud.contact(3) is None


    print(
        "=== PASS ==="
    )



if __name__ == "__main__":
    main()