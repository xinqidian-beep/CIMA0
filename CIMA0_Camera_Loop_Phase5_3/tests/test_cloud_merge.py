"""
CIMA0 Phase5_2

CloudField merge test

Verify:

    empty slot
        |
        v
    receive

        |
        v

    collision

        |
        v

    merge event

        |
        v

    release slot

"""


import sys
import os


# allow import from project root

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)



from core.internal_dynamics import CloudField





def print_cells(
    cloud,
    title
):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


    for i, cell in enumerate(
        cloud.cells
    ):

        print(
            i,
            "value=",
            cell.value,
            "age=",
            cell.age,
            "activity=",
            cell.activity
        )





def test_receive():

    print()

    print(
        "TEST 1 : receive into empty slots"
    )


    cloud = CloudField(
        capacity=4
    )


    cloud.cells[0].occupy(
        0.40
    )


    cloud.cells[1].occupy(
        0.45
    )


    print_cells(
        cloud,
        "Before collision"
    )


    assert cloud.cells[0].value == 0.40

    assert cloud.cells[1].value == 0.45



    print(
        "PASS"
    )





def test_collision_merge():

    print()

    print(
        "TEST 2 : autonomous merge"
    )


    cloud = CloudField(
        capacity=4
    )


    cloud.cells[0].occupy(
        0.40
    )


    cloud.cells[1].occupy(
        0.45
    )


    print_cells(
        cloud,
        "Before step"
    )


    cloud.collision()



    print_cells(
        cloud,
        "After collision"
    )


    print(
        "merge_events:",
        cloud.merge_events
    )


    assert len(
        cloud.merge_events
    ) == 1



    values = [

        c.value

        for c in cloud.cells

        if not c.empty

    ]


    assert len(values) == 1



    assert abs(
        values[0] - 0.425
    ) < 0.0001



    print(
        "PASS"
    )





def test_decay_release():

    print()

    print(
        "TEST 3 : decay release"
    )


    cloud = CloudField(
        capacity=2
    )


    cloud.cells[0].occupy(
        0.02
    )


    print_cells(
        cloud,
        "Before decay"
    )


    cloud.decay(
        rate=0.1,
        release_threshold=0.01
    )


    print_cells(
        cloud,
        "After decay"
    )


    assert cloud.cells[0].empty



    print(
        "PASS"
    )





def test_reuse_empty_slot():

    print()

    print(
        "TEST 4 : empty slot reuse"
    )


    cloud = CloudField(
        capacity=2
    )


    cloud.cells[0].occupy(
        0.5
    )


    cloud.cells[0].release()



    assert cloud.cells[0].value is None



    cloud.receive(
        [0.8]
    )


    print_cells(
        cloud,
        "After reuse"
    )



    values = [

        c.value

        for c in cloud.cells

        if not c.empty

    ]


    assert len(values) == 1



    print(
        "PASS"
    )





def main():


    print(
        """
============================================================
CIMA0 Phase5_2 CloudField Merge Test

ESC not required

============================================================
"""
    )


    test_receive()

    test_collision_merge()

    test_decay_release()

    test_reuse_empty_slot()



    print()

    print(
        "ALL TESTS PASSED"
    )





if __name__ == "__main__":

    main()