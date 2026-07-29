from hardware.usb_camera import USBCamera
from core.io import InputField


def main():

    camera = USBCamera()

    io = InputField()


    while True:

        frame = camera.read()

        if frame is None:
            break


        raw = io.receive(
            frame
        )


        print(
            raw.shape,
            raw.dtype
        )


    camera.close()



if __name__ == "__main__":
    main()