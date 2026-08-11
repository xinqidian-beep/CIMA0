import numpy as np

from .cell import Cell


class CloudField:
    """
    Sparse autonomous cloud field.

    Input:

        byte packet

    Output:

        internal cloud state


    Does NOT know:

        camera
        image
        semantic
        display
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

        if raw is None:
            return


        #
        # packet decode
        #
        if isinstance(raw, dict):

            try:

                data = np.frombuffer(
                    raw["bytes"],
                    dtype=np.dtype(
                        raw["dtype"]
                    )
                ).astype(
                    np.float32
                )

            except Exception:

               return

 
        elif isinstance(raw, np.ndarray):

            data = raw.astype(
                np.float32
            )

        else:

            return



        #
        # invalid protection
        #
        data = data.reshape(
            -1
        )


        if data.size == 0:
            return



        #
        # normalize only numerical safety
        #
        data = np.nan_to_num(
            data,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )



        #
        # IMPORTANT:
        #
        # 不再逐 byte 注入
        #
        # 保留空间片段
        #

        fragments = np.array_split(
            data,
            len(self.cells)
        )



        for fragment in fragments:


            if fragment.size == 0:
                continue



            self._inject_fragment(
                fragment
            )
    # -------------------------------------------------  

    def _inject_fragment(
        self,
        fragment 
    ):


        value = float(
            np.mean(
                fragment
            )
        )


        target = self._select_cell(
            value
        )


        if target is not None:

            target.occupy(
                value
            ) 

    
    # -------------------------------------------------            
    def _select_cell(
        self,
        value
    ):
        
        if not np.isfinite(value):

            return None


        best = None

        best_score = -1



        for cell in self.cells:


            #
            # empty cell
            #

            if cell.empty:

                score = 1.0


            else:
                
                if not np.isfinite(
                    cell.value
                ):

                    continue



                distance = abs(
                    float(cell.value)
                    -
                    float(value)
                )


                similarity = 1.0 / (
                    1.0 + distance
                )


                freshness = 1.0 / (
                    1 + cell.age
                )


                
                score = (
                    similarity
                    +
                    freshness
                    +
                    cell.activity
                )



            if score > best_score:

                best_score = score

                best = cell



        return best    



    # -------------------------------------------------

    def _extract_fragments(
        self,
        packet
    ):
        """
        Convert byte stream into anonymous fragments.

        No semantic decoding.

        No image resize.

        """

        try:

            raw = np.frombuffer(

                packet["bytes"],

                dtype=np.uint8

            )


        except Exception:

            return []



        if raw.size == 0:

            return []



        fragments = []


        #
        # anonymous byte fragments
        #
        # only preserve stream structure
        #

        fragment_size = max(

            32,

            raw.size //
            max(
                1,
                len(self.cells)
            )

        )



        for i in range(
            0,
            raw.size,
            fragment_size
        ):


            part = raw[

                i:i+fragment_size

            ]


            if part.size == 0:

                continue



            value = float(

                np.mean(
                    part.astype(
                        np.float32
                    )
                )

            )


            fragments.append(

                value

            )



        return fragments



    # -------------------------------------------------

    def _claim(
        self,
        incoming
    ):
        """
        Cell competition.

        No fixed mapping.

        """

        winner = None

        best_score = -1e9



        for cell in self.cells:


            score = self._claim_score(

                cell,

                incoming

            )


            if score > best_score:

                best_score = score

                winner = cell



        if winner is not None:

            winner.occupy(

                incoming

            )



    # -------------------------------------------------

    def _claim_score(
        self,
        cell,
        incoming
    ):
        """
        Three-state competition.

        value
        age
        activity

        """

        #
        # empty cell
        #

        if cell.empty:

            return 0.1



        similarity = 1.0 - min(

            1.0,

            abs(

                cell.value -
                incoming

            )
            /
            255.0

        )



        freshness = 1.0 / (

            1.0 +
            cell.age

        )



        activity = min(

            1.0,

            cell.activity

            /
            255.0

        )



        return (

            similarity * 0.5

            +

            freshness * 0.3

            +

            activity * 0.2

        )



    # -------------------------------------------------

    def request_compute(
        self
    ):

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


        cloud = allocation.get(

            "cloud",

            {}

        )


        self.collision(

            int(
                cloud.get(
                    "collision",
                    0
                )
            )

        )


        self.decay(

            int(
                cloud.get(
                    "decay",
                    0
                )
            )

        )



    # -------------------------------------------------

    def collision(
        self,
        limit=1
    ):


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

                i+1,

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


                if distance < 5.0:


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
        release_threshold=0.5
    ):


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

        pass



    # -------------------------------------------------

    def step(
        self
    ):

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