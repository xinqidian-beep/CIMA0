class CameraCompute:
    """
    External camera computation resource.


    Responsibility:

        estimate own available computation
        recover own resource
        grant temporary computation slots


    No:

        image understanding
        sampling decision
        priority judgment
        control
        memory
    """



    def __init__(
        self,
        capacity_slots=10000,
        recovery_rate=0.05
    ):


        #
        # maximum temporary capability
        #

        self.capacity_slots = int(
            capacity_slots
        )


        #
        # current available resource
        #

        self.available_slots = (
            self.capacity_slots
        )


        #
        # natural recovery
        #

        self.recovery_rate = (
            recovery_rate
        )



    def step_compute(
        self
    ):
        """
        Resource self recovery.

        No external dependency.
        """


        self.available_slots += (

            self.capacity_slots -
            self.available_slots

        ) * self.recovery_rate



        if (
            self.available_slots >
            self.capacity_slots
        ):

            self.available_slots = (
                self.capacity_slots
            )



    def grant_ephemeral_slots(
        self,
        request_ephemeral
    ):
        """
        Respond to temporary computation request.


        Input:

            request_ephemeral

        Output:

            temporary granted slots


        Does not know:

            request source
            image structure
            sampling location
        """



        if request_ephemeral < 0:

            request_ephemeral = 0



        grant_slots = min(

            int(
                request_ephemeral
            ),

            int(
                self.available_slots
            )

        )



        #
        # consume computation
        #

        self.available_slots -= (
            grant_slots
        )



        if self.available_slots < 0:

            self.available_slots = 0



        return {

            "compute_slots_ephemeral":

                grant_slots

        }



    def snapshot(
        self
    ):

        return {

            "compute_capacity":
                self.capacity_slots,


            "compute_available_ephemeral":
                self.available_slots

        }