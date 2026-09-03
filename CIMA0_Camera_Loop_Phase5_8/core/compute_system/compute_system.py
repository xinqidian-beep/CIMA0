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
        memory_capacity=32,
        recovery_rate=1.0
    ):

        self.capacity = float(
            capacity
        )

        self.available = self.capacity
        
        self.recovery_rate = max(
            float(recovery_rate),
            0.0
        )
        
        #
        # observation history
        #
        # Compute owns comparison context.
        #

        self.previous_observation = None

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
    # observation comparison
    # -------------------------------------------------

    def compare(
        self,
        observation
    ):
        """
        Compare current observation with the
        previous observation.

        Responsibility:

            current observation
                    +
            previous observation
                    |
                    v
                comparison
                    |
                    v
                observed change

        Does NOT:

            - modify dynamical state
            - select
            - commit
            - define evolution rules
            - infer causality
        """

        if observation is None:

            return None

        previous = self.previous_observation

        #
        # current becomes history only AFTER
        # comparison context has been obtained.
        #

        self.previous_observation = observation

        #
        # first observation has no comparison pair
        #

        if previous is None:

            return {
                "changed": False,
                "first": True,
                "changes": {}
            }

        return self._compare_observations(
            previous,
            observation
        )
        
        
    def _compare_observations(
        self,
        previous,
        current
    ):
        """
        Compare factual observation values.

        This is deliberately conservative.

        It does not infer an evolution law.

        It only reports observable numerical changes.
        """

        changes = {}

        #
        # -------------------------------------------------
        # compare top-level observed entities
        # -------------------------------------------------
        #

        names = set()

        if isinstance(previous, dict):

            names.update(
                previous.keys()
            )

        if isinstance(current, dict):

            names.update(
                current.keys()
            )

        for name in names:

            before = previous.get(
                name
            )

            after = current.get(
                name
            )

            if before is None or after is None:

                continue

            if not isinstance(
                before,
                dict
            ):

                continue

            if not isinstance(
                after,
                dict
            ):

                continue

            entity_changes = {}

            #
            # only compare values that actually exist
            # in both observations
            #

            keys = (
                set(before.keys())
                &
                set(after.keys())
            )

            for key in keys:

                b = before.get(
                    key
                )

                a = after.get(
                    key
                )

                #
                # scalar numerical values
                #

                if (
                    isinstance(
                        b,
                        (int, float)
                    )
                    and
                    isinstance(
                        a,
                        (int, float)
                    )
                ):

                    delta = float(a) - float(b)

                    if delta != 0.0:

                        entity_changes[key] = {
                            "before": float(b),
                            "after": float(a),
                            "delta": delta
                        }

            if entity_changes:

                changes[name] = entity_changes

        return {
            "changed": bool(changes),
            "first": False,
            "changes": changes
        }
        


    # -------------------------------------------------
    # compute regeneration
    # -------------------------------------------------

    def step(
        self
    ):

        self.step_count += 1


        #
        # compute resource recovery
        #
        # recover 1% of the remaining gap
        # between available and capacity.
        #

        self.available += (
            self.capacity
            -
            self.available
        ) * 0.01


        #
        # capacity is the absolute upper bound
        #

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