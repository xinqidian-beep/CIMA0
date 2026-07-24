import numpy as np



class Observer:


    def __init__(self,n):

        self.last=np.zeros(n)

        self.activity=np.zeros(n)



    def read(self,x):


        change=np.abs(

            x-self.last

        )


        self.activity*=0.999


        self.activity += change*0.001


        self.last=x.copy()



        return self.activity