import sys
import os
import cv2
import numpy as np


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)


from core.display_io import DisplayIO



def main():

    print("=" * 60)
    print("Phase4 direct camera byte stream display test")
    print("=" * 60)



    display = DisplayIO(
        height=240,
        width=320
    )


    camera = cv2.VideoCapture(0)


    if not camera.isOpened():

        print("camera open failed")
        return



    previous = None

    frame_id = 0



    while True:


        ret, frame = camera.read()


        if not ret:

            continue



        #
        # hardware frame
        #

        camera_bytes = frame.tobytes()



        #
        # bytes -> array
        #

        arr = np.frombuffer(
            camera_bytes,
            dtype=np.uint8
        )


        arr = arr.reshape(
            frame.shape
        )



        #
        # stream change
        #

        if previous is None:

            delta = 0.0

        else:

            delta = float(
                np.mean(
                    np.abs(
                        arr.astype(
                            np.int16
                        )
                        -
                        previous.astype(
                            np.int16
                        )
                    )
                )
            )


        previous = arr.copy()



        #
        # display
        #

        output = display.encode(
            arr
        )


        if output is not None:

            cv2.imshow(
                "Direct Camera Stream",
                output
            )



        print(
            "frame:",
            frame_id,
            "bytes:",
            len(camera_bytes),
            "delta:",
            delta
        )


        frame_id += 1



        key = cv2.waitKey(1) & 0xff


        if key == 27:

            break



    camera.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()