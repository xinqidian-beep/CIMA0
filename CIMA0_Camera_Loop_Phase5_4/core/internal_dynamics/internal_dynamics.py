import numpy as np


class InternalDynamics:
    """
    CIMA0 Phase5_4

    Internal dynamics container.

    Responsibility:

        planet
            |
            v
        internal evolution


        organs
            |
            v
        external byte driven structures


    Keeps:

        identity
        structure
        state
        activity
        color/channel information


    Does NOT:

        interpret meaning

        classify

        control organ evolution

    """



    def __init__(
        self,
        planet,
        compute=None
    ):


        self.planet = planet
        self.compute = compute
        
        #
        # planet internal clock
        #

        self.planet_clock = 0
        self.planet_interval = 60


        #
        # organ registry
        #

        self.organs = {}



        #
        # last complete snapshot
        #

        self.last_observation = None




    #
    # register organ
    #

    def register(
        self,
        name,
        organ
    ):

        self.organs[name] = organ




    #
    # external input broadcast
    #

    def receive(
        self,
        packet
    ):


        for name, organ in self.organs.items():


            if hasattr(
                organ,
                "receive"
            ):


                organ.receive(
                    packet
                )



    #
    # evolution step
    #

    def step(self):

        requests = self.observe_requests()


        allocation = None


        if self.compute is not None:

            allocation = self.compute.step(
                requests
            )


        self.apply_step(
            allocation
        )
        
        print(
            "allocation:",
            allocation
        )
        
        
    def observe_requests(self):

        requests = []
        
        for name, organ in self.organs.items():

            if hasattr(
                organ,
                "compute_request"
            ):
                
                request = organ.compute_request()
                
                if request is not None:

                    requests.append(
                        request
                    )
        
        return requests    
        print(
            "requests:",
            requests
        )
        
    def apply_step(
        self,
        allocation
    ):

        if allocation is None:

            return
            
        #
        # send compute budget
        #

        for name, organ in self.organs.items():


            if name in allocation:


                if hasattr(
                    organ,
                    "apply_compute"
                ):


                    organ.apply_compute(
                        allocation[name]
                    )
            
        #
        # organ evolution fast organs
        #

        for name, organ in self.organs.items():


            if hasattr(
                organ,
                "step"
            ):


                organ.step()
            
        #
        # planet base evolution slow planet
        #
        
        self.planet_clock += 1

        if self.planet_clock >= self.planet_interval:
            
            self.planet.step()
            
            self.planet_clock = 0
        
    #
    # fixed empty schema
    #

    def _empty_organ_schema(
        self,
        name
    ):


        return {


            "type":
                name,


            #
            # current state
            #

            "state":
                None,


            #
            # internal representation
            #

            "cloud":
                None,


            #
            # activity
            #

            "activity":
                None,


            #
            # structure information
            #

            "structure":
                {


                    "input":
                    {


                        "format":
                            None,


                        "channels":
                        {


                            "B":
                            {

                                "index":0,

                                "value":None

                            },


                            "G":
                            {

                                "index":1,

                                "value":None

                            },


                            "R":
                            {

                                "index":2,

                                "value":None

                            }


                        }

                    },


                    "internal":
                        None


                },



            #
            # future compute interface
            #

            "compute_request":
                None

        }



    #
    # snapshot
    #

    def snapshot(
        self
    ):



        result = {



            #
            # Planet
            #

            "planet":
                None,



            #
            # organs
            #

            "organs":
                {}

        }



        #
        # Planet snapshot
        #

        if hasattr(
            self.planet,
            "snapshot"
        ):


            result["planet"] = (

                self.planet.snapshot()

            )



        #
        # create fixed organ schema
        #

        for name, organ in self.organs.items():


            schema = self._empty_organ_schema(
                name
            )


            #
            # organ state
            #

            if hasattr(
                organ,
                "snapshot"
            ):


                data = organ.snapshot()



                if data is not None:


                    if "cloud" in data:

                        schema["cloud"] = data["cloud"]


                    if "activity" in data:

                        schema["activity"] = data["activity"]


                    if "structure" in data:

                        schema["structure"] = data["structure"]


                    if "state" in data:

                        schema["state"] = data["state"]



            #
            # compute request
            #

            if hasattr(
                organ,
                "compute_request"
            ):


                schema["compute_request"] = (

                    organ.compute_request()

                )



            result["organs"][name] = schema



        self.last_observation = result


        return result.copy()