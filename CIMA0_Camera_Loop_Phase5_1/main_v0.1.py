import cv2
import time


from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem
from core.display_io import DisplayIO


from core.camera_planet import CameraPlanet

from archive.planet import Planet

from core.clip_field import CLIPField


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



class LocalClock:
    """
    Independent module clock.
    """

    def __init__(
        self,
        interval
    ):

        self.interval = interval

        self.last = time.perf_counter()



    def due(
        self
    ):

        now = time.perf_counter()


        if now - self.last >= self.interval:

            self.last = now

            return True


        return False





def main():


    print("=" * 60)
    print("CIMA0 Phase5 Internal Clock Loop")
    print("ESC : exit")
    print("=" * 60)



    #
    # internal world
    #

    internal = InternalDynamics()



    #
    # organs
    #

    planet = Planet()


    visual = CLIPField(
        weight_path=CLIP_WEIGHT,
        device="cpu"
    )



    internal.register(
        "planet",
        planet
    )


    internal.register(
        "visual",
        visual
    )



    #
    # external input
    #

    camera = cv2.VideoCapture(0)


    camera_planet = CameraPlanet()



    #
    # observer
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
    # clocks
    #

    camera_clock = LocalClock(
        1 / 30
    )


    internal_clock = LocalClock(
        0.01
    )


    observer_clock = LocalClock(
        0.1
    )


    display_clock = LocalClock(
        1 / 10
    )



    latest_snapshot = None



    if not camera.isOpened():

        print(
            "camera open failed"
        )

        return



    while True:



        #
        # Camera -> IO boundary
        #

        if camera_clock.due():


            ret, frame = camera.read()


            if ret:


                camera_planet.step(
                    frame
                )


                packet = camera_planet.state()



                if packet is not None:


                    #
                    # broadcast only
                    #

                    internal.receive(
                        packet
                    )




        #
        # internal evolution
        #

        if internal_clock.due():
            
            
            
            request = {

                "internal": 1.0

            }


            allocation = compute.allocate(
                request
            )


            if allocation.get(
                "internal",
                0
            ) > 0:    


                internal.step()




        #
        # observer
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
        # display
        #

        if display_clock.due():


            display_packet = internal.output_display(
                "visual"
            )


            if display_packet is not None:


                frame_out = display.encode(
                    display_packet
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