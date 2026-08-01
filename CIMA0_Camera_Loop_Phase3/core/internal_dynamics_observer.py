import numpy as np


class InternalDynamicsObserver:
    def __init__(self):
        self.prev_planet = None
        self.prev_clip = None

    def step_observe(self, snapshot):
        if snapshot is None or not isinstance(snapshot, dict):
            return None

        planet_obs = self._observe_planet(snapshot.get("planet"))
        clip_obs = self._observe_clip(snapshot.get("clip"))

        if planet_obs is None and clip_obs is None:
            return None

        planet_activity = planet_obs.get("activity", 0.0) if planet_obs else 0.0
        clip_activity = clip_obs.get("activity", 0.0) if clip_obs else 0.0

        return {
            "active": True,
            "activity": max(planet_activity, clip_activity),
            "planet": planet_obs,
            "clip": clip_obs,
        }

    def _observe_planet(self, planet):
        if not isinstance(planet, dict):
            return None

        state_raw = planet.get("state", [])
        velocity_raw = planet.get("velocity", [])
        energy_raw = planet.get("energy", 0.0)
        phase_raw = planet.get("phase", 0.0)

        if state_raw is None:
            state_raw = []
        if velocity_raw is None:
            velocity_raw = []
        if energy_raw is None:
            energy_raw = 0.0
        if phase_raw is None:
            phase_raw = 0.0

        state = np.asarray(state_raw, dtype=np.float32)
        velocity = np.asarray(velocity_raw, dtype=np.float32)
        energy = float(energy_raw)
        phase = float(phase_raw)

        if state.size == 0 and velocity.size == 0 and energy == 0.0 and phase == 0.0:
            return None

        if self.prev_planet is None:
            self.prev_planet = {
                "state": state.copy(),
                "velocity": velocity.copy(),
                "energy": energy,
                "phase": phase,
            }
            return {
                "activity": 0.0,
                "state_delta": 0.0,
                "velocity_delta": 0.0,
                "energy_delta": 0.0,
                "phase_delta": 0.0,
            }

        prev = self.prev_planet

        if state.shape == prev["state"].shape:
            state_delta = float(np.linalg.norm(state - prev["state"]))
        else:
            state_delta = float(np.linalg.norm(state)) if state.size else 0.0

        if velocity.shape == prev["velocity"].shape:
            velocity_delta = float(np.linalg.norm(velocity - prev["velocity"]))
        else:
            velocity_delta = float(np.linalg.norm(velocity)) if velocity.size else 0.0

        energy_delta = abs(energy - prev["energy"])
        phase_delta = abs(phase - prev["phase"])
        activity = state_delta + velocity_delta + energy_delta + phase_delta

        self.prev_planet = {
            "state": state.copy(),
            "velocity": velocity.copy(),
            "energy": energy,
            "phase": phase,
        }

        return {
            "activity": activity,
            "state_delta": state_delta,
            "velocity_delta": velocity_delta,
            "energy_delta": energy_delta,
            "phase_delta": phase_delta,
        }

    def _observe_clip(self, clip):
        if not isinstance(clip, dict):
            return None

        layers_raw = clip.get("visual_layers", [])
        embedding_raw = clip.get("embedding", [])
        basin_state_raw = clip.get("basin_state", {})

        if layers_raw is None:
            layers_raw = []
        if embedding_raw is None:
            embedding_raw = []
        if basin_state_raw is None:
            basin_state_raw = {}

        layers = [np.asarray(x, dtype=np.float32) for x in layers_raw]
        embedding = np.asarray(embedding_raw, dtype=np.float32)
        basin_state = basin_state_raw

        if not layers and embedding.size == 0 and not basin_state:
            return None

        if self.prev_clip is None:
            self.prev_clip = {
                "layers": [x.copy() for x in layers],
                "embedding": embedding.copy(),
                "basin_state": basin_state.copy() if isinstance(basin_state, dict) else basin_state,
            }
            return {
                "activity": 0.0,
                "layer_activities": [0.0 for _ in layers],
                "embedding_activity": 0.0,
                "basin_movement": 0.0,
                "focus_layer": None,
            }

        prev = self.prev_clip
        prev_layers = prev["layers"]

        layer_activities = []
        for i, layer in enumerate(layers):
            if i < len(prev_layers) and layer.shape == prev_layers[i].shape:
                layer_activities.append(float(np.linalg.norm(layer - prev_layers[i])))
            else:
                layer_activities.append(float(np.linalg.norm(layer)) if layer.size else 0.0)

        if embedding.size and prev["embedding"].size and embedding.shape == prev["embedding"].shape:
            embedding_activity = float(np.linalg.norm(embedding - prev["embedding"]))
        else:
            embedding_activity = float(np.linalg.norm(embedding)) if embedding.size else 0.0

        basin_movement = 0.0
        if isinstance(basin_state, dict) and isinstance(prev["basin_state"], dict):
            keys = set(basin_state.keys()) | set(prev["basin_state"].keys())
            for k in keys:
                a = basin_state.get(k, 0.0)
                b = prev["basin_state"].get(k, 0.0)
                if a is None:
                    a = 0.0
                if b is None:
                    b = 0.0
                try:
                    basin_movement += abs(float(a) - float(b))
                except Exception:
                    pass

        focus_layer = int(np.argmax(layer_activities)) if layer_activities else None
        activity = sum(layer_activities) + embedding_activity + basin_movement

        self.prev_clip = {
            "layers": [x.copy() for x in layers],
            "embedding": embedding.copy(),
            "basin_state": basin_state.copy() if isinstance(basin_state, dict) else basin_state,
        }

        return {
            "activity": activity,
            "layer_activities": layer_activities,
            "embedding_activity": embedding_activity,
            "basin_movement": basin_movement,
            "focus_layer": focus_layer,
        }

    def snapshot(self):
        return {
            "module": "InternalDynamicsObserver",
            "state": "observing",
        }