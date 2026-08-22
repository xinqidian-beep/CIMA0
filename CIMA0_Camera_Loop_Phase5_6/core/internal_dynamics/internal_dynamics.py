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

    def step(
        self
    ):

        #
        # observation
        #

        signals = self._observe()

        #
        # attention update
        #
        # all organs use same envelope
        #

        if self.attention_field is not None:


            for signal in signals:


                state = signal.get(
                    "state",
                    {}
                )


                if state is None:

                    continue


                self.attention_field.receive(
                    state
                )


            self.attention_field.step()



        #
        # save attention snapshot
        #

        if self.attention_field is not None:

            self.last_signals = (
                self.attention_field.snapshot()
            )



        #
        # compute competition
        #

        self._compute(
            signals
        )



        #
        # internal organs evolution
        #

        self._evolve()



        #
        # output internal fields
        #

        self._sample()



        #
        # planet evolution
        #

        self._planet_step()

 
  
    #
    # observation stage
    #
    def _observe(
        self
    ):
        
        """
        Collect internal observations.

        Responsibility:

            planet snapshot
            organ snapshot

            |
            v

            observer description
            observation cache
            activity signal


        Does NOT:

            - compute
            - select
            - route
            - display

        """
        
        signals = []

        print(self.organs.keys())
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
 

            #
            # readonly description
            #

            observation = (
                self.observer.describe(
                    snapshot
                )    
            )
            
            #
            # observation cache short-lived cache
            #

            change = None


            if self.observation_cache is not None:

                change = (
                    self.observation_cache.step(
                        snapshot
                    )
                )


            #
            # preserve high dimensional field
            #
            # NOT for compute
            #

            if change is not None:
 
                delta = change.get(
                    "delta"
                )


                if isinstance(
                    delta,
                    dict
                ):

                    self.internal_fields.update(
                        delta
                    )



            #
            # lightweight attention signal
            #

            activity = 0.0


            if change is not None:

                activity = change.get(
                    "signal",
                    0.0
                )
                
            print(
                "PLANET ACTIVITY:",
                activity
            )
                

            signals.append(
                {
                    "name":
                        "planet",


                    "organ":
                        self.planet,


                    "state":
                        {

                            #
                            # readonly description
                            #

                            "observation":
                                observation,


                            #
                            # attention / compute signal
                            #


                            "activity":
                                float(activity),
                                
                            "signal":
                                float(activity),    
                                
                            "changed":
                                False
                                if change is None
                                else change.get(
                                    "changed",
                                    False
                                ),
                            
                            "source":
                                "planet"

                        }
                }
            )    
                
        #
        # organ observation
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
                "apply_compute"
            ):

                organ.apply_compute(
                    1
                )
                
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