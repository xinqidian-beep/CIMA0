import sys
import os

# 保证可以找到 core
sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from core.cloud import CloudMatrix


def main():

    print("=== Phase9.0 Zero Value Test ===")


    N = 16


    cloud = CloudMatrix(
        size=N
    )


    # -------------------------
    # Test 1:
    # NaN = no cloud
    # -------------------------

    cid = 3

    result = cloud.contact(cid)


    print(
        "NaN contact:",
        result
    )


    assert result is None


    print(
        "PASS: NaN means no signal"
    )



    # -------------------------
    # Test 2:
    # 0.0 = real cloud value
    # -------------------------

    cloud.field[cid] = 0.0


    result = cloud.contact(cid)


    print(
        "Zero contact:",
        result
    )


    assert result == 0.0


    print(
        "PASS: zero is real signal"
    )



    # -------------------------
    # Test 3:
    # negative value
    # -------------------------

    cloud.field[cid] = -0.5


    result = cloud.contact(cid)


    print(
        "Negative contact:",
        result
    )


    assert result == -0.5


    print(
        "PASS: negative value preserved"
    )



    # -------------------------
    # Test 4:
    # positive value
    # -------------------------

    cloud.field[cid] = 0.8


    result = cloud.contact(cid)


    print(
        "Positive contact:",
        result
    )


    assert result == 0.8


    print(
        "PASS: positive value preserved"
    )



    print(
        "\n=== ALL TESTS PASSED ==="
    )



if __name__ == "__main__":
    main()