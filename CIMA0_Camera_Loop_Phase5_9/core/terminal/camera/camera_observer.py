import numpy as np

from core.io.transport.packet import BitPacket
from core.observer.internal_dynamics_observer import InternalDynamicsObserver


class CameraObserver:
    """
    CIMA0 Camera Observer / sampling module.

    Input:

        BitPacket(camera_raw)

    Output:

        BitPacket(camera_observation)

    Responsibility:

        decode incoming BitPacket
        hand frame to the sampling module
        pack sampling result back into BitPacket

    Does NOT:

        define sampling rules
        interpret frame
        decide what downstream needs
        discard unused information

    The sampling module (InternalDynamicsObserver) owns its own
    rules and timing.

    This is wiring only.
    """

    def __init__(self, sampler=None):
        self.sampler = sampler or InternalDynamicsObserver()

        #
        # self-reference / previous
        #
        # kept as an internal field.
        # what it holds and how it evolves
        # is left open.
        #
        self.previous = None

    def observe(self, packet):
        if packet is None:
            return None

        #
        # 1. decode (BitPacket -> frame)
        #
        frame = self._decode(packet)
        if frame is None:
            return None

        #
        # 2. sampling (delegate to the sampling module, unchanged)
        #
        observation = self.sampler.observe({"frame": frame})
        if observation is None:
            return None

        #
        # 3. encode (frame + observation -> BitPacket)
        #
        return self._encode(observation, frame)

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

    def _encode(self, observation, frame):
        return BitPacket(
            source="camera",
            tag="camera_observation",
            data=frame.tobytes(),
            shape=frame.shape,
            dtype=str(frame.dtype),
            schema="media.bgr",
            meta={"observation": observation},
        )