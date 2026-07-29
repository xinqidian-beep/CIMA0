import numpy as np


class CloudField:
    """
    Minimal three-value cloud dynamics.


    Own state:

        cloud_void
        cloud_neg
        cloud_act


    External influence:

        io disturbance
        sampling disturbance


    Does not:

        - understand meaning
        - control dynamics
        - know observer
        - know global state

    """


    def __init__(
        self,
        cloud_size=64,
        cloud_decay_rate=0.001
    ):

        self.cloud_size = int(
            cloud_size
        )


        #
        # Three topology states
        #

        self.cloud_state_void = (
            np.ones(
                (
                    self.cloud_size,
                    self.cloud_size
                ),
                dtype=bool
            )
        )


        self.cloud_state_neg = (
            np.zeros(
                (
                    self.cloud_size,
                    self.cloud_size
                ),
                dtype=np.float64
            )
        )


        self.cloud_state_act = (
            np.zeros(
                (
                    self.cloud_size,
                    self.cloud_size
                ),
                dtype=np.float64
            )
        )


        #
        # Ephemeral disturbances
        #

        self.cloud_ephemeral_io_disturbance = 0.0

        self.cloud_ephemeral_sample_disturbance = 0.0


        self.cloud_decay_rate = float(
            cloud_decay_rate
        )



    def receive_cloud_ephemeral_disturbance(
        self,
        value
    ):
        """
        Receive temporary disturbance.

        Source is unknown.

        It may come from:
            external boundary
            internal sampling

        Cloud does not care.

        """

        self.cloud_ephemeral_disturbance = float(
            value
        )



    def receive_sample_ephemeral_disturbance(
        self,
        sample_ephemeral_value
    ):

        """
        Receive internal observation disturbance.

        Observer does not control cloud.

        It only creates a temporary influence.

        """

        self.cloud_ephemeral_sample_disturbance = (
            float(sample_ephemeral_value)
        )



    def step_cloud_dynamics(
        self
    ):

        """
        Cloud autonomous evolution.

        Disturbance changes tendency,
        not direct state replacement.

        """


        cloud_ephemeral_force = (

            self.cloud_ephemeral_io_disturbance

            +

            self.cloud_ephemeral_sample_disturbance

        )



        #
        # Local three-value transition
        #

        if cloud_ephemeral_force > 0:


            self.cloud_state_act += (
                cloud_ephemeral_force
                *
                0.01
            )


        elif cloud_ephemeral_force < 0:


            self.cloud_state_neg += (
                abs(
                    cloud_ephemeral_force
                )
                *
                0.01
            )


        else:

            #
            # no disturbance:
            # void gradually appears
            #

            self.cloud_state_act *= (
                1.0
                -
                self.cloud_decay_rate
            )

            self.cloud_state_neg *= (
                1.0
                -
                self.cloud_decay_rate
            )



        #
        # Topology update
        #

        self.cloud_state_void[:] = (
            (
                np.abs(
                    self.cloud_state_act
                )
                <
                1e-9
            )

            &

            (
                np.abs(
                    self.cloud_state_neg
                )
                <
                1e-9
            )
        )



        #
        # Temporary influence disappears
        #

        self.cloud_ephemeral_io_disturbance = 0.0

        self.cloud_ephemeral_sample_disturbance = 0.0



    def project_ephemeral_local_state(
        self,
        cloud_y,
        cloud_x
    ):

        """
        Local black-box projection.

        No global understanding.

        """

        return {

            "cloud_local_act":

                float(
                    self.cloud_state_act[
                        cloud_y,
                        cloud_x
                    ]
                ),


            "cloud_local_neg":

                float(
                    self.cloud_state_neg[
                        cloud_y,
                        cloud_x
                    ]
                ),


            "cloud_local_void":

                bool(
                    self.cloud_state_void[
                        cloud_y,
                        cloud_x
                    ]
                )

        }