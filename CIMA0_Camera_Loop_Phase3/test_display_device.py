import numpy as np
from hardware.display_device import DisplayDevice

def main():
    d = DisplayDevice()

    frame = np.zeros((32, 240, 3), dtype=np.uint8)
    frame[:, :80] = (255, 0, 0)
    frame[:, 80:160] = (0, 255, 0)
    frame[:, 160:] = (0, 0, 255)

    while True:
        d.show(frame)
        if d.step_display() == 27:
            break

    d.close()

if __name__ == "__main__":
    main()