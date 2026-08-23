import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_7

    Interaction field between clouds.


    Input:

        planet cloud
        clip cloud


    Output:

        collision response


    Does NOT:

        modify cloud

        allocate compute

        decide winner

        understand meaning

    """



    def __init__(
        self,
        threshold=0.05
    ):

        self.threshold = threshold


        self.last_result = None



    def collide(
        self,
        planet_cloud,
        clip_cloud
    ):


        if planet_cloud is None:

            return None


        if clip_cloud is None:

            return None



        planet_values = self._extract(
            planet_cloud
        )


        clip_values = self._extract(
            clip_cloud
        )


        if len(planet_values)==0:

            return None


        if len(clip_values)==0:

            return None



        result = self._compare(
            planet_values,
            clip_values
        )


        self.last_result = result


        return result



    def _extract(
        self,
        cloud
    ):

        values=[]


        for cell in cloud.cells:

            if cell.empty:

                continue


            values.append(
                cell.value
            )


        return np.asarray(
            values,
            dtype=np.float32
        )



    def _compare(
        self,
        a,
        b
    ):


        distance = abs(
            np.mean(a)
            -
            np.mean(b)
        )


        if distance < self.threshold:


            interaction = (
                np.mean(a)
                +
                np.mean(b)
            ) / 2.0


            return {

                "collision":
                    True,


                "distance":
                    float(distance),


                "interaction":
                    float(interaction),


                "planet":
                    float(np.mean(a)),


                "clip":
                    float(np.mean(b))

            }



        return {


            "collision":
                False,


            "distance":
                float(distance),


            "interaction":
                0.0,


            "planet":
                float(np.mean(a)),


            "clip":
                float(np.mean(b))

        }