import numpy as np

from core.io.transport.packet import BitPacket


class CameraObserver:
    """
    CIMA0 Camera Observer / sampling module.

    Input:

        BitPacket(camera_raw)

    Output:

        BitPacket(camera_observation)

    Function subdivision (module self-holding):

        activity()      : raise hand (signal)
        _sample()       : local sampling (gray + layered sparse)
        _local_exact()  : focus exact (full delta)

    System internal drive:

        received via IO (receive), not held as references.
        this keeps module self-holding.

    exact_rhythm_base:

        state offset, affected by system internal drive,
        but does not change rules or timing.

    Does NOT:

        - know what other modules need
        - decide global consistency
        - discard unused information
        - change timing
    """

    def __init__(self):
        self.previous = None
        self.field = None
        self.age = 0

        #
        # internal drive: received via IO
        #
        self.internal_drive = None

        #
        # internal rhythm for focus exact
        #
        self.exact_rhythm = 0
        self.exact_rhythm_base = 10.0

    #
    # receive internal drive (disturbance)
    #
    def receive(self, packet):
        if packet is None:
            return

        if packet.tag != "internal_drive":
            return

        self.internal_drive = dict(packet.meta)

    #
    # raise hand
    #
    def activity(self):
        if self.previous is None:
            return {
                "activity": 1.0,
                "signal": 1.0,
                "changed": True,
                "source": "camera",
                "age": self.age,
            }

        delta = np.mean(
            np.abs(
                self.field.astype(np.int16)
                - self.previous.astype(np.int16)
            )
        )

        return {
            "activity": float(delta),
            "signal": float(delta),
            "changed": bool(delta > 0),
            "source": "camera",
            "age": self.age,
        }

    #
    # local sampling
    #
    def _sample(self):
        if self.field is None:
            return None

        gray = self._to_gray(self.field)
        prev_gray = (
            self._to_gray(self.previous)
            if self.previous is not None
            else None
        )

        height, width = gray.shape

        root = (0, 0, height, width)
        path = []
        region = root
        level = 0

        while True:
            children = self._split_region(region)
            if len(children) == 1:
                break

            candidates = []
            for child in children:
                signal = self._region_hand(gray, prev_gray, child)
                candidates.append({"region": child, "signal": signal})

            winner = max(candidates, key=lambda item: item["signal"])
            region = winner["region"]
            path.append({
                "level": level,
                "region": region,
                "signal": float(winner["signal"]),
            })
            level += 1

            x0, y0, x1, y1 = region
            if x1 - x0 <= 1 and y1 - y0 <= 1:
                break

        return {"path": path, "region": region, "level": level}

    def _to_gray(self, frame):
        if frame.ndim == 3 and frame.shape[2] == 3:
            return frame.astype(np.float32).mean(axis=2)
        return frame.astype(np.float32)

    def _split_region(self, region):
        x0, y0, x1, y1 = region
        if x1 - x0 <= 1 and y1 - y0 <= 1:
            return [region]

        xm = x0 + (x1 - x0) // 2
        ym = y0 + (y1 - y0) // 2

        children = [
            (x0, y0, xm, ym),
            (x0, ym, xm, y1),
            (xm, y0, x1, ym),
            (xm, ym, x1, y1),
        ]

        return [c for c in children if c[0] < c[2] and c[1] < c[3]]

    def _region_hand(self, gray, prev_gray, region):
        x0, y0, x1, y1 = region
        if x1 <= x0 or y1 <= y0:
            return 0.0

        points = [
            (x0, y0),
            ((x0 + x1 - 1) // 2, (y0 + y1 - 1) // 2),
            (x1 - 1, y1 - 1),
        ]

        total = 0.0
        count = 0
        for x, y in points:
            if 0 <= x < gray.shape[0] and 0 <= y < gray.shape[1]:
                current = abs(float(gray[x, y]))
                temporal = 0.0
                if prev_gray is not None and prev_gray.shape == gray.shape:
                    temporal = abs(float(gray[x, y] - prev_gray[x, y]))
                total += current + temporal
                count += 1

        if count == 0:
            return 0.0
        return total / count

    #
    # focus exact
    #
    def _local_exact(self, region):
        x0, y0, x1, y1 = region
        local = self.field[x0:x1, y0:y1]
        if local.size == 0:
            return None

        result = {
            "shape": local.shape,
            "mean": float(np.mean(local)),
            "energy": float(np.mean(np.abs(local))),
            "variance": float(np.var(local)),
        }

        if self.previous is not None:
            prev = self.previous[x0:x1, y0:y1]
            delta = np.abs(local.astype(np.int16) - prev.astype(np.int16))
            result["delta"] = delta
            result["max_delta"] = float(np.max(delta))

        return result

    #
    # internal rhythm: read internal_drive (disturbance).
    # state offset only. does not change rules or timing.
    #
    def _update_rhythm_base(self):
        if self.internal_drive is None:
            return

        drive = 0.0
        count = 0

        for key in ("planet_activity", "clip_activity"):
            value = self.internal_drive.get(key)
            if value is not None:
                try:
                    drive += float(value)
                    count += 1
                except (TypeError, ValueError):
                    pass

        if count == 0:
            return

        mean_drive = drive / count

        target = 10.0 / (1.0 + max(0.0, mean_drive))

        current = float(self.exact_rhythm_base)
        self.exact_rhythm_base = current + 0.1 * (target - current)

    #
    # should exact
    #
    def _should_exact(self, activity_signal):
        self._update_rhythm_base()
        self.exact_rhythm += 1
        threshold = self.exact_rhythm_base * (1.0 + float(activity_signal))
        if self.exact_rhythm > threshold:
            self.exact_rhythm = 0
            return True
        return False

    #
    # observe
    #
    def observe(self, packet):
        if packet is None:
            return None

        frame = self._decode(packet)
        if frame is None:
            return None

        self.field = frame

        activity = self.activity()
        sample = self._sample()

        meta = {
            "activity": activity,
            "sample": sample,
        }

        if sample is not None and self._should_exact(activity["signal"]):
            meta["exact"] = self._local_exact(sample["region"])

        self.previous = frame.copy()
        self.age += 1

        return self._encode(meta, frame)

    def _decode(self, packet):
        try:
            raw = np.frombuffer(packet.data, dtype=np.dtype(packet.dtype))
            frame = raw.reshape(packet.shape)
        except Exception:
            return None

        if frame.ndim != 3:
            return None
        if frame.shape[2] != 3:
            return None
        return frame

    def _encode(self, meta, frame):
        return BitPacket(
            source="camera",
            tag="camera_observation",
            data=frame.tobytes(),
            shape=frame.shape,
            dtype=str(frame.dtype),
            schema="media.bgr",
            meta=meta,
        )