import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_8

    Cloud-native collision.

    Core principle
    --------------

    Collision does not invent a spatial correspondence between
    heterogeneous clouds.

    PlanetField and CLIPField may have completely different
    internal structures.

    Collision therefore works on already existing local states.

    It may discover a structural relation between states, but
    it does not decide that the states occupy the same position.

    Collision produces:

        structural relation
            +
        candidate change

    It does NOT:

        - modify PlanetField
        - modify CLIPField
        - evolve Planet
        - evolve CLIP
        - select Focus
        - allocate compute
        - select winner
        - commit a change
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
        similarity_threshold=0.05
    ):

        self.change_threshold = float(
            change_threshold
        )

        self.similarity_threshold = float(
            similarity_threshold
        )

        self.last_result = None


    # ==========================================================
    # public
    # ==========================================================

    def collide(
        self,
        planet_cloud,
        clip_cloud
    ):
        """
        Discover structural relations between two already
        existing clouds.

        No positional correspondence is invented.
        """

        if planet_cloud is None:
            return None

        if clip_cloud is None:
            return None

        planet = self._extract_cloud(
            planet_cloud
        )

        clip = self._extract_cloud(
            clip_cloud
        )

        if planet is None:
            return None

        if clip is None:
            return None

        planet_states = self._states(
            planet,
            source="planet"
        )

        clip_states = self._states(
            clip,
            source="clip"
        )

        result = self._discover_relations(
            planet_states,
            clip_states
        )

        self.last_result = result

        return result


    # ==========================================================
    # extraction
    # ==========================================================

    def _extract_cloud(
        self,
        packet
    ):

        if not isinstance(
            packet,
            dict
        ):
            return None

        if "cloud" not in packet:
            return None

        return packet["cloud"]


    # ==========================================================
    # state extraction
    # ==========================================================

    def _states(
        self,
        cloud,
        source
    ):
        """
        Convert a cloud into a collection of existing local
        states.

        This is NOT a spatial projection.

        Each state keeps:

            source
            identity
            value
            existence
            structural location
        """

        states = []

        if isinstance(
            cloud,
            np.ndarray
        ):

            arr = np.asarray(
                cloud
            )

            for index in np.ndindex(
                arr.shape
            ):

                value = arr[index]

                state = {

                    "source":
                        source,

                    "identity":
                        index,

                    "value":
                        self._safe_value(
                            value
                        ),

                    "exists":
                        True

                }

                states.append(
                    state
                )

            return states


        if isinstance(
            cloud,
            (list, tuple)
        ):

            for index, value in enumerate(
                cloud
            ):

                states.append({

                    "source":
                        source,

                    "identity":
                        index,

                    "value":
                        self._safe_value(
                            value
                        ),

                    "exists":
                        True

                })

            return states


        if isinstance(
            cloud,
            dict
        ):

            for identity, value in cloud.items():

                states.append({

                    "source":
                        source,

                    "identity":
                        identity,

                    "value":
                        self._safe_value(
                            value
                        ),

                    "exists":
                        True

                })

            return states


        return states


    # ==========================================================
    # safe value
    # ==========================================================

    def _safe_value(
        self,
        value
    ):

        try:

            number = float(
                value
            )

        except Exception:

            return None

        if not np.isfinite(
            number
        ):

            return None

        return number


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

        if value == 0.0:

            return self.ZERO_VALUE

        return self.NONZERO_VALUE


    # ==========================================================
    # relation discovery
    # ==========================================================

    def _discover_relations(
        self,
        planet_states,
        clip_states
    ):
        """
        Discover relations without assuming positional identity.

        Important:

            identity from Planet is never compared with identity
            from CLIP.

        Only the local state values are examined.

        This means:

            Planet position
                !=
            CLIP position

        unless some future explicit relation mechanism says so.
        """

        relations = []

        penetrate = 0
        change = 0
        bounce = 0

        #
        # Compare state populations rather than coordinates.
        #
        # The relation is explicitly marked as
        # "value_relation", not "position_relation".
        #

        for planet_state in planet_states:

            p_value = planet_state["value"]

            p_state = self._classify(
                planet_state["exists"],
                p_value
            )

            if p_state in (
                self.EMPTY_SLOT,
                self.EMPTY_VALUE
            ):
                continue


            for clip_state in clip_states:

                c_value = clip_state["value"]

                c_state = self._classify(
                    clip_state["exists"],
                    c_value
                )

                if c_state in (
                    self.EMPTY_SLOT,
                    self.EMPTY_VALUE
                ):
                    continue


                collision = self._collision_type(
                    p_state,
                    c_state,
                    p_value,
                    c_value
                )

                if collision is None:
                    continue


                if collision == self.PENETRATE:

                    penetrate += 1

                elif collision == self.CHANGE:

                    change += 1

                elif collision == self.BOUNCE:

                    bounce += 1


                relation = {

                    "type":
                        collision,

                    "relation":
                        "value_relation",

                    "planet":
                        {

                            "identity":
                                planet_state[
                                    "identity"
                                ],

                            "value":
                                p_value,

                            "state":
                                p_state

                        },

                    "clip":
                        {

                            "identity":
                                clip_state[
                                    "identity"
                                ],

                            "value":
                                c_value,

                            "state":
                                c_state

                        }

                }


                candidate = self._make_candidate(
                    relation
                )

                relation[
                    "candidate_change"
                ] = candidate


                relations.append(
                    relation
                )


        return {

            "collision":
                bool(
                    len(relations) > 0
                ),

            "total_relations":
                len(relations),

            "penetrate":
                penetrate,

            "change":
                change,

            "bounce":
                bounce,

            "candidate_changes":
                [

                    relation[
                        "candidate_change"
                    ]

                    for relation in relations

                    if relation[
                        "candidate_change"
                    ] is not None

                ],

            "relations":
                relations,

            "planet_count":
                len(
                    planet_states
                ),

            "clip_count":
                len(
                    clip_states
                ),

            "heterogeneous":
                True

        }


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
            planet_state == self.ZERO_VALUE
            and
            clip_state == self.ZERO_VALUE
        ):

            return None


        #
        # zero / non-zero
        #

        if (
            planet_state == self.ZERO_VALUE
            and
            clip_state == self.NONZERO_VALUE
        ):

            return self.CHANGE


        if (
            planet_state == self.NONZERO_VALUE
            and
            clip_state == self.ZERO_VALUE
        ):

            return self.CHANGE


        #
        # non-zero / non-zero
        #

        if (
            planet_state == self.NONZERO_VALUE
            and
            clip_state == self.NONZERO_VALUE
        ):

            product = (
                planet_value
                *
                clip_value
            )

            #
            # opposite sign
            #

            if product < 0:

                return self.BOUNCE

            #
            # same sign
            #

            return self.PENETRATE


        return None


    # ==========================================================
    # candidate
    # ==========================================================

    def _make_candidate(
        self,
        relation
    ):
        """
        Convert a collision relation into a candidate change.

        This is only a proposal.

        Nothing is written back.
        """

        collision_type = relation[
            "type"
        ]


        if collision_type == self.CHANGE:

            return {

                "kind":
                    "candidate_change",

                "relation":
                    "value_relation",

                "collision":
                    self.CHANGE,

                "source":
                    "cloud_collision",

                "planet_identity":
                    relation[
                        "planet"
                    ][
                        "identity"
                    ],

                "clip_identity":
                    relation[
                        "clip"
                    ][
                        "identity"
                    ],

                "planet_value":
                    relation[
                        "planet"
                    ][
                        "value"
                    ],

                "clip_value":
                    relation[
                        "clip"
                    ][
                        "value"
                    ],

                "committed":
                    False

            }


        if collision_type == self.PENETRATE:

            return {

                "kind":
                    "candidate_change",

                "relation":
                    "value_relation",

                "collision":
                    self.PENETRATE,

                "source":
                    "cloud_collision",

                "planet_identity":
                    relation[
                        "planet"
                    ][
                        "identity"
                    ],

                "clip_identity":
                    relation[
                        "clip"
                    ][
                        "identity"
                    ],

                "planet_value":
                    relation[
                        "planet"
                    ][
                        "value"
                    ],

                "clip_value":
                    relation[
                        "clip"
                    ][
                        "value"
                    ],

                "committed":
                    False

            }


        if collision_type == self.BOUNCE:

            return {

                "kind":
                    "candidate_change",

                "relation":
                    "value_relation",

                "collision":
                    self.BOUNCE,

                "source":
                    "cloud_collision",

                "planet_identity":
                    relation[
                        "planet"
                    ][
                        "identity"
                    ],

                "clip_identity":
                    relation[
                        "clip"
                    ][
                        "identity"
                    ],

                "planet_value":
                    relation[
                        "planet"
                    ][
                        "value"
                    ],

                "clip_value":
                    relation[
                        "clip"
                    ][
                        "value"
                    ],

                "committed":
                    False

            }


        return None