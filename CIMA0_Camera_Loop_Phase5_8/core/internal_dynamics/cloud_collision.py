import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_8

    Cloud-native collision.

    Responsibility
    --------------

        PlanetField cloud
                +
        CLIPField cloud
                |
                v
        local collision relation
                |
                v
        candidate_change
                |
                v
        Sampler

    Collision DOES:

        - inspect local cloud states
        - distinguish empty / zero / non-zero
        - detect penetrate
        - detect change
        - detect bounce
        - create candidate changes

    Collision DOES NOT:

        - modify PlanetField
        - modify CLIPField
        - apply candidate changes
        - select a winner
        - allocate compute
        - consume compute
        - perform semantic interpretation
        - perform Focus
        - create final state

    Important
    ---------

        collision result
            !=
        state change

        candidate_change
            !=
        committed change

    The candidate is only an opportunity for a later
    compute-selected winner to be committed.
    """

    EMPTY_SLOT = "empty_slot"
    EMPTY_VALUE = "empty_value"
    ZERO_VALUE = "zero_value"
    NONZERO_VALUE = "nonzero_value"

    PENETRATE = "penetrate"
    CHANGE = "change"
    BOUNCE = "bounce"

    CANDIDATE_CHANGE = "candidate_change"

    def __init__(
        self,
        change_threshold=1e-6,
        bounce_threshold=0.0
    ):

        self.change_threshold = float(
            change_threshold
        )

        self.bounce_threshold = float(
            bounce_threshold
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
        Produce collision candidates.

        No source cloud is modified.
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

        planet_view = self._make_collision_view(
            planet
        )

        clip_view = self._make_collision_view(
            clip
        )

        if planet_view is None:
            return None

        if clip_view is None:
            return None

        result = self._collide_views(
            planet_view,
            clip_view
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
    # view
    # ==========================================================

    def _make_collision_view(
        self,
        cloud
    ):

        if isinstance(
            cloud,
            np.ndarray
        ):
            return self._array_view(
                cloud
            )

        if isinstance(
            cloud,
            dict
        ):
            return self._dict_view(
                cloud
            )

        if isinstance(
            cloud,
            (list, tuple)
        ):
            return self._array_view(
                np.asarray(
                    cloud
                )
            )

        return None

    # ==========================================================
    # dense array
    # ==========================================================

    def _array_view(
        self,
        cloud
    ):

        arr = np.asarray(
            cloud
        )

        if arr.size == 0:

            return {
                "kind": "array",

                "shape":
                    tuple(
                        arr.shape
                    ),

                "values":
                    arr,

                "exists":
                    np.zeros(
                        arr.shape,
                        dtype=bool
                    )
            }

        try:

            values = arr.astype(
                np.float32,
                copy=False
            )

        except Exception:

            return None

        exists = np.ones(
            values.shape,
            dtype=bool
        )

        return {
            "kind": "array",

            "shape":
                tuple(
                    values.shape
                ),

            "values":
                values,

            "exists":
                exists
        }

    # ==========================================================
    # sparse
    # ==========================================================

    def _dict_view(
        self,
        cloud
    ):

        positions = []
        values = []

        for position, value in cloud.items():

            if not self._is_position(
                position
            ):
                continue

            positions.append(
                position
            )

            values.append(
                value
            )

        return {
            "kind": "sparse",

            "positions":
                positions,

            "values":
                values
        }

    # ==========================================================
    # state classification
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

            number = float(
                value
            )

        except Exception:

            return self.EMPTY_VALUE

        if not np.isfinite(
            number
        ):
            return self.EMPTY_VALUE

        if number == 0.0:
            return self.ZERO_VALUE

        return self.NONZERO_VALUE

    # ==========================================================
    # dispatch
    # ==========================================================

    def _collide_views(
        self,
        planet,
        clip
    ):

        if (
            planet["kind"] == "array"
            and
            clip["kind"] == "array"
        ):

            return self._collide_arrays(
                planet,
                clip
            )

        if (
            planet["kind"] == "sparse"
            and
            clip["kind"] == "sparse"
        ):

            return self._collide_sparse(
                planet,
                clip
            )

        return self._collide_mixed(
            planet,
            clip
        )

    # ==========================================================
    # array collision
    # ==========================================================

    def _collide_arrays(
        self,
        planet,
        clip
    ):

        p = planet["values"]
        c = clip["values"]

        dimensions = min(
            p.ndim,
            c.ndim
        )

        if dimensions <= 0:
            return self._empty_result()

        common_shape = tuple(
            min(
                p.shape[i],
                c.shape[i]
            )
            for i in range(
                dimensions
            )
        )

        if not common_shape:
            return self._empty_result()

        p_slices = tuple(
            slice(
                0,
                common_shape[i]
            )
            for i in range(
                dimensions
            )
        )

        c_slices = tuple(
            slice(
                0,
                common_shape[i]
            )
            for i in range(
                dimensions
            )
        )

        p_view = p[
            p_slices
        ]

        c_view = c[
            c_slices
        ]

        return self._compare_arrays(
            p_view,
            c_view,
            common_shape
        )

    # ==========================================================
    # array comparison
    # ==========================================================

    def _compare_arrays(
        self,
        planet,
        clip,
        shape
    ):

        penetrate = 0
        change = 0
        bounce = 0

        zero_zero = 0
        zero_nonzero = 0
        nonzero_zero = 0
        nonzero_nonzero = 0

        candidates = []

        total = int(
            np.prod(
                shape
            )
        )

        for index in np.ndindex(
            shape
        ):

            p = float(
                planet[index]
            )

            c = float(
                clip[index]
            )

            p_state = self._classify(
                True,
                p
            )

            c_state = self._classify(
                True,
                c
            )

            collision_type = self._collision_type(
                p_state,
                c_state,
                p,
                c
            )

            #
            # state statistics
            #

            if collision_type == self.PENETRATE:

                penetrate += 1

            elif collision_type == self.CHANGE:

                change += 1

            elif collision_type == self.BOUNCE:

                bounce += 1

            #
            # state pair statistics
            #

            if (
                p_state == self.ZERO_VALUE
                and
                c_state == self.ZERO_VALUE
            ):

                zero_zero += 1

            elif (
                p_state == self.ZERO_VALUE
                and
                c_state == self.NONZERO_VALUE
            ):

                zero_nonzero += 1

            elif (
                p_state == self.NONZERO_VALUE
                and
                c_state == self.ZERO_VALUE
            ):

                nonzero_zero += 1

            elif (
                p_state == self.NONZERO_VALUE
                and
                c_state == self.NONZERO_VALUE
            ):

                nonzero_nonzero += 1

            #
            # candidate generation
            #

            if collision_type is not None:

                candidate = self._make_candidate(
                    index=index,
                    planet_value=p,
                    clip_value=c,
                    planet_state=p_state,
                    clip_state=c_state,
                    collision_type=collision_type
                )

                if candidate is not None:

                    candidates.append(
                        candidate
                    )

        return self._result(
            total=total,
            penetrate=penetrate,
            change=change,
            bounce=bounce,
            zero_zero=zero_zero,
            zero_nonzero=zero_nonzero,
            nonzero_zero=nonzero_zero,
            nonzero_nonzero=nonzero_nonzero,
            shape=shape,
            candidates=candidates
        )

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

        #
        # empty does not collide
        #

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

            if product < self.bounce_threshold:

                return self.BOUNCE

            return self.PENETRATE

        return None

    # ==========================================================
    # candidate
    # ==========================================================

    def _make_candidate(
        self,
        index,
        planet_value,
        clip_value,
        planet_state,
        clip_state,
        collision_type
    ):
        """
        Convert collision relation into candidate change.

        IMPORTANT:

            No state is changed here.

        We deliberately do NOT calculate a final value.

        The candidate carries only the information required
        by the later compute / commit stage.
        """

        difference = (
            clip_value
            -
            planet_value
        )

        if (
            collision_type == self.CHANGE
            and
            abs(difference)
            <= self.change_threshold
        ):

            return None

        return {

            "type":
                self.CANDIDATE_CHANGE,

            "position":
                tuple(index),

            "collision":
                collision_type,

            "planet": {

                "state":
                    planet_state,

                "value":
                    float(
                        planet_value
                    )

            },

            "clip": {

                "state":
                    clip_state,

                "value":
                    float(
                        clip_value
                    )

            },

            #
            # Difference is descriptive only.
            #
            # It is NOT written back.
            #

            "difference":
                float(
                    difference
                ),

            "committed":
                False
        }

    # ==========================================================
    # sparse
    # ==========================================================

    def _collide_sparse(
        self,
        planet,
        clip
    ):

        planet_map = dict(
            zip(
                planet["positions"],
                planet["values"]
            )
        )

        clip_map = dict(
            zip(
                clip["positions"],
                clip["values"]
            )
        )

        positions = (
            set(
                planet_map.keys()
            )
            |
            set(
                clip_map.keys()
            )
        )

        penetrate = 0
        change = 0
        bounce = 0

        candidates = []

        for position in positions:

            p_exists = (
                position in planet_map
            )

            c_exists = (
                position in clip_map
            )

            p_value = (
                planet_map.get(
                    position
                )
                if p_exists
                else None
            )

            c_value = (
                clip_map.get(
                    position
                )
                if c_exists
                else None
            )

            p_state = self._classify(
                p_exists,
                p_value
            )

            c_state = self._classify(
                c_exists,
                c_value
            )

            collision = self._collision_type(
                p_state,
                c_state,
                0.0
                if p_value is None
                else float(p_value),
                0.0
                if c_value is None
                else float(c_value)
            )

            if collision == self.PENETRATE:

                penetrate += 1

            elif collision == self.CHANGE:

                change += 1

            elif collision == self.BOUNCE:

                bounce += 1

            if collision is not None:

                candidate = self._make_candidate(
                    index=position,
                    planet_value=
                        0.0
                        if p_value is None
                        else float(p_value),
                    clip_value=
                        0.0
                        if c_value is None
                        else float(c_value),
                    planet_state=p_state,
                    clip_state=c_state,
                    collision_type=collision
                )

                if candidate is not None:

                    candidates.append(
                        candidate
                    )

        return self._result(
            total=len(
                positions
            ),
            penetrate=penetrate,
            change=change,
            bounce=bounce,
            zero_zero=0,
            zero_nonzero=0,
            nonzero_zero=0,
            nonzero_nonzero=0,
            shape=None,
            candidates=candidates
        )

    # ==========================================================
    # mixed
    # ==========================================================

    def _collide_mixed(
        self,
        planet,
        clip
    ):

        return {
            "collision": False,

            "total": 0,

            "penetrate": 0,
            "change": 0,
            "bounce": 0,

            "zero_zero": 0,
            "zero_nonzero": 0,
            "nonzero_zero": 0,
            "nonzero_nonzero": 0,

            "shape": None,

            "heterogeneous": True,

            "reason":
                "no direct positional collision domain",

            "candidates": []
        }

    # ==========================================================
    # result
    # ==========================================================

    def _result(
        self,
        total,
        penetrate,
        change,
        bounce,
        zero_zero,
        zero_nonzero,
        nonzero_zero,
        nonzero_nonzero,
        shape,
        candidates
    ):

        collided = (
            penetrate
            +
            change
            +
            bounce
        )

        return {

            "collision":
                bool(
                    collided > 0
                ),

            "total":
                int(
                    total
                ),

            "penetrate":
                int(
                    penetrate
                ),

            "change":
                int(
                    change
                ),

            "bounce":
                int(
                    bounce
                ),

            "zero_zero":
                int(
                    zero_zero
                ),

            "zero_nonzero":
                int(
                    zero_nonzero
                ),

            "nonzero_zero":
                int(
                    nonzero_zero
                ),

            "nonzero_nonzero":
                int(
                    nonzero_nonzero
                ),

            "shape":
                shape,

            "heterogeneous":
                False,

            #
            # New Phase5_8 boundary:
            #
            # collision creates candidates,
            # not final state.
            #

            "candidates":
                candidates
        }

    # ==========================================================
    # empty
    # ==========================================================

    def _empty_result(
        self
    ):

        return {

            "collision":
                False,

            "total":
                0,

            "penetrate":
                0,

            "change":
                0,

            "bounce":
                0,

            "zero_zero":
                0,

            "zero_nonzero":
                0,

            "nonzero_zero":
                0,

            "nonzero_nonzero":
                0,

            "shape":
                None,

            "heterogeneous":
                True,

            "reason":
                "empty collision domain",

            "candidates":
                []
        }

    # ==========================================================
    # position
    # ==========================================================

    def _is_position(
        self,
        position
    ):

        if isinstance(
            position,
            tuple
        ):

            return all(
                isinstance(
                    item,
                    (
                        int,
                        np.integer
                    )
                )
                for item in position
            )

        if isinstance(
            position,
            list
        ):

            return all(
                isinstance(
                    item,
                    (
                        int,
                        np.integer
                    )
                )
                for item in position
            )

        return False