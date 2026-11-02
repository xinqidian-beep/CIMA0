import copy

import pytest

from core.internal_dynamics.cloud.cloud_state import CloudState


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def make_relation(clip=True, **extra):
    """构造一个最小可用的 collision relation。"""
    relation = {"clip": clip}
    relation.update(extra)
    return relation


# ---------------------------------------------------------------------------
# receive
# ---------------------------------------------------------------------------

class TestReceive:

    def test_receive_appends_cell(self):
        state = CloudState()
        relation = make_relation(clip=True)

        state.receive(relation)

        assert len(state.cells) == 1
        cell = state.cells[0]
        assert cell["value"] is relation
        assert cell["age"] == 0
        assert cell["source"] == "collision"
        assert cell["step"] == state.step_count

    def test_receive_does_not_copy_value(self):
        """receive 是原样 append，不做 deepcopy。"""
        state = CloudState()
        relation = make_relation(clip=True)

        state.receive(relation)

        assert state.cells[0]["value"] is relation

    def test_receive_evicts_oldest_when_over_capacity(self):
        state = CloudState(capacity=3)
        relations = [make_relation(clip=True, idx=i) for i in range(5)]

        for r in relations:
            state.receive(r)

        assert len(state.cells) == 3
        kept = [c["value"]["idx"] for c in state.cells]
        assert kept == [2, 3, 4]  # 最旧的 0、1 被 pop(0)

    def test_receive_respects_custom_capacity(self):
        state = CloudState(capacity=1)

        state.receive(make_relation(clip=True, idx=1))
        state.receive(make_relation(clip=True, idx=2))

        assert len(state.cells) == 1
        assert state.cells[0]["value"]["idx"] == 2


# ---------------------------------------------------------------------------
# step
# ---------------------------------------------------------------------------

class TestStep:

    def test_step_increments_step_count(self):
        state = CloudState()

        state.step()
        state.step()

        assert state.step_count == 2

    def test_step_increments_cell_age(self):
        state = CloudState()
        state.receive(make_relation(clip=True))

        state.step()
        state.step()

        assert state.cells[0]["age"] == 2

    def test_step_keeps_clip_cell_within_age_limit(self):
        state = CloudState()
        state.receive(make_relation(clip=True))

        # age 从 0 开始，step 79 次后 age == 79，应保留
        for _ in range(79):
            state.step()

        assert len(state.cells) == 1
        assert state.cells[0]["age"] == 79

    def test_step_drops_clip_cell_at_age_limit(self):
        state = CloudState()
        state.receive(make_relation(clip=True))

        # step 80 次后 age == 80，条件 age < 80 为假，应淘汰
        for _ in range(80):
            state.step()

        assert state.cells == []

    def test_step_drops_non_clip_cell_immediately(self):
        state = CloudState()
        state.receive(make_relation(clip=False))

        state.step()

        assert state.cells == []

    def test_step_drops_cell_missing_clip_key(self):
        """value 是 dict 但没有 'clip' 键 → .get('clip') 为 None，应淘汰。"""
        state = CloudState()
        state.receive({"region": "x"})

        state.step()

        assert state.cells == []

    def test_step_handles_non_dict_value(self):
        """
        当前实现会对非 dict 的 value 调用 .get()，预期抛 AttributeError。
        这个用例用于锁定现状；如果后续加了类型防御，改成断言不崩。
        """
        state = CloudState()
        state.receive("not-a-dict")

        with pytest.raises(AttributeError):
            state.step()

    def test_step_keeps_only_clip_cells_after_mixed_receive(self):
        state = CloudState()
        state.receive(make_relation(clip=True, idx=1))
        state.receive(make_relation(clip=False, idx=2))
        state.receive(make_relation(clip=True, idx=3))

        state.step()

        kept = [c["value"]["idx"] for c in state.cells]
        assert kept == [1, 3]


# ---------------------------------------------------------------------------
# snapshot
# ---------------------------------------------------------------------------

class TestSnapshot:

    def test_snapshot_returns_copy(self):
        state = CloudState()
        state.receive(make_relation(clip=True))

        snap = state.snapshot()

        assert len(snap) == 1
        assert snap is not state.cells
        assert snap[0] is not state.cells[0]

    def test_snapshot_is_deep_copy(self):
        state = CloudState()
        relation = make_relation(clip=True, nested={"k": [1, 2]})
        state.receive(relation)

        snap = state.snapshot()
        snap[0]["value"]["nested"]["k"].append(3)

        assert state.cells[0]["value"]["nested"]["k"] == [1, 2]

    def test_snapshot_reflects_current_state(self):
        state = CloudState()
        state.receive(make_relation(clip=True))

        snap_before = state.snapshot()
        state.receive(make_relation(clip=True))
        snap_after = state.snapshot()

        assert len(snap_before) == 1
        assert len(snap_after) == 2

    def test_snapshot_empty(self):
        state = CloudState()

        assert state.snapshot() == []