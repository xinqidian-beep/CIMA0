import copy


class InternalDynamics:
    """
    CIMA0 Phase5_4

    Internal Dynamics Container.


    Responsibility:

        hold internal entities

        route external packets

        provide compute opportunity

        trigger local evolution



    Does NOT:

        define time

        define fast/slow

        interpret meaning

        control organ rules

        modify planet rules


    Time appears only in Observer.
    """


    def __init__(
        self,
        planet,
        compute=None
    ):

        self.planet = planet

        self.compute = compute

        self.organs = {}
        
        self.last_signals = []

        self.last_observation = None



    #
    # register organ
    #

    def register(
        self,
        name,
        organ
    ):

        self.organs[name] = organ



    #
    # external input
    #

    def receive(
        self,
        packet
    ):
                
        for organ in self.organs.values():

            if hasattr(organ,"receive"):

                organ.receive(packet)    
        
    #
    # internal evolution
    #

    def step(self):
        
        signals=[]


        for name, organ in self.organs.items():

            if hasattr(
                organ,
                "activity"
            ):

                state=organ.activity()

                if state is not None:

                    signals.append(
                        {
                            "name":name,   
                            "organ": organ,
                            "state":state
                        }
                    )
                    
        #
        # save attention observation
        #

        self.last_signals = [
            {
                "name":s["name"],
                "state":s["state"]
            }
            for s in signals
        ]        
                    
        if self.compute is not None:


            winner=None


            if self.compute.available > 0:

                winner=self.compute.select(
                    signals
                )


            if winner is not None:
                
                organ=winner["organ"]


                if hasattr(
                    organ,
                    "apply_compute"
                ):

                    organ.apply_compute(
                        1
                    )


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



        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()

    #
    # observer interface
    #

    def snapshot(self):

        return {

            "organs":
            {
                name:
                    organ.snapshot()
                    if hasattr(
                        organ,
                        "snapshot"
                    )
                    else None

                for name,organ
                in self.organs.items()
            },


            "attention":
                self.last_signals,


            "planet":
                self.planet.snapshot()
                if hasattr(
                    self.planet,
                    "snapshot"
                )
                else None

        }