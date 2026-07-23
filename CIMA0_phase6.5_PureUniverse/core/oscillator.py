class Oscillator:

    @staticmethod
    def coupling(
        a,
        b,
        strength=0.05
    ):

        return (
            strength *
            (b.x-a.x)
        )