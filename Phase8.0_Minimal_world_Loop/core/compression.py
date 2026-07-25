class Compression:


    def __init__(self):

        self.history = []



    def record(
        self,
        universe
    ):

        self.history.append(

            {
                "time":
                    universe.time,

                "environment":
                    universe.environment.field
            }

        )


        # keep compressed history

        if len(self.history)>1000:

            self.history.pop(0)



    def snapshot(self):

        return self.history[-1]