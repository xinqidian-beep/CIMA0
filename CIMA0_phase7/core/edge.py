class Edge:

    def __init__(self,a,b,w=0.5):

        self.a=a
        self.b=b
        self.w=w


    def update(self,cells):

        ca=cells[self.a]
        cb=cells[self.b]

        correlation = ca.x * cb.x

        self.w += 0.00001 * correlation

        self.w *= 0.99999


        if self.w<0:
            self.w=0


    def alive(self):

        return self.w>0.01