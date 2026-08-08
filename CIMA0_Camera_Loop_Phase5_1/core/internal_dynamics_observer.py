import numpy as np


class InternalDynamicsObserver:
    """
    Read only observer.

    Responsibility:

        snapshot
            |
            v
        local competitive read
            |
            v
        cached same-structure output


    Own state only:

        observe_previous
        read_previous
        cache
        age


    No:

        modify source state
        understand planet
        understand clip
        allocate resource
        control modules

    """


    def __init__(self):

        self.observe_previous = {}

        self.read_previous = {}

        self.cache = {}

        self.age = {}



    # ---------------------------------------------------------
    # request estimation
    # ---------------------------------------------------------

    def observe(
        self,
        snapshot
    ):

        requests = {}

        if snapshot is None:
            return requests


        for key, value in snapshot.items():

            requests[key] = self._activity(
                key,
                value
            )


        return requests



    def _activity(
        self,
        path,
        value
    ):

        if value is None:
            return 0.0


        if isinstance(value, dict):

            result = {}


            for k, v in value.items():

                result[k] = self._activity(
                    f"{path}.{k}",
                    v
                )
                           

            return result



        if isinstance(value, np.ndarray):

            flat = value.reshape(-1).astype(
                np.float32
            )


            old = self.observe_previous.get(
                path
            )


            if old is None:

                delta = 1.0

            else:

                delta = float(
                    np.mean(
                        np.abs(
                            flat - old
                        )
                    )
                )


            self.observe_previous[path] = flat.copy()


            return min(
                1.0,
                delta
            )



        if isinstance(value, (int, float)):

            old = self.observe_previous.get(
                path,
                value
            )


            delta = abs(
                float(value) -
                float(old)
            )


            self.observe_previous[path] = value


            return min(
                1.0,
                delta
            )


        return 0.0



    # ---------------------------------------------------------
    # budget controlled read
    # ---------------------------------------------------------

    def read(
        self,
        snapshot,
        allocation
    ):

        result = {}


        for key, value in snapshot.items():

            budget = allocation.get(
                key,
                0
            )


            result[key] = self._read(
                key,
                value,
                budget
            )


        return result



    def _read(
        self,
        path,
        value,
        budget
    ):


        if isinstance(value, dict):

            result = {}

            count = max(
                1,
                len(value)
            )


            child_budget = (
                budget / count
            )


            for k, v in value.items():

                result[k] = self._read(
                    f"{path}.{k}",
                    v,
                    child_budget
                )


            return result



        if isinstance(value, np.ndarray):

            return self._read_array(
                path,
                value,
                budget
            )


        if isinstance(value, (int, float)):

            return value


        return value



    # ---------------------------------------------------------
    # local sparse focus read
    # ---------------------------------------------------------

    def _read_array(
        self,
        path,
        array,
        budget
    ):

        flat = array.reshape(-1).astype(
            np.float32
        )


        size = flat.size



        if path not in self.cache:

            self.cache[path] = flat.copy()

            self.age[path] = np.zeros(
                size,
                dtype=np.int32
            )


            self.read_previous[path] = flat.copy()


            return self.cache[path].reshape(
                array.shape
            )



        old = self.read_previous.get(
            path
        )


        if old is None:

            delta = np.ones(
                size,
                dtype=np.float32
            )

        else:

            delta = np.abs(
                flat - old
            )



        self.read_previous[path] = flat.copy()



        self.age[path] += 1



        score = (
            delta +
            self.age[path].astype(
                np.float32
            ) * 0.01
        )



        count = int(
            budget
        )


        count = max(
            1,
            min(
                size,
                count
            )
        )



        if count >= size:

            index = np.arange(
                size
            )

        else:

            index = np.argpartition(
                score,
                -count
            )[-count:]



        self.cache[path][index] = flat[index]

        self.age[path][index] = 0



        return self.cache[path].reshape(
            array.shape
        )