import copy
import numpy as np

from .cloud.cloud_state import CloudState
from core.memory.observation_memory import ObservationMemory

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
        collision=None,
        observer=None,
        observation_cache=None,
        attention_field=None,
        transport=None
    ):
        
        self.step_count = 0
        
        #
        # dynamical core
        #

        self.planet = planet
        
        self.cloud = CloudState()
        
        #
        # computation system
        #

        self.compute = compute
        
        self.collision = collision


        #
        # observer window
        #

        self.observer = observer
        
        self.observation_cache = observation_cache

        self.attention_field = attention_field

        self.observation_memory = ObservationMemory(
            capacity=128
        )
        self.observation_memory = self.observation_memory
                     
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
                
    def _collect_clouds(
        self
    ):
        print(
            "PLANET COLLISION METHOD:",
            hasattr(
                self.planet,
                "collision_projection"
            )
        )
        clouds = {}
        #
        # planet
        #

        if self.planet is not None:
            print(
                "PLANET FOR CLOUD:",
                self.planet.collision_projection()
            )

            if hasattr(
                self.planet,
                "collision_projection"
            ):

                clouds["planet"] = (
                    self.planet
                    .collision_projection()
                )

            else:

                clouds["planet"] = (
                    self.planet.snapshot()
                )
        #
        # organs
        #

        for name, organ in self.organs.items():

            if hasattr(
                organ,
                "collision_projection"
            ):

                cloud =(
                    organ
                    .collision_projection()
                )
                
                clouds[name] = cloud
                
                if hasattr(
                    organ,
                    "debug_state"
                ):
                    state = organ.debug_state()
                    print(
                        "CLOUD:",
                        name,
                        organ.debug_state()
                    )
        return clouds  

    def _evaluate_memory(
        self
    ):

        if self.observation_memory is None:

            return


        pending = (
            self.observation_memory
            .pending_evaluation
        )


        if pending is None:

            return


        winner = pending.get(
            "winner"
        )
        

        for name, organ in self.organs.items():
            
            if name != winner:

                continue
            
            if hasattr(
                organ,
                "activity"
            ):

                state = organ.activity()

                if state is not None:
                    result = (
                        self.observation_memory
                        .evaluate_pending(
                            state
                        )
                    )
                    
                    print(
                        "MEMORY EVALUATION:",
                        result
                    )

                    break
        
                                
    #
    # main evolution cycle
    #

    def step(
        self
    ):
                
        self.step_count += 1
        collision_result = None
                
        #
        # previous observation
        #

        previous_signals = self._observe()          
        
        
        #
        # evaluate previous selection
        #

        if self.observation_memory is not None:

            self.observation_memory.evaluate_pending(
                previous_signals
            )
        #
        # collect clouds
        #

        clouds = self._collect_clouds()
        
        if self.collision:
            
            print(
                "PLANET CLOUD:",
                clouds.get("planet")
            )

            print(
                "CLIP CLOUD:",
                clouds.get("clip")
            )

            collision_result = self.collision.collide(
                clouds.get("planet"),
                clouds.get("clip")
            )
            print(
                "COLLISION RESULT:",
                collision_result
            )
        
        #
        # observation
        #

        current_signals = self._observe()
        
        #
        # collision signal
        #

        if collision_result is not None:

            interaction = collision_result.get(
                "interaction",
                0.0
            )


            if interaction > 0:

                collision_signal = {
                    "source": "collision",
                    "signal": float(interaction),
                    "step": self.step_count
                }


                current_signals.append(
                    {
                        "name": "collision",
                        "organ": self.collision,
                        "state": collision_signal
                    }
                )


                self.cloud.receive(
                    collision_signal
                )

        #
        # attention update
        #
        # all organs use same envelope
        #

        if self.attention_field is not None:


            for signal in current_signals:


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
        # compute competition(new compute decision)
        #

        self._compute(
            current_signals
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

        planet_delta = self._planet_step()
        
        
        #
        # cloud evolution
        #
        
        self.cloud.step()
        


  
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
        
        self.observation_memory.receive(
            {
                "signals": signals,

                "winner":
                    None
                    if winner is None
                    else winner["name"],

                "step":
                    self.step_count
            }
        )
        
        if winner is not None:
            
                        
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


            delta = self.planet.step()
            print(
                "PLANETFIELD DELTA:",
                delta
            )
            
            return delta

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