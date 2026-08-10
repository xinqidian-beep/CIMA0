import cv2

from core.camera_planet import CameraPlanet
from core.clip_field import CLIPField
from core.display_io import DisplayIO


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


def main():

    print("=== CIMA0 minimal debug loop ===")

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("camera open failed")
        return

    camera_planet = CameraPlanet()

    clip_field = CLIPField(
        weight_path=CLIP_WEIGHT,
        device="cpu"
    )

    display = DisplayIO(
        height=240,
        width=320
    )

    #
    # 一次性打印 preprocess 实际配置的目标尺寸
    # 用来确认 A 假设：preprocess 给的到底是不是 224
    #
    print("preprocess pipeline:", clip_field.preprocess)

    frame_count = 0

    while True:

        ret, frame = camera.read()

        if not ret:
            print("camera read failed")
            break

        frame_count += 1

        #
        # 1) camera -> packet
        #

        camera_planet.step(frame)

        packet = camera_planet.state()

        if packet is None:
            continue

        #
        # 2) packet -> CLIPField
        #

        clip_field.receive(packet)
        clip_field.step()

        #
        # 3) 打印 field 形状，只在它变化时打印，避免刷屏
        #

        if clip_field.field is not None:

            print(
                f"[frame {frame_count}] "
                f"clip_field.field.shape = {clip_field.field.shape}"
            )

        #
        # 4) field -> display packet -> DisplayIO
        #

        display_packet = clip_field.display_field()

        if display_packet is not None:

            print(
                f"[frame {frame_count}] "
                f"display_packet shape/dtype = "
                f"{display_packet['shape']} / {display_packet['dtype']}"
            )

            frame_out = display.encode(display_packet)

            if frame_out is not None:

                print(
                    f"[frame {frame_count}] "
                    f"frame_out.shape (after resize) = {frame_out.shape}"
                )

                cv2.imshow("CIMA0 minimal", frame_out)

        if cv2.waitKey(1) == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()