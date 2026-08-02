# core/internal_dynamics_observer.py


class InternalDynamicsObserver:
    """
    Read-only observation boundary.

    Responsibility:

        internal request
              |
              v

        consume observation resource
              |
              v

        output snapshot


    Does NOT:

        interpret
        merge
        classify
        control
        select
    """


    def __init__(self):

        self.resource = 0



    def update_resource(
        self,
        resource
    ):
        """
        Resource comes from Compute.

        Observer does not request.
        """

        self.resource = max(
            0,
            int(resource)
        )



    def observe(
        self,
        internal_state
    ):
        """
        Consume available observation resource.

        Internal state decides what can be observed.
        """

        if internal_state is None:
            return None


        if hasattr(
            internal_state,
            "observe"
        ):

            return internal_state.observe(
                self.resource
            )


        return internal_state