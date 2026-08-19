import numpy as np


class InternalDynamicsObserver:


    def __init__(self):

        self.previous = None
        self.current = None



    #
    # attention selector
    #
    # output:
    #
    # {
    #     name,
    #     organ,
    #     state
    # }
    #
    # no sampling
    # no packet
    # no IO
    #

    def attention(
        self
    ):


        if self.current is None:

            return None



        signals = (
            self.current
            .get(
                "attention",
                []
            )
        )


        if len(signals) == 0:

            return None



        winner = max(

            signals,

            key=lambda x:

                x["state"]
                .get(
                    "activity",
                    0
                )

        )


        return {

            "name":
                winner["name"],


            "organ":
                winner["organ"],


            "state":
                winner["state"]

        }
        
        selected = observer.attention()

        print("IO SOURCE:", selected)

        if selected is not None:

            organ = selected.get("organ")

            if organ is not None and hasattr(organ, "packet"):

                packet = organ.packet()

                if packet is not None:

                    display.receive(packet)

        if display.frame is not None:

            cv2.imshow(
                "CIMA0",
                display.frame
            )
        

    def _trigger(
        self,
        snapshot
    ):

        #
        # 暂时保留原逻辑
        # 后面可以扩展
        #

        fields = (
            snapshot
            .get(
                "fields",
                {}
            )
        )


        clip = fields.get(
            "clip"
        )


        if clip is not None:

            return True


        return True



    def observe(
        self,
        snapshot
    ):


        if self._trigger(snapshot):

            self.previous = self.current

            self.current = snapshot



        return {

            "state":
                self.current,

            "delta":
                self._compare()

        }



    def _compare(
        self
    ):


        if (
            self.previous is None
            or
            self.current is None
        ):

            return None



        delta = {}



        old_planet = (
            self.previous
            .get(
                "planet"
            )
        )


        new_planet = (
            self.current
            .get(
                "planet"
            )
        )



        if (
            old_planet is not None
            and
            new_planet is not None
        ):


            delta["planet"] = (
                new_planet
                -
                old_planet
            )


            print(
                "OBSERVER PLANET DELTA:",
                float(
                    np.mean(
                        np.abs(
                            delta["planet"]
                        )
                    )
                )
            )



        return delta



    def read(
        self
    ):

        return self.current