# 本次修复说明

## 1. 修复了 main.py 的崩溃 bug（核心问题）
- 现象：运行 `main.py` 报错
  `ValueError: shapes (512,) and (128,) not aligned: 512 (dim 0) != 128 (dim 0)`
- 原因：`main.py` 生成的测试刺激向量是 128 维，但 `Cell`（core/cell.py）和
  `AttractorGraph`（core/attractor.py）默认维度都是 512 维，两边对不上。
- 处理：
  - `main.py` 里的测试向量改为 512 维
  - `Cloud.__init__` 新增 `dim=512` 参数，统一往下传给 `Cell` 和 `AttractorGraph`，
    以后要改维度只需要改 `Cloud(dim=...)` 一处，不用满仓库找

## 2. 归档了不兼容的旧版本文件（未删除，移动到 archive/）
以下文件是早期"相位耦合（Kuramoto振荡器）"思路的实现，字段（phase/frequency）和
现在的 Cell（state/energy）完全不兼容，直接运行会报错，`main_V0.1.py` 甚至还有
语法错误（漏了个逗号）。为避免以后误改/误跑，全部移到了 `archive/`：

- `archive/main_V0.1.py`
- `archive/main_V0.2.py`
- `archive/core/cell_V0.1.py`
- `archive/core/cell_V0.2.py`
- `archive/core/cloud_V0.1.py`
- `archive/core/cloud_V0.2.py`
- `archive/core/dynamics.py`（未被任何地方 import，死代码）

如果这些文件都用不上了，可以直接删掉整个 `archive/` 目录。

## 3. 统一了 Stimulus 类定义 + 修了大小写文件名问题
- 之前 `core/stimulus.py` 和 `input/Bus.py` 各自定义了一份不完全一样的 `Stimulus`
  类，现在统一只保留 `core/stimulus.py` 这一份（补充了 `timestamp` 字段），
  `input/bus.py` 改为从 `core.stimulus` 里 import。
- `input/Bus.py` 重命名为 `input/bus.py`（全小写）。原因：Windows 文件系统不
  区分大小写，本地能跑；但 `core/main.py` 里写的是
  `from input.bus import InputBus`（小写），一旦部署到 Linux / 云端 /
  GitHub Actions 这类区分大小写的环境，会直接报 `ModuleNotFoundError`。

## 4. 已验证可运行
- `python main.py` —— 简单测试循环，已跑通
- `python -m core.main`（**注意：要用 `-m` 模块方式在项目根目录运行**，
  不能直接 `python core/main.py`，否则 Python 找不到同级的 `input` 包）
  —— 完整运行时（InputBus + Cloud + Memory），已跑通

## 没有改动的部分
- "云结构是与或关系、立体分层"这个设计方向**没有动**，这是核心架构层面的调整，
  需要先确认具体想法（比如"层"具体指什么、AND/OR 具体怎么参与到 stimulate/step
  的计算里）后再动手，避免猜错方向。
- 其余空文件（encoders/、perception/、modality/ 等）都还是占位符，没有改动。

---

## 补充：分层云 + 自适应连接 + 发展阶段控制器（新增）

### core/layered_cloud.py —— LayeredCloud
- 每种模态一层，层内复用现有的 `Cloud`
- 刺激按 `stimulus.kind` 自动路由到对应层，不做人工筛选
- 层与层之间没有写死的 AND/OR 规则，只有一张会自增自减的连接权重表：
  同时活跃就加强，没有同时活跃就自然衰减
- **已知局限（跑demo时发现的）**：目前用"层内细胞平均能量"衡量层活跃度，
  这个指标会被"刺激向量本身的多样性"干扰（向量越五花八门，覆盖的细胞越广，
  即使强度不高也会拉高平均值），不完全等于"这个组合有多稳定地被反复唤起"。
  实测中这导致了一个反直觉的结果：故意设计成"总是一起出现"的 vision-audio，
  连接权重反而比其他组合更低。这不是设计逻辑的bug，是测量口径需要换一种更
  贴近"事实上同时发生过"而不是"层有多热"的方式。下一步可以考虑直接在
  receive() 那一刻记录"这次是哪几层同时被喂了东西"，不再依赖能量这种间接指标。

### core/development.py —— DevelopmentController
- 按自然顺序（默认 听觉->视觉->文字）逐层解锁，一开始只有第一层收刺激，
  其余层的刺激直接丢弃（不是关掉，只是还没轮到）
- 解锁下一层的时机：当前层最近一段时间的波动幅度，是否比它自己的历史
  波动基线明显更小了（不是外部写死的固定阈值，是每层自己的历史在给自己定标准）
- 实测已验证：能观察到 audio 稳定后自动解锁 vision，vision 稳定后自动
  解锁 text 的完整过程，解锁时机完全由系统自身状态触发，没有人为指定步数

### demo_layered.py / demo_development.py
- 两个可以直接跑的最小演示脚本，运行方式：
  `python demo_layered.py`（看层间连接权重自己变化）
  `python demo_development.py`（看发展阶段自动解锁）
- 这两个是探索/验证用的独立脚本，还没有接入 main.py 主流程，
  等确认方向没问题后再考虑怎么整合进正式的运行时入口
