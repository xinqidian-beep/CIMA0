import numpy as np


class CloudCollision:
    """
    CIMA0 Phase5_8 / V2

    Cloud-native structural collision.

    ------------------------------------------------------------
    Core principle
    ------------------------------------------------------------

    PlanetField and CLIPField are heterogeneous clouds.

    They do NOT share:

        - coordinate system
        - topology
        - tensor shape
        - index meaning
        - token meaning
        - spatial correspondence

    Therefore Collision does NOT invent a positional mapping.

    Collision observes only states that have already formed
    inside the participating clouds.

    ------------------------------------------------------------
    Responsibility
    ------------------------------------------------------------

        existing Planet local states
                    +
        existing CLIP local states
                    |
                    v
              CloudCollision
                    |
                    v
             structural relations
                    |
                    v
             candidate changes

    ------------------------------------------------------------
    Does NOT
    ------------------------------------------------------------

        - interpret camera data
        - interpret semantic meaning
        - resize clouds
        - reshape clouds
        - flatten clouds
        - truncate clouds
        - average clouds
        - project Planet into CLIP
        - project CLIP into Planet
        - invent coordinates
        - modify PlanetField
        - modify CLIPField
        - execute changes
        - select winner
        - allocate compute
        - perform Focus

    ------------------------------------------------------------
    Important
    ------------------------------------------------------------

    candidate_change is only a possibility.

        collision
            |
            v
        candidate_change
            |
            v
        Sampler
            |
            v
        winner
            |
            v
        Compute
            |
            v
        Commit

    Collision stops before Sampler.
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
        max_relations=None
    ):
        self.change_threshold = float(
            change_threshold
        )

        self.bounce_threshold = float(
            bounce_threshold
        )

        self.max_relations = (
            None
            if max_relations is None
            else int(max_relations)
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
        Compare already-formed local cloud states.

        No positional correspondence is invented.

        Each cloud is first converted into a collection of
        local state observations.

        The observations are then compared structurally.

        The output contains relations and candidate changes only.
        """

        if planet_cloud is None:
            return None

        if clip_cloud is None:
            return None

        planet_states = self._extract_states(
            planet_cloud,
            source="planet"
        )

        clip_states = self._extract_states(
            clip_cloud,
            source="clip"
        )

        if planet_states is None:
            return None

        if clip_states is None:
            return None

        result = self._collide_states(
            planet_states,
            clip_states
        )

        self.last_result = result

        return result

    # ==========================================================
    # state extraction
    # ==========================================================

    def _extract_states(
        self,
        packet,
        source
    ):
        """
        Convert a cloud into local state observations.

        This is a read-only boundary operation.

        Important:

            position is metadata only.

        It is NEVER used to assert that Planet position X
        corresponds to CLIP position X.
        """

        cloud = self._extract_cloud(
            packet
        )

        if cloud is None:
            return None

        states = []

        # ------------------------------------------------------
        # ndarray
        # ------------------------------------------------------

        if isinstance(
            cloud,
            np.ndarray
        ):

            arr = np.asarray(
                cloud
            )

            if arr.size == 0:
                return states

            try:
                values = arr.astype(
                    np.float32,
                    copy=False
                )

            except Exception:
                return states

            for index in np.ndindex(
                values.shape
            ):

                value = values[index]

                if np.asarray(value).ndim != 0:
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
                        "source": source,
                        "position": index,
                        "value": value,
                        "state": state
                    }
                )

            return states

        # ------------------------------------------------------
        # list / tuple
        # ------------------------------------------------------

        if isinstance(
            cloud,
            (list, tuple)
        ):

            for index, value in enumerate(
                cloud
            ):

                self._append_value_state(
                    states,
                    source,
                    index,
                    value
                )

            return states

        # ------------------------------------------------------
        # dict
        # ------------------------------------------------------

        if isinstance(
            cloud,
            dict
        ):

            self._extract_dict_states(
                states,
                cloud,
                source
            )

            return states

        # ------------------------------------------------------
        # Cell-like object
        # ------------------------------------------------------

        if hasattr(
            cloud,
            "cells"
        ):

            return self._extract_cells(
                cloud.cells,
                source
            )

        return states

    # ==========================================================
    # packet extraction
    # ==========================================================

    def _extract_cloud(
        self,
        packet
    ):
        """
        Extract cloud object without changing it.

        Supported:

            {
                "cloud": ...
            }

        or a raw cloud object.

        No numerical interpretation occurs here.
        """

        if isinstance(
            packet,
            dict
        ):

            if "cloud" in packet:
                return packet["cloud"]

            return packet

        return packet

    # ==========================================================
    # dict states
    # ==========================================================

    def _extract_dict_states(
        self,
        states,
        cloud,
        source
    ):
        """
        Extract explicit local states from dictionaries.

        A dictionary is not assumed to be a tensor.

        Supported forms include:

            {
                position: value
            }

        and:

            {
                "cells": [...]
            }
        """

        if "cells" in cloud:

            cells = cloud.get(
                "cells"
            )

            if isinstance(
                cells,
                (list, tuple)
            ):

                extracted = self._extract_cells(
                    cells,
                    source
                )

                states.extend(
                    extracted
                )

                return

        if "value" in cloud:

            self._append_value_state(
                states,
                source,
                None,
                cloud.get("value")
            )

            return

        for position, value in cloud.items():

            if position in (
                "source",
                "representation",
                "layers",
                "layer_activity",
                "structure",
                "shape",
                "dtype"
            ):
                continue

            self._append_value_state(
                states,
                source,
                position,
                value
            )

    # ==========================================================
    # Cell extraction
    # ==========================================================

    def _extract_cells(
        self,
        cells,
        source
    ):
        states = []

        for index, cell in enumerate(
            cells
        ):

            if cell is None:
                continue

            if hasattr(
                cell,
                "empty"
            ):

                try:
                    if cell.empty:
                        continue
                except Exception:
                    pass

            if hasattr(
                cell,
                "value"
            ):

                value = cell.value

            elif isinstance(
                cell,
                dict
            ):

                value = cell.get(
                    "value"
                )

            else:

                value = cell

            self._append_value_state(
                states,
                source,
                index,
                value
            )

        return states

    # ==========================================================
    # append state
    # ==========================================================

    def _append_value_state(
        self,
        states,
        source,
        position,
        value
    ):
        state = self._classify(
            True,
            value
        )

        if state in (
            self.EMPTY_SLOT,
            self.EMPTY_VALUE
        ):
            return

        try:
            number = float(
                value
            )
        except Exception:
            return

        states.append(
            {
                "source": source,
                "position": position,
                "value": number,
                "state": state
            }
        )

    # ==========================================================
    # classification
    # ==========================================================

    def _classify(
        self,
        exists,
        value
    ):
        """
        Structural value classification.

        Empty slot
            no state exists

        Empty value
            slot exists but has no usable numeric value

        Zero value
            actual numeric zero

        Non-zero value
            actual non-zero value

        Negative values remain valid non-zero values.
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
    # structural collision
    # ==========================================================

    def _collide_states(
        self,
        planet_states,
        clip_states
    ):
        """
        Compare states without positional pairing.

        There is deliberately no:

            planet[i] <-> clip[i]

        and no:

            planet[position] <-> clip[position]

        Instead, every existing local state is allowed to
        establish a structural relation with another existing
        state according to the local value rule.

        This still produces candidates only.
        """

        relations = []

        penetrate = 0
        change = 0
        bounce = 0

        zero_zero = 0
        zero_nonzero = 0
        nonzero_zero = 0
        nonzero_nonzero = 0

        comparisons = 0

        for planet in planet_states:

            for clip in clip_states:

                p_value = planet["value"]
                c_value = clip["value"]

                p_state = planet["state"]
                c_state = clip["state"]

                collision_type = self._collision_type(
                    p_state,
                    c_state,
                    p_value,
                    c_value
                )

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

                comparisons += 1

                if collision_type is None:
                    continue

                if collision_type == self.PENETRATE:
                    penetrate += 1

                elif collision_type == self.CHANGE:
                    change += 1

                elif collision_type == self.BOUNCE:
                    bounce += 1

                relation = self._make_relation(
                    planet,
                    clip,
                    collision_type
                )

                relations.append(
                    relation
                )

                if (
                    self.max_relations is not None
                    and
                    len(relations) >= self.max_relations
                ):
                    break

            if (
                self.max_relations is not None
                and
                len(relations) >= self.max_relations
            ):
                break

        return {
            "collision": bool(
                len(relations) > 0
            ),

            "total_planet_states":
                int(len(planet_states)),

            "total_clip_states":
                int(len(clip_states)),

            "comparisons":
                int(comparisons),

            "penetrate":
                int(penetrate),

            "change":
                int(change),

            "bounce":
                int(bounce),

            "zero_zero":
                int(zero_zero),

            "zero_nonzero":
                int(zero_nonzero),

            "nonzero_zero":
                int(nonzero_zero),

            "nonzero_nonzero":
                int(nonzero_nonzero),

            "candidate_changes":
                relations,

            "heterogeneous":
                True
        }

    # ==========================================================
    # relation
    # ==========================================================

    def _make_relation(
        self,
        planet,
        clip,
        collision_type
    ):
        """
        Create a candidate relation.

        Nothing is written back.

        The relation records:

            who
            local state
            collision type
            candidate change

        Candidate change remains declarative.
        """

        candidate = self._make_candidate(
            planet,
            clip,
            collision_type
        )

        return {
            "type":
                collision_type,

            "planet":
                {
                    "position":
                        planet["position"],

                    "value":
                        planet["value"],

                    "state":
                        planet["state"]
                },

            "clip":
                {
                    "position":
                        clip["position"],

                    "value":
                        clip["value"],

                    "state":
                        clip["state"]
                },

            "candidate_change":
                candidate
        }

    # ==========================================================
    # candidate
    # ==========================================================

    def _make_candidate(
        self,
        planet,
        clip,
        collision_type
    ):
        """
        Produce a possible change.

        IMPORTANT:

            This method never modifies either cloud.

        The candidate is only a proposal for downstream
        sampling.
        """

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
                "candidate_change",

            "collision":
                collision_type,

            "planet_value":
                p,

            "clip_value":
                c,

            "proposed_value":
                proposed,

            "committed":
                False
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
        """
        Fundamental local collision rule.

        Empty states:
            no collision

        Zero / zero:
            coincidence, no change

        Zero / non-zero:
            change

        Non-zero / non-zero:

            same sign
                penetrate

            opposite sign
                bounce
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
    # snapshot
    # ==========================================================

    def snapshot(
        self
    ):
        """
        Read-only diagnostic snapshot.
        """

        if self.last_result is None:
            return None

        result = dict(
            self.last_result
        )

        if "candidate_changes" in result:

            result["candidate_changes"] = [
                dict(item)
                for item
                in result["candidate_changes"]
            ]

        return result