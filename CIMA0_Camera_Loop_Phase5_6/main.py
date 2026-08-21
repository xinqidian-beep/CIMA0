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
        "CIMA0 Phase5_6 Internal Dynamics Loop"
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



    #
    # Compute
    #

    compute = ComputeSystem(
        capacity=1024
    )



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
    # external visual field enters dynamics
    #

    transport.subscribe(

        "visual",

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


                camera_state = {

                    "field":
                        frame.reshape(
                            -1,
                            3
                        )

                }



                packet = camera_io.encode(
                    camera_state
                )



                if packet is not None:


                    transport.publish(
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

                cv2.imshow(
                    "CIMA0",
                    display.frame
                )



    #
    # shutdown
    #

    if camera_available:

        cap.release()



    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()