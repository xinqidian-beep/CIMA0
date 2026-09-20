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
        recovery_rate=1.0,
        sampler=None
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
        # observation / selection memory
        #

        self.memory = ObservationMemory(
            capacity=memory_capacity
        )
        
        if sampler is None:
            sampler = Sampler()

        self.sampler = sampler

        self.sampler.attach_memory(
            self.memory
        )

        self.step_count = 0
        

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
        Select one internal candidate and allocate
        one finite compute opportunity.

        Responsibilities of ComputeSystem:

            1. receive internal compute requests
            2. determine candidate eligibility
            3. build the competition set
            4. ask Sampler to select
            5. allocate compute resource
            6. record the selection

        ComputeSystem owns the permission.

        Sampler only performs selection.
        Organ only raises candidates and executes
        after receiving compute permission.

        No organ execution happens here.
        """

        #
        # --------------------------------------------------
        # 0. no signals
        # --------------------------------------------------
        #

        if not signals:
            return None


        #
        # --------------------------------------------------
        # 1. Compute evaluates pending memory
        #
        #    Memory observes/records the competition context.
        #    It does not grant permission.
        # --------------------------------------------------
        #

        if self.memory is not None:

            self.memory.evaluate_pending(
                signals
            )


        #
        # --------------------------------------------------
        # 2. Build eligible compute requests
        #
        #    Organ only says:
        #
        #        request = "compute"
        #        candidate
        #        candidate_value
        #
        #    Compute decides whether the request
        #    is eligible to enter competition.
        # --------------------------------------------------
        #

        requests = []

        for signal in signals:

            state = signal.get(
                "state",
                {}
            )

            if not isinstance(
                state,
                dict
            ):
                continue


            #
            # Organ must explicitly request compute.
            #

            request = state.get(
                "request"
            )

            if request != "compute":
                continue


            #
            # Internal candidate.
            #

            candidate = state.get(
                "candidate"
            )


            #
            # Internal candidate strength.
            #

            candidate_value = state.get(
                "candidate_value",
                0.0
            )


            #
            # Compute owns candidate eligibility.
            #
            # No candidate:
            #     no competition.
            #
            # Non-positive candidate value:
            #     currently treated as no valid
            #     compute candidate.
            #

            #if candidate is None:
            #    continue

            try:
                candidate_value = float(
                    candidate_value
                )
            except (
                TypeError,
                ValueError
            ):
                candidate_value = 0.0  
            #    continue

            #if candidate_value <= 0.0:
            #    continue
            

            #
            # Candidate is now admitted into
            # the Compute competition field.
            #

            requests.append(
                signal
            )


        #
        # --------------------------------------------------
        # 3. No eligible candidate
        # --------------------------------------------------
        #

        if not requests:
            return None


        #
        # --------------------------------------------------
        # 4. Compute resource availability
        # --------------------------------------------------
        #

        if self.available <= 0:
            return None


        #
        # --------------------------------------------------
        # 5. Convert eligible requests into
        #    Sampler-compatible generic states.
        #
        #    Sampler remains semantically blind.
        #
        #    It does NOT know:
        #
        #        candidate
        #        candidate_value
        #        organ
        #        compute
        #        source
        #
        #    It only receives:
        #
        #        age
        #        activity
        #        delta
        # --------------------------------------------------
        #

        states = []

        for signal in requests:

            state = signal.get(
                "state",
                {}
            )

            states.append(
                {
                    "age": state.get(
                        "age",
                        0.0
                    ),

                    "activity": state.get(
                        "activity",
                        0.0
                    ),

                    "delta": state.get(
                        "signal",
                        0.0
                    )
                }
            )


        #
        # --------------------------------------------------
        # 6. Debug: show candidates entering Compute
        #
        #    This is deliberately before Sampler.
        # --------------------------------------------------
        #

        print(
            "COMPUTE CANDIDATES:",
            [
                {
                    "name": signal.get("name"),
                    "candidate":
                        signal.get(
                            "state",
                            {}
                        ).get(
                            "candidate"
                        ),
                    "candidate_value":
                        signal.get(
                            "state",
                            {}
                        ).get(
                            "candidate_value",
                            0.0
                        ),
                    "age":
                        signal.get(
                            "state",
                            {}
                        ).get(
                            "age",
                            0.0
                        ),
                    "activity":
                        signal.get(
                            "state",
                            {}
                        ).get(
                            "activity",
                            0.0
                        ),
                    "delta":
                        signal.get(
                            "state",
                            {}
                        ).get(
                            "signal",
                            0.0
                        )
                }
                for signal in requests
            ]
        )


        #
        # --------------------------------------------------
        # 7. Sampler performs selection only
        # --------------------------------------------------
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


        #
        # --------------------------------------------------
        # 8. Recover the actual winner
        #
        #    Sampler only returned an index.
        #    Compute maps it back to the actual
        #    internal request.
        # --------------------------------------------------
        #

        winner_index = int(
            index[0]
        )

        winner = requests[
            winner_index
        ]


        #
        # --------------------------------------------------
        # 9. Record selection
        #
        #    Memory records what Compute selected.
        #    Memory does not make the decision.
        # --------------------------------------------------
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
                                    s.get(
                                        "name"
                                    ),

                                "state":
                                    s.get(
                                        "state"
                                    )
                            }

                            for s in requests
                        ],

                    "available":
                        self.available
                }
            )

            self.memory.record_selection(
                [
                    {
                        "name":
                            s.get(
                                "name"
                            ),

                        "state":
                            s.get(
                                "state"
                            )
                    }

                    for s in requests
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
        # --------------------------------------------------
        # 10. Compute allocates resource
        #
        #     This is the actual permission boundary.
        # --------------------------------------------------
        #

        allocation = self.allocate(
            winner
        )

        if allocation is None:
            return None


        #
        # --------------------------------------------------
        # 11. Return the Compute decision
        #
        #     No execution here.
        #
        #     commit() will consume the allocation
        #     and grant it to the organ.
        # --------------------------------------------------
        #

        return {
            "name":
                winner.get(
                    "name"
                ),

            "organ":
                winner.get(
                    "organ"
                ),

            "state":
                winner.get(
                    "state"
                ),

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