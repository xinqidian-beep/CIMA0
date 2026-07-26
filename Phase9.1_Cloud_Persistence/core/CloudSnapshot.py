class CloudSnapshot:

    def __init__(self):

        self.data = {}


    def capture(self, cloud, t):

        field = cloud.field


        active = ~np.isnan(field)


        self.data = {

            "time": t,

            "active":
                int(np.sum(active)),

            "mean":
                float(
                    np.nanmean(field)
                )
                if np.any(active)
                else 0.0,


            "std":
                float(
                    np.nanstd(field)
                )
                if np.any(active)
                else 0.0,


            "max":
                float(
                    np.nanmax(field)
                )
                if np.any(active)
                else 0.0,


            "min":
                float(
                    np.nanmin(field)
                )
                if np.any(active)
                else 0.0
        }


        return self.data