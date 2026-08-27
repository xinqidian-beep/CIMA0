import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_7


    Heterogeneous cloud collision.


    Input:


        PlanetField

            |

            v

        planet_cloud


        CLIPField

            |

            v

        clip_cloud



    Collision is not:

        field matching


    Collision is:

        state relationship comparison



    Does NOT:


        modify cloud


        select winner


        allocate compute


        interpret meaning

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



        if (
            "cloud" not in planet_cloud
            or
            "cloud" not in clip_cloud
        ):

            return None



        planet_state = (
            planet_cloud["cloud"]
        )


        clip_state = (
            clip_cloud["cloud"]
        )



        #
        # three-state collision
        #

        result = self._compare(
            planet_state,
            clip_state
        )


        self.last_result = result


        return result




    def _compare(
        self,
        planet,
        clip
    ):


        keys = (

            "mean",

            "energy",

            "variance",

            "density"

        )



        distance = {}

        collision_score = 0.0



        valid = 0



        for key in keys:


            if (
                key not in planet
                or
                key not in clip
            ):

                continue



            a = float(
                planet[key]
            )


            b = float(
                clip[key]
            )



            d = abs(
                a-b
            )


            distance[key] = d


            collision_score += d


            valid += 1



        if valid == 0:

            return None



        collision_score /= valid



        collision = (

            collision_score
            <
            self.threshold

        )



        #
        # three value state
        #

        empty_state = self._match(

            planet.get(
                "density",
                0.0
            ),

            clip.get(
                "density",
                0.0
            ),

            0.0

        )



        zero_state = self._match(

            planet.get(
                "energy",
                0.0
            ),

            clip.get(
                "energy",
                0.0
            ),

            0.0

        )



        negative_state = (

            np.sign(
                planet.get(
                    "mean",
                    0.0
                )
            )

            ==
            
            np.sign(
                clip.get(
                    "mean",
                    0.0
                )
            )

        )



        interaction = 0.0


        if collision:


            interaction = (

                planet.get(
                    "energy",
                    0.0
                )

                +

                clip.get(
                    "energy",
                    0.0
                )

            ) / 2.0



        return {


            "collision":

                collision,



            "distance":

                distance,



            "collision_score":

                float(
                    collision_score
                ),



            "planet_activity":

                float(
                    planet.get(
                        "energy",
                        0.0
                    )
                ),



            "clip_activity":

                float(
                    clip.get(
                        "energy",
                        0.0
                    )
                ),



            "empty_match":

                bool(
                    empty_state
                ),



            "zero_match":

                bool(
                    zero_state
                ),



            "negative_match":

                bool(
                    negative_state
                ),



            "interaction":

                float(
                    interaction
                )

        }




    def _match(
        self,
        a,
        b,
        target
    ):


        return (

            abs(
                float(a)
                -
                target
            )
            <
            self.threshold

            and

            abs(
                float(b)
                -
                target
            )
            <
            self.threshold

        )