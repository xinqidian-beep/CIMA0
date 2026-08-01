import numpy as np
from core.internal_dynamics import InternalDynamics
from core.clip_region import ClipRegion


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


class DummyPlanet:
    def __init__(self):
        self.state = np.random.rand(224, 224, 3).astype(np.float32)
        self.velocity = np.zeros((224, 224, 3), dtype=np.float32)
        self.energy = 1.0
        self.phase = 0.0

    def inject(self, data):
        pass

    def step(self):
        self.state = np.clip(self.state + 0.01 * np.random.randn(*self.state.shape), 0, 1).astype(np.float32)


def main():
    planet = DummyPlanet()
    clip = ClipRegion(CLIP_WEIGHT)
    internal = InternalDynamics(planet, clip)

    data = b'\x01\x02\x03\x04'
    internal.receive(data)

    for i in range(5):
        internal.step()
        s = internal.snapshot()
        print("step", i)
        print("planet:", s["planet"])
        print("clip:", s["clip"])


if __name__ == "__main__":
    main()