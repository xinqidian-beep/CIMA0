class DisplayIO:
    """
    Display boundary IO.


    Responsibility:

        transfer internal output frame
        to display hardware


    No:

        rendering
        conversion
        enhancement
    """


    def output_frame(
        self,
        frame
    ):

        return frame