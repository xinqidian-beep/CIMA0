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


from core.camera_observer import CameraObserver



def main():

    print("=" * 60)
    print("Phase4 CameraObserver byte stream test")
    print("=" * 60)


    observer = CameraObserver()



    previous = None

    frame_id = 0



    while True:


        #
        # simulate camera hardware bytes
        #

        camera_frame = (
            np.random.rand(
                240,
                320,
                3
            )
            *
            255
        ).astype(
            np.uint8
        )


        input_bytes = (
            camera_frame
            .tobytes()
        )



        #
        # observer output
        #

        output_bytes = observer.observe(
            input_bytes,
            {
                "available": 1.0
            }
        )



        output = np.frombuffer(
            output_bytes,
            dtype=np.uint8
        )



        #
        # byte stream delta
        #

        if previous is None:

            delta = 0.0

        else:

            delta = float(
                np.mean(
                    np.abs(
                        output.astype(
                            np.int16
                        )
                        -
                        previous.astype(
                            np.int16
                        )
                    )
                )
            )


        previous = output.copy()



        #
        # input/output compare
        #

        input_array = np.frombuffer(
            input_bytes,
            dtype=np.uint8
        )


        input_delta = float(
            np.mean(
                np.abs(
                    input_array.astype(
                        np.int16
                    )
                    -
                    output.astype(
                        np.int16
                    )
                )
            )
        )



        print(
            "frame:",
            frame_id,
            "bytes:",
            len(output_bytes),
            "output_delta:",
            delta,
            "input_output_delta:",
            input_delta
        )


        frame_id += 1



        #
        # show observer output
        #

        try:

            image = output.reshape(
                240,
                320,
                3
            )


            cv2.imshow(
                "CameraObserver",
                image
            )


        except Exception:

            pass



        key = cv2.waitKey(30) & 0xff


        if key == 27:

            break



    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()