import copy
import numpy as np

class InternalDynamics:
    """
    CIMA0 Phase5_6

    Internal Dynamics Container.


    Responsibility:

        hold internal entities

        route external packets

        provide compute opportunity

        coordinate observation

        trigger local evolution



    Does NOT:

        define planet rules

        modify organ rules

        interpret meaning

        generate display data


    Observation:

        InternalDynamics owns observation context.

        Observer only describes current state.

    """


    def __init__(
        self,
        planet,
        compute=None,
        observer=None,
        observation_cache=None,
        attention_field=None,
        transport=None
    ):


        #
        # dynamical core
        #

        self.planet = planet


        #
        # computation system
        #

        self.compute = compute


        #
        # observer window
        #

        self.observer = observer
        
        self.observation_cache = observation_cache

        self.attention_field = attention_field                
                     
        #
        # information transport
        #

        self.transport = transport



        #
        # internal entities
        #

        self.organs = {}



        #
        # attention output
        #

        self.last_signals = []



        #
        # packet cache
        #

        self.internal_fields = {}


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

            if hasattr(
                organ,
                "receive"
            ):

                organ.receive(
                    packet
                )



    #
    # main evolution cycle
    #
    def step(self):


        signals = self._observe()
        
        #
        # attention update
        #
        
        if self.attention_field:

            for signal in signals:

                change = (
                    signal["state"]
                    .get("change")
                )
                
                if change is not None:

                    self.attention_field.receive(
                        change
                    )
        
        #
        # read attention state
        #
        
        attention = None
       
        if self.attention_field:

            attention = (
                self.attention_field.snapshot()
            )


        self.last_signals = attention
        
        print(
            "========== ATTENTION =========="
        )


        for signal in signals:

            print(
                signal["name"],
                signal["state"]
            )


        print(
            "==============================="
        )

        self._compute(
            signals
        )

        self._evolve()


        self._sample()


        self._planet_step()
    
    
    def _measure_change(
        self,
        name,
        current
    ):


        previous = (
            self.previous_observations
            .get(name)
        )


        if previous is None:

            delta = 0.0


        else:

            delta = float(
                np.mean(
                    np.abs(
                        current
                        -
                        previous
                    )
                )
            )


        self.previous_observations[name] = (
            current.copy()
        )


        return delta
                
    #
    # observation stage
    #
    def _observe(
        self
    ):

        signals = []


        #
        # planet observation
        #

        if (
            self.observer is not None
            and hasattr(
                self.planet,
                "snapshot"
            )
        ):


            snapshot = {
    
                "planet":
                    self.planet.snapshot()

            }


            observation = self.observer.describe(
                snapshot
            )


            change = None


            if self.observation_cache is not None:

                change =( 
                    self.observation_cache.step(
                        snapshot
                    )
                )



            signal = {
              
                    "name":
                        "planet",

                    "organ":
                        self.planet,

                    "state":
                        {
                            "observation":
                                observation,

                            "change":
                                change,
                                
                            "activity":
                                0.0 if change is None else 1.0    
                        }
            }
            signals.append(signal)
          
        #
        # organs observation
        #

        for name, organ in self.organs.items():


            if hasattr(
                organ,
                "activity"
            ):


                state = organ.activity()


                if state is not None:


                    signals.append(
                        {
                            "name":
                                name,

                            "organ":
                                organ,

                            "state":
                                state
                        }
                    )


        return signals
    
    #
    # compute stage
    #

    def _compute(
        self,
        signals
    ):
        
        print(
            "COMPUTE INPUT:",
            [
                (
                    s["name"],
                    s["state"]
                )
                for s in signals
            ]
        )
        
        if self.compute is None:

            return None



        if self.compute.available <= 0:

            self.compute.step()

            return None



        winner = self.compute.select(
            signals
        )



        if winner is not None:


            print(
                "COMPUTE WINNER:",
                winner["name"]
            )



            organ = winner["organ"]



            if hasattr(
                organ,
                "update"
            ):

                organ.update()
                
            self.compute.consume(
                1
            )



        self.compute.step()



        return winner




    #
    # internal organ evolution
    #

    def _evolve(
        self
    ):


        for organ in self.organs.values():


            if getattr(
                organ,
                "dynamic",
                True
            ):
                if hasattr(
                    organ,
                    "step"
                ):                
                    organ.step()

    #
    # packet sampling
    #

    def _sample(
        self
    ):


        if self.transport is None:

            return



        #
        # organs
        #

        for name, organ in self.organs.items():


            if hasattr(
                organ,
                "packet"
            ):


                packet = organ.packet()



                if packet is not None:


                    self.internal_fields[name] = packet



                    self.transport.publish(
                        packet
                    )



        #
        # planet
        #

        if hasattr(
            self.planet,
            "packet"
        ):


            packet = self.planet.packet()



            if packet is not None:


                self.internal_fields[
                    "planet"
                ] = packet



                self.transport.publish(
                    packet
                )




    #
    # planet evolution
    #

    def _planet_step(
        self
    ):


        if hasattr(
            self.planet,
            "step"
        ):


            print(
                "PLANET OBJECT:",
                type(self.planet)
            )


            self.planet.step()




    #
    # external snapshot
    #

    def snapshot(
        self
    ):


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


                for name, organ
                in self.organs.items()

            },


            "attention":

                self.last_signals,



            "fields":

                self.internal_fields,



            "planet":

                self.planet.snapshot()

                if hasattr(
                    self.planet,
                    "snapshot"
                )

                else None

        }