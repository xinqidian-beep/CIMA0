import numpy as np



class InternalDynamics:
    """
    CIMA0 Phase5_4


    Internal organism container.


    Structure:


        external packet


              |


              v


        organs


              |


              v


        cloud fields


              |


              v


        planet dynamics



    Knows:


        organ interface


        planet interface



    Does NOT know:


        visual meaning


        modality meaning


        sampling rule


        collision rule


        semantic meaning

    """



    def __init__(
        self,
        planet,
        compute_system=None
    ):


        self.planet = planet


        self.compute_system = compute_system


        #
        # internal organs
        #

        self.organs = {}



        #
        # snapshots
        #

        self.last_snapshot = {}





    #
    # organ registration
    #

    def register(
        self,
        name,
        organ
    ):


        if organ is None:

            return


        self.organs[name] = organ





    #
    # external input
    #

    def receive(
        self,
        packet
    ):


        if packet is None:

            return



        #
        # broadcast packet
        #

        for organ in self.organs.values():


            if hasattr(
                organ,
                "receive"
            ):

                organ.receive(
                    packet
                )






    #
    # internal clock
    #

    def step(
        self
    ):


        #
        # organs evolve
        #

        for organ in self.organs.values():


            if hasattr(
                organ,
                "step"
            ):

                organ.step()



        #
        # compute allocation
        #

        if self.compute_system is not None:


            requests = []


            for name,organ in self.organs.items():


                if hasattr(
                    organ,
                    "compute_request"
                ):


                    request = (
                        organ.compute_request()
                    )


                    if request is not None:

                        request["source"] = name

                        requests.append(
                            request
                        )



            allocation = (
                self.compute_system.step(
                    requests
                )
            )


            #
            # give budget back
            #

            for name,organ in self.organs.items():


                if name in allocation:


                    if hasattr(
                        organ,
                        "execute_compute"
                    ):

                        organ.execute_compute(
                            allocation[name]
                        )




        #
        # planet evolution
        #

        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()



        self._snapshot()






    #
    # snapshot
    #

    def _snapshot(
        self
    ):


        result = {}



        if hasattr(
            self.planet,
            "snapshot"
        ):

            result["planet"] = (
                self.planet.snapshot()
            )



        organs = {}



        for name,organ in self.organs.items():


            if hasattr(
                organ,
                "snapshot"
            ):


                organs[name] = (
                    organ.snapshot()
                )



        result["organs"] = organs



        self.last_snapshot = result






    def snapshot(
        self
    ):


        return self.last_snapshot.copy()