from collections import deque

class ObservationMemory:

    """
    CIMA0 Observation Memory

    Store observation history.

    Does NOT:
        select
        allocate
        control

    Provides:
        historical observation statistics
    """

    def __init__(
        self,
        capacity=128
    ):

        self.capacity = capacity

        self.records =deque(
            maxlen=capacity
        )

    def record_observation(
        self,
        observation
    ):
        """
        Store one finite observation.

        ObservationMemory only stores history.
        It does not select, allocate, evolve,
        or interpret the observation.
        """

        if observation is None:

            return

        self.receive(
            observation
        )


    def recent_observations(
        self,
        count=None
    ):
        """
        Return recent observations.

        Does not modify stored history.
        """

        if count is None:

            return list(
                self.records
            )

        if count <= 0:

            return []

        return list(
            self.records
        )[-count:]

    def statistics(self):

        if len(self.records)==0:
            return {
                
                "activity":0.0,
                "delta":0.0,
                "age":0.0,
                "occupancy":0.0
            }


        activity=0
        delta=0
        age=0


        count=0


        for record in self.records:

            if "signals" in record:

                signals = record["signals"]

            else:

                signals = [
                    {
                        "state":
                            record.get(
                                "state",
                                {}
                            )
                    }
                ]


            for signal in signals:

                state=signal.get(
                    "state",
                    {}
                )
                
                activity += float(
                    state.get(
                        "activity",
                        0
                    )
                )
                
                delta += float(
                    state.get(
                        "signal",
                        0
                    )
                )

                age += float(
                    state.get(
                        "age",
                        0
                    )
                )

                

                

                count += 1


        if count==0:
            return {                
                "activity":0.0,
                "delta":0.0,
                "age":0.0,
                "occupancy":
                    len(self.records)
                    /
                    self.capacity
            }


        return {            
            "activity":activity/count,
            "delta":delta/count,
            "age":age/count,
            "occupancy":
                len(self.records)
                /
                self.capacity
        }    
        
    def receive(
        self,
        record
    ):
        
        self.records.append(
            record
        )
    def occupancy(
        self
    ):

        if self.capacity <= 0:

            return 0.0


        return (
            len(self.records)
            /
            self.capacity
        )    
               
    def pressure(
        self
    ):
        """
        Historical pressure.

        Used by sampler.

        Not decision.
        """

        return self.occupancy()


    def debug_state(
        self
    ):

        return {

            "size":
                len(self.records),

            "capacity":
                self.capacity,

            "pressure":
                self.pressure(),
                
            #"last_selection":
            #    self.last_selection,

            #"last_result":
            #    self.last_result,
                       
            #"pending_evaluation":
            #    self.pending_evaluation,

            #"last_evaluation":
            #    self.last_evaluation
                
        }   