class LocalCoupling:


    def __init__(
        self,
        strength=0.01
    ):

        self.strength=strength

        self.links=[]



    def clear(self):

        self.links=[]



    def connect(
        self,
        a,
        b,
        strength=None
    ):

        if strength is None:
            strength=self.strength


        self.links.append(
            (
                a,
                b,
                strength
            )
        )



    def apply(self):

        for a,b,w in self.links:


            dx=(b.x-a.x)*w


            a.add_field(
                dx
            )

            b.add_field(
                -dx
            )