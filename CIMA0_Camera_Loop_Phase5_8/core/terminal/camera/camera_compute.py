import numpy as np

from core.compute_system.sampling.sampler import Sampler



class CameraCompute:
    """
    CIMA0 Camera Compute Organ.


    Responsibility:


        CameraObserver request


                |


                v


        execute sampling



    Knows:


        sampling execution



    Does NOT know:


        camera meaning

        image semantics

        field update

        display

    """



    def __init__(
        self
    ):

        self.sampler = Sampler()



    def execute(
        self,
        request,
        allocation
    ):
        """
        Execute compute request.


        request:

            {
                type,
                score,
                shape
            }


        allocation:

            {
                budget
            }

        """



        if request is None:

            return None



        if allocation is None:

            return None



        if "score" not in request:

            return None



        score = request["score"]



        budget = allocation.get(
            "budget",
            0
        )



        selected = self.sampler.select(
            score,
            budget
        )



        return {


            "type":

                "sample_result",



            "source":

                "camera_compute",



            "indices":

                selected,



            "count":

                int(
                    selected.size
                )

        }



    def step(
        self,
        requests,
        allocations
    ):
        """
        Batch execution.

        Supports multiple fields.
        """


        results = []


        for request in requests:


            source = request.get(
                "source"
            )


            allocation = allocations.get(
                source
            )


            result = self.execute(

                request,

                allocation

            )


            if result is not None:

                results.append(
                    result
                )


        return results