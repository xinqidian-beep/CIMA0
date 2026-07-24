class SparseCompute:


    def __init__(self):

        self.field={}



    def compress(
        self,
        observations
    ):


        for idx,state in observations:


            old=self.field.get(
                idx
            )


            if old is None:


                self.field[idx]={

                    "mean_energy":
                        state["energy"],

                    "activity":
                        state["activity"],

                    "samples":1

                }


            else:


                n=old["samples"]


                old["mean_energy"]=(

                    old["mean_energy"]*n

                    +

                    state["energy"]

                )/(n+1)


                old["activity"]=(

                    old["activity"]*0.99

                    +

                    state["activity"]*0.01

                )


                old["samples"]+=1




    def expand_candidates(self):

        """
        计算系统自己的需要

        不是控制动力

        """

        result=[]


        for idx,data in self.field.items():


            if data["samples"]>10:

                result.append(idx)



        return result