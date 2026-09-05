"""
CIMA0 Phase5_7

PlanetField

Local continuous evolution field.

Responsibility:

    hold planetary local state

    receive external disturbance

    delegate evolution to Planet rule

    provide activity signal

    export collision projection


Does NOT know:

    camera
    bytes
    image
    RGB
    CLIP
    display
    compute policy
    CloudField


Architecture:


external disturbance

        |

        v


PlanetField.receive()


        |

        v


pending disturbance


        |

        v


Planet.evolve()


        |

        v


PlanetField state


        |

        v


collision projection


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
        # external disturbance buffer
        #

        self.pending_disturbance = None



        #
        # history
        #

        self.previous_state = None

        self.age = 0



        #
        # compute
        #

        self.compute_budget = 0
        
        
        #
        # sparse glimpse state
        #
                
        self.glimpse_state = {
            "pending": False,
            "path": [],
            "region": None,
            "level": 0,
            "observation": None
        }


    #
    # external input
    #

    def receive(
        self,
        disturbance
    ):


        if disturbance is None:

            return



        if not isinstance(
            disturbance,
            np.ndarray
        ):

            return



        self.pending_disturbance = (

            disturbance
            .astype(
                np.float32,
                copy=True
            )

        )






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
    # compute allocation
    #

    def execute_compute(
        self,
        allocation
    ):
        
        """
        Planet does not consume compute to gate its evolution.

        Receiving a compute opportunity here is intentionally
        inert. Planet's evolution is sovereign and unconditional
        (see CONSTITUTION.md §8, Planet Sovereignty).

        This method exists only so ComputeSystem's dispatch
        interface remains uniform across organs; it must not
        be extended to control Planet.step().
        """
        

        if allocation is None:
            return
            
        if isinstance(
            allocation,
            dict
        ):    
            
            amount = allocation.get(
                "amount",
                0.0
            )
        else:
            amount = allocation

        try:
            amount = float(
                amount
            )
        except Exception:
            return

        if amount <= 0.0:
            return

        self.compute_budget += amount
        
        print(
            "APPLY COMPUTE:",
            type(self).__name__,
            amount
        )


        

    def _apply_collision(
        self,
        collision
    ):
        """
        Apply an already-produced collision result
        to PlanetField.

        CloudCollision does not modify PlanetField.

        PlanetField remains the owner of disturbance intake.
        """

        if collision is None:
            return False


        if not collision.get(
            "collision"
        ):

            return False


        result = collision.get(
            "collision_result"
        )

        if result is None:
            return False


        if not result.get(
            "exists"
        ):

            return False


        disturbance = result.get(
            "disturbance"
        )

        if disturbance is None:
            return False


        #
        # First complete loop:
        #
        # collision result is converted into a local
        # disturbance field compatible with PlanetField.
        #
        # PlanetField still owns the actual state mutation.
        #
 
        state = self.planet.state


        if state is None:
            return False


        disturbance_array = np.zeros_like(
            state,
            dtype=np.float32
        )


        #
        # For the first closed-loop execution we inject
        # the collision result as a bounded global field.
        #
        # This is deliberately the LAST bridge.
        #
        # It does not mean CLIP was projected into Planet.
        #
        disturbance_array[...] = np.float32(
            disturbance
        )


        print(
            "PLANETFIELD DISTURBANCE:",
            float(
                disturbance
            )
        )


        self.planet.receive(
            disturbance_array
        )


        return True
        
        
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

        self.glimpse_state = {
            "pending": True,
            "path": path,
            "region": region,
            "level": level,
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

        return self.glimpse_state["observation"]
        
        
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
        
    def local_variance(
        self,
        region
    ):
        """
        Measure local state variance inside a region.

        region:
            (x0, y0, x1, y1)

        Read-only observation.
        Does not modify Planet or PlanetField state.
        """

        x0, y0, x1, y1 = region

        local = self.state[
            x0:x1,
            y0:y1
        ]

        if local.size == 0:

            return 0.0

        return float(
            np.var(local)
        )



    def sign_structure(
        self,
        region
    ):
        """
        Observe positive / negative structure inside a region.

        region:
            (x0, y0, x1, y1)

        Returns:
            positive_ratio
            negative_ratio
            balance

        balance measures the degree of positive/negative
        asymmetry.
        """

        x0, y0, x1, y1 = region

        local = self.state[
            x0:x1,
            y0:y1
        ]

        if local.size == 0:

            return {
                "positive_ratio": 0.0,
                "negative_ratio": 0.0,
                "balance": 0.0
            }

        positive = np.count_nonzero(
            local > 0
        )

        negative = np.count_nonzero(
            local < 0
        )

        total = local.size

        positive_ratio = (
            positive / total
        )

        negative_ratio = (
            negative / total
        )

        balance = abs(
            positive_ratio
            -
            negative_ratio
        )

        return {
            "positive_ratio": float(
                positive_ratio
            ),
            "negative_ratio": float(
                negative_ratio
            ),
            "balance": float(
                balance
            )
        }



    def energy_observation(
        self
    ):
        """
        Observe the current global state energy.

        This is an observation metric only.
        It does not modify the internal state.
        """

        if self.state is None:

            return 0.0

        if self.state.size == 0:

            return 0.0

        return float(
            np.mean(
                np.square(
                    self.state
                )
            )
        )



    def observe_region(
        self,
        region
    ):
        """
        Produce one finite observation of a region.

        region:
            (x0, y0, x1, y1)

        This function only observes.
        It does not evolve, select, or modify the state.
        """

        variance = self.local_variance(
            region
        )

        sign = self.sign_structure(
            region
        )

        energy = self.energy_observation()

        return {
            "region": region,

            "level": self.glimpse_state[
                "level"
            ],

            "variance": variance,

            "positive_ratio":
                sign[
                    "positive_ratio"
                ],

            "negative_ratio":
                sign[
                    "negative_ratio"
                ],

            "sign_balance":
                sign[
                    "balance"
                ],

            "energy": energy,

            "age": self.age
        }     

        
    def _region_hand(
        self,
        region
    ):
        """
        Sparse internal hand-up signal.

        Only a few positions are inspected.
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

        count = 0

        for x, y in points:

            current = float(
                self.state[x, y]
            )

            value = abs(
                current
            )

            #
            # local temporal change
            #

            if self.previous_state is not None:
 
                previous = float(
                    self.previous_state[x, y]
                )

                value += abs(
                    current - previous
                )

            #
            # external disturbance
            #

            if self.pending_disturbance is not None:

                try:

                    value += abs(
                        float(
                            self.pending_disturbance[
                                x,
                                y
                            ]
                        )
                    )

                except (
                    TypeError,
                    IndexError,
                    ValueError
                ):
                    pass

            signal += value

            count += 1

        if count == 0:
            return 0.0

        return signal / count
        
    
        
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

        if self.pending_disturbance is not None:

            try:

                disturbance = (
                    self.pending_disturbance[
                        x0:x1,
                        y0:y1
                    ]
                )

                result[
                    "disturbance"
                ] = float(
                    np.mean(
                        np.abs(
                            disturbance
                        )
                    )
                )

            except (
                TypeError,
                IndexError,
                ValueError
            ):
                pass

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

        if hasattr(
            self.planet,
            "evolve"
        ):


            self.state = (

                self.planet.evolve(

                    self.state,

                    self.pending_disturbance

                )

            ).astype(

                np.float32,

                copy=True

            )



        else:


            #
            # compatibility fallback
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
        # disturbance consumed
        #

        self.pending_disturbance = None



        self.compute_budget = 0




    #
    # packet output
    #

    def packet(
        self
    ):


        print(
            "PLANET PACKET CREATED"
        )


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