"""
CIMA0 验收测试

这份文件把整个设计讨论过程里确认过的所有约束，变成会自动运行、
会失败的断言。任何一版新代码，改动完之后先跑这份测试；
跑不过，不能算"完成"，不能进入下一步讨论。

覆盖的约束（对应讨论历史）：
  1. 元神不死       —— omega 初始化后不可被任何外部代码修改
  2. 不死           —— 长跑后 x_std 不能塌缩到接近 0（没有冻结）
  3. 不崩           —— 长跑后能量不能发散（没有 NaN/Inf，没有指数爆炸）
  4. 温和尾端       —— 能量分布的 max/median 比值有界，不是极端重尾
  5. 曲线趋势       —— energy_mean 的增长率应该收敛/放缓，不是持续加速
                        （用于区分"随机噪声会被抹平" vs "系统性偏差会累积"）
  6. 局部耦合存在   —— neighbors 拓扑真实存在、对称、且被 event() 使用
  7. 无全局访问点   —— 任何单次 event()/attention 调用，touch 的 cell 数量
                        严格有界（不会在同一时刻访问全部 N 个 cell）
  8. 无禁用关键词   —— core/ 目录源码里不能出现 reward/loss/optimizer/target 等
  9. 概率而非排序   —— attention 的出队方式是 FIFO，不是按分数 sorted 取 top-k
"""

import os
import re
import sys
import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from core.universe import Universe
from core.attention import AttentionField


# ---------- 工具函数 ----------

def run_universe(n=1024, steps=500_000, seed=42, perturb_schedule=None):
    u = Universe(n=n, seed=seed)
    energy_log = []
    log_every = max(steps // 20, 1)
    for t in range(steps):
        pmap = perturb_schedule(t) if perturb_schedule else None
        u.event(pmap)
        if t % log_every == 0:
            xs = np.array([c.x for c in u.cells])
            vs = np.array([c.v for c in u.cells])
            e = 0.5 * (vs**2 + np.array([c.omega for c in u.cells])**2 * xs**2)
            energy_log.append(float(e.mean()))
    return u, energy_log


# ---------- 1. 元神不死 ----------

def test_omega_is_immutable():
    u = Universe(n=256, seed=1)
    initial_omegas = [c.omega for c in u.cells]

    # 试图从外部修改 omega，应该直接报错（因为 omega 是只读 property）
    with pytest.raises(AttributeError):
        u.cells[0].omega = 999.0

    for _ in range(50_000):
        u.event()

    final_omegas = [c.omega for c in u.cells]
    assert initial_omegas == final_omegas, "omega 在运行过程中被改变了，元神层被污染"


# ---------- 2 & 3. 不死 / 不崩 ----------

def test_no_death_no_explosion():
    u, energy_log = run_universe(n=1024, steps=500_000)

    xs = np.array([c.x for c in u.cells])
    x_std = float(xs.std())

    assert np.isfinite(x_std), "出现 NaN/Inf，系统崩溃"
    assert x_std > 1e-4, f"x_std={x_std:.2e} 太接近 0，系统冻结了（死）"
    assert x_std < 1e3, f"x_std={x_std:.2e} 过大，系统发散了（崩）"

    for e in energy_log:
        assert np.isfinite(e), "energy_mean 出现 NaN/Inf"
        assert e < 1e6, f"energy_mean={e:.2e} 过大，疑似发散"


# ---------- 4. 温和尾端 ----------

def test_mild_tail():
    u, _ = run_universe(n=2048, steps=500_000)
    omegas = np.array([c.omega for c in u.cells])
    xs = np.array([c.x for c in u.cells])
    vs = np.array([c.v for c in u.cells])
    energies = 0.5 * (vs**2 + omegas**2 * xs**2)

    median = np.median(energies)
    max_e = energies.max()
    if median < 1e-9:
        pytest.skip("median 能量太接近 0，比值无意义，跳过（应结合 no_death 一起看）")

    ratio = max_e / median
    assert ratio < 50, f"max/median={ratio:.1f}，尾端过重，个别 cell 占据了不成比例的能量"


# ---------- 5. 能量曲线趋势：区分随机噪声 vs 系统性偏差 ----------

def test_energy_trend_is_not_runaway():
    """
    检查 energy_mean 曲线后半段的增长速率，不应该比前半段更快（加速发散）。
    随机噪声允许有波动，但不允许持续、单调、加速地往上涨。
    """
    _, energy_log = run_universe(n=1024, steps=1_000_000)
    energy_log = np.array(energy_log)
    n = len(energy_log)
    first_half_growth = energy_log[n // 2 - 1] - energy_log[0]
    second_half_growth = energy_log[-1] - energy_log[n // 2 - 1]

    # 后半段的增长量不应该显著大于前半段（允许一定波动余量）
    assert second_half_growth < abs(first_half_growth) * 3 + 1e-6, (
        f"后半段增长({second_half_growth:.4f})远超前半段({first_half_growth:.4f})，"
        "疑似系统性偏差在累积，不是随机噪声"
    )


# ---------- 6. 局部耦合存在且对称 ----------

def test_coupling_topology_exists_and_symmetric():
    u = Universe(n=512, degree=4, seed=7)
    total_edges = 0
    for i in range(len(u.cells)):
        assert len(u.neighbors[i]) > 0, f"cell {i} 没有任何邻居，耦合缺失"
        for j in u.neighbors[i]:
            total_edges += 1
            assert i in u.neighbors[j], f"邻居关系不对称: {i}->{j} 存在但 {j}->{i} 不存在"

    assert total_edges > 0


def test_coupling_actually_used_in_dynamics():
    """两个互不相连的 cell 集合，其中一个持续被强扰动，另一个不应该被明显波及。"""
    u = Universe(n=1024, seed=3)
    perturbed_ids = set(list(range(20)))
    control_ids = [i for i in range(1024) if i not in perturbed_ids
                   and not any(j in perturbed_ids for j in u.neighbors[i])][:20]

    def schedule(t):
        return {i: 0.5 for i in perturbed_ids}

    for _ in range(300_000):
        u.event(schedule(0))

    pert_mean = np.mean([abs(u.cells[i].x) for i in perturbed_ids])
    ctrl_mean = np.mean([abs(u.cells[i].x) for i in control_ids])

    assert pert_mean > ctrl_mean * 2, (
        "受扰动组和对照组差异不明显，耦合力可能没有真正接入 step()"
    )
    assert ctrl_mean < 1.0, "对照组(无连接)被明显波及，局部性被破坏，扰动发生了泄漏"


# ---------- 7. 无全局访问点 ----------

def test_no_single_call_touches_all_cells():
    """
    对 Universe.event() 和 AttentionField.observe_after_step() 做插桩，
    确认单次调用触达的 cell 数量严格有界，远小于总数 N。
    """
    n = 4096
    u = Universe(n=n, seed=9)
    attn = AttentionField(max_queue=256, propagate_prob=0.3, min_delay=50)

    touch_counts = []
    orig_local_coupling = u._local_coupling

    def instrumented(idx):
        result = orig_local_coupling(idx)
        touch_counts.append(1 + len(u.neighbors[idx]))
        return result

    u._local_coupling = instrumented

    perturb = {i: 3.0 for i in range(20)}
    for _ in range(50_000):
        idx = u.event(perturb)
        t = attn.observe_after_step(u, idx)
        touch_counts.append(t)

    max_touch = max(touch_counts)
    assert max_touch < 0.05 * n, (
        f"某次调用触达了 {max_touch} 个 cell（总数 {n} 的 {max_touch/n:.1%}），"
        "疑似出现了全局扫描/上帝视角"
    )


# ---------- 8. 源码里不能出现被禁用的关键词 ----------

BANNED_PATTERNS = [
    r"\breward\b",
    r"\bloss\b",
    r"\boptimizer\b",
    r"\btarget\b",
    r"\bgrad(ient)?\b",
    r"top_k\s*\(",
    r"\.sort\(",
    r"sorted\(.*key\s*=",
]


def test_no_banned_keywords_in_core():
    core_dir = os.path.join(ROOT, "core")
    violations = []
    for fname in os.listdir(core_dir):
        if not fname.endswith(".py"):
            continue
        path = os.path.join(core_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        for pat in BANNED_PATTERNS:
            for m in re.finditer(pat, content, re.IGNORECASE):
                line_no = content[:m.start()].count("\n") + 1
                violations.append(f"{fname}:{line_no}: matched /{pat}/")

    assert not violations, "core/ 中出现被禁用的关键词:\n" + "\n".join(violations)


# ---------- 9. 出队方式必须是 FIFO，不是按分数排序 ----------

def test_attention_pop_is_fifo_not_ranked():
    attn = AttentionField(max_queue=10, propagate_prob=0.0, min_delay=0)
    for i in range(5):
        attn._enqueue(i, now=0)

    ready = attn.pop_ready(now=100, k=10)
    assert ready == [0, 1, 2, 3, 4], (
        f"出队顺序 {ready} 不是先进先出，可能被改成了按分数排序（隐藏的 top-k optimizer）"
    )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
