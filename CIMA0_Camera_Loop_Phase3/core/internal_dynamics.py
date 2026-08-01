import numpy as np


class InternalDynamics:
    def __init__(self, planet, clip):
        self.planet = planet
        self.clip = clip
        self.external_bytes = b""

    def receive(self, data):
        self.external_bytes = data

    def _to_frame(self, x):
        if x is None:
            return None

        arr = np.asarray(x, dtype=np.float32)
        if arr.size == 0:
            return None

        arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
        arr = arr - np.min(arr)
        mx = np.max(arr)
        if mx > 0:
            arr = arr / mx

        arr = (arr * 255.0).clip(0, 255).astype(np.uint8)

        if arr.ndim == 1:
            arr = arr[None, :]

        return arr

    def step(self):
        if hasattr(self.planet, "inject"):
            self.planet.inject(self.external_bytes)

        self.planet.step()

        frame = None

        for name in ("frame", "image", "render", "output"):
            if hasattr(self.planet, name):
                obj = getattr(self.planet, name)
                frame = obj() if callable(obj) else obj
                if frame is not None:
                    break

        if frame is None:
            for name in ("state", "field", "matrix"):
                if hasattr(self.planet, name):
                    candidate = getattr(self.planet, name)
                    frame = candidate() if callable(candidate) else candidate
                    if frame is not None:
                        frame = self._to_frame(frame)
                        break

        if frame is not None and hasattr(self.clip, "update"):
            self.clip.update(frame)

    def snapshot(self):
        planet_snapshot = None
        if hasattr(self.planet, "snapshot"):
            planet_snapshot = self.planet.snapshot()
        else:
            planet_snapshot = {
                "state": getattr(self.planet, "state", None),
                "velocity": getattr(self.planet, "velocity", None),
                "energy": getattr(self.planet, "energy", None),
                "phase": getattr(self.planet, "phase", None),
            }

        clip_snapshot = None
        if hasattr(self.clip, "state"):
            clip_snapshot = self.clip.state()
        elif hasattr(self.clip, "snapshot"):
            clip_snapshot = self.clip.snapshot()
        else:
            clip_snapshot = {}

        return {
            "planet": planet_snapshot,
            "clip": clip_snapshot,
        }