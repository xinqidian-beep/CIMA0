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

        self.collision_cursor = 0

    # -------------------------------------------------

    def receive(
        self,
        raw
    ):
        """
        Inject external packet.
        
        Accept:

            {
                bytes,
                shape,
                dtype
            }

        Convert:

            image field
                |
                v
            spatial samples
                |
                v
            cells

        No semantic interpretation.
        """

        if raw is None:

            return
            
        #
        # packet decode
        #

        if isinstance(
            raw,
            dict
        ):


            try:
                
                data = np.frombuffer(
                    raw["bytes"],
                    dtype=np.dtype(
                        raw["dtype"]
                    )
                )

                data = data.reshape(
                    raw["shape"]
                )


            except (
                KeyError,
                ValueError,
                TypeError
            ):
                
                raise RuntimeError(
                    "CloudField.receive(): invalid packet"
                )


        elif isinstance(
            raw,
            np.ndarray
        ):

            data = raw


        else:

            raise TypeError(
                "CloudField.receive(): unsupported input type"
            )
            
            
        #
        # spatial sampling
        #
        # keep spatial distribution
        #

        values = self._spatial_sample(
            data
        )



        #
        # inject cells
        #

        for value in values:

            if abs(value) < 0.05:

                continue



        for cell in self.cells:

            if cell.empty:

                cell.occupy(
                    value
                )

                break
                
    # -------------------------------------------------
    
    def _spatial_sample(
        self,
        data,
        grid=8
    ):
        """
        Uniform spatial sampling.

        No recognition.

        Only preserve spatial distribution.
        """

        if data.ndim == 3:

            #
            # BGR/RGB
            # keep luminance only
            #

            data = np.mean(
                data,
                axis=2
            )



        h,w = data.shape



        values = []



        step_y = max(
            1,
            h // grid
        )

        step_x = max(
            1,
            w // grid
        )



        for y in range(
            0,
            h,
            step_y
        ):


            for x in range(
                0,
                w,
                step_x
            ):


                block = data[
                    y:y+step_y,
                    x:x+step_x
                ]


                if block.size == 0:

                    continue



                value = float(
                    np.mean(block)
                )



                values.append(
                    value / 255.0
                )



        return values


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

        if limit <= 0:

            return


        self.merge_events.clear()


        active = [

            c

            for c in self.cells

            if not c.empty

        ]


        size = len(active)


        if size < 2:

            return


        count = 0


        start = (

            self.collision_cursor

            % size

        )


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


                # 防御检查

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


                        self.collision_cursor = (

                            i + 1

                        ) % size


                        return



        self.collision_cursor = (

            self.collision_cursor + 1

        ) % size



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