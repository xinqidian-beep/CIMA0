import numpy as np


class InternalDynamicsObserver:
    """
    CIMA0 Phase5_3

    Read only observer.

    Responsibility:

        InternalDynamics snapshot
                |
                v
        selected state read
                |
                v
        internal packet
                |
                v
        IO field packet


    Does NOT know:

        camera
        planet dynamics
        clip generation
        cloud generation
        activity calculation
        sampler
        compute allocation rules
        meaning
    """


    def __init__(self):

        self.cache = {}



    def read(
        self,
        snapshot,
        allocation=None
    ):
        """
        Read selected parts of internal state.

        allocation is produced by ComputeSystem.

        Observer only executes the decision.
        """

        if snapshot is None:

            return None


        result = {}


        for name, value in snapshot.items():

            selected = None


            if allocation is None:

                selected = value


            else:

                selected = self._read_value(
                    name,
                    value,
                    allocation.get(
                        name,
                        None
                    )
                )


            result[name] = selected


        return result



    def _read_value(
        self,
        path,
        value,
        allocation
    ):

        if value is None:

            return None



        if isinstance(
            value,
            np.ndarray
        ):

            return self._read_array(
                path,
                value,
                allocation
            )



        if isinstance(
            value,
            dict
        ):

            result = {}


            for key, child in value.items():

                child_allocation = None


                if isinstance(
                    allocation,
                    dict
                ):

                    child_allocation = allocation.get(
                        key
                    )


                result[key] = self._read_value(
                    f"{path}.{key}",
                    child,
                    child_allocation
                )


            return result



        if isinstance(
            value,
            list
        ):

            return [

                self._read_value(
                    f"{path}.{i}",
                    v,
                    allocation
                )

                for i,v in enumerate(value)

            ]


        return value



    def _read_array(
        self,
        path,
        array,
        allocation
    ):
        """
        Observer does not decide sampling.

        If compute gives no restriction,
        return current state.

        """

        if allocation is None:

            return array.copy()



        #
        # allocation format is decided by ComputeSystem.
        #
        # Observer only applies it.
        #

        return array.copy()



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



    def encode_field(
        self,
        data,
        source="internal" 
    ):

        if data is None:
            return None


        if isinstance(data, dict):

            if "planet" in data:

                array = data["planet"]


                if isinstance(
                    array,
                    np.ndarray
                ):

                    array = array.astype(
                        np.float32
                    )


                    return {

                        "type":
                            "field",

                        "source":
                            source,

                        "bytes":
                            array.tobytes(),

                        "shape":
                            array.shape,

                        "dtype":
                            str(array.dtype)

                    }


        return None



    def _collect_values(
        self,
        value,
        result
    ):


        if isinstance(
            value,
            np.ndarray
        ):

            result.extend(

                value.reshape(-1)
                .astype(np.float32)

            )

            return



        if isinstance(
            value,
            dict
        ):

            for child in value.values():

                self._collect_values(
                    child,
                    result
                )

            return



        if isinstance(
            value,
            list
        ):

            for child in value:

                self._collect_values(
                    child,
                    result
                )

            return



        if isinstance(
            value,
            (int,float)
        ):

            result.append(
                float(value)
            )