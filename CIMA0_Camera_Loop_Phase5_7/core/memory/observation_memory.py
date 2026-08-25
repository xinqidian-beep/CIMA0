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
        historical pressure
    """

    def __init__(
        self,
        capacity=128
    ):

        self.capacity = capacity

        self.records =deque(
            maxlen=capacity
        )
    def statistics(self):

        if len(self.records)==0:
            return {
                "age":0.0,
                "activity":0.0,
                "delta":0.0
            }


        age=0
        activity=0
        delta=0


        count=0


        for record in self.records:

            signals=record.get(
                "signals",
                []
            )


            for signal in signals:

                state=signal.get(
                    "state",
                    {}
                )

                age += float(
                    state.get(
                        "age",
                        0
                    )
                )

                activity += float(
                    state.get(
                        "activity",
                        0
                    )
                )

                delta += float(
                    state.get(
                        "delta",
                        0
                    )
                )

                count += 1


        if count==0:
            return {
                "age":0.0,
                "activity":0.0,
                "delta":0.0
            }


        return {
            "age":age/count,
            "activity":activity/count,
            "delta":delta/count
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
                self.pressure()

        }