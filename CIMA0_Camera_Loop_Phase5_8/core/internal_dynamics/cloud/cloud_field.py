import numpy as np

from .cell import Cell


class CloudField:
    """
    Sparse internal state field.

    Own rules:

        collision()
        decay()
        propagation()

    Does NOT know:

        cpu
        gpu
        scheduler
        external meaning
    """



    def __init__(
        self,
        capacity=32
    ):

        self.cells = [

            Cell()

            for _ in range(capacity)

        ]


        self.merge_events = []

        self.last_allocation = {}



    # -------------------------------------------------

    def receive(
        self,
        raw
    ):
        """
        Input injection.

        No interpretation.

        Find empty slot only.

        Existing state is not overwritten.
        """


        if raw is None:

            return



        try:

            value = float(
                np.mean(raw)
            )


        except Exception:

            return



        if abs(value) < 0.05:

            return



        for cell in self.cells:


            if cell.empty:


                cell.occupy(
                    value
                )

                return



    # -------------------------------------------------

    def request_compute(
        self
    ):
        """
        Report compute demand.

        CloudField only reports need.

        It does not know resource.
        """


        collision_activity = 0.0

        decay_activity = 0.0



        for cell in self.cells:


            if cell.empty:

                continue



            collision_activity += abs(
                cell.value
            )


            decay_activity += cell.activity



        return {


            "cloud":

            {


                "collision":

                collision_activity,


                "decay":

                decay_activity


            }

        }



    # -------------------------------------------------

    def execute_compute(
        self,
        allocation
    ):
        """
        Receive compute budget.

        ComputeSystem decides amount.

        CloudField only executes.
        """


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



        self.collision(
            limit=collision_budget
        )


        self.decay(
            limit=decay_budget
        )



    # -------------------------------------------------

    def collision(
        self,
        limit=1
    ):
        """
        Autonomous merge.

        Active state only.
        """


        if limit <= 0:

            return



        self.merge_events.clear()


        count = 0



        active = [

            c

            for c in self.cells

            if not c.empty

        ]



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



                distance = abs(

                    a.value -

                    b.value

                )



                if distance < 0.05:


                    merged = (

                        a.value +

                        b.value

                    ) / 2.0



                    a.occupy(
                        merged
                    )


                    b.release()



                    self.merge_events.append(

                        {

                            "value":

                            merged

                        }

                    )


                    count += 1



                    if count >= limit:

                        return



    # -------------------------------------------------

    def decay(
        self,
        limit=1,
        rate=0.95,
        release_threshold=0.01
    ):
        """
        Natural state decay.
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

                cell.value -

                old

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
        Reserved.

        Future local influence.
        """

        pass



    # -------------------------------------------------

    def step(
        self
    ):
        """
        Local evolution.

        Default autonomous step.
        """

        self.collision()

        self.decay()

        self.propagation()



    # -------------------------------------------------

    def snapshot(
        self
    ):

        return {


            "cells":

            [

                {

                    "value":
                    c.value,


                    "age":
                    c.age,


                    "activity":
                    c.activity

                }


                for c in self.cells

            ],


            "merge_events":

            self.merge_events.copy()

        }