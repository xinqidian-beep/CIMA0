from .sampling.sampler import Sampler

from .sampling.sampler import Sampler
from core.memory.observation_memory import ObservationMemory

class ComputeSystem:
    """
    CIMA0 Compute Field

    Local compute energy field.

    Does NOT know:

        organ
        meaning
        source

    """

    def __init__(
        self,
        capacity=1024,
    ):

        self.capacity = capacity

        self.available = capacity
        
        self.memory = ObservationMemory(capacity=32)
        self.sampler = Sampler()
        self.sampler.attach_memory(
            self.memory
        )
        
        self.step_count = 0

    def step(self):

        self.available += (
            self.capacity
            -
            self.available
        ) * 0.01


        self.available = min(
            self.available,
            self.capacity
        )

    def select(
        self,
        signals
    ):
        if not signals:
            return None
            
        self.step_count += 1
        
        if not signals:

            return None

        #
        # evaluate previous decision
        #

        if self.memory is not None:

            self.memory.evaluate_pending(
                signals
            )            
                
        states = []


        for s in signals:

            state = s.get(
                "state",
                {}
            )


            states.append(
                {

                    "age":
                        state.get(
                            "age",
                            0.0
                        ),


                   "activity":
                        state.get(
                            "activity",
                            0.0
                        ),


                   "delta":
                        state.get(
                            "signal",
                            0.0
                        )

                }
            )
        
        index = self.sampler.select(
            states,
            budget=1
        )

        if len(index)==0:
            
            return None
            
        winner_index=int(
            index[0]
        )
        winner = signals[
            winner_index
        ]  

        if self.memory is not None:
            #
            # save current candidates
            #
            self.memory.receive(
            {
                "type":
                    "selection_input",

                "signals":
                    [
                        {
                            "name":
                                s.get("name"),

                            "state":
                                s.get("state")
                        }

                        for s in signals
                    ],

                "available":
                    self.available
            }
            )
            
            self.memory.record_selection(
                [
                   {
                        "name":s.get("name"),
                        "state":s.get("state")
                    }

                    for s in signals
                ],

                {
                    "index":
                        winner_index,

                    "name":
                        winner["name"],

                    "state":
                        winner["state"]

                },
                step=self.step_count
            )
        
        return signals[
            winner_index
        ]
        
    def allocate(
        self,
        demand
    ):

        if demand is None:
            return {}


        if not isinstance(
            demand,
            dict
        ):
            return {}


        total = 0.0

        for value in demand.values():

            try:

                value = float(value)

            except Exception:

                continue


            if value > 0:

                total += value


        if total <= 0:
            return {}


        if self.available <= 0:
            return {}


        ratio = min(
            1.0,
            self.available / total
        )


        allocation = {}


        for name, value in demand.items():

            try:

                value = float(value)

            except Exception:

                value = 0.0


            if value < 0:
                value = 0.0


            allocation[name] = (
                value * ratio
            )


        allocated = sum(
            allocation.values()
        )


        self.consume(
            allocated
        )


        return allocation    
        
        
    def consume(
        self,
        amount
    ):
        
        if amount is None:
            return


        amount = max(
            float(amount),
            0.0
        )


        amount = min(
            amount,
            self.available
        )        
        
        self.available -= amount


        print(
            "MEMORY:",
            self.memory.debug_state()
        )