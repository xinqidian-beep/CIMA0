class InternalDynamicsObserver:


    def __init__(self):

        self.previous=None



    def observe(self,snapshot):

        current=snapshot


        delta=self.compare(
            self.previous,
            current
        )


        self.previous=current


        return {
            "state":current,
            "delta":delta
        }