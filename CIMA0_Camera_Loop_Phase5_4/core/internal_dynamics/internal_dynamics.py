import numpy as np


class InternalDynamics:
    """
    CIMA0 Phase5_4

    Internal Dynamics Container.


    Responsibility:

        hold internal entities

        route external packets

        provide compute field

        trigger local evolution



    Does NOT:

        define time

        define fast/slow

        interpret meaning

        control organ behavior

        modify planet rules



    Time appears only in observation.

    """


    def __init__(
        self,
        planet,
        compute=None
    ):

        #
        # original dynamical entity
        #

        self.planet = planet


        #
        # local compute field
        #

        self.compute = compute



        #
        # internal organs
        #

        self.organs = {}



        #
        # latest complete observation
        #

        self.last_observation = None



    #
    # register internal organ
    #

    def register(
        self,
        name,
        organ
    ):

        self.organs[name] = organ



    #
    # receive external information flow
    #

    def receive(
        self,
        packet
    ):

        for organ in self.organs.values():


            if hasattr(
                organ,
                "receive"
            ):

                organ.receive(
                    packet
                )



    #
    # internal evolution cycle
    #

    def step(
        self
    ):


        #
        # collect local activity
        #
        # compute does not know organ
        #

        signals = []


        for organ in self.organs.items():


            if hasattr(
                organ,
                "activity"
            ):


                signal = organ.activity()


                if signal is not None:

                    signals.append(
                        {
                            "organ": organ,
                            "signal": signal
                        }
                    )



        #
        # compute field chooses
        #
        # only resource allocation
        #

        if self.compute:


            winner = self.compute.select(
                signals
            )


            if winner:


                organ = winner["organ"]


                if hasattr(
                    organ,
                    "apply_compute"
                ):

                    organ.apply_compute()



                self.compute.consume(
                    1
                )


            self.compute.step()
            
        for organ in self.organs.values():

            if hasattr(
                organ,
                "step"
            ):

                organ.step()    
            
                
    #
    # snapshot for observer
    #

    def snapshot(
        self
    ):


        result = {


            "planet": None,


            "organs": {}

        }



        #
        # Planet snapshot
        #

        if hasattr(
            self.planet,
            "snapshot"
        ):

            result["planet"] = (
                self.planet.snapshot()
            )



        #
        # organ snapshot
        #

        for name, organ in self.organs.items():


            if hasattr(
                organ,
                "snapshot"
            ):


                result["organs"][name] = (
                    organ.snapshot()
                )


            else:


                result["organs"][name] = None



        self.last_observation = result


        return result.copy()