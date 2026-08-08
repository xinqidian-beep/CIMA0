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


        #
        # dictionary tree
        #

        if isinstance(value, dict):


            result = {}


            if isinstance(
                budget,
                dict
            ):

                for k, v in value.items():

                    child_budget = budget.get(
                        k,
                        0
                    )


                    result[k] = self._read(
                        f"{path}.{k}",
                        v,
                        child_budget
                    )


            else: 

                count = max(
                    1,
                    len(value)
                )


                child_budget = (
                    float(budget)
                    /
                    count
                )


                for k, v in value.items():

                    result[k] = self._read(
                        f"{path}.{k}",
                        v,
                        child_budget
                    )


            return result



        #
        # array leaf
        #

        if isinstance(
            value,
            np.ndarray
        ):

            return self._read_array(
                path,
                value,
                budget
            )



        #
        # scalar
        #

        if isinstance(
            value,
            (int,float)
        ):

            return value



        import numpy as np


class InternalDynamicsObserver:
    """
    Read only observer.

    Responsibility:

        snapshot
            |
            v
        activity estimation
            |
            v
        budget read
            |
            v
        anonymous byte packet


    Own state:

        observe_previous
        read_previous
        cache
        age


    Does NOT know:

        camera
        clip
        image
        meaning
        display

    """



    def __init__(self):

        self.observe_previous = {}

        self.read_previous = {}

        self.cache = {}

        self.age = {}



    #
    # activity estimation
    #

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



        if isinstance(
            value,
            dict
        ):

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




        if isinstance(
            value,
            np.ndarray
        ):


            flat = value.reshape(
                -1
            ).astype(
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




        if isinstance(
            value,
            (int,float)
        ):


            old = self.observe_previous.get(
                path,
                value
            )


            delta = abs(
                float(value)
                -
                float(old)
            )


            self.observe_previous[path] = value


            return min(
                1.0,
                delta
            )



        return 0.0





    #
    # budget read
    #

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


        #
        # tree
        #

        if isinstance(
            value,
            dict
        ):


            result = {}



            if isinstance(
                budget,
                dict
            ):


                for k,v in value.items():

                    result[k] = self._read(
                        f"{path}.{k}",
                        v,
                        budget.get(
                            k,
                            0
                        )
                    )


            else:


                count = max(
                    1,
                    len(value)
                )


                child_budget = (
                    float(budget)
                    /
                    count
                )



                for k,v in value.items():

                    result[k] = self._read(
                        f"{path}.{k}",
                        v,
                        child_budget
                    )



            return result




        #
        # array
        #

        if isinstance(
            value,
            np.ndarray
        ):


            return self._read_array(
                path,
                value,
                budget
            )




        #
        # scalar
        #

        if isinstance(
            value,
            (int,float)
        ):

            return value



        return value





    #
    # sparse array read
    #

    def _read_array(
        self,
        path,
        array,
        budget
    ):


        flat = array.reshape(
            -1
        ).astype(
            np.float32
        )


        size = flat.size



        if path not in self.cache:


            self.cache[path] = flat.copy()


            self.read_previous[path] = flat.copy()


            self.age[path] = np.zeros(
                size,
                dtype=np.int32
            )


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
            delta
            +
            self.age[path].astype(
                np.float32
            )
            *
            0.01
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





    #
    # anonymous byte packet
    #

    def pack(
        self,
        data
    ):
        """
        Convert sampled internal state
        into byte stream.

        No semantic information.
        """

        array = self._find_array(
            data
        )


        if array is None:

            return None



        return {

            "bytes":
                array.astype(
                    np.float32
                ).tobytes(),


            "shape":
                array.shape,


            "dtype":
                "float32"

        }




    def _find_array(
        self,
        value
    ):


        if isinstance(
            value,
            np.ndarray
        ):

            return value



        if isinstance(
            value,
            dict
        ):


            for v in value.values():

                result = self._find_array(
                    v
                )


                if result is not None:

                    return result



        return None





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