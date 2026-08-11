"""
CIMA0 Phase5_2

ComputeSystem allocation test


Verify:

    request tree

          |

    ComputeSystem

          |

    allocation tree


No:
    cloud
    camera
    clip
    meaning

"""


import sys
import os


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)



from core.compute_system import ComputeSystem





def sum_tree(
    value
):

    if isinstance(
        value,
        dict
    ):

        total = 0.0

        for v in value.values():

            total += sum_tree(v)

        return total



    if isinstance(
        value,
        (int,float)
    ):

        return float(value)


    return 0.0





def print_tree(
    value,
    prefix=""
):

    if isinstance(
        value,
        dict
    ):

        for k,v in value.items():

            print(
                prefix,
                k
            )

            print_tree(
                v,
                prefix + "  "
            )


    else:

        print(
            prefix,
            value
        )





def test_basic_allocation():


    print()

    print(
        "TEST 1 : basic allocation"
    )


    compute = ComputeSystem(
        capacity=100
    )


    requests = {

        "cloud":

        {

            "cell0":50,

            "cell1":50

        },


        "display":100

    }



    result = compute.allocate(
        requests
    )


    print()

    print(
        "allocation:"
    )

    print_tree(
        result
    )


    total = sum_tree(
        result
    )


    print(
        "total:",
        total
    )


    assert total <= 100.0001



    print(
        "PASS"
    )





def test_weight_ratio():


    print()

    print(
        "TEST 2 : weighted ratio"
    )


    compute = ComputeSystem(
        capacity=100
    )


    requests = {

        "A":20,

        "B":80

    }


    result = compute.allocate(
        requests
    )


    print_tree(
        result
    )


    assert abs(
        result["A"] - 20
    ) < 0.001


    assert abs(
        result["B"] - 80
    ) < 0.001


    print(
        "PASS"
    )





def test_nested_allocation():


    print()

    print(
        "TEST 3 : nested tree"
    )


    compute = ComputeSystem(
        capacity=200
    )


    requests = {


        "internal":

        {

            "cloud":100,

            "dynamics":100

        },


        "io":200

    }



    result = compute.allocate(
        requests
    )


    print_tree(
        result
    )



    total = sum_tree(
        result
    )


    print(
        "total:",
        total
    )


    assert total <= 200.0001



    print(
        "PASS"
    )





def test_empty_request():


    print()

    print(
        "TEST 4 : empty request"
    )


    compute = ComputeSystem(
        capacity=100
    )


    result = compute.allocate(
        {}
    )


    print(
        result
    )


    assert result == {}



    print(
        "PASS"
    )





def main():


    print(
"""
============================================================
CIMA0 Phase5_2 ComputeSystem Allocation Test

============================================================
"""
    )


    test_basic_allocation()

    test_weight_ratio()

    test_nested_allocation()

    test_empty_request()



    print()

    print(
        "ALL TESTS PASSED"
    )





if __name__ == "__main__":

    main()