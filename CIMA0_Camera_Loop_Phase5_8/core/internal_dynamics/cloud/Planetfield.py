"""
CIMA0 Phase5_8

PlanetField

Local observation-time field over Planet state.

Responsibility:

```
hold the observed Planet state

preserve observation-time state

record temporal change

provide activity signal

provide sparse glimpse

export visual packet

export collision projection
```

Does NOT know:

```
camera
bytes
image
RGB
CLIP
display
compute policy
CloudField
```

Architecture:

Planet

```
|

v
```

Planet.step()

```
|

v
```

Planet.snapshot()

```
|

v
```

PlanetField.state

```
|

+----> previous_state
|
+----> temporal change
|
+----> activity
|
+----> sparse glimpse
|
+----> visual packet
|
+----> collision projection
```

Temporal model:

```
Planet
    |
    | one evolution step
    v
PlanetField observation
    |
    +----> current state
    |
    +----> previous observation
    |
    +----> observed change
```

PlanetField observes Planet
through its own observation time.

It does not interpret or synchronize
Planet's internal time.

PlanetField does not:

```
control Planet evolution

receive external input

modify Planet rules

select compute

allocate compute

execute Organ behavior
```

"""




import numpy as np

from core.io.transport.packet import BitPacket




class PlanetField:


    def __init__(
        self,
        planet,
        size=128,
        initial_state=None
    ):
        

        self.planet = planet



        if initial_state is not None:


            self.state = (
                initial_state
                .astype(
                    np.float32,
                    copy=True
                )
            )


        else:


            self.state = (
                np.random.randn(
                    size,
                    size
                )
                .astype(
                    np.float32
                )
                *
                0.01
            )


        #
        # history
        #

        self.previous_state = None

        self.age = 0
        
        #
        # sparse glimpse state
        #
                
        self.glimpse_state = {
            "path": [],
            "region": None,
            "level": 0,
            "observation": None
        }


    #
    # attention signal
    #

    def activity(
        self
    ):


        if self.previous_state is None:


            return {


                "activity":
                    float(
                        np.mean(
                            np.abs(
                                self.state
                            )
                        )
                    ),


                "signal":
                    1.0,


                "changed":
                    True,


                "source":
                    "planet",


                "age":
                    self.age

            }




        delta = np.mean(

            np.abs(

                self.state

                -

                self.previous_state

            )

        )



        return {


            "activity":
                float(delta),


            "signal":
                float(delta),


            "changed":
                bool(
                    delta > 0
                ),


            "source":
                "planet",


            "age":
                self.age

        }


    #
    # sparse recursive glimpse
    #
    def glimpse(
        self
    ):
        """
        Take one endogenous sparse glimpse.

        No region is supplied from outside.

        The field itself raises candidates.
        """

        if self.state is None:
            return None

        height, width = self.state.shape[:2]

        root = (
            0,
            0,
            height,
            width
        )

        path = []

        region = root

        level = 0

        while True:

            children = self._split_region(
                region
            )

            if len(children) == 1:
                break

            candidates = []

            for child in children:

                signal = self._region_hand(
                    child
                )

                candidates.append(
                    {
                        "region": child,
                        "signal": signal
                    }
                )
 
            winner = max(
                candidates,
                key=lambda item: item["signal"]
            )

            region = winner["region"]

            path.append(
                {
                    "level": level,
                    "region": region,
                    "signal": float(
                        winner["signal"]
                    )
                }
            )

            level += 1
 
            x0, y0, x1, y1 = region

            if (
                x1 - x0 <= 1
                and
                y1 - y0 <= 1
            ):
                break

        #
        # only now perform exact local inspection
        #

        exact = self._local_exact(
            region
        )
        
        x0, y0, x1, y1 = region

        local_state = self.state[
            x0:x1,
            y0:y1
        ].copy()

        self.glimpse_state = {
            "path": path,
            "region": region,
            "level": level,
            "local_state": local_state,
            "observation": {
                "source": "planet",
                "type": "glimpse",
                "level": level,
                "region": region,
                "path": path,
                "exact": exact,
                "age": self.age
            }
        }

        return {
            "observation": self.glimpse_state["observation"],
            "local_state": self.glimpse_state["local_state"]
        }
        
        
    def _split_region(
        self,
        region
    ):
        x0, y0, x1, y1 = region

        if (
            x1 - x0 <= 1
            and
            y1 - y0 <= 1
        ):
            return [
                region
            ]

        xm = x0 + (
            x1 - x0
        ) // 2

        ym = y0 + (
            y1 - y0
        ) // 2

        children = [
            (x0, y0, xm, ym),
            (x0, ym, xm, y1),
            (xm, y0, x1, ym),
            (xm, ym, x1, y1)
        ]

        return [
            child
            for child in children
            if (
                child[0] < child[2]
                and
                child[1] < child[3]
            )
        ]

        
    def _region_hand(
        self,
        region
    ):
        """
        Sparse internal hand-up signal.

        Diagnostic version: 
            current contribution 
            temporal change contribution 
            
        Calculation semantics are unchanged.
        """

        x0, y0, x1, y1 = region

        if (
            x1 <= x0
            or
            y1 <= y0
        ):
            return 0.0

        points = [
            (
                x0,
                y0
            ),
            (
                (x0 + x1 - 1) // 2,
                (y0 + y1 - 1) // 2
            ),
            (
                x1 - 1,
                y1 - 1
            )
        ]

        signal = 0.0
        
        current_total = 0.0 
        
        temporal_total = 0.0 

        count = 0

        for x, y in points:

            current = float(
                self.state[x, y]
            )

            # 
            # current state contribution 
            # 
            
            current_value = abs( 
                current 
            )

            #
            # local temporal change
            #
            
            temporal_value = 0.0

            if self.previous_state is not None:
 
                previous = float(
                    self.previous_state[x, y]
                )

                temporal_value = abs(
                    current - previous
                )

            # 
            # original total 
            # 
            
            value = ( 
                current_value 
                + 
                temporal_value 
            ) 
            
            current_total += current_value 
            temporal_total += temporal_value 
            
            signal += value 
            count += 1 
        if count == 0: 
            return 0.0 
            
        current_average = ( 
            current_total / count 
        ) 
        
        temporal_average = ( 
            temporal_total / count 
        ) 
        
        signal_average = ( 
            signal / count 
        ) 
        
        #print( 
        #    "REGION HAND:", 
        #    region, 
        #    "current=", 
        #    current_average, 
        #    "temporal=", 
        #    temporal_average,
        #    "total=", 
        #    signal_average 
        #) 
        
        return signal_average
        
    
        
    def _local_exact(
        self,
        region
    ):
        x0, y0, x1, y1 = region

        local = self.state[
            x0:x1,
            y0:y1
        ]

        if local.size == 0:
            return None

        result = {
            "shape": local.shape,
            "mean": float(
                np.mean(local)
            ),
            "energy": float(
                np.mean(
                    np.abs(local)
                )
            ),
            "variance": float(
                np.var(local)
            )
        }

        if self.previous_state is not None:

            previous = self.previous_state[
                x0:x1,
                y0:y1
            ]

            delta = np.abs(
                local - previous
            )

            result[
                "delta"
            ] = float(
                np.mean(delta)
            )

            result[
                "max_delta"
            ] = float(
                np.max(delta)
            )


        return result
        
        
        
        
    #
    # evolution
    #

    def step(
        self
    ):


        if self.planet is None:

            return



        old_state = (

            self.state
            .copy()

        )



        #
        # Planet owns evolution
        #

        self.planet.step()

        self.state = (

            self.planet
            .snapshot()
            .astype(
                np.float32,
                copy=True
            )

        )


        delta = np.mean(

            np.abs(

                self.state

                -

                old_state

            )

        )
        
        print(
            "PLANETFIELD DELTA:",
            float(delta)
        )



        self.previous_state = old_state


        self.age += 1




    #
    # packet output
    #

    def packet(
        self
    ):


        field = (

            self.state
            .astype(
                np.float32
            )

        )



        return BitPacket(


            source="planet",


            tag="visual",


            data=field.tobytes(),


            shape=field.shape,


            dtype="float32",


            schema="continuous_field",


            meta={

                "age":
                    self.age

            }

        )






    #
    # collision projection
    #

    def collision_projection(
        self
    ):
        """
        PlanetField state

                |

                v

        planet cloud representation


        Read only.
        Used by CloudCollision.
        No modification.

        No activity evaluation.

        """



        field = self.state.copy()



        cloud = {


            "mean":

                float(
                    np.mean(field)
                ),



            "energy":

                float(
                    np.mean(
                        np.abs(field)
                    )
                ),



            "variance":

                float(
                    np.var(field)
                ),



            "density":

                float(

                    np.count_nonzero(field)

                    /

                    field.size

                )

        }



        return {


            "source":

                "planet",



            "representation":

                "planet_cloud",



            "cloud":

                cloud,



            "shape":

                field.shape

        }






    #
    # observer
    #

    def snapshot(
        self
    ):


        return self.state.copy()