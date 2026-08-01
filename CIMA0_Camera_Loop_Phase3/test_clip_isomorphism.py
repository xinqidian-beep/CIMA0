import numpy as np
from core.clip_region import ClipRegion

CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


def main():
    clip = ClipRegion(CLIP_WEIGHT)

    print("has_clip:", clip.has_clip)

    # 固定输入模式 A
    frame_a = np.zeros((224, 224, 3), dtype=np.uint8)
    frame_a[50:100, 50:100] = 255

    # 固定输入模式 B
    frame_b = np.zeros((224, 224, 3), dtype=np.uint8)
    frame_b[150:200, 150:200] = 255

    print("input A: square at (50,50)")
    print("input B: square at (150,150)")

    # 先喂 A
    for i in range(10):
        clip.update(frame_a)
        state = clip.state()
        print(f"step {i} A: norm={state['norm']:.4f}, mean={state['mean']:.4f}")

    # 再喂 B
    for i in range(10):
        clip.update(frame_b)
        state = clip.state()
        print(f"step {i} B: norm={state['norm']:.4f}, mean={state['mean']:.4f}")

    # 再回 A
    for i in range(10):
        clip.update(frame_a)
        state = clip.state()
        print(f"step {i} A-again: norm={state['norm']:.4f}, mean={state['mean']:.4f}")


if __name__ == "__main__":
    main()