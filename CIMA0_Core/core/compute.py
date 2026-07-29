class ComputeSystem:


    def __init__(self):

        self.budget = 1.0



    def allocate(
        self,
        signal
    ):

        deviation = signal["deviation"]


        if deviation > 0.8:

            return {
                "radius":8,
                "resolution":4
            }


        elif deviation > 0.4:

            return {
                "radius":4,
                "resolution":2
            }


        else:

            return {
                "radius":2,
                "resolution":1
            }