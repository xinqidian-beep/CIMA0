import numpy as np


class InternalDynamicsObserver:
    """
    CIMA0 Phase5_3

    Read only observer.


    Responsibility:

        snapshot
            |
            v
        activity estimation
            |
            v
        budget controlled read
            |
            v
        internal packet
            |
            v
        field byte packet for IO


    Own state only:

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

            result = {}


            for k,v in value.items():

                result[k] = self._activity(
                    f"{path}.{k}",
                    v
                )


            return result




        if isinstance(
            value,
            list
        ):

            result = {}


            for i,v in enumerate(value):

                result[str(i)] = self._activity(
                    f"{path}.{i}",
                    v
                )


            return result




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
                            flat-old
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


        if snapshot is None:

            return result



        for key,value in snapshot.items():

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


        if isinstance(
            value,
            dict
        ):

            result = {}


            for k,v in value.items():

                child_budget = 0


                if isinstance(
                    budget,
                    dict
                ):

                    child_budget = budget.get(
                        k,
                        0
                    )


                result[k] = self._read(
                    f"{path}.{k}",
                    v,
                    child_budget
                )


            return result




        if isinstance(
            value,
            list
        ):

            result = []


            for i,v in enumerate(value):

                result.append(

                    self._read(
                        f"{path}.{i}",
                        v,
                        budget
                    )

                )


            return result




        if isinstance(
            value,
            np.ndarray
        ):

            return self._read_array(
                path,
                value,
                budget
            )




        return value




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



        old = self.read_previous[path]


        delta = np.abs(
            flat-old
        )


        self.read_previous[path] = flat.copy()


        self.age[path] += 1



        score = (

            delta

            +

            self.age[path] * 0.01

        )



        count = max(
            1,
            min(
                size,
                int(budget)
            )
        )



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
    # internal packet
    #

    def pack(
        self,
        data
    ):

        if data is None:

            return None


        if isinstance(
            data,
            dict
        ):

            return {

                k:
                self.pack(v)

                for k,v in data.items()

            }


        if isinstance(
            data,
            list
        ):

            return [

                self.pack(v)

                for v in data

            ]


        return data



    #
    # convert internal state to IO byte packet
    #

    def encode_field(
        self,
        data,
        source="internal"
    ):


        values = []


        self._collect_values(
            data,
            values
        )


        if len(values) == 0:

            return None



        field = np.asarray(
            values,
            dtype=np.float32
        )


        return {

            "type":
                "field",


            "source":
                source,


            "bytes":
                field.tobytes(),


            "shape":
                field.shape,


            "dtype":
                str(field.dtype)

        }




    def _collect_values(
        self,
        value,
        result
    ):

        if isinstance(
            value,
            dict
        ):


            #
            # Cell state
            #
            if "value" in value:


                cell_value = value.get(
                    "value"
                )


                if cell_value is None:

                    return


                result.append(
                    float(cell_value)
                )


                return



            #
            # normal tree
            #
            for v in value.values():

                self._collect_values(
                    v,
                    result
                )


            return




        if isinstance(
            value,
            list
        ):


            for v in value:

                self._collect_values(
                    v,
                    result
                )


            return




        if isinstance(
            value,
            np.ndarray
        ):


            flat = value.reshape(
                -1
            ).astype(
                np.float32
            )


            for x in flat:

                result.append(
                    float(x)
                )


            return




        if isinstance(
            value,
            (int,float)
        ):


            result.append(
                float(value)
            )