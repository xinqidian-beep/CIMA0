import numpy as np


class AdaptiveTopology:


    def __init__(
        self,
        n,
        initial_edges
    ):

        self.n = n


        # connection weights

        self.weights = {}


        for a,b in initial_edges:

            key = (
                min(a,b),
                max(a,b)
            )

            self.weights[key] = 0.5



        self.update_count = 0



    def get_weight(
        self,
        a,
        b
    ):


        key = (
            min(a,b),
            max(a,b)
        )


        return self.weights.get(
            key,
            0.5
        )



    def update(
        self,
        states
    ):

        """
        slow local topology drift

        no goal
        no optimization
        no pruning

        """

        self.update_count += 1



        xs=np.asarray(
            states,
            dtype=float
        )


        for key,w in list(
            self.weights.items()
        ):


            a,b=key


            if (
                a>=len(xs)
                or
                b>=len(xs)
            ):
                continue



            #
            # local correlation
            #

            interaction = (

                abs(
                    xs[a]*xs[b]
                )

            )



            #
            # slow drift
            #

            dw = (

                0.00001 *

                (
                    interaction
                    -
                    w
                )

            )



            self.weights[key] += dw



            #
            # physical lower/upper boundary
            #

            if self.weights[key] < 0:

                self.weights[key]=0.0


            if self.weights[key] > 2:

                self.weights[key]=2.0




    def stats(self):


        if len(self.weights)==0:


            return {

                "weight_mean":0.0,

                "weight_std":0.0

            }



        values=np.array(

            list(
                self.weights.values()
            )

        )


        return {


            "weight_mean":

                float(
                    values.mean()
                ),


            "weight_std":

                float(
                    values.std()
                ),


            "connections":

                len(
                    values
                )

        }