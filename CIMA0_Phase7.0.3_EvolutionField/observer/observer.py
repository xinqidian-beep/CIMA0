import numpy as np


class Observer:

    def __init__(self):
        self.history = []


    def record(self, response):

        response = np.asarray(
            response,
            dtype=np.float64
        )

        info = {
            "std": float(np.std(response)),
            "mean": float(np.mean(response)),
            "active": int(
                np.sum(
                    np.abs(response) > 1e-8
                )
            )
        }

        self.history.append(info)

        # 只保留最近一段
        if len(self.history) > 1000:
            self.history.pop(0)


        return info