import numpy as np


class DisplayIO:
    def __init__(self):
        pass

    def encode(self, snapshot):
        if snapshot is None:
            return None

        activity = float(snapshot.get("activity", 0.0))
        planet = snapshot.get("planet") or {}
        clip = snapshot.get("clip") or {}

        planet_activity = float(planet.get("activity", 0.0))
        clip_activity = float(clip.get("activity", 0.0))
        focus_layer = clip.get("focus_layer", None)
        emb_activity = float(clip.get("embedding_activity", 0.0))

        print(
            "DISPLAY INPUT",
            "obs=", activity,
            "planet=", planet_activity,
            "clip=", clip_activity,
            "focus=", focus_layer,
            "emb=", emb_activity,
        )

        h, w = 32, 240
        frame = np.zeros((h, w, 3), dtype=np.uint8)

        def clamp01(x):
            return max(0.0, min(1.0, float(x)))

        obs_bar = int(clamp01(activity) * (w - 1))
        planet_bar = int(clamp01(planet_activity) * (w - 1))
        clip_bar = int(clamp01(clip_activity) * (w - 1))
        emb_bar = int(clamp01(emb_activity) * (w - 1))

        frame[2:6, :obs_bar, 0] = 255
        frame[10:14, :planet_bar, 1] = 255
        frame[18:22, :clip_bar, 2] = 255
        frame[26:30, :emb_bar, :] = 180

        if focus_layer is not None:
            x = int((focus_layer + 1) * w / 8)
            x = max(0, min(w - 1, x))
            frame[:, x:x+2, :] = 255

        return frame