from core.oscillator import Oscillator


class Cell:


    def __init__(
        self,
        idx,
        x,
        v
    ):

        self.id=idx


        self.oscillator=Oscillator(
            x,
            v
        )


        self.neighbors=[]


        # 自己的局部时间
        self.local_time=0



    def interact(self):

        field=0.0


        for n,w in self.neighbors:

            dx=(
                n.oscillator.x
                -
                self.oscillator.x
            )

            field += w*dx


        return field



    def update(self):

        field=self.interact()


        self.oscillator.step(
            field
        )


        self.local_time+=1