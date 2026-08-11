import numpy as np

from .cell import Cell


class CloudField:
    """
    Sparse internal cloud organ.

    Owns:

        collision()
        decay()
        propagation()

    Does NOT know:

        scheduler
        cpu
        gpu
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

        self.scan_cursor = 0



    # -------------------------------------------------

    def receive(
        self,
        raw
    ):
        """
        Inject external packet.

        No semantic interpretation.
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
        Report computation demand.
        """

        collision_need = 0.0

        decay_need = 0.0


        for cell in self.cells:

            if cell.empty:

                continue


            collision_need += abs(
                cell.value
            )


            decay_need += cell.activity



        return {

            "cloud":

            {

                "collision":
                    collision_need,

                "decay":
                    decay_need

            }

        }



    # -------------------------------------------------

    def execute_compute(
        self,
        allocation
    ):
        """
        Execute allocated budget.

        ComputeSystem decides.
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
            collision_budget
        )


        self.decay(
            decay_budget
        )



    # -------------------------------------------------

    def collision(
        self,
        limit=1
    ):
        """
        Local merge event.
        """

        if limit <= 0:

            return


        self.merge_events.clear()


        active = [

            c

            for c in self.cells

            if not c.empty

        ]


        count = 0


        start = self.scan_cursor

        size = len(active)


        for offset in range(size):

            i = (
                start + offset
            ) % size


            for j in range(
                i + 1,
                size
            ):


                a = active[i]

                b = active[j]


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

                        self.scan_cursor = (

                            i + 1

                        ) % max(
                            size,
                            1
                        )

                        return



        self.scan_cursor = (

            self.scan_cursor + 1

        ) % max(
            size,
            1
        )



    # -------------------------------------------------

    def decay(
        self,
        limit=1,
        rate=0.95,
        release_threshold=0.01
    ):
        """
        Natural decay.

        Uses rotating scan.
        """

        if limit <= 0:

            return


        count = 0

        size = len(
            self.cells
        )


        for offset in range(size):

            index = (

                self.scan_cursor +

                offset

            ) % size


            cell = self.cells[index]


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

                self.scan_cursor = (

                    index + 1

                ) % size

                return



    # -------------------------------------------------

    def propagation(
        self
    ):
        """
        Reserved local influence rule.
        """

        pass



    # -------------------------------------------------

    def step(
        self
    ):
        """
        Passive organ tick.

        No compute execution here.

        ComputeSystem drives:
            collision()
            decay()
        """

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
                        cell.value,

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