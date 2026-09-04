import os
import cv2


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

from core.internal_dynamics.cloud import PlanetField

from core.internal_dynamics.internal_dynamics import (
    InternalDynamics
)


#
# readonly observer
#

from core.observer.internal_dynamics_observer import (
    InternalDynamicsObserver
)


#
# observation system
#

from core.internal_dynamics.cache.observation_cache import (
    ObservationCache
)

from core.internal_dynamics.attention.attention_field import (
    AttentionField
)


#
# compute
#

from core.compute_system.compute_system import (
    ComputeSystem
)

from core.internal_dynamics.cloud_collision import CloudCollision
#
# io
#

from core.io.display_io import (
    DisplayIO
)


from core.io.transport import (
    TransportRouter
)


#
# camera
#

from core.terminal.camera import (
    CameraPlanet
)


from core.terminal.camera.camera_io import (
    CameraIO
)


#
# organ
#

from core.internal_dynamics.organs.clip_field import (
    CLIPField
)



def main():


    print("=" * 60)

    print(
        "CIMA0 Phase5_8 Internal Dynamics Loop"
    )

    print("=" * 60)



    #
    # Planet
    #

    planet_rule = Planet(
        size=128
    )


    planet = PlanetField(
        planet_rule
    )

    region = (
        0,
        0,
        128,
        128
    )

    print(
        "PLANET OBSERVATION:",
        planet.observe_region(region)
    )

    #
    # Compute
    #

    compute = ComputeSystem(
        capacity=1024
    )


    collision = CloudCollision()
    #
    # Observer
    #

    observer = InternalDynamicsObserver()



    #
    # Observation cache
    #

    observation_cache = ObservationCache()



    #
    # Attention
    #

    attention_field = AttentionField()



    #
    # Transport
    #

    transport = TransportRouter()



    #
    # Internal Dynamics
    #

    dynamics = InternalDynamics(

        planet=planet,

        compute=compute,
        
        collision=collision,

        observer=observer,

        observation_cache=observation_cache,

        attention_field=attention_field,

        transport=transport

    )



    #
    # Display
    #

    display = DisplayIO()



    #
    # CLIP organ
    #

    clip_field = CLIPField(

        weight_path=CLIP_WEIGHT

    )


    dynamics.register(
        "clip",
        clip_field
    )


    #
    # Transport route
    # external camera_raw field enters dynamics
    #

    transport.subscribe(

        "camera_raw",

        dynamics

    )


    #
    # output visual field to display
    #

    transport.subscribe(

        "visual",

        display

    )



    #
    # Camera IO
    #

    camera_io = CameraIO()



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



    #
    # main loop
    #

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
        # external input
        #

        if camera_available:


            ret, frame = cap.read()



            if ret and frame is not None:

                print(
                    "CAMERA FRAME:",
                    type(frame),
                    frame.shape,
                    frame.dtype
                )
                camera_state = {

                    "field":
                        frame

                }



                packet = camera_io.encode(
                    camera_state
                )
                print(
                    "CAMERA PACKET:",
                    packet
                )


                if packet is not None:


                    dynamics.receive(
                        packet
                    )



        #
        # internal evolution
        #

        dynamics.step()



        #
        # display
        #

        snapshot = dynamics.snapshot()


        if snapshot is not None:

            if display.frame is not None:
                
                print( 
                    "IMSHOW:", 
                    display.frame.shape, 
                    display.frame.dtype 
                )

                cv2.imshow(
                    "CIMA0",
                    display.frame
                )
            key=cv2.waitKey(1)&0xff

            if key==27:
                break    



    #
    # shutdown
    #

    if camera_available:

        cap.release()



    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()