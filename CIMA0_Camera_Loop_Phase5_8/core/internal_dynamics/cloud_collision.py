import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_8

    Local cloud collision.

    Core flow:

        CLIP complete cloud
                |
                v
        response coordinate
                |
                v
        local associated cloud
                |
                +
                |
        PlanetField local cloud
                |
                v
             collision
                |
                v
        collision result

    Important:

        winner is only the entrance.

        The collision material is the associated local cloud
        discovered around the response coordinate.

    This class does NOT:

        - select winner
        - allocate compute
        - modify CLIPField
        - modify PlanetField
        - call Planet.evolve()
        - perform observation
        - perform sampling
    """

    EMPTY_SLOT = "empty_slot"
    EMPTY_VALUE = "empty_value"
    ZERO_VALUE = "zero_value"
    NONZERO_VALUE = "nonzero_value"

    PENETRATE = "penetrate"
    CHANGE = "change"
    BOUNCE = "bounce"

    def __init__(
        self,
        change_threshold=1e-6,
        bounce_threshold=0.0,
        association_radius=1
    ):

        self.change_threshold = float(
            change_threshold
        )

        self.bounce_threshold = float(
            bounce_threshold
        )

        self.association_radius = int(
            max(
                association_radius,
                0
            )
        )

        self.last_result = None


    # ==========================================================
    # public
    # ==========================================================

    def collide(
        self,
        planet_cloud,
        clip_cloud,
        winner
    ):
        """
        Perform one local collision.

        winner identifies the CLIP response entrance.

        The winner itself is NOT treated as the complete
        collision material.

        Local associated states are discovered from it.
        """

        if planet_cloud is None:
            return None

        if clip_cloud is None:
            return None

        if winner is None:
            return None


        clip_states = self._extract_clip_local_states(
            clip_cloud,
            winner
        )

        planet_states = self._extract_planet_local_states(
            planet_cloud
        )


        if not clip_states:
            result = {
                "collision": False,
                "reason": "no_clip_local_states",
                "winner": winner,
                "collision_material": []
            }

            self.last_result = result

            return result


        if not planet_states:
            result = {
                "collision": False,
                "reason": "no_planet_local_states",
                "winner": winner,
                "collision_material": clip_states
            }

            self.last_result = result

            return result


        result = self._collide_local(
            planet_states,
            clip_states,
            winner
        )


        self.last_result = result

        return result


    # ==========================================================
    # CLIP local association
    # ==========================================================

    def _extract_clip_local_states(
        self,
        cloud,
        winner
    ):
        """
        Extract local CLIP cloud associated with winner.

        Current CLIP topology:

            (12, 50, 768)

        winner currently identifies a layer.

        Therefore the layer is the entrance coordinate.

        We do NOT flatten the whole cloud.

        We retain:

            layer
            token
            dimension
            value
        """

        arr = self._extract_array(
            cloud
        )

        if arr is None:
            return []


        if arr.ndim != 3:
            return []


        levels, tokens, dimensions = arr.shape


        layer = self._winner_layer(
            winner,
            levels
        )


        if layer is None:
            return []


        radius = self.association_radius

        start = max(
            0,
            layer - radius
        )

        end = min(
            levels,
            layer + radius + 1
        )


        states = []


        for current_layer in range(
            start,
            end
        ):

            layer_data = arr[
                current_layer
            ]


            #
            # A layer is a local cloud.
            #
            # Preserve token/dimension topology.
            #

            for token in range(
                tokens
            ):

                vector = layer_data[
                    token
                ]


                #
                # Collision requires scalar local values.
                #
                # We do not destroy the complete CLIP cloud.
                #
                # The collision material is derived only here.
                #

                for dimension in range(
                    dimensions
                ):

                    value = float(
                        vector[
                            dimension
                        ]
                    )


                    state = self._classify(
                        True,
                        value
                    )


                    if state in (
                        self.EMPTY_SLOT,
                        self.EMPTY_VALUE
                    ):
                        continue


                    states.append(
                        {
                            "source":
                                "clip",

                            "position":
                                (
                                    current_layer,
                                    token,
                                    dimension
                                ),

                            "value":
                                value,

                            "state":
                                state,

                            "distance":
                                abs(
                                    current_layer
                                    -
                                    layer
                                )
                        }
                    )


        return states


    def _winner_layer(
        self,
        winner,
        levels
    ):
        """
        Accept the current CLIP winner representation.

        Supported:

            11

            {"coordinate": 11}

            {"layer": 11}

            {"winner": 11}
        """

        if isinstance(
            winner,
            dict
        ):

            if "coordinate" in winner:
                winner = winner[
                    "coordinate"
                ]

            elif "layer" in winner:
                winner = winner[
                    "layer"
                ]

            elif "winner" in winner:
                winner = winner[
                    "winner"
                ]

            else:
                return None


        try:
            layer = int(
                winner
            )

        except Exception:
            return None


        if layer < 0:
            return None

        if layer >= levels:
            return None


        return layer


    # ==========================================================
    # Planet local states
    # ==========================================================

    def _extract_planet_local_states(
        self,
        planet_cloud
    ):
        """
        Extract existing PlanetField states.

        Planet topology is NOT mapped to CLIP topology.

        Planet positions remain Planet positions.
        """

        arr = self._extract_array(
            planet_cloud
        )

        if arr is None:
            return []


        states = []


        for position in np.ndindex(
            arr.shape
        ):

            value = arr[
                position
            ]


            if np.asarray(
                value
            ).ndim != 0:
                continue


            value = float(
                value
            )


            state = self._classify(
                True,
                value
            )


            if state in (
                self.EMPTY_SLOT,
                self.EMPTY_VALUE
            ):
                continue


            states.append(
                {
                    "source":
                        "planet",

                    "position":
                        position,

                    "value":
                        value,

                    "state":
                        state
                }
            )


        return states


    # ==========================================================
    # array extraction
    # ==========================================================

    def _extract_array(
        self,
        packet
    ):

        if isinstance(
            packet,
            dict
        ):

            if "cloud" in packet:

                packet = packet[
                    "cloud"
                ]

            elif "state" in packet:

                packet = packet[
                    "state"
                ]


        if isinstance(
            packet,
            np.ndarray
        ):

            return packet


        try:

            return np.asarray(
                packet
            )

        except Exception:

            return None


    # ==========================================================
    # collision
    # ==========================================================

    def _collide_local(
        self,
        planet_states,
        clip_states,
        winner
    ):

        relations = []


        for clip in clip_states:

            #
            # We do not invent coordinate equivalence.
            #
            # Planet states participate as local available
            # states.
            #

            for planet in planet_states:

                collision_type = (
                    self._collision_type(
                        planet["state"],
                        clip["state"],
                        planet["value"],
                        clip["value"]
                    )
                )


                if collision_type is None:
                    continue


                candidate = (
                    self._make_candidate(
                        planet,
                        clip,
                        collision_type
                    )
                )


                relations.append(
                    {
                        "type":
                            collision_type,

                        "planet":
                            dict(
                                planet
                            ),

                        "clip":
                            dict(
                                clip
                            ),

                        "candidate_change":
                            candidate
                    }
                )


        #
        # Collision material is the actual local relation set.
        #

        result = {

            "collision":
                bool(
                    len(relations) > 0
                ),

            "winner":
                winner,

            "clip_local_states":
                int(
                    len(clip_states)
                ),

            "planet_local_states":
                int(
                    len(planet_states)
                ),

            "relations":
                relations,

            #
            # This is the important output.
            #
            # It is not a prediction anymore.
            #

            "collision_result":
                self._build_collision_result(
                    relations
                ),

            "heterogeneous":
                True
        }


        return result


    # ==========================================================
    # result
    # ==========================================================

    def _build_collision_result(
        self,
        relations
    ):

        if not relations:

            return {
                "exists":
                    False,

                "count":
                    0,

                "disturbance":
                    None
            }


        proposed = []


        for relation in relations:

            candidate = relation.get(
                "candidate_change"
            )

            if candidate is None:
                continue


            value = candidate.get(
                "proposed_value"
            )


            if value is None:
                continue


            try:

                proposed.append(
                    float(value)
                )

            except Exception:
                continue


        if not proposed:

            return {
                "exists":
                    False,

                "count":
                    0,

                "disturbance":
                    None
            }


        #
        # For the first complete loop we create one scalar
        # local disturbance from the actual collision result.
        #
        # This is NOT the CLIP cloud.
        #
        # This is the result of collision.
        #

        disturbance_value = float(
            np.mean(
                proposed
            )
        )


        return {
            "exists":
                True,

            "count":
                int(
                    len(proposed)
                ),

            "disturbance":
                disturbance_value
        }


    # ==========================================================
    # classification
    # ==========================================================

    def _classify(
        self,
        exists,
        value
    ):

        if not exists:
            return self.EMPTY_SLOT


        if value is None:
            return self.EMPTY_VALUE


        try:

            value = float(
                value
            )

        except Exception:

            return self.EMPTY_VALUE


        if not np.isfinite(
            value
        ):

            return self.EMPTY_VALUE


        if value == 0.0:

            return self.ZERO_VALUE


        return self.NONZERO_VALUE


    # ==========================================================
    # collision rule
    # ==========================================================

    def _collision_type(
        self,
        planet_state,
        clip_state,
        planet_value,
        clip_value
    ):

        if planet_state in (
            self.EMPTY_SLOT,
            self.EMPTY_VALUE
        ):
            return None


        if clip_state in (
            self.EMPTY_SLOT,
            self.EMPTY_VALUE
        ):
            return None


        #
        # zero / zero
        #

        if (
            planet_state
            ==
            self.ZERO_VALUE
            and
            clip_state
            ==
            self.ZERO_VALUE
        ):

            return None


        #
        # zero / non-zero
        #

        if (
            planet_state
            ==
            self.ZERO_VALUE
            and
            clip_state
            ==
            self.NONZERO_VALUE
        ):

            return self.CHANGE


        if (
            planet_state
            ==
            self.NONZERO_VALUE
            and
            clip_state
            ==
            self.ZERO_VALUE
        ):

            return self.CHANGE


        #
        # non-zero / non-zero
        #

        if (
            planet_state
            ==
            self.NONZERO_VALUE
            and
            clip_state
            ==
            self.NONZERO_VALUE
        ):

            product = (
                planet_value
                *
                clip_value
            )


            if product < self.bounce_threshold:

                return self.BOUNCE


            return self.PENETRATE


        return None


    # ==========================================================
    # candidate
    # ==========================================================

    def _make_candidate(
        self,
        planet,
        clip,
        collision_type
    ):

        p = float(
            planet["value"]
        )

        c = float(
            clip["value"]
        )


        if collision_type == self.CHANGE:

            if abs(p) <= self.change_threshold:

                proposed = c

            elif abs(c) <= self.change_threshold:

                proposed = p

            else:

                proposed = (
                    p + c
                ) / 2.0


        elif collision_type == self.PENETRATE:

            proposed = (
                p + c
            ) / 2.0


        elif collision_type == self.BOUNCE:

            proposed = (
                p - c
            )


        else:

            proposed = None


        return {
            "kind":
                "collision_change",

            "collision":
                collision_type,

            "planet_value":
                p,

            "clip_value":
                c,

            "proposed_value":
                proposed,

            "committed":
                True
        }


    # ==========================================================
    # snapshot
    # ==========================================================

    def snapshot(
        self
    ):

        if self.last_result is None:
            return None


        return dict(
            self.last_result
        )