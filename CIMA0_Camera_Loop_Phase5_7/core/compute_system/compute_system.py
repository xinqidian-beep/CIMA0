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
            
        self.memory.receive(
            {
                "signals":
                [
                    {
                        "name": s.get("name"),
                        "state": s.get("state")
                    }
                    for s in signals
                ],

                "available":
                    self.available
            }
        )
            
        index = self.sampler.select(
            [
                s["state"]
                for s in signals
            ],
            budget=1
        )

        if len(index)==0:
            
            return None
            
        winner_index=int(
            index[0]
        )
            
        return signals[
            winner_index
        ]
        
    def consume(
        self,
        amount=1
    ):
        self.available=max(
            self.available,
            0
        )
        
        amount=min(
            float(amount),
            self.available
        )

        self.available-=amount

        print(
            "MEMORY:",
            self.memory.debug_state()
        )
