class SparseCompute:


    def __init__(self):

        self.compressed={}



    def receive(
        self,
        observations
    ):

        for idx,activity in observations:


            if idx not in self.compressed:

                self.compressed[idx]={
                    "activity":activity,
                    "age":0
                }

            else:

                self.compressed[idx]["activity"] = (
                    self.compressed[idx]["activity"]*0.99
                    +
                    activity*0.01
                )



    def select_precision(self):

        """
        不是top-k排序

        只是概率展开
        """

        result=[]


        for idx,data in self.compressed.items():

            if data["activity"] > 0.02:

                result.append(idx)


        return result