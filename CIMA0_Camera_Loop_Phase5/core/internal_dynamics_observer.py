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

        previous
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

        self.previous = {}

        self.cache = {}

        self.age = {}



    # ---------------------------------------------------------
    # request estimation
    # ---------------------------------------------------------

    def observe(self, snapshot):

        requests = {}
        
        if snapshot is None:
            return requests

        for key, value in snapshot.items():

            requests[key] = self._activity(
                key,
                value
            )

        return requests



    def _activity(self, path, value):
        
        if value is None:
            return 0.0

        if isinstance(value, dict):

            total = 0.0

            count = 0

            for k, v in value.items():

                total += self._activity(
                    f"{path}.{k}",
                    v
                )

                count += 1

            if count:

                return min(
                    1.0,
                    total / count
                )

            return 0.0



        if isinstance(value, np.ndarray):

            flat = value.reshape(-1).astype(
                np.float32
            )


            old = self.previous.get(
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


            self.previous[path] = flat.copy()


            return min(
                1.0,
                delta
            )



        if isinstance(value, (int, float)):

            old = self.previous.get(
                path,
                value
            )


            delta = abs(
                float(value) -
                float(old)
            )


            self.previous[path] = value


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



        #
        # initialize cache
        #

        if path not in self.cache:


            self.cache[path] = flat.copy()

            self.age[path] = np.zeros(
                size,
                dtype=np.int32
            )


            return self.cache[path].reshape(
                array.shape
            )



        #
        # previous comparison
        #

        old = self.previous.get(
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



        self.previous[path] = flat.copy()



        #
        # aging
        #

        self.age[path] += 1



        #
        # competition score
        #

        score = (
            delta +
            self.age[path].astype(
                np.float32
            ) * 0.01
        )



        #
        # compute budget decides precision count
        #

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



        #
        # focus selection
        #

        if count >= size:

            index = np.arange(
                size
            )

        else:

            index = np.argpartition(
                score,
                -count
            )[-count:]



        #
        # local precision update
        #

        self.cache[path][index] = flat[index]

        self.age[path][index] = 0



        #
        # return same shape
        #

        return self.cache[path].reshape(
            array.shape
        )