import copy
import time
import numpy as np


from .cloud.cloud_state import CloudState
from core.memory.observation_memory import ObservationMemory
from core.internal_dynamics.cloud_collision import CloudCollision

class LocalClock:

    def __init__(
        self,
        interval=1
    ):

        self.interval = interval
        self.last = time.perf_counter()


    def due(
        self
    ):

        now = time.perf_counter()

        if (
            now - self.last
            >= self.interval
        ):

            self.last = now

            return True

        return False



class InternalDynamics:
    """
    CIMA0 Phase5_8

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
        
        self.planet_clock = LocalClock(interval=1.0)
        
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
        self.planet_glimpse_version = 0
        self.planet_glimpse_observed_version = -1
        
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
            print(
                "INTERNAL RECEIVE:",
                packet.source,
                packet.tag
            )
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
        
        clouds = {}
        #
        # planet
        #

        if self.planet is not None:
           

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

        return clouds  
                             
    #
    # main evolution cycle
    #

    def step(
        self
    ):

        #
        # -------------------------------------------------
        # 1. computational opportunity recovers
        # -------------------------------------------------
        #

        self.compute.step()


        #
        # -------------------------------------------------
        # 2. Planet evolves according to its own internal clock
        # -------------------------------------------------
        #
        
        if self.planet_clock.due():
            self._planet_step()
            
        
        #
        # -------------------------------------------------
        # 3. observe current state
        #
        # Observer is still before the next decision.
        # It does not know future collision.
        # -------------------------------------------------
        #

        signals = self._observe()


        #
        # -------------------------------------------------
        # 4. compute selects one opportunity
        # -------------------------------------------------
        #

        result = self._compute(
            signals
        )


        #
        # -------------------------------------------------
        # 5. commit computational resource
        #
        # ComputeSystem -> organ
        # -------------------------------------------------
        #

        self.commit(
            result
        )


        #
        # -------------------------------------------------
        # 6. internal dynamics evolution
        # -------------------------------------------------
        #

        self._evolve()


        #
        # -------------------------------------------------
        # 7. collision happens AFTER computation
        # collision relation
        # No Observer here.
        # -------------------------------------------------
        #
        
        collision = self._collision(
            result
        )
        # text
        if collision is None:

            print(
                "COLLISION:",
                None
            )
        else:
            print(
                 "COLLISION:",
                {
                    "clip_local_states":
                        collision.get("clip_local_states"),
                    "planet_local_states":
                        collision.get("planet_local_states"),
                    "response_count":
                        collision.get(
                            "collision_result",
                            {}
                        ).get("count")
                }
            )

        #
        # -------------------------------------------------
        # 8. sample AFTER the event
        #
        # The next observation is therefore post-event.
        # -------------------------------------------------
        #

        return self._sample()


  
    #
    # observation stage
    #
    def _observe(
        self
    ):

        signals = []

        #
        # -------------------------------------------------
        # Planet glimpse
        # -------------------------------------------------
        #

        glimpse = self.internal_fields.get(
            "planet_glimpse"
        )

        if (
            glimpse is not None
            and
            self.planet_glimpse_version 
            != 
            self.planet_glimpse_observed_version
        ):
            observed = None
            
            
            #
            # Observer
            #

            if self.observer is not None:
                
                observation = glimpse.get(
                    "observation"
                )

                observed = self.observer.observe(
                    observation
                )
                

            #
            # complete observation
            #

            observation = None

            if (
                observed is not None
                and
                "observation" in observed
            ):

                observation = observed["observation"]


            #
            # ObservationCache
            #

            change = None

            if (
                observation is not None
                and
                self.observation_cache is not None
            ):

                change = self.observation_cache.step(
                    observation
                )
                
                print("PLANET CHANGE:", change)                
                
            #
            # AttentionField
            #    
                
            if (
                change is not None
                and
                self.attention_field is not None
                and
                change.get("changed", False)
            ):

                self.attention_field.receive(
                    {
                        "source": "planet",
                        "change": change
                        
                    }
                )

                self.attention_field.step()
                
                
                
            self.planet_glimpse_observed_version = (
                self.planet_glimpse_version
            )
                
        #
        # -------------------------------------------------
        # organs
        # -------------------------------------------------
        #

        for name, organ in self.organs.items():

            if hasattr(
                organ,
                "activity"
            ):

                state = organ.activity()
                print(
                    "OBSERVE:",
                    name,
                    state
                )
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


        #
        # -------------------------------------------------
        # existing compute-selection path
        # -------------------------------------------------
        #

        if self.compute.available <= 0:

            return None

        requests = []

        for signal in signals:

            state = signal.get(
                "state",
                {}
            )

            request = state.get(
                "request"
            )

            if request == "compute":

                requests.append(
                    signal
                )

        if not requests:

            return None

        winner = self.compute.select(
            requests
        )
        if winner is None:

            return None

        organ = winner.get(
            "organ"
        )

        if organ is None:

            return None

        return {
            "organ":
                organ,
                
            "allocation":
                winner.get(
                    "allocation"
                ),
                
            "winner": winner.get(
                "name"
            ),
            "state": winner.get(
                "state"
            )    

        }
        
        
    def commit(
        self,
        result
    ):
        """
        Commit one computational opportunity.

        Responsibility:

            allocation
                |
                +----> consume system resource
                |
                +----> grant local compute permission

        ComputeSystem owns resource accounting.

        Organ owns execution.

        ComputeSystem does NOT execute the organ.
        """

        if result is None:

            return


        organ = result.get(
            "organ"
        )

        if organ is None:

            return


        allocation = result.get(
            "allocation"
        )

        if allocation is None:

            return


        
        


        #
        # -------------------------------------------------
        # consume system resource
        # -------------------------------------------------
        #

        consumed = self.compute.consume(
            allocation
        )
        print(
            "COMMIT:",
            type(organ).__name__,
            "ALLOCATION:",
            allocation,
            "CONSUMED:",
            consumed
        )

        if consumed <= 0.0:

            return
            
        organ.apply_compute(
            consumed
        )    


    def _collision(
        self,
        result
    ):

        if result is None:
            return None


        organ = result.get(
            "organ"
        )

        if organ is None:
            return None


        if not hasattr(
            organ,
            "collision_projection"
        ):
            return None


        projection = organ.collision_projection()
 
        if projection is None:
            return None


        winner = projection.get(
            "winner"
        )

        if winner is None:
            return None
            
        matrix_coordinate = projection.get(
            "matrix_coordinate"
        )

        if matrix_coordinate is None:
            return None

        clip_cloud = projection.get(
            "cloud"
        )

        if clip_cloud is None:
            return None
        
        #
        # Planet local material
        # selected by Planet.glimpse()
        #
        
        glimpse = self.internal_fields.get(
            "planet_glimpse"
        )

        if glimpse is None:
            return None

        planet_cloud = {
            "region": glimpse.get(
                "observation",
                {}
            ).get(
                "region"
            ),
            "local_state": glimpse.get(
                "local_state"
            )
        }

        if (
            planet_cloud["region"] is None
            or
            planet_cloud["local_state"] is None
        ):
            return None

        collision_result = self.collision.collide(
            planet_cloud,
            clip_cloud,
            winner,
            matrix_coordinate
        )


        if collision_result is None:
            return None

        return collision_result
   
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
    # planet evolution / endogenous glimpse
    #
    def _planet_step(
        self
    ):
        """
        Advance PlanetField according to its own clock,
        then expose its current internal candidate.

        InternalDynamics does not choose a region.
        """

        if self.planet is None:
            return None

        if not hasattr(
            self.planet,
            "step"
        ):
            return None

        self.planet.step()

        if not hasattr(
            self.planet,
            "glimpse"
        ):
            return None

        result = self.planet.glimpse()
        

        if result is None:
            return None

        self.internal_fields[
            "planet_glimpse"
        ] = result
        
        self.planet_glimpse_version += 1

        return result

        
        
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