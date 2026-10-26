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
        bounce_threshold=0.0
    ):

        self.bounce_threshold = float(
            bounce_threshold
        )

        self.last_result = None

        #
        # endogenous max_states base.
        # placeholder: later this should evolve from her own history.
        #
        self.max_states_base = 10

    # ==========================================================
    # public
    # ==========================================================

    def collide(
        self,
        planet_cloud,
        clip_cloud,
        winner,
        matrix_coordinate
    ):
        """
        Perform one local collision.
        """

        if planet_cloud is None:
            return None

        if clip_cloud is None:
            return None

        if winner is None:
            return None

        if matrix_coordinate is None:
            return None

        clip_states = self._extract_clip_local_states(
            clip_cloud,
            winner,
            matrix_coordinate
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
    # endogenous max_states
    # ==========================================================

    def _compute_max_states(self, matrix_coordinate):
        """
        Endogenous max_states.

        Rule (designed by us, later should evolve):

            higher activity -> larger connected region
            lower activity  -> smaller connected region

        Activity is derived from the coordinate value itself
        (not from the whole cloud, to keep it local).
        """

        if matrix_coordinate is None:
            return self.max_states_base

        value = matrix_coordinate.get("current")
        if value is None:
            return self.max_states_base

        try:
            activity = abs(float(value))
        except (TypeError, ValueError):
            return self.max_states_base

        max_states = int(self.max_states_base * (1.0 + activity))

        #
        # hard bounds (placeholder)
        #
        max_states = max(1, max_states)
        max_states = min(100, max_states)

        return max_states

    # ==========================================================
    # CLIP local association
    # ==========================================================

    def _extract_clip_local_states(
        self,
        cloud,
        winner,
        matrix_coordinate
    ):
        """
        Extract the local connected region around the sampled coordinate.

        Uses 4-neighbour BFS, capped at endogenous max_states.
        """

        arr = self._extract_array(cloud)
        if arr is None:
            return []

        if arr.ndim != 3:
            return []

        levels, tokens, dimensions = arr.shape

        if matrix_coordinate is None:
            return []

        layer = matrix_coordinate.get("layer")
        token = matrix_coordinate.get("token")
        dimension = matrix_coordinate.get("dimension")

        if (
            layer is None
            or token is None
            or dimension is None
        ):
            return []

        layer = int(layer)
        token = int(token)
        dimension = int(dimension)

        if not (0 <= layer < levels):
            return []

        if not (0 <= token < tokens):
            return []

        if not (0 <= dimension < dimensions):
            return []

        #
        # endogenous max_states
        #
        max_states = self._compute_max_states(matrix_coordinate)

        visited = set()
        queue = [(token, dimension)]
        states = []

        while queue and len(states) < max_states:

            t, d = queue.pop(0)

            if (t, d) in visited:
                continue

            visited.add((t, d))

            if not (0 <= t < tokens and 0 <= d < dimensions):
                continue

            value = float(arr[layer, t, d])
            state = self._classify(True, value)

            if state in (
                self.EMPTY_SLOT,
                self.EMPTY_VALUE
            ):
                continue

            if state == self.ZERO_VALUE:
                continue

            distance = abs(t - token) + abs(d - dimension)

            states.append(
                {
                    "source": "clip",
                    "position": (layer, t, d),
                    "value": value,
                    "state": state,
                    "distance": distance,
                }
            )

            queue.append((t + 1, d))
            queue.append((t - 1, d))
            queue.append((t, d + 1))
            queue.append((t, d - 1))

        return states

    # ==========================================================
    # Planet local states
    # ==========================================================

    def _extract_planet_local_states(
        self,
        planet_cloud
    ):

        region = None

        if isinstance(planet_cloud, dict):
            region = planet_cloud.get("region")
            arr = planet_cloud.get("local_state")
        else:
            arr = self._extract_array(planet_cloud)

        if arr is None:
            return []

        states = []

        for position in np.ndindex(arr.shape):

            value = arr[position]

            if np.asarray(value).ndim != 0:
                continue

            value = float(value)

            state = self._classify(True, value)

            if state in (
                self.EMPTY_SLOT,
                self.EMPTY_VALUE
            ):
                continue

            if region is None:
                global_position = position
            else:
                global_position = (
                    int(region[0]) + int(position[0]),
                    int(region[1]) + int(position[1])
                )

            states.append(
                {
                    "source": "planet",
                    "region": region,
                    "position": global_position,
                    "value": value,
                    "state": state
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

        if isinstance(packet, dict):

            if "cloud" in packet:
                packet = packet["cloud"]
            elif "state" in packet:
                packet = packet["state"]

        if isinstance(packet, np.ndarray):
            return packet

        try:
            return np.asarray(packet)
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

                relations.append(
                    {
                        "type": collision_type,
                        "planet": dict(planet),
                        "clip": dict(clip)
                    }
                )

        result = {
            "collision": bool(len(relations) > 0),
            "winner": winner,
            "clip_local_states": int(len(clip_states)),
            "planet_local_states": int(len(planet_states)),
            "relations": relations,
            "collision_result": self._build_collision_result(relations),
            "heterogeneous": True
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
                "exists": False,
                "count": 0,
                "responses": []
            }

        responses = []

        for relation in relations:

            responses.append(
                {
                    "type": relation.get("type"),
                    "planet": dict(relation.get("planet", {})),
                    "clip": dict(relation.get("clip", {}))
                }
            )

        if not responses:
            return {
                "exists": False,
                "count": 0,
                "responses": []
            }

        return {
            "exists": True,
            "count": int(len(responses)),
            "responses": responses
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
            value = float(value)
        except Exception:
            return self.EMPTY_VALUE

        if not np.isfinite(value):
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

        if (
            planet_state == self.ZERO_VALUE
            and clip_state == self.ZERO_VALUE
        ):
            return None

        if (
            planet_state == self.ZERO_VALUE
            and clip_state == self.NONZERO_VALUE
        ):
            return self.CHANGE if (clip_value or 0.0) > 0 else None

        if (
            planet_state == self.NONZERO_VALUE
            and clip_state == self.ZERO_VALUE
        ):
            return self.CHANGE if (planet_value or 0.0) > 0 else None

        if (
            planet_state == self.NONZERO_VALUE
            and clip_state == self.NONZERO_VALUE
        ):

            product = planet_value * clip_value

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

        if self.last_result is None:
            return None

        return dict(self.last_result)