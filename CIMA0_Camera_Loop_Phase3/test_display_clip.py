import cv2
import numpy as np

from core.display_io import DisplayIO
from core.clip_region import ClipRegion


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


def main():

    print("=" * 60)
    print("CIMA0 Clip Display Test")
    print("=" * 60)


    clip = ClipRegion(
        CLIP_WEIGHT
    )


    display = DisplayIO()


    cap = cv2.VideoCapture(0)


    if not cap.isOpened():

        print("camera failed")
        return



    while True:


        ret, frame = cap.read()


        if not ret:
            continue
            

        data = frame.tobytes()

        #
        # BGR frame
        #
        # 直接进入 ClipRegion
        #

        clip.receive(
            data
        )
        clip.step()
        
        field = clip.snapshot()



        #
        # 临时访问真实内部状态
        #

        



        print(
            "FIELD:",
            field.shape,
            field.dtype,
            field.min(),
            field.max()
        )


        out = display.encode(
            field
        )


        if out is not None:

            cv2.imshow(
                "CLIP FIELD",
                out
            )


        key = cv2.waitKey(1) & 0xff


        if key == 27:

            break



    cap.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()