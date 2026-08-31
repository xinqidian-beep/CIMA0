
from .cell import Cell


class CloudField:
    """
    CIMA0 Phase5_8

    Sparse transient internal state cloud.

    Responsibility:

        receive a local internal state
        maintain a small number of Cells
        expose local activity
        perform local collision
        perform natural decay
        preserve transient state

    CloudField does NOT:

        interpret external input
        decode bytes
        inspect images
        perform attention
        select important regions
        compress large fields
        know Planet
        know CLIP
        know scheduler
        know CPU / GPU
        allocate compute

    Important:

        CloudField capacity is only an upper bound.

        It is NOT the size of the represented world.

        Normally only a small number of Cells are occupied.
    """


    def __init__(
        self,
        capacity=32
    ):

        self.capacity = int(
            capacity
        )


        self.cells = [

            Cell()

            for _ in range(
                self.capacity
            )

        ]


        #
        # collision history
        #

        self.merge_events = []


    # -------------------------------------------------
    # receive
    # -------------------------------------------------

    def receive(
        self,
        value
    ):
        """
        Inject one already-determined local state.

        The caller is responsible for:

            attention
            change detection
            local correspondence
            state reconstruction

        CloudField does none of these.

        Existing occupied Cells are not overwritten.
        """

        if value is None:

            return False


        try:

            value = float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return False


        #
        # find one empty transient slot
        #

        for cell in self.cells:

            if cell.empty:

                cell.occupy(
                    value
                )

                return True


        #
        # cloud is temporarily full
        #

        return False


    # -------------------------------------------------
    # activity
    # -------------------------------------------------

    def activity(
        self
    ):
        """
        Return total local activity.

        Activity represents actual state change,
        not merely state magnitude.
        """

        total = 0.0


        for cell in self.cells:

            if cell.empty:

                continue


            total += abs(
                cell.activity
            )


        return float(
            total
        )


    # -------------------------------------------------
    # occupancy
    # -------------------------------------------------

    def occupancy(
        self
    ):
        """
        Fraction of occupied Cells.
        """

        if self.capacity <= 0:

            return 0.0


        count = 0


        for cell in self.cells:

            if not cell.empty:

                count += 1


        return (
            float(count)
            /
            float(self.capacity)
        )


    # -------------------------------------------------
    # request compute
    # -------------------------------------------------

    def request_compute(
        self
    ):
        """
        Report local compute demand.

        CloudField reports need only.

        It does not allocate resources.

        Collision demand is based on
        actual local change.

        Decay demand is based on
        active occupied state.
        """

        collision_activity = 0.0

        decay_activity = 0.0


        for cell in self.cells:

            if cell.empty:

                continue


            #
            # what changed?
            #

            collision_activity += abs(
                cell.activity
            )


            #
            # what is currently alive?
            #

            decay_activity += abs(
                cell.value
            )


        return {

            "cloud": {

                "collision":
                    collision_activity,

                "decay":
                    decay_activity

            }

        }


    # -------------------------------------------------
    # execute compute
    # -------------------------------------------------

    def execute_compute(
        self,
        allocation
    ):
        """
        Execute an already allocated compute budget.

        ComputeSystem decides the budget.

        CloudField only performs local operations.
        """

        if allocation is None:

            return


        if not isinstance(
            allocation,
            dict
        ):

            return


        cloud = allocation.get(
            "cloud",
            {}
        )


        if not isinstance(
            cloud,
            dict
        ):

            return


        collision_budget = int(

            cloud.get(
                "collision",
                0
            )

        )


        decay_budget = int(

            cloud.get(
                "decay",
                0
            )

        )


        #
        # execute only what was allocated
        #

        self.collision(
            limit=collision_budget
        )


        self.decay(
            limit=decay_budget
        )


    # -------------------------------------------------
    # collision
    # -------------------------------------------------

    def collision(
        self,
        limit=1
    ):
        """
        Local state collision.

        Current experimental rule:

            sufficiently similar scalar states
            may merge.

        This is a local dynamical rule.

        It is NOT:

            attention
            interpretation
            semantic matching
            global selection
        """

        if limit <= 0:

            return


        self.merge_events.clear()


        count = 0


        active = [

            cell

            for cell in self.cells

            if not cell.empty

        ]


        #
        # local pairwise collision
        #

        for i in range(
            len(active)
        ):

            for j in range(
                i + 1,
                len(active)
            ):

                a = active[i]

                b = active[j]


                if a.empty or b.empty:

                    continue


                #
                # current temporary rule
                #

                distance = abs(

                    a.value
                    -
                    b.value

                )


                if distance < 0.05:

                    merged = (

                        a.value
                        +
                        b.value

                    ) / 2.0


                    #
                    # preserve collision
                    # as a new local state
                    #

                    a.occupy(
                        merged
                    )


                    b.release()


                    self.merge_events.append({

                        "value":
                            merged,

                        "source":
                            "collision"

                    })


                    count += 1


                    if count >= limit:

                        return


    # -------------------------------------------------
    # decay
    # -------------------------------------------------

    def decay(
        self,
        limit=1,
        rate=0.95,
        release_threshold=0.01
    ):
        """
        Natural local state decay.

        Only the allocated number of Cells
        may be processed.
        """

        if limit <= 0:

            return


        count = 0


        for cell in self.cells:

            if cell.empty:

                continue


            old = cell.value


            #
            # natural decay
            #

            cell.value *= rate


            cell.age += 1


            #
            # actual local change
            #

            cell.delta = abs(

                cell.value
                -
                old

            )


            cell.activity = (
                cell.delta
            )


            #
            # state disappears naturally
            #

            if abs(
                cell.value
            ) < release_threshold:

                cell.release()


            count += 1


            if count >= limit:

                return


    # -------------------------------------------------
    # propagation
    # -------------------------------------------------

    def propagation(
        self
    ):
        """
        Reserved for future local influence.

        No propagation rule is currently assumed.
        """

        pass


    # -------------------------------------------------
    # step
    # -------------------------------------------------

    def step(
        self
    ):
        """
        CloudField itself does not consume compute
        autonomously.

        Evolution is performed through:

            request_compute()
                    |
                    v
              ComputeSystem
                    |
                    v
            execute_compute()

        This method is intentionally inert.
        """

        pass


    # -------------------------------------------------
    # snapshot
    # -------------------------------------------------

    def snapshot(
        self
    ):
        """
        Read-only snapshot of the transient cloud.
        """

        return {

            "capacity":
                self.capacity,

            "occupancy":
                self.occupancy(),

            "activity":
                self.activity(),

            "cells": [

                {

                    "value":
                        cell.value,

                    "previous":
                        cell.previous,

                    "delta":
                        cell.delta,

                    "age":
                        cell.age,

                    "activity":
                        cell.activity

                }

                for cell in self.cells

            ],

            "merge_events":
                self.merge_events.copy()

        }
