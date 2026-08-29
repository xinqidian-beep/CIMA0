import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_8

    Cloud-native collision.

    Core principle
    --------------

    A Cloud contains heterogeneous states:

        empty slot
        empty value
        zero value
        non-zero value
        negative value

    Collision is performed between positions that
    actually exist in the participating clouds.

    Collision does NOT:

        - interpret camera data
        - interpret semantic meaning
        - reduce CLIP to a scalar
        - reduce Planet to CLIP space
        - select a Focus
        - allocate compute
        - modify PlanetField directly
        - modify CLIPField directly
        - discard unselected layers
        - choose a winner

    Collision only produces a structural collision result.

    Collision states
    ----------------

        penetrate
        change
        bounce

    The distinction is based on the local cloud states.

    Important
    ---------

    Empty slot and zero value are NOT the same thing.

        empty slot
            position does not currently contain a cloud value

        empty value
            slot exists but contains no value

        zero value
            value == 0

        non-zero value
            value != 0

    Negative values are valid non-zero values.

    The collision result is therefore a structural description
    of what happened at corresponding positions.

    No semantic interpretation is performed here.
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
    # public interface
    # ==========================================================

    def collide(
        self,
        planet_cloud,
        clip_cloud
    ):
        """
        Perform one collision pass.

        Planet Cloud and CLIP Cloud remain heterogeneous.

        The method does not force their tensors into a common
        representation.

        Instead, each cloud is converted only into a local
        collision view.

        The collision view preserves:

            position
            existence
            value

        and the actual collision rule operates on those states.
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

        result = self._collide_views(
            planet_view,
            clip_view
        )

        self.last_result = result

        return result

    # ==========================================================
    # cloud extraction
    # ==========================================================

    def _extract_cloud(
        self,
        packet
    ):
        """
        Extract the actual cloud without changing it.

        Supported packet:

            {
                "cloud": ...
            }

        The original object is never modified.
        """

        if not isinstance(
            packet,
            dict
        ):
            return None

        if "cloud" not in packet:
            return None

        return packet["cloud"]

    # ==========================================================
    # collision view
    # ==========================================================

    def _make_collision_view(
        self,
        cloud
    ):
        """
        Build a local collision view.

        This is NOT a replacement for the Cloud.

        It is only a read-only description used by collision.

        For dense numpy arrays:

            every array position is a slot.

        For object/dict based clouds:

            existing positions are discovered without forcing
            the cloud into another representation.
        """

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
    # ndarray view
    # ==========================================================

    def _array_view(
        self,
        cloud
    ):
        """
        Dense cloud view.

        Every position exists as a slot.

        Therefore:

            NaN      -> empty value
            0        -> zero value
            non-zero -> non-zero value

        A dense ndarray has no empty slot unless the source
        representation explicitly encodes one.
        """

        arr = np.asarray(
            cloud
        )

        if arr.size == 0:
            return {
                "kind": "array",
                "shape": tuple(
                    arr.shape
                ),
                "values": arr,
                "exists": np.zeros(
                    arr.shape,
                    dtype=bool
                ),
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
            "shape": tuple(
                values.shape
            ),
            "values": values,
            "exists": exists,
        }

    # ==========================================================
    # dict / sparse cloud view
    # ==========================================================

    def _dict_view(
        self,
        cloud
    ):
        """
        Sparse/object cloud view.

        Expected possibilities include:

            {
                position: value
            }

        or a Cell-like structure.

        This method intentionally does not interpret arbitrary
        dictionaries as numeric tensors.
        """

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
            "positions": positions,
            "values": values,
        }

    # ==========================================================
    # state classification
    # ==========================================================

    def _classify(
        self,
        exists,
        value
    ):
        """
        Classify one cloud position.

        Order matters.

        empty slot
            no slot exists

        empty value
            slot exists but no usable value exists

        zero value
            actual numeric zero

        non-zero value
            any actual non-zero value, including negative values
        """

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
    # dense collision
    # ==========================================================

    def _collide_views(
        self,
        planet,
        clip
    ):
        """
        Dispatch according to cloud representation.
        """

        if planet["kind"] == "array" and \
           clip["kind"] == "array":

            return self._collide_arrays(
                planet,
                clip
            )

        if planet["kind"] == "sparse" and \
           clip["kind"] == "sparse":

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
        """
        Collision between dense fields.

        Heterogeneous shapes are allowed.

        We do NOT resize either cloud.

        Instead, collision uses their common positional
        intersection.

        This is important:

            Planet 128 x 128
            CLIP   12 x 50 x 768

        are NOT converted into one another.

        Only actual corresponding positions in the common
        structural domain are examined.
        """

        p = planet["values"]
        c = clip["values"]

        p_shape = p.shape
        c_shape = c.shape

        dimensions = min(
            p.ndim,
            c.ndim
        )

        common_shape = tuple(
            min(
                p_shape[i],
                c_shape[i]
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
    # actual array comparison
    # ==========================================================

    def _compare_arrays(
        self,
        planet,
        clip,
        shape
    ):
        """
        Local collision rule.

        The important part is that collision is decided from
        the actual local states, not from global statistics.
        """

        penetrate = 0
        change = 0
        bounce = 0

        zero_zero = 0
        zero_nonzero = 0
        nonzero_zero = 0
        nonzero_nonzero = 0

        total = int(
            np.prod(shape)
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

            if collision_type == self.PENETRATE:
                penetrate += 1

            elif collision_type == self.CHANGE:
                change += 1

            elif collision_type == self.BOUNCE:
                bounce += 1

            if p_state == self.ZERO_VALUE and \
               c_state == self.ZERO_VALUE:

                zero_zero += 1

            elif p_state == self.ZERO_VALUE and \
                 c_state == self.NONZERO_VALUE:

                zero_nonzero += 1

            elif p_state == self.NONZERO_VALUE and \
                 c_state == self.ZERO_VALUE:

                nonzero_zero += 1

            elif p_state == self.NONZERO_VALUE and \
                 c_state == self.NONZERO_VALUE:

                nonzero_nonzero += 1

        return self._result(
            total=total,
            penetrate=penetrate,
            change=change,
            bounce=bounce,
            zero_zero=zero_zero,
            zero_nonzero=zero_nonzero,
            nonzero_zero=nonzero_zero,
            nonzero_nonzero=nonzero_nonzero,
            shape=shape
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
        """
        Fundamental collision rule.

        1. Empty states do not collide.

        2. Zero with non-zero produces change.

        3. Non-zero with non-zero:

            same sign
                penetration / continuation

            opposite sign
                bounce

        4. Zero with zero
            is a valid coincident state but produces no change.

        Negative values are fully preserved as non-zero values.
        """

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

        # ------------------------------------------------------
        # zero / zero
        # ------------------------------------------------------

        if (
            planet_state == self.ZERO_VALUE
            and
            clip_state == self.ZERO_VALUE
        ):
            return None

        # ------------------------------------------------------
        # zero / non-zero
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # non-zero / non-zero
        # ------------------------------------------------------

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
    # sparse collision
    # ==========================================================

    def _collide_sparse(
        self,
        planet,
        clip
    ):
        """
        Sparse clouds.

        Only positions that exist in either cloud are examined.

        Missing positions remain empty slots.

        Nothing is created merely because another cloud has
        a value at that position.
        """

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

        positions = set(
            planet_map.keys()
        ) | set(
            clip_map.keys()
        )

        penetrate = 0
        change = 0
        bounce = 0

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
            shape=None
        )

    # ==========================================================
    # mixed representations
    # ==========================================================

    def _collide_mixed(
        self,
        planet,
        clip
    ):
        """
        Mixed representations are intentionally not coerced
        into one tensor.

        This version records that the clouds are structurally
        heterogeneous and therefore have no direct positional
        collision domain.

        This is preferable to silently inventing a projection.
        """

        return {
            "collision": False,

            "penetrate": 0,
            "change": 0,
            "bounce": 0,

            "total": 0,

            "zero_zero": 0,
            "zero_nonzero": 0,
            "nonzero_zero": 0,
            "nonzero_nonzero": 0,

            "shape": None,

            "heterogeneous": True,

            "reason":
                "no direct positional collision domain",

            "relations": []
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
        shape
    ):
        collided = (
            penetrate
            +
            change
            +
            bounce
        )

        return {
            "collision": bool(
                collided > 0
            ),

            "total": int(
                total
            ),

            "penetrate": int(
                penetrate
            ),

            "change": int(
                change
            ),

            "bounce": int(
                bounce
            ),

            "zero_zero": int(
                zero_zero
            ),

            "zero_nonzero": int(
                zero_nonzero
            ),

            "nonzero_zero": int(
                nonzero_zero
            ),

            "nonzero_nonzero": int(
                nonzero_nonzero
            ),

            "shape": shape,

            "heterogeneous": False
        }

    # ==========================================================
    # empty
    # ==========================================================

    def _empty_result(
        self
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

            "relations": []
        }

    # ==========================================================
    # position validation
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
                    (int, np.integer)
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
                    (int, np.integer)
                )
                for item in position
            )

        return False