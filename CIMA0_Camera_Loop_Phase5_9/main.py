import os
import cv2

from core.io.transport.packet import BitPacket


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

from core.compute_system.sampling.sampler import (
    Sampler
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
    CameraPlanet,
    CameraObserver,
)

from core.io.camera_io import (
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
    
    
    # 
    # Observation cache
    #

    observation_cache = ObservationCache()

    #
    # Compute
    #
    
    sampler = Sampler()

    compute = ComputeSystem(
        capacity=1024,
        sampler=sampler
    )


    collision = CloudCollision()
    #
    # Observer
    #

    observer = InternalDynamicsObserver()



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

        attention_field=attention_field

    )



    #
    # Display
    #

    display = DisplayIO()



    #
    # CLIP organ
    #

    clip_field = CLIPField(

        weight_path=CLIP_WEIGHT,
        sampler=sampler

    )


    dynamics.register(
        "clip",
        clip_field
    )


    #
    # camera
    #

    cap = cv2.VideoCapture(

        0,

        cv2.CAP_DSHOW

    )


    camera_available = cap.isOpened()
    # camera
    camera_io = CameraIO()
    camera_observer = CameraObserver()
    
    #
    # 暂时保留，待后面随机删除
    #
    camera_planet = CameraPlanet()


    if not camera_available:

        print(
            "camera open failed, running without camera"
        )

    #
    # Transport route
    # external camera_raw field enters dynamics
    #

    transport.subscribe(

        "camera_raw",

        dynamics

    )
    
    transport.subscribe("camera_observation", dynamics)
    
    transport.subscribe("internal_drive", camera_observer)
    
    #
    # output visual field to display
    #

    transport.subscribe(

        "visual",

        display

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
                camera_state = {"field": frame}
                raw_packet = camera_io.encode(camera_state)          # camera_raw
                if raw_packet is not None:
                    observation_packet = camera_observer.observe(raw_packet)  # camera_observation
                    if observation_packet is not None:
                        transport.publish(observation_packet)         # 到 dynamics



        #
        # internal evolution
        #

        snapshot_from_step, drive_packet = dynamics.step()
        if drive_packet is not None:
            transport.publish(drive_packet)
        
        #
        # produce internal_drive (综合动力)
        #
        planet_act = 0.0
        if hasattr(planet, "activity"):
            p = planet.activity()
            if isinstance(p, dict):
                planet_act = float(p.get("activity", 0.0))

        clip_act = 0.0
        if hasattr(clip_field, "activity"):
            c = clip_field.activity()
            if isinstance(c, dict):
                clip_act = float(c.get("activity", 0.0))

        collision_count = 0
        if hasattr(collision, "last_result") and collision.last_result is not None:
            collision_count = collision.last_result.get("collision_result", {}).get("count", 0)

        cloud_count = len(dynamics.cloud_state.snapshot())

        drive_packet = BitPacket(
            source="internal",
            tag="internal_drive",
            data=b"",
            shape=(),
            dtype="uint8",
            schema="drive",
            meta={
                "planet_activity": planet_act,
                "clip_activity": clip_act,
                "collision_count": int(collision_count),
                "cloud_count": int(cloud_count),
            },
        )
        transport.publish(drive_packet)
        

        #
        # display
        #

        snapshot = dynamics.snapshot()
        display.receive_snapshot(snapshot)
        
        display.receive_snapshot(
            snapshot
        )
        
        if snapshot is not None:
            

            if display.frame is not None:
                
                
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