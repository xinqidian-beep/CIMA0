from collections import deque


class TemporalSnapshot:
    """
    Observation time window.

    Only stores sampled history.

    Does not:
        modify cell
        influence dynamics
        control world

    Data will be overwritten.
    """

    def __init__(self, window_size=32):
        self.window = deque(
            maxlen=window_size
        )


    def push(self, time, states):

        self.window.append(
            {
                "time": time,
                "states": states
            }
        )


    def latest(self):

        if not self.window:
            return None

        return self.window[-1]


    def history(self):

        return list(self.window)


    def size(self):

        return len(self.window)