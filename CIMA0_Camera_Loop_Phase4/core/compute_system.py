class ComputeSystem:
    """
    Autonomous resource allocator.

    Only knows:

        capacity
        requests

    Does NOT know:

        planet
        clip
        meaning
    """


    def __init__(
        self,
        capacity=100
    ):

        self.capacity = capacity



    def self_check(
        self
    ):

        return {
            "capacity":
                self.capacity
        }



    def allocate(
        self,
        requests
    ):

        total = sum(
            requests.values()
        )


        if total <= 0:

            return {}


        result = {}


        for key,value in requests.items():

            result[key] = (
                self.capacity *
                value /
                total
            )


        return result