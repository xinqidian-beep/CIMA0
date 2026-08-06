import cv2
import time


from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem
from core.display_io import DisplayIO


from core.camera_planet import CameraPlanet
from core.camera_observer import CameraObserver
from core.camera_compute import CameraComputeSystem


from archive.planet import Planet
from core.clip_region import ClipRegion

CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



class LocalClock:
    """
    Independent module clock.
    """

    def __init__(self, interval):

        self.interval = interval
        self.last = time.perf_counter()



    def due(self):

        now = time.perf_counter()

        if now - self.last >= self.interval:

            self.last = now
            return True

        return False





def main():


    print("=" * 60)
    print("CIMA0 Phase4 Internal Clock Loop")
    print("")
    print("ESC : exit")
    print("=" * 60)



    #
    # internal world
    #
    
    internal = InternalDynamics()



    planet = Planet()
    
    clip = ClipRegion(
        64,
        64,
        3
    )



    internal.register(
        "planet",
        planet
    )


    internal.register(
        "clip",
        clip
    )



    

    #
    # camera input
    #

    camera = cv2.VideoCapture(0)


    camera_planet = CameraPlanet()

    camera_observer = CameraObserver()

    camera_compute = CameraComputeSystem()



    #
    # observer + compute
    #

    observer = InternalDynamicsObserver()


    compute = ComputeSystem(
        capacity=100
    )



    #
    # display
    #

    display = DisplayIO()



    #
    # module clocks
    #

    camera_clock = LocalClock(
        1 / 30
    )


    planet_clock = LocalClock(
        0.01
    )


    observer_clock = LocalClock(
        0.1
    )


    display_clock = LocalClock(
        1 / 60
    )



    #
    # readonly snapshot cache
    #

    latest_snapshot = None



    if not camera.isOpened():

        print(
            "Camera open failed"
        )



    while True:



        #
        # camera own time
        #

        if camera_clock.due():


            ret, frame = camera.read()


            if ret:
                #
                # camera local module
                #
                camera_planet.step(
                    
                    frame
                    
                )


                camera_state = camera_planet.state()
                
                
                if camera_state is not None:
                    
                    #
                    # external observation
                    #
                    
                    processed = camera_observer.observe(
                    
                        camera_state,
                        camera_compute.step()
                    )    
                    
                    #
                    # byte interface boundary
                    #
                    
                    internal.receive(
                        processed["bytes"]
                    )
                    
                
                



                



        #
        # internal dynamics own time
        #

        if planet_clock.due():

            internal.step()



        #
        # observer own time
        #

        if observer_clock.due():


            latest_snapshot = internal.snapshot()



            request = observer.observe(
                latest_snapshot
            )



            allocation = compute.allocate(
                request
            )



            observer.read(
                latest_snapshot,
                allocation
            )



        #
        # display own time
        #

        if display_clock.due():
            
            snapshot = internal.snapshot()


            if snapshot is not None:


                frame_out = display.encode(
                    snapshot.get("clip")
                )



                if frame_out is not None:


                    cv2.imshow(
                        "CIMA0",
                        frame_out
                    )



        #
        # keyboard
        #

        key = cv2.waitKey(1) & 0xff



        if key == 27:

            print(
                "CIMA0 stopped"
            )

            break



    camera.release()

    cv2.destroyAllWindows()





if __name__ == "__main__":

    main()