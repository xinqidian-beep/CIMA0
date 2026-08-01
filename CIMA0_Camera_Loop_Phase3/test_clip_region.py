import numpy as np
from core.clip_region import ClipRegion

CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


def main():
    clip = ClipRegion(CLIP_WEIGHT)

    print("has_clip:", clip.has_clip)

    frame = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

    print("input frame:", frame.shape, frame.dtype, frame.min(), frame.max())

    clip.update(frame)

    state = clip.state()
    print("clip state:", state)

    frame2 = np.zeros((224, 224, 3), dtype=np.uint8)
    frame2[50:150, 50:150] = 255

    clip.update(frame2)

    state2 = clip.state()
    print("clip state 2:", state2)


if __name__ == "__main__":
    main()