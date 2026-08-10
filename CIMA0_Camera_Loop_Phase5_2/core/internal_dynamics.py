"""
CIMA0 Phase5_2

Internal Dynamics

Architecture:

    InternalDynamics
            |
            |
        local organs


    CloudField
            |
            |
          Cell


Rules belong to organs.

InternalDynamics does NOT know:

    camera
    planet
    image
    clip
    meaning
    semantic


Every organ only needs:

    receive(raw)
    step()
    snapshot()

"""


import numpy as np



# =========================================================
# Cell
# =========================================================

class Cell:
    """
    Minimal state slot.

    value:

        None
            empty slot

        float
            existing state


    age:

        existence duration


    activity:

        state change amount

    """


    def __init__(self):

        self.value = None

        self.age = 0

        self.activity = 0.0



    @property
    def empty(self):

        return self.value is None



    def occupy(
        self,
        value
    ):

        self.value = float(value)

        self.age = 0

        self.activity = abs(
            self.value
        )



    def release(self):

        self.value = None

        self.age = 0

        self.activity = 0.0



# =========================================================
# CloudField
# =========================================================


class CloudField:
    """
    Sparse internal state field.

    Own rules:

        collision()

        decay()

        propagation()

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



    # -----------------------------------------------------

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



        # field full
        # no overwrite



    # -----------------------------------------------------

    def collision(self):

        """
        Internal autonomous merge.

        Active state only.

        Empty slots ignored.

        """


        self.merge_events.clear()



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

                            "value": merged

                        }

                    )


                    return



    # -----------------------------------------------------

    def decay(
        self,
        rate=0.95,
        release_threshold=0.01
    ):

        """
        Natural state decay.

        """

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



    # -----------------------------------------------------

    def propagation(self):

        """
        Reserved.

        Future:

            local state influence.

        """

        pass



    # -----------------------------------------------------

    def step(self):

        """
        Local evolution.

        """

        self.collision()

        self.decay()

        self.propagation()



    # -----------------------------------------------------

    def snapshot(self):

        """

        Read only export.

        """

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





# =========================================================
# InternalDynamics
# =========================================================


class InternalDynamics:
    """
    Internal dynamics container.


    Only manages:

        registered local organs


    Does NOT know:

        planet
        clip
        camera
        image
        meaning


    Every organ only needs:

        receive(raw)

        step()

        snapshot()

    """



    def __init__(self):

        self.organs = {}

        self.last_snapshot = {}



    def register(
        self,
        name,
        organ
    ):

        self.organs[name] = organ



    def receive(
        self,
        raw
    ):
        """
        External byte stream.

        Broadcast only.

        No interpretation.

        """

        for organ in self.organs.values():


            organ.receive(
                raw
            )



    def step(
        self
    ):
        """
        Local evolution.

        Each organ owns
        its own rule.

        """

        for name, organ in self.organs.items():


            organ.step()



        self.last_snapshot = {


            name:

            organ.snapshot()


            for name, organ

            in self.organs.items()


        }



    def snapshot(
        self
    ):
        """
        Read only export.
        """

        return self.last_snapshot.copy()



    def output(
        self,
        name
    ):
        """
        Read one organ snapshot
        as external output source.

        No interpretation.
        """


        organ = self.organs.get(
            name
        )


        if organ is None:

            return None



        if hasattr(
            organ,
            "read"
        ):

            return organ.read()



        return None



    def output_display(
        self,
        name
    ):
        """
        Read one organ display output.

        """

        organ = self.organs.get(
            name
        )


        if organ is None:

            return None



        if hasattr(
            organ,
            "display_field"
        ):

            return organ.display_field()



        return None