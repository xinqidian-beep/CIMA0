import numpy as np

class ComputeSystem:
    """
    CIMA0 Compute Resource Manager.


    Responsibility:

        collect requests

        allocate budget



    Does NOT know:

        field meaning

        organ meaning

        sampling meaning

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
        
        print(
            "submit:",
            request
        )    

        if not isinstance(
            request,
            dict
        ):

            return


        if request.get(
            "type"
        ) != "compute_request":

            return



        self.requests.append(
            request
        )



    def allocate(
        self
    ):


        if len(
            self.requests
        ) == 0:

            return {}



        demands=[]



        for r in self.requests:


            score = r.get(
                "score"
            )


            if score is None:

                demand=0

            else:

                demand=float(
                    np.sum(
                        np.abs(score)
                    )
                )


            demands.append(
                demand
            )



        total=sum(
            demands
        )



        result={}



        for r,d in zip(
            self.requests,
            demands
        ):


            name=r.get(
                "source",
                "unknown"
            )


            if total>0:

                budget=int(

                    self.capacity

                    *

                    d

                    /

                    total

                )

            else:

                budget=0



            result[name]={

                "budget":
                    budget,


                "source":
                    name,


                "shape":
                    r.get(
                        "shape"
                    )

            }



        self.requests.clear()


        return result
        
        print(
            "allocation result:",
            allocation
        )
        
    def step(
        self,
        requests
    ):
        """
        Compute cycle.

        Receive requests,
        allocate resources.

        No semantic knowledge.
        """

        if requests is None:
            return {}


        for request in requests:

            self.submit(
                request
            )


        return self.allocate()