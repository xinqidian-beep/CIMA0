class LocalCoupling:


    def __init__(
        self,
        strength=0.01
    ):

        self.strength=strength

        self.pending=[]



    def connect(
        self,
        a,
        b,
        strength=None
    ):

        if strength is None:
            strength=self.strength


        self.pending.append(
            (
                a,
                b,
                strength
            )
        )



    def apply(self):

        for a,b,s in self.pending:


            da = (
                b.x-a.x
            )*s


            db = (
                a.x-b.x
            )*s


            a.add_field(da)

            b.add_field(db)



        self.pending.clear()