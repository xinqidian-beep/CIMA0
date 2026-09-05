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
        
        #
        # current observation cycle(selection feedback state)
        #

        self.last_selection = None

        self.last_result = None
        
        self.last_evaluation = None
        
        self.pending_evaluation = None
        
        self.last_step = None

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

    
    def record_selection(
        self,
        candidates,
        result,
        step=None
    ):

        self.last_selection = {

            "candidate_count":
                len(candidates),

            "candidates":
                candidates

        }


        self.last_result = result
        
        self.pending_evaluation = {

            "winner":
                result.get(
                    "name"
                ),

            "before":
                result.get(
                    "state"
                ),

            "step":
                self.last_step

        }
        
    def evaluate_pending(
        self,
        current_state
    ):

        if self.pending_evaluation is None:

            return None
            
        winner = (
            self.pending_evaluation["winner"]
        )    
            
        before = (
            self.pending_evaluation
            ["before"]
        )
                        
        after = None
        
        for item in current_state:

            if item.get("name") == winner:

                after = item.get("state")
                
                break
                
        if after is None:

            return None    

        evaluation = {

            "winner":
                winner,

            "before":
                before,

            "after":
                after,

            "gain":
                after["activity"]
                -
                before["activity"]

        }
        
        self.last_evaluation = evaluation


        self.pending_evaluation = None
        
        return evaluation 

    def _compare(
        self,
        before,
        after
    ):

        if before is None or after is None:

            return 0.0


        b = before.get(
            "signal",
            0.0
        )


        a = after.get(
            "signal",
            0.0
        )


        return float(
            a-b
        )        
        
    def record_evaluation(
        self,
        evaluation
    ):

        self.last_evaluation = evaluation    
                
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
                
            "last_selection":
                self.last_selection,

            "last_result":
                self.last_result,
                
            "last_evaluation":
                self.last_evaluation,

            "pending_evaluation":
                self.pending_evaluation,

            "last_evaluation":
                self.last_evaluation
                
        }   