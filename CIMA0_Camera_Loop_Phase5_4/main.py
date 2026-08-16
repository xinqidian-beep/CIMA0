import os
import cv2
import time
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)


CLIP_WEIGHT = os.path.join(
    BASE_DIR,
    "models",
    "open_clip_pytorch_model.bin"
)
from archive.planet import Planet


from core.internal_dynamics.internal_dynamics import (
    InternalDynamics
)

from core.observer.internal_dynamics_observer import (
    InternalDynamicsObserver
)

from core.compute_system.compute_system import (
    ComputeSystem
)

from core.io.display_io import (
    DisplayIO
)

from core.io.transport import (
    TransportRouter
)

from core.terminal.camera import (
    CameraPlanet
)
from core.terminal.camera.camera_io import (
    CameraIO
)

from core.internal_dynamics.organs.clip_field import (
    CLIPField
)

def main():


    print("=" * 60)
    print(
        "CIMA0 Phase5_4 Internal Dynamics Loop"
    )
    print("=" * 60)



    #
    # Planet
    #
    # base internal dynamical space
    #

    planet = Planet(
        size=128
    )



    #
    # Compute system
    #
    # independent resource allocator
    #

    compute = ComputeSystem(
        capacity=1024
    )



    #
    # Internal Dynamics
    #

    dynamics = InternalDynamics(
        planet=planet,
        compute=compute
    )


    
    #
    # readonly observer
    #

    observer = InternalDynamicsObserver()



    #
    # display port
    #

    display = DisplayIO()
    
    #
    # information transport
    #

    transport = TransportRouter()
    
    #
    # Internal organ
    #
    # CLIPField is not vision here.
    #
    # It is an evolved internal organ.
    #

    clip_field = CLIPField(
        weight_path=
        CLIP_WEIGHT
    )


    dynamics.register(
        "clip",
        clip_field
    )
    
    #
    # transport connection
    #

    transport.subscribe(
        "visual",
        dynamics
    )
    
    #
    # camera io adapter
    #

    camera_io = CameraIO()
    
    #
    # external boundary
    #

    camera_planet = CameraPlanet()



    #
    # camera
    #

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )


    camera_available = cap.isOpened()



    if not camera_available:

        print(
            "camera open failed, running without camera"
        )



    while True:


        #
        # window event
        #

        key = cv2.waitKey(
            1
        ) & 0xff


        if key == 27:

            break



        #
        # external packet
        #

        if camera_available:


            ret, frame = cap.read()


            if not ret or frame is None:

                print(
                    "camera frame unavailable"
                )

            else:

                #
                # camera state
                #

                camera_state = {
                    "field": frame.reshape(
                        -1,
                        3
                    )
                }


                #
                # camera local io
                #

                packet = camera_io.encode(
                    camera_state
                )


                #
                # publish information
                #

                if packet is not None:

                    transport.publish(
                        packet
                    )



        #
        # internal clock
        #

        dynamics.step()



        #
        # snapshot
        #

        snapshot = dynamics.snapshot()



        #
        # observer
        #

        read_state = observer.read(
            snapshot
        )



        #
        # display
        #

        display_packet = observer.encode_field(
            read_state,
            source="internal"
        )



        frame_out = display.encode(
            display_packet
        )



        if frame_out is not None:


            cv2.imshow(
                "CIMA0",
                frame_out
            )



    if camera_available:

        cap.release()


    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()