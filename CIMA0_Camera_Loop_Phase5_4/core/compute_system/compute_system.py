from .sampling.sampler import Sampler

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

        self.sampler = Sampler()
    
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



        index = self.sampler.select(
            signals,
            budget=1
        )

        if winner is None:
            
            return None
            
        return signals[index]
        
    def consume(
        self,
        amount=1
    ):
        
        self.available -= float(
            amount
        )


        self.available = max(
            self.available,
            0
        )



