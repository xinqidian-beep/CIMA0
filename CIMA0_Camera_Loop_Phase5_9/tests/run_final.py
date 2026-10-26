# run_final.py
"""
最小反馈实验 2：demand -> winner_layer。
- k_demand = 0.0, demand_penalty = 0.0：基线
- k_demand > 0：demand 推高 tax_rate（上一轮已验证）
- demand_penalty > 0：demand 惩罚所有层，改变 argmax 的 winner 选择
其余逻辑不变。
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, field
from typing import Callable, Any
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ============================================================
# 一、核心逻辑
# ============================================================

def default_capacity_fn(state: dict) -> float:
    return state["capacity_init"]


def default_tax_rate_fn(state: dict) -> float:
    """tax_rate = base + k_demand * demand_before。"""
    return state["tax_rate_init"] + state["k_demand"] * state["demand_before"]


@dataclass
class DemandTaxState:
    demand: float = 0.0
    capacity_init: float = 1.0
    tax_rate_init: float = 0.1
    k_demand: float = 0.0
    demand_penalty: float = 0.0     # 新增：demand 对 winner 选择的惩罚强度
    allow_negative: bool = False
    capacity_fn: Callable[[dict], float] = field(default=default_capacity_fn)
    tax_rate_fn: Callable[[dict], float] = field(default=default_tax_rate_fn)


def step_demand_tax(
    state: DemandTaxState,
    activity: float,
    step_info: dict[str, Any] | None = None,
) -> dict[str, float]:
    info = dict(step_info or {})
    info["activity"] = activity
    info["capacity_init"] = state.capacity_init
    info["tax_rate_init"] = state.tax_rate_init
    info["k_demand"] = state.k_demand
    info["demand_penalty"] = state.demand_penalty
    info["demand_before"] = state.demand

    capacity = state.capacity_fn(info)
    tax_rate = state.tax_rate_fn(info)
    tax = (activity + capacity) * tax_rate

    demand_before = state.demand
    new_demand = demand_before + activity - tax
    if not state.allow_negative:
        new_demand = max(new_demand, 0.0)
    state.demand = new_demand

    return {
        "activity": activity,
        "capacity": capacity,
        "tax_rate": tax_rate,
        "tax": tax,
        "demand_before": demand_before,
        "demand": state.demand,
    }


# ============================================================
# 二、winner 选择（新增 demand_penalty）
# ============================================================

def choose_winner(
    local_response: dict[int, float],
    demand_before: float,
    demand_penalty: float,
    prev_winner: int,
) -> tuple[int, dict[int, float]]:
    penalty = demand_penalty * demand_before
    current = prev_winner
    total_resp = sum(local_response.values()) or 1.0
    n = len(local_response)
    scores = {k: v - penalty * (local_response[k] / total_resp - 1.0 / n) for k, v in local_response.items()}
    winner = max(scores, key=scores.get)
    return winner, scores


def simulate_winner_with_penalty(
    records: list[dict],
    state: DemandTaxState,
    activity_field: str = "clip_activity",
) -> tuple[list[dict], list[dict]]:
    """
    按记录重演一遍，但 winner 由 choose_winner 决定（而不是直接读 records 的 winner_layer）。
    返回：
      - records_with_winner: 每条记录里 winner_layer 被替换为 choose_winner 的结果
      - dt_log: 每步 demand/tax
    """
    new_records = []
    dt_log = []
    prev_winner = records[0].get("winner_layer", 11) if records else 11

    for rec in records:
        activity = float(rec.get(activity_field, 0.0))

        # clip_local_response 不在 records.json 里，这里用占位：
        # 用 records 里现有的 winner_layer 构造一个"只有两层"的 local response，
        # 让 winner 层的 response = clip_activity，其余层为 0。
        # 这样 demand_penalty=0 时，argmax 仍然选原来的 winner_layer，
        # 和基线行为一致；demand_penalty>0 时，demand 高会把 winner 推向另一层。
        existing_winner = rec.get("winner_layer")
        # 用 records 的真实字段构造 local_response，不再用 activity 占位
        base_coll = float(rec.get("collision_count", 0) or 0)
        c_norm = max(0.0, min(1.0, base_coll / 100.0))
        # collision 越高 → 层 10 响应越高、层 11 越低（依据：10 层均值 84 > 11 层 48）
        local_response = {
            10: activity * c_norm,
            11: activity * (1.0 - c_norm),
        }

        out = step_demand_tax(state, activity, {
            "step": rec.get("step"),
            "winner_layer": existing_winner,
            "cloud_count": rec.get("cloud_count"),
            "response_count": rec.get("response_count"),
            "planet_activity": rec.get("planet_activity"),
        })
        dt_log.append(out)

        winner, scores = choose_winner(
            local_response,
            demand_before=out["demand_before"],
            demand_penalty=state.demand_penalty,
            prev_winner=prev_winner,
        )
        prev_winner = winner

        new_rec = dict(rec)
        new_rec["winner_layer"] = winner
        new_rec["_winner_scores"] = scores
        new_rec["_demand_before"] = out["demand_before"]
        new_rec["_demand_after"] = out["demand"]
        new_rec["_tax"] = out["tax"]
        new_rec["_tax_rate"] = out["tax_rate"]
        new_records.append(new_rec)

    return new_records, dt_log


# ============================================================
# 三、分析（和之前一致，但用新 records）
# ============================================================

def build_avalanche(records: list[dict]) -> dict:
    sizes = [int(r.get("response_count", 0)) for r in records]
    counter = Counter(sizes)
    xs = sorted(counter.keys())
    ys = [counter[x] for x in xs]
    return {"sizes": xs, "freqs": ys}


def build_markov(records: list[dict], field: str = "winner_layer") -> dict:
    trans = defaultdict(Counter)
    prev = None
    for r in records:
        cur = r.get(field)
        if prev is not None and cur is not None:
            trans[prev][cur] += 1
        prev = cur
    return {k: dict(v) for k, v in trans.items()}


def plot_avalanche(av: dict, path: str, title: str) -> None:
    xs, ys = av["sizes"], av["freqs"]
    plt.figure(figsize=(7, 5))
    plt.loglog(xs, ys, marker="o", linestyle="-", markersize=4)
    plt.xlabel("response_count")
    plt.ylabel("frequency")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def plot_markov(mk: dict, path: str, title: str) -> None:
    states = sorted({k for k in mk} | {k for v in mk.values() for k in v})
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    mat = [[0] * n for _ in range(n)]
    for a, row in mk.items():
        for b, c in row.items():
            mat[idx[a]][idx[b]] = c
    vmax = max((max(r) for r in mat), default=0)
    plt.figure(figsize=(6, 5))
    plt.imshow(mat, cmap="Blues", aspect="auto", vmin=0, vmax=vmax)
    plt.colorbar()
    plt.xticks(range(n), [str(s) for s in states])
    plt.yticks(range(n), [str(s) for s in states])
    plt.xlabel("to winner_layer")
    plt.ylabel("from winner_layer")
    plt.title(title)
    for i in range(n):
        for j in range(n):
            if mat[i][j]:
                plt.text(j, i, str(mat[i][j]), ha="center", va="center",
                         color="white" if vmax and mat[i][j] > vmax * 0.5 else "black")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def analyze(records: list[dict], dt_log: list[dict]) -> dict:
    av = build_avalanche(records)
    mk = build_markov(records, "winner_layer")
    switch_count = sum(
        1 for a, b in zip(records, records[1:])
        if a.get("winner_layer") != b.get("winner_layer")
    )
    clip_acts = [float(r.get("clip_activity", 0.0)) for r in records]
    mean = sum(clip_acts) / len(clip_acts) if clip_acts else 0.0
    var = sum((x - mean) ** 2 for x in clip_acts) / len(clip_acts) if clip_acts else 0.0
    zero_state = sum(1 for r in records if r.get("response_count", 0) == 0)

    demands = [d["demand"] for d in dt_log]
    tax_rates = [d["tax_rate"] for d in dt_log]
    taxes = [d["tax"] for d in dt_log]

    return {
        "avalanche": av,
        "markov": mk,
        "clip_activity_mean": mean,
        "clip_activity_variance": var,
        "winner_switch_count": switch_count,
        "winner_switch_rate": switch_count / max(len(records) - 1, 1),
        "zero_state_count": zero_state,
        "zero_state_ratio": zero_state / max(len(records), 1),
        "demand_final": demands[-1] if demands else 0.0,
        "demand_max": max(demands, default=0.0),
        "demand_mean": sum(demands) / len(demands) if demands else 0.0,
        "demand_std": (sum((x - sum(demands) / len(demands)) ** 2 for x in demands) / len(demands)) ** 0.5 if demands else 0.0,
        "tax_rate_mean": sum(tax_rates) / len(tax_rates) if tax_rates else 0.0,
        "tax_rate_max": max(tax_rates, default=0.0),
        "tax_mean": sum(taxes) / len(taxes) if taxes else 0.0,
    }


# ============================================================
# 四、路径解析 + main
# ============================================================

def resolve_records_path(cli_path: str | None) -> str:
    candidates = []
    if cli_path:
        candidates.append(os.path.abspath(cli_path))
    candidates.append(os.path.abspath("records.json"))
    here = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(here, "records.json"))
    candidates.append(os.path.join(os.path.dirname(here), "records.json"))
    seen, out = set(), []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    for c in out:
        if os.path.isfile(c) and os.path.getsize(c) > 0:
            with open(c, "r", encoding="utf-8", errors="replace") as f:
                head = f.read(64).lstrip()
            if head and head[0] in "[{":
                return c
    raise FileNotFoundError("records.json not usable. Tried:\n" + "\n".join(out))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", default=None)
    parser.add_argument("--capacity_init", type=float, default=1.0)
    parser.add_argument("--tax_rate_init", type=float, default=0.1)
    parser.add_argument("--k_demand", type=float, default=0.0)
    parser.add_argument("--demand_penalty", type=float, default=0.0,
                        help="demand 对 winner 选择的惩罚；0 = 不接这条边")
    parser.add_argument("--allow_negative", action="store_true")
    parser.add_argument("--activity_field", default="clip_activity",
                        choices=["clip_activity", "planet_activity"])
    parser.add_argument("--out_dir", default=None)
    args = parser.parse_args()

    records_path = resolve_records_path(args.records)
    with open(records_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    print(f"[run] records = {records_path} ({len(records)} records)")
    print(f"[run] k_demand = {args.k_demand}, demand_penalty = {args.demand_penalty}")

    out_dir = os.path.abspath(args.out_dir) if args.out_dir else os.path.dirname(records_path)
    os.makedirs(out_dir, exist_ok=True)
    tag = f"k{args.k_demand:g}_p{args.demand_penalty:g}"

    state = DemandTaxState(
        demand=0.0,
        capacity_init=args.capacity_init,
        tax_rate_init=args.tax_rate_init,
        k_demand=args.k_demand,
        demand_penalty=args.demand_penalty,
        allow_negative=args.allow_negative,
    )

    new_records, dt_log = simulate_winner_with_penalty(
        records, state, args.activity_field
    )
    stats = analyze(new_records, dt_log)

    print("=== RESULT ===")
    for k in ["demand_final", "demand_max", "demand_mean", "demand_std",
              "tax_rate_mean", "tax_rate_max", "tax_mean",
              "winner_switch_count", "winner_switch_rate",
              "zero_state_count", "zero_state_ratio"]:
        print(f"{k:20s} = {stats[k]}")
    print("markov =", stats["markov"])
    av_map = dict(zip(stats["avalanche"]["sizes"], stats["avalanche"]["freqs"]))
    print("avalanche 100-bin freq =", av_map.get(100, 0))
    print("avalanche head (first 5) =", list(zip(stats["avalanche"]["sizes"][:5], stats["avalanche"]["freqs"][:5])))

    analysis_path = os.path.join(out_dir, f"analysis_final_{tag}.json")
    log_path = os.path.join(out_dir, f"demand_tax_log_{tag}.json")
    winner_path = os.path.join(out_dir, f"winner_log_{tag}.json")
    av_path = os.path.join(out_dir, f"avalanche_final_{tag}.png")
    mk_path = os.path.join(out_dir, f"markov_final_{tag}.png")

    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(dt_log, f, ensure_ascii=False, indent=2)
    with open(winner_path, "w", encoding="utf-8") as f:
        json.dump([
            {
                "step": r.get("step"),
                "original_winner": records[i].get("winner_layer"),
                "new_winner": r.get("winner_layer"),
                "demand_before": r.get("_demand_before"),
                "demand_after": r.get("_demand_after"),
                "tax": r.get("_tax"),
                "tax_rate": r.get("_tax_rate"),
                "scores": r.get("_winner_scores"),
            }
            for i, r in enumerate(new_records)
        ], f, ensure_ascii=False, indent=2)

    plot_avalanche(stats["avalanche"], av_path, f"Power-law avalanche ({tag})")
    plot_markov(stats["markov"], mk_path, f"Markov transition ({tag})")
    print(f"saved: {analysis_path}")
    print(f"saved: {log_path}")
    print(f"saved: {winner_path}")
    print(f"saved: {av_path}")
    print(f"saved: {mk_path}")


if __name__ == "__main__":
    main()