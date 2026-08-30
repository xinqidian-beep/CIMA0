from .sampling.sampler import Sampler
from core.memory.observation_memory import ObservationMemory


class ComputeSystem:
    """
    CIMA0 Compute Field

    A local field of finite computational opportunity.

    Responsibilities:

        - regenerate compute availability
        - evaluate candidate signals
        - select one candidate
        - allocate a finite compute opportunity
        - consume the used opportunity

    Does NOT know:

        - organ meaning
        - organ internal rules
        - collision
        - decay
        - propagation
        - source
        - external representation

    Principle:

        ComputeSystem decides WHO gets an opportunity
        and HOW MUCH opportunity is available.

        The selected entity decides WHAT TO DO with it.
    """

    def __init__(
        self,
        capacity=1024,
        memory_capacity=32
    ):

        self.capacity = float(
            capacity
        )

        self.available = self.capacity

        #
        # observation / selection memory
        #

        self.memory = ObservationMemory(
            capacity=memory_capacity
        )

        self.sampler = Sampler()

        self.sampler.attach_memory(
            self.memory
        )

        self.step_count = 0


    # -------------------------------------------------
    # compute regeneration
    # -------------------------------------------------

    def step(self):

        recovery = (
            self.capacity
            -
            self.available
        ) * 0.01

        self.available += recovery

        self.available = min(
            self.available,
            self.capacity
        )


    # -------------------------------------------------
    # selection
    # -------------------------------------------------

    def select(
        self,
        signals
    ):
        """
        Select one candidate.

        Selection does not execute the candidate.

        Returns:

            {
                "name": ...,
                "organ": ...,
                "state": ...,
                "allocation": ...
            }

        or None.
        """

        if not signals:
            return None


        self.step_count += 1


        #
        # evaluate previous decision
        #

        if self.memory is not None:

            self.memory.evaluate_pending(
                signals
            )


        #
        # reduce candidate state to
        # selection-relevant information
        #

        states = []


        for signal in signals:

            state = signal.get(
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


        #
        # no compute opportunity
        #

        if self.available <= 0:

            return None


        #
        # available compute itself becomes
        # the upper bound of this opportunity
        #

        budget = min(
            1.0,
            self.available
        )


        index = self.sampler.select(
            states,
            budget=budget
        )


        if len(index) == 0:
            return None


        winner_index = int(
            index[0]
        )

        winner = signals[
            winner_index
        ]


        #
        # record selection context
        #

        if self.memory is not None:

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
                        "name":
                            s.get("name"),

                        "state":
                            s.get("state")
                    }

                    for s in signals
                ],

                {
                    "index":
                        winner_index,

                    "name":
                        winner.get(
                            "name"
                        ),

                    "state":
                        winner.get(
                            "state"
                        )
                },

                step=self.step_count
            )


        #
        # allocate opportunity
        #
        # ComputeSystem does NOT describe
        # what this opportunity means.
        #

        allocation = self.allocate(
            winner
        )


        if allocation is None:
            return None
            
            print(
                "COMPUTE WINNER:",
                winner.get("name")
            )

            print(
                "COMPUTE AVAILABLE BEFORE:",
                self.available
            )

            print(
                "COMPUTE ALLOCATION:",
                allocation
            )
            

        return {
            "name":
                winner.get("name"),

            "organ":
                winner.get("organ"),

            "state":
                winner.get("state"),

            "allocation":
                allocation
        }


    # -------------------------------------------------
    # allocation
    # -------------------------------------------------

    def allocate(
        self,
        winner
    ):
        """
        Allocate one unit of computational opportunity.

        The allocation is deliberately generic.

        ComputeSystem does not know whether the receiver
        will use it for collision, decay, propagation,
        inference, or anything else.
        """

        if winner is None:
            return None


        if self.available <= 0:
            return None


        amount = min(
            1.0,
            self.available
        )


        return {
            "amount":
                amount
        }


    # -------------------------------------------------
    # consume
    # -------------------------------------------------

    def consume(
        self,
        allocation
    ):
        """
        Consume an already allocated opportunity.

        Allocation must come from allocate().
        """

        if allocation is None:
            return 0.0


        if isinstance(
            allocation,
            dict
        ):

            amount = allocation.get(
                "amount",
                0.0
            )

        else:

            amount = allocation


        amount = max(
            float(amount),
            0.0
        )

        amount = min(
            amount,
            self.available
        )


        self.available -= amount


        return amount


    # -------------------------------------------------
    # state
    # -------------------------------------------------

    def snapshot(
        self
    ):

        return {
            "capacity":
                self.capacity,

            "available":
                self.available,

            "step":
                self.step_count
        }