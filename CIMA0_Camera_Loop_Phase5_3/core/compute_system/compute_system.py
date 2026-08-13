import numpy as np



class ComputeSystem:
    """
    CIMA0 Compute Allocation System.


    Responsibility:


        receive compute requests


                |


                v


        allocate compute budget



    Knows:

        request strength

        available capacity



    Does NOT know:

        camera

        planet

        cloud

        sampling meaning

        field semantics

    """



    def __init__(
        self,
        capacity=1024
    ):

        self.capacity = capacity


        self.requests = []



    def submit(
        self,
        request
    ):
        """
        Receive hand raising request.
        """

        if request is None:

            return



        if not isinstance(
            request,
            dict
        ):

            return



        if request.get(
            "type"
        ) != "compute_request":

            return



        if "score" not in request:

            return



        self.requests.append(
            request
        )



    def allocate(
        self
    ):
        """
        Allocate compute budget.

        No field interpretation.
        """

        if len(
            self.requests
        ) == 0:

            return {}



        #
        # calculate total demand
        #

        demands = []


        for request in self.requests:


            score = request["score"]


            demand = float(

                np.sum(
                    np.abs(score)
                )

            )


            demands.append(
                demand
            )



        total = sum(
            demands
        )



        allocations = {}



        #
        # proportional allocation
        #

        for request, demand in zip(
            self.requests,
            demands
        ):


            source = request.get(
                "source",
                "unknown"
            )


            if total <= 0:


                budget = 0



            else:


                budget = int(

                    self.capacity

                    *

                    demand

                    /

                    total

                )



            allocations[source] = {


                "budget":

                    budget,



                "shape":

                    request.get(
                        "shape"
                    )

            }



        #
        # clear current cycle
        #

        self.requests.clear()



        return allocations



    def step(
        self,
        requests
    ):
        """
        Convenience interface.

        requests:

            iterable of requests

        """


        for request in requests:

            self.submit(
                request
            )


        return self.allocate()