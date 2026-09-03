import numpy as np

from .cell import Cell


class CloudField:
    """
    CIMA0 CloudField

    Responsibility:

        preserve an incoming internal state field
        and provide local state slots after collision.

    CloudField does NOT:

        - interpret CLIP
        - classify
        - select semantic features
        - know CPU / GPU
        - know scheduler policy
        - perform expensive neural computation

    Important:

        The incoming field is preserved in its original
        structure.

        Example:

            CLIP cloud
                (12, 50, 768)

        remains:

            (12, 50, 768)

        It is NOT converted to:

            float
            scalar mean
            layer mean
            token mean
    """

    def __init__(
        self,
        capacity=32
    ):

        self.cells = [
            Cell()
            for _ in range(capacity)
        ]

        #
        # complete incoming state field
        #

        self.field = None

        #
        # previous complete field
        #

        self.previous_field = None

        #
        # state change of complete field
        #

        self.delta = 0.0

        #
        # local collision events
        #

        self.merge_events = []

        self.response_events = []

        #
        # compute bookkeeping
        #

        self.last_allocation = {}

    # -------------------------------------------------

    def receive(
        self,
        value
    ):
        """
        Receive one complete internal state field.

        No reduction.

        No mean.

        No interpretation.

        The complete structure is preserved.
        """

        if value is None:

            return False

        try:

            field = np.asarray(
                value,
                dtype=np.float32
            )

        except Exception:

            return False

        if field.size == 0:

            return False

        #
        # preserve previous field
        #

        self.previous_field = (
            None
            if self.field is None
            else self.field.copy()
        )

        #
        # install complete new field
        #

        self.field = field.copy()

        #
        # calculate complete-field change
        #

        if self.previous_field is None:

            self.delta = float(
                np.mean(
                    np.abs(
                        self.field
                    )
                )
            )

        elif (
            self.previous_field.shape
            ==
            self.field.shape
        ):

            self.delta = float(
                np.mean(
                    np.abs(
                        self.field
                        -
                        self.previous_field
                    )
                )
            )

        else:

            #
            # structural change
            #

            self.delta = 1.0

        return True

    # -------------------------------------------------

    def has_field(
        self
    ):

        return self.field is not None

    # -------------------------------------------------

    def shape(
        self
    ):

        if self.field is None:

            return None

        return self.field.shape

    # -------------------------------------------------

    def activity(
        self
    ):

        return float(
            self.delta
        )

    # -------------------------------------------------

    def request_compute(
        self
    ):
        """
        Report local compute demand.

        CloudField reports state pressure only.

        It does not allocate compute.
        """

        if self.field is None:

            return {
                "cloud": {
                    "collision": 0.0,
                    "decay": 0.0
                }
            }

        occupied = sum(
            1
            for cell in self.cells
            if not cell.empty
        )

        return {
            "cloud": {

                #
                # complete field exists
                #

                "collision":
                    float(
                        self.delta
                    ),

                #
                # local occupied cells
                #

                "decay":
                    float(
                        occupied
                    )
            }
        }

    # -------------------------------------------------

    def execute_compute(
        self,
        allocation
    ):
        """
        Execute only the operations permitted
        by ComputeSystem.
        """

        if allocation is None:

            return

        cloud = allocation.get(
            "cloud",
            {}
        )

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

        self.last_allocation = dict(
            cloud
        )

        if collision_budget > 0:

            self.collision(
                limit=collision_budget
            )

        if decay_budget > 0:

            self.decay(
                limit=decay_budget
            )

    # -------------------------------------------------

    def collision(
        self,
        limit=1
    ):
        """
        Process local collision responses.

        This method does NOT compress the complete field.

        A collision implementation may later create
        local Cell states.

        For now, CloudField only clears the event buffer.

        The complete field remains untouched.
        """

        if limit <= 0:

            return

        self.merge_events.clear()

        self.response_events.clear()

        #
        # Important:
        #
        # Do NOT do:
        #
        #     float(np.mean(self.field))
        #
        # Do NOT create a Cell from the
        # complete CLIP cloud.
        #

        return

    # -------------------------------------------------

    def inject_local_response(
        self,
        value
    ):
        """
        Insert a collision-produced local response.

        This is the only path that creates a Cell.

        The caller has already determined that
        'value' represents a local response.
        """

        if value is None:

            return False

        #
        # Cell currently represents scalar local state.
        #

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
        # ignore empty / insignificant response
        #

        if abs(value) < 0.05:

            return False

        #
        # find empty slot
        #

        for cell in self.cells:

            if cell.empty:

                cell.occupy(
                    value
                )

                self.response_events.append(
                    {
                        "value": value
                    }
                )

                return True

        return False

    # -------------------------------------------------

    def decay(
        self,
        limit=1,
        rate=0.95,
        release_threshold=0.01
    ):
        """
        Natural decay of local Cell responses.

        The complete incoming field is NOT decayed here.

        CLIP's pre-evolved state remains intact.
        """

        if limit <= 0:

            return

        count = 0

        for cell in self.cells:

            if cell.empty:

                continue

            old = cell.value

            cell.value *= rate

            cell.age += 1

            cell.activity = abs(
                cell.value - old
            )

            if abs(
                cell.value
            ) < release_threshold:

                cell.release()

            count += 1

            if count >= limit:

                return

    # -------------------------------------------------

    def propagation(
        self
    ):
        """
        Reserved for future local influence.

        Must not alter the complete source field
        unless an explicit evolution rule is added.
        """

        pass

    # -------------------------------------------------

    def step(
        self
    ):
        """
        Autonomous local maintenance only.

        Important:

            This does NOT evolve the incoming
            CLIP state.

        CLIPField already provides a pre-evolved
        state block.

        CloudField only maintains local responses.
        """

        self.collision()

        self.decay()

        self.propagation()

    # -------------------------------------------------

    def snapshot(
        self
    ):
        """
        Read-only snapshot.
        """

        return {

            #
            # complete source field
            #

            "field":
                None
                if self.field is None
                else self.field.copy(),

            #
            # source field structure
            #

            "shape":
                None
                if self.field is None
                else self.field.shape,

            "dtype":
                None
                if self.field is None
                else str(
                    self.field.dtype
                ),

            #
            # whole-field activity
            #

            "delta":
                float(
                    self.delta
                ),

            #
            # local response cells
            #

            "cells": [

                {

                    "value":
                        cell.value,

                    "age":
                        cell.age,

                    "activity":
                        cell.activity

                }

                for cell in self.cells

            ],

            #
            # collision events
            #

            "merge_events":
                self.merge_events.copy(),

            "response_events":
                self.response_events.copy()

        }