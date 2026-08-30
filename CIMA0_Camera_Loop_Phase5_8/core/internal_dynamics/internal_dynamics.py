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
        # raw external packet cache
        #

        self.external_packets = {}        
        
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
        """
        Receive one homogeneous packet.

        Responsibility:

            external packet
                    |
                    +----> preserve
                    |
                    +----> broadcast to organs

        InternalDynamics does NOT:

            - decode packet
            - interpret packet
            - select packet content
            - discard unused information
            - transform representation

        Every organ decides independently
        which part of the packet it needs.

        The original packet remains intact.
        """

        if packet is None:
            return


        print(
            "INTERNAL RECEIVE:",
            packet.source,
            packet.tag,
            packet.schema,
            packet.shape
        )


        #
        # preserve original physical stream
        #

        if not hasattr(
            self,
            "external_packets"
        ):

            self.external_packets = {}


        #
        # Camera is an external physical stream.
        #
        # Preserve the complete packet.
        #

        if (
            packet.source == "camera"
            and
            packet.tag == "camera_raw"
        ):

            self.external_packets[
                "camera_raw"
            ] = packet


        #
        # Broadcast unchanged packet.
        #
        # Each organ decides what it needs.
        #

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

                               
    #
    # main evolution cycle
    #

    def step(self):
        #
        # 1. internal evolution
        #

        self._planet_step()

        self._evolve()
        #
        # 2. observe current change
        #

        signals = self._observe()


        #
        # 3. compute
        #

        result = self._compute(
            signals
        )


        #
        # 4. commit exactly once
        #

        self.commit(
            result
        )


        #
        # 5. sample exactly once
        #

        return self._sample()
        


  
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
        
        
        if winner is  None:
            return None
                        
        organ = winner.get(
            "organ"
        )


        if organ is None:
            return None


        return {
            "organ": organ,
            "winner": winner
        }

    def commit(
        self,
        result
    ):

        if result is None:
            return


        organ = result.get(
            "organ"
        )

        if organ is None:
            return


        winner = result.get(
            "winner"
        )
        
        if winner is None:
            return
        
        allocation = winner.get(
            "allocation"
        )
        
        if allocation is None:
            
            if hasattr(
                organ,
                "execute_compute"
            ):

                organ.execute_compute(
                    allocation
                )

                self.compute.consume(
                    allocation
                )
            
                return
        
        #
        # selected organ
        #
        if hasattr(
            organ,
            "commit"
        ):

            organ.commit(
                winner.get(
                    "state"
                )
            )


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

        snapshot = {
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

            "planet":
                self.planet.snapshot()
                if hasattr(
                    self.planet,
                    "snapshot"
                )
                else None,

            "fields":
                copy.deepcopy(
                    self.internal_fields
                )    
        
        }

        

        self.last_snapshot = snapshot

        return snapshot
                
 
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

            "external":
                self.external_packets,  

            "planet":

                self.planet.snapshot()

                if hasattr(
                    self.planet,
                    "snapshot"
                )

                else None
                
              

        }