from core.internal_dynamics.cloud.cloud_field import CloudField


# ---------------------------------------------------------------------------
# receive：完整场保真持有,锁定"接入点被执行"这一事实，且不依赖真实 CLIP 模型。
# ---------------------------------------------------------------------------

class TestReceive:

    def test_receive_holds_field(self):
        cf = CloudField()
        field = [[1.0, 2.0], [3.0, 4.0]]

        assert cf.receive(field) is True
        assert cf.has_field() is True
        assert cf.shape() == (2, 2)

    def test_receive_none_returns_false(self):
        cf = CloudField()

        assert cf.receive(None) is False
        assert cf.has_field() is False

    def test_receive_second_time_tracks_delta(self):
        cf = CloudField()
        cf.receive([[1.0, 1.0], [1.0, 1.0]])
        cf.receive([[2.0, 2.0], [2.0, 2.0]])

        assert cf.previous_field is not None
        assert cf.field.shape == (2, 2)
        assert abs(cf.delta - 1.0) < 1e-6

    def test_receive_shape_change_marks_structural_delta(self):
        cf = CloudField()
        cf.receive([[1.0, 1.0], [1.0, 1.0]])
        cf.receive([1.0, 2.0, 3.0])

        assert cf.delta == 1.0


# ---------------------------------------------------------------------------
# step：观测面维护（当前无 Cell，应只清事件、不崩）
# ---------------------------------------------------------------------------

class TestStep:

    def test_step_without_field_is_safe(self):
        cf = CloudField()
        cf.step()  # 不崩

        assert cf.has_field() is False

    def test_step_with_field_does_not_evolve_field(self):
        cf = CloudField()
        cf.receive([[1.0, 2.0]])

        before = cf.field.copy()
        cf.step()

        assert (cf.field == before).all()


# ---------------------------------------------------------------------------
# snapshot：只读，完整场 + 空 Cell 池
# ---------------------------------------------------------------------------

class TestSnapshot:

    def test_snapshot_empty(self):
        cf = CloudField()
        snap = cf.snapshot()

        assert snap["field"] is None
        assert snap["shape"] is None
        assert len(snap["cells"]) == 32
        assert all(c["value"] is None for c in snap["cells"])
        assert snap["merge_events"] == []
        assert snap["response_events"] == []

    def test_snapshot_returns_field_copy(self):
        cf = CloudField()
        cf.receive([[1.0, 2.0]])

        snap = cf.snapshot()
        snap["field"][0][0] = 99.0

        assert cf.field[0][0] == 1.0

    def test_snapshot_cells_empty_without_injection(self):
        cf = CloudField()
        cf.receive([[1.0, 2.0]])
        cf.step()

        snap = cf.snapshot()
        assert all(c["value"] is None for c in snap["cells"])