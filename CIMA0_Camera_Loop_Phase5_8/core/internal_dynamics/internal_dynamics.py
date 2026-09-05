import copy
import numpy as np

from .cloud.cloud_state import CloudState
from core.memory.observation_memory import ObservationMemory
from core.internal_dynamics.cloud_collision import CloudCollision


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
        # 2. existing Planet continues its own evolution
        # -------------------------------------------------
        #

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
        # 8. collision happens AFTER computation
        #
        # No Observer here.
        # -------------------------------------------------
        #
        #
        #collision = self._collision(
        #    result
        #)
        #


        #
        # -------------------------------------------------
        # 9. collision result enters PlanetField
        # -------------------------------------------------
        #
        #
        #self._apply_collision(
        #    collision
        #)
        #


        #
        # -------------------------------------------------
        # 10. sample AFTER the event
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

        if glimpse is not None:
            
            print(
                "PLANET GLIMPSE OBSERVED:",
                glimpse["region"],
                glimpse["level"],
                glimpse["exact"]
            )

            signals.append(
                {
                    "name":
                        "planet",

                    "organ":
                        self.planet,

                    "state":
                        {
                            "observation":
                                glimpse,

                            "activity":
                                0.0,

                            "signal":
                                0.0,

                            "changed":
                                False,

                            "source":
                                "planet",

                            "request":
                                False
                        }
                }
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
        # collect observations
        # -------------------------------------------------
        #

        observations = {}

        for signal in signals:

            name = signal.get(
                "name"
            )

            state = signal.get(
                "state",
                {}
            )

            observation = state.get(
                "observation"
            )

            if observation is not None:

                observations[name] = observation

        #
        # -------------------------------------------------
        # Compute performs comparison
        # -------------------------------------------------
        #

        comparison = None

        if observations:

            comparison = self.compute.compare(
                observations
            )

        #
        # comparison is information.
        #
        # It is NOT yet a candidate.
        #

        if comparison is not None:

            print(
                "COMPUTE COMPARISON:",
                comparison
            )

        #
        # -------------------------------------------------
        # existing compute-selection path
        # -------------------------------------------------
        #

        if self.compute.available <= 0:

            self.compute.step()

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

            "winner":
                winner,

            "comparison":
                comparison
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


        winner = result.get(
            "winner"
        )

        if winner is None:

            return


        allocation = winner.get(
            "allocation"
        )

        if allocation is None:

            return


        print(
            "COMMIT ORGAN:",
            type(organ).__name__
        )

        print(
            "COMMIT ALLOCATION:",
            allocation
        )


        #
        # -------------------------------------------------
        # consume system resource
        # -------------------------------------------------
        #

        consumed = self.compute.consume(
            allocation
        )


        if consumed <= 0.0:

            return


        print(
            "COMPUTE CONSUME:",
            consumed
        )

        print(
            "COMPUTE AVAILABLE AFTER:",
            self.compute.available
        )


        #
        # -------------------------------------------------
        # grant local compute opportunity
        # -------------------------------------------------
        #

        if hasattr(
            organ,
            "apply_compute"
        ):

            print(
                "APPLY COMPUTE:",
                type(organ).__name__,
                consumed
            )

            organ.apply_compute(
                consumed
            )

            return


        #
        # -------------------------------------------------
        # alternate execution interface
        # -------------------------------------------------
        #

        if hasattr(
            organ,
            "execute_compute"
        ):

            print(
                "EXECUTE COMPUTE:",
                type(organ).__name__,
                consumed
            )

            organ.execute_compute(
                {
                    "amount":
                        consumed
                }
            )

            return


        print(
            "COMPUTE DISPATCH:",
            type(organ).__name__,
            "NO EXECUTION INTERFACE"
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


        clip_cloud = projection.get(
            "cloud"
        )

        if clip_cloud is None:
            return None


        planet_cloud = self.planet.state


        print(
            "COLLISION ENTRANCE:",
            winner
        )


        collision_result = self.collision.collide(
            planet_cloud,
            clip_cloud,
            winner
        )


        if collision_result is None:
            return None


        print(
            "COLLISION:",
            collision_result.get(
                "collision"
            )
        )


        print(
            "COLLISION RESULT:",
            collision_result.get(
                "collision_result"
            )
        )


        return collision_result

    def _apply_collision(
        self,
        collision
    ):
        """
        Apply collision result to PlanetField.

        CloudCollision does not modify PlanetField.

        PlanetField remains the owner of disturbance intake.
        """

        if collision is None:
            return False


        if not collision.get(
            "collision"
        ):

            return False


        collision_result = collision.get(
            "collision_result"
        )

        if collision_result is None:
            return False


        if not collision_result.get(
            "exists"
        ):

            return False


        disturbance = collision_result.get(
            "disturbance"
        )

        if disturbance is None:
            return False


        state = self.planet.state

        if state is None:
            return False


        disturbance_field = np.zeros_like(
            state,
            dtype=np.float32
        )


        disturbance_field[...] = np.float32(
            disturbance
        )


        print(
            "PLANETFIELD DISTURBANCE:",
            float(
                disturbance
            )
        )


        self.planet.receive(
            disturbance_field
        )


        return True
    
    
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
        Give the endogenous PlanetField an opportunity
        to expose its current internal candidate.

        InternalDynamics does not choose a region and does
        not force a full Planet.step().
        """

        if self.planet is None:
            return None

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