class InternalDynamicsObserver:


    def __init__(self):

        self.previous=None
        
        self.current=None
        
    def observe(self,snapshot):
        
        #
        # temporary check only
        #
        clip = (
            snapshot
            .get("fields", {})
            .get("clip")
        )

        if clip is not None:

            self.previous = self.current
        
            self.current = snapshot
               
        return {

            "state": self.current,

            "delta": self._compare()

        }


    def _compare(
        self
    ):


        if self.previous is None:

            return None


        delta={}



        #
        # planet
        #

        old_planet=self.previous.get(
            "planet"
        )

        new_planet=self.current.get(
            "planet"
        )
        
        if (
            old_planet is not None
            and
            new_planet is not None
        ):

            delta["planet"]=(
                new_planet
                -
                old_planet
            )



        #
        # organs
        #
        
        delta["organs"]={}


        for name,new in self.current.get(
            "organs",
            {}
        ).items():


            old=self.previous.get(
                "organs",
                {}
            ).get(
                name
            )


            if old is None:

                delta["organs"][name]=None

            else:

                delta["organs"][name]={
                    "changed":True
                }



        return delta
        
    def read(
        self
    ):

        return self.current