class Lifecycle:


    def __init__(self):

        self.history=[]



    def update(
        self,
        step,
        observation
    ):


        record={

            "step":step,

            "clusters":
                observation["clusters"],

            "max_cluster":
                observation["max_cluster"],

            "phase_std":
                observation["phase_std"]

        }


        self.history.append(
            record
        )



    def summary(self):

        return {

            "samples":
                len(self.history),

            "max_seen_cluster":
                max(
                    [
                        x["max_cluster"]
                        for x in self.history
                    ]
                )

        }