import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_8

    Native Cloud Collision.

    ------------------------------------------------------------
    Responsibility
    ------------------------------------------------------------

    Compare heterogeneous cloud structures by their
    topological positions.

    Collision is NOT statistical similarity.

    Collision is NOT semantic similarity.

    Collision is NOT attention.

    Collision is NOT Focus.

    Collision is NOT compute allocation.

    Collision does NOT modify either cloud.

    ------------------------------------------------------------
    Cloud Cell States
    ------------------------------------------------------------

        EMPTY_SLOT
            |
            | no Cell exists
            v

        EMPTY_VALUE
            |
            | Cell exists, value is None
            v

        ZERO_VALUE
            |
            | value == 0
            v

        NONZERO_VALUE
            |
            | value != 0
            |
            +-- positive
            |
            +-- negative

    ------------------------------------------------------------
    Collision
    ------------------------------------------------------------

        topology position
              |
              v
        Planet Cell  <---->  CLIP Cell
              |
              v
        state pair
              |
        +-----+------+ 
        |            |
        v            v
    penetration    occupied collision
                      |
                +-----+-----+
                |           |
                v           v
              change      bounce

    ------------------------------------------------------------

    The collision engine observes structure only.

    It does not modify PlanetField or CLIPField.

    It does not create Focus.

    Focus belongs to a later layer.
    """

    EMPTY_SLOT = "empty_slot"
    EMPTY_VALUE = "empty_value"
    ZERO_VALUE = "zero_value"
    NONZERO_VALUE = "nonzero_value"

    PENETRATE = "penetrate"
    CHANGE = "change"
    BOUNCE = "bounce"

    def __init__(self):

        self.last_result = None

    # ============================================================
    # PUBLIC
    # ============================================================

    def collide(
        self,
        planet_cloud,
        clip_cloud
    ):
        """
        Perform native cloud collision.

        Inputs are cloud structures.

        No semantic interpretation.
        No scalar reduction.
        No winner selection.
        No mutation.
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

        # --------------------------------------------------------
        # topology
        # --------------------------------------------------------

        topology = self._build_topology(
            planet_cloud,
            clip_cloud,
            planet,
            clip
        )

        if topology is None:
            return None

        # --------------------------------------------------------
        # collision
        # --------------------------------------------------------

        collisions = []

        counts = {
            self.PENETRATE: 0,
            self.CHANGE: 0,
            self.BOUNCE: 0
        }

        state_pairs = {}

        for position in topology:

            planet_cell = self._planet_cell(
                planet,
                position
            )

            clip_cell = self._clip_cell(
                clip,
                position
            )

            planet_state = self._classify(
                planet_cell
            )

            clip_state = self._classify(
                clip_cell
            )

            key = (
                planet_state,
                clip_state
            )

            state_pairs[key] = (
                state_pairs.get(key, 0) + 1
            )

            collision_type = self._resolve_collision(
                planet_cell,
                clip_cell,
                planet_state,
                clip_state
            )

            if collision_type is None:
                continue

            counts[
                collision_type
            ] += 1

            collisions.append({

                "position":
                    position,

                "planet_state":
                    planet_state,

                "clip_state":
                    clip_state,

                "planet_value":
                    self._safe_value(
                        planet_cell
                    ),

                "clip_value":
                    self._safe_value(
                        clip_cell
                    ),

                "collision":
                    collision_type

            })

        # --------------------------------------------------------
        # structural result
        # --------------------------------------------------------

        total = len(topology)

        collision_count = len(
            collisions
        )

        result = {

            "collision":
                bool(
                    collision_count > 0
                ),

            "topology_count":
                int(
                    total
                ),

            "collision_count":
                int(
                    collision_count
                ),

            "penetrate":
                int(
                    counts[
                        self.PENETRATE
                    ]
                ),

            "change":
                int(
                    counts[
                        self.CHANGE
                    ]
                ),

            "bounce":
                int(
                    counts[
                        self.BOUNCE
                    ]
                ),

            "state_pairs":
                state_pairs,

            "collisions":
                collisions

        }

        self.last_result = result

        return result

    # ============================================================
    # CLOUD EXTRACTION
    # ============================================================

    def _extract_cloud(
        self,
        packet
    ):
        """
        Extract the actual cloud structure.

        Accepted form:

            {
                "cloud": ...
            }

        The collision engine does not convert the cloud
        into statistics.
        """

        if not isinstance(
            packet,
            dict
        ):
            return None

        if "cloud" not in packet:
            return None

        return packet[
            "cloud"
        ]

    # ============================================================
    # TOPOLOGY
    # ============================================================

    def _build_topology(
        self,
        planet_packet,
        clip_packet,
        planet,
        clip
    ):
        """
        Build correspondence positions.

        Preferred:

            explicit cloud topology

        Otherwise:

            native positional correspondence where possible.

        The important rule is that topology defines
        correspondence.

        CloudCollision does not invent semantic meaning.
        """

        # --------------------------------------------------------
        # explicit topology
        # --------------------------------------------------------

        topology = None

        if isinstance(
            clip_packet,
            dict
        ):

            topology = clip_packet.get(
                "topology"
            )

        if topology is None:

            topology = (
                planet_packet.get(
                    "topology"
                )
                if isinstance(
                    planet_packet,
                    dict
                )
                else None
            )

        if topology is not None:

            return list(
                topology
            )

        # --------------------------------------------------------
        # native array topology
        # --------------------------------------------------------

        planet_array = self._array_view(
            planet
        )

        clip_array = self._array_view(
            clip
        )

        if (
            planet_array is not None
            and
            clip_array is not None
        ):

            return self._native_topology(
                planet_array,
                clip_array
            )

        # --------------------------------------------------------
        # cell dictionary topology
        # --------------------------------------------------------

        if isinstance(
            planet,
            dict
        ) and isinstance(
            clip,
            dict
        ):

            planet_keys = set(
                planet.keys()
            )

            clip_keys = set(
                clip.keys()
            )

            common = (
                planet_keys
                &
                clip_keys
            )

            if common:

                return list(
                    common
                )

        return None

    # ============================================================
    # ARRAY TOPOLOGY
    # ============================================================

    def _array_view(
        self,
        cloud
    ):
        """
        Return ndarray only when the cloud itself is
        a numerical field.

        Dictionaries containing statistics are deliberately
        rejected.

        This prevents the old scalar-statistics collision
        from silently returning.
        """

        if isinstance(
            cloud,
            np.ndarray
        ):

            if cloud.dtype.kind in (
                "b",
                "i",
                "u",
                "f"
            ):

                return cloud

        return None

    def _native_topology(
        self,
        planet,
        clip
    ):
        """
        Build positional correspondence for arrays.

        Heterogeneous arrays are not reshaped into one
        representation.

        Correspondence is established by normalized
        coordinate position.
        """

        if planet.ndim == 0:
            return []

        if clip.ndim == 0:
            return []

        planet_shape = (
            planet.shape
        )

        clip_shape = (
            clip.shape
        )

        planet_count = (
            int(
                np.prod(
                    planet_shape
                )
            )
        )

        clip_count = (
            int(
                np.prod(
                    clip_shape
                )
            )
        )

        count = min(
            planet_count,
            clip_count
        )

        if count <= 0:
            return []

        topology = []

        for index in range(
            count
        ):

            topology.append({
                "planet_index":
                    index,

                "clip_index":
                    index

            })

        return topology

    # ============================================================
    # POSITION ACCESS
    # ============================================================

    def _planet_cell(
        self,
        cloud,
        position
    ):
        """
        Read one Planet position.

        Read only.
        """

        if isinstance(
            position,
            dict
        ):

            index = position.get(
                "planet_index"
            )

            if index is not None:

                return self._read_index(
                    cloud,
                    index
                )

        return self._read_index(
            cloud,
            position
        )

    def _clip_cell(
        self,
        cloud,
        position
    ):
        """
        Read one CLIP position.

        Read only.
        """

        if isinstance(
            position,
            dict
        ):

            index = position.get(
                "clip_index"
            )

            if index is not None:

                return self._read_index(
                    cloud,
                    index
                )

        return self._read_index(
            cloud,
            position
        )

    def _read_index(
        self,
        cloud,
        index
    ):
        """
        Read a cloud position without modifying it.
        
        Missing position -> EMPTY_SLOT
        Existing position with value=None -> None
        """

        if isinstance(
            cloud,
            np.ndarray
        ):

            try:

                return cloud[
                    np.unravel_index(
                        int(index),
                        cloud.shape
                    )
                ]

            except Exception:

                return_EMPTY_SLOT

        if isinstance(
            cloud,
            dict
        ):
            if index not in cloud:

                return _EMPTY_SLOT

            return cloud[
                index
            ]

        if isinstance(
            cloud,
            (list, tuple)
        ):

            try:

                return cloud[
                    int(index)
                ]

            except Exception:

                return _EMPTY_SLOT

        

        return _EMPTY_SLOT

    # ============================================================
    # STATE CLASSIFICATION
    # ============================================================

    def _classify(
        self,
        cell
    ):
        """
        Classify exactly four cloud states.

        Important:

            None here is interpreted as an empty value
            when a Cell/value exists.

        A missing position is represented separately
        by EMPTY_SLOT where topology permits it.
        """

        if cell is _EMPTY_SLOT:
            return self.EMPTY_SLOT

        if cell is None:
            return self.EMPTY_VALUE

        # --------------------------------------------------------
        # Cell-like object
        # --------------------------------------------------------

        if hasattr(
            cell,
            "value"
        ):

            value = cell.value

            if value is None:

                return self.EMPTY_VALUE

            try:

                if float(value) == 0.0:

                    return self.ZERO_VALUE

                return self.NONZERO_VALUE

            except Exception:

                return self.EMPTY_VALUE

        # --------------------------------------------------------
        # numpy scalar / numeric value
        # --------------------------------------------------------

        try:

            value = float(
                np.asarray(
                    cell
                )
            )

        except Exception:

            return self.EMPTY_VALUE

        if value == 0.0:

            return self.ZERO_VALUE

        return self.NONZERO_VALUE

    # ============================================================
    # COLLISION RULE
    # ============================================================

    def _resolve_collision(
        self,
        planet_cell,
        clip_cell,
        planet_state,
        clip_state
    ):
        """
        Native collision rule.

        --------------------------------------------------------
        Empty space
        --------------------------------------------------------

        If either side is an empty slot/value, the other
        structure can pass through.

            empty + occupied
                    |
                    v
                PENETRATE

        --------------------------------------------------------
        Zero
        --------------------------------------------------------

        Zero is a real value.

        It is NOT empty.

        Therefore:

            zero + zero
            zero + nonzero

        participate in collision structure.

        --------------------------------------------------------
        Non-zero
        --------------------------------------------------------

        Both sides contain actual values.

        Same-direction interaction:

            positive + positive
            negative + negative

                -> CHANGE

        Opposing interaction:

            positive + negative
            negative + positive

                -> BOUNCE

        --------------------------------------------------------
        """

        # --------------------------------------------------------
        # empty slot
        # --------------------------------------------------------

        if (
            planet_state
            ==
            self.EMPTY_SLOT
            or
            clip_state
            ==
            self.EMPTY_SLOT
        ):

            return self.PENETRATE

        # --------------------------------------------------------
        # empty value
        # --------------------------------------------------------

        if (
            planet_state
            ==
            self.EMPTY_VALUE
            or
            clip_state
            ==
            self.EMPTY_VALUE
        ):

            return self.PENETRATE

        # --------------------------------------------------------
        # zero participates as a real state
        # --------------------------------------------------------

        if (
            planet_state
            ==
            self.ZERO_VALUE
            or
            clip_state
            ==
            self.ZERO_VALUE
        ):

            return self.CHANGE

        # --------------------------------------------------------
        # both are non-zero
        # --------------------------------------------------------

        planet_value = (
            self._safe_value(
                planet_cell
            )
        )

        clip_value = (
            self._safe_value(
                clip_cell
            )
        )

        if (
            planet_value is None
            or
            clip_value is None
        ):

            return self.PENETRATE

        # --------------------------------------------------------
        # opposite signs
        # --------------------------------------------------------

        if (
            planet_value < 0
            and
            clip_value > 0
        ):

            return self.BOUNCE

        if (
            planet_value > 0
            and
            clip_value < 0
        ):

            return self.BOUNCE

        # --------------------------------------------------------
        # same sign
        # --------------------------------------------------------

        return self.CHANGE

    # ============================================================
    # VALUE
    # ============================================================

    def _safe_value(
        self,
        cell
    ):
        """
        Extract scalar value for reporting only.

        This method never changes the Cell.
        """

        if cell is _EMPTY_SLOT:
            return None

        if cell is None:
            return None

        if hasattr(
            cell,
            "value"
        ):

            cell = cell.value

        try:

            arr = np.asarray(
                cell
            )

            if arr.size != 1:

                return float(
                    np.mean(
                        arr
                    )
                )

            return float(
                arr.reshape(-1)[0]
            )

        except Exception:

            return None


class _EmptySlot:
    """
    Internal marker.

    Distinguishes:

        empty slot

    from:

        existing Cell with value=None
    """

    pass


_EMPTY_SLOT = _EmptySlot()