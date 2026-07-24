class SparseCompute:


    def __init__(self, region_size=64):

        self.region_size=region_size

        self.field={}



    def region(self, idx):

        return idx // self.region_size



    def compress(self, observations):


        for idx,state in observations:


            r=self.region(idx)


            if r not in self.field:

                self.field[r]={
                    "energy":state["energy"],
                    "activity":state["activity"],
                    "count":1
                }

            else:

                f=self.field[r]

                n=f["count"]


                f["energy"]=(
                    f["energy"]*n
                    +
                    state["energy"]
                )/(n+1)


                f["activity"]=(
                    f["activity"]*0.99
                    +
                    state["activity"]*0.01
                )


                f["count"]+=1