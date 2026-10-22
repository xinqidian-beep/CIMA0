import numpy as np

from core.io.transport.packet import BitPacket
from core.observer.internal_dynamics_observer import InternalDynamicsObserver


class CameraSampling:
    """
    Camera sampling bridge.

    Responsibility:

        camera frame
            |
            v
        sampling module (InternalDynamicsObserver)
            |
            v
        homogeneous packet

    Does NOT:

        - define sampling rules
        - interpret frame
        - decide what downstream needs
        - discard unused information

    This is wiring only.

    The sampling module owns its own rules and timing.
    """

    def __init__(self):
        self.sampler = InternalDynamicsObserver()

    def sample(self, frame):
        """
        Wire one camera frame through the sampling module.

        Returns a homogeneous packet.

        All sampling output is preserved.
        Nothing is discarded.
        """

        if frame is None:
            return None

        if not isinstance(frame, np.ndarray):
            return None

        # camera frame shape (H, W, 3) — colour channels preserved
        size = tuple(frame.shape)

        # hand frame to the sampling module
        # the sampling module decides its own rules
        observation = self.sampler.observe({"frame": frame})

        if observation is None:
            return None

        # homogeneous packing
        # size + state + all sampling output preserved
        packet = BitPacket(
            source="camera",
            tag="camera_sampled",
            data=frame.tobytes(),
            shape=size,
            dtype=str(frame.dtype),
            schema="media.bgr",
            meta={
                "size": size,
                "sampling": observation,
            },
        )

        return packet