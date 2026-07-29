import numpy as np



class Observer:


    """
    只观察

    不控制动力
    """


    def scan(
        self,
        snapshot
    ):


        activity = np.abs(snapshot)


        index = np.unravel_index(
            np.argmax(activity),
            activity.shape
        )


        value = activity[index]


        return {

            "center":index,
            "deviation":float(value)

        }



    def sample(
        self,
        snapshot,
        budget
    ):

        x,y = budget["center"]

        r = budget["radius"]


        x1=max(0,x-r)
        x2=min(snapshot.shape[0],x+r)

        y1=max(0,y-r)
        y2=min(snapshot.shape[1],y+r)


        return snapshot[x1:x2,y1:y2]