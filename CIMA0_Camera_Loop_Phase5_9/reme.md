
"全模块地图"（Phase5_8）
已接入主循环（main.py 实际跑）：

Planet（archive）→ PlanetField

CameraIO → TransportRouter → InternalDynamics.receive → 广播 CLIPField

InternalDynamics.step()：CloudState / ComputeSystem / Sampler / InternalDynamicsObserver / ObservationCache / AttentionField / CLIPField / CloudCollision

InternalDynamics.snapshot() → DisplayIO.receive_snapshot → cv2.imshow

已实现、未接入：

CameraPlanet（main.py 创建了但没用）

CameraObserver（没 import）

CameraCompute（没 import）

CloudField（没实例化）

USBCamera（main.py 直接 cv2）

DisplayDevice（main.py 直接 cv2）

transport.subscribe("visual", display)（无 publish）

AttentionField.snapshot()（无消费者）

InternalDynamicsObserver.description（无消费者）

已删除：

ObservationMemory（已删除）

未读：

core/debug/（attention_history.py / compute_history.py）（只有名字，无内容）

tests/
***********************************************************
Phase5_8 的结构理解（主环）
Camera (cv2)
  ↓
CameraIO.encode → BitPacket(camera_raw, media.bgr)
  ↓
TransportRouter.publish
  ↓
InternalDynamics.receive(packet)
  ├─ external_packets["camera_raw"] = packet
  └─ 广播给 organs → CLIPField.receive(packet)（dirty=True）
  ↓
InternalDynamics.step():
  1. cloud_state.step()          ← 瞬态云老化
  2. compute.step()              ← 资源恢复 1%
  3. planet_clock.due() → _planet_step()
       → PlanetField.step() → Planet.step() + snapshot
       → PlanetField.glimpse() → internal_fields["planet_glimpse"]
  4. _observe():
       - Planet glimpse → Observer.observe → Cache.step → AttentionField.receive+step
       - organs.activity() → signals（CLIPField.activity）
  5. _compute(signals) → ComputeSystem.select → Sampler.select（比较筛选，选 1 个）
  6. commit(result) → ComputeSystem.consume + organ.apply_compute
  7. _evolve() → organ.step()（自检 budget，CLIPField forward）
  8. _collision(result) → CloudCollision.collide(planet_cloud, clip_cloud, winner, matrix_coordinate)
       → cloud_state.receive(relations)
  9. _sample() → snapshot
  ↓
DisplayIO.receive_snapshot(snapshot)
  → _merge_planet_camera(planet, camera_raw)
  → framebuffer
  ↓
cv2.imshow
*****************************************
五个关键分离
动力/状态分离：Planet 是动力，PlanetField/CLIPField 是状态

观察/比较分离：Observer 只观察，Cache 只比较

计算/执行分离：Compute 只给机会，organ 自己决定用不用（step() 自检 budget）

碰撞/状态分离：Collision 只产关系，CloudState 承接，不回流 Planet

内部/输出分离：内部不合流，DisplayIO 才合流
*********************************************
合规的（我判断为"符合涌现模型原则"）：
CloudCollision 是纸壳筛选器机制的精确落地——负/零/空位直接决定 change/bounce/penetrate，无 _make_candidate() 裁判链

CloudField 明确拒绝标量压缩——"Do NOT do: mean(field)"，完整 field 保留

PlanetField.glimpse() 无外部 region——内部自动举手，递归逼近

PacketView 保留原 packet——"不需要 ≠ 删除"的载体级落地

AttentionField docstring 自认 "consumer: none"——最诚实的白名单声明

DisplayIO._merge_planet_camera 是唯一合流点——内部不合流，输出才合流

CLIPField.step() 自检 budget——commit 给权限，organ 自检用不用

ObservationCache 只存一个 previous——观察者有限，不 store history
********************************************
已实现未接入（我判断为"写了但主环没接"）：
CameraPlanet（main.py 创建不用）

CameraObserver（没 import）

CameraCompute（没 import）

CloudField（没实例化）

USBCamera / DisplayDevice（main.py 直接 cv2）

transport.subscribe("visual", display)（无 publish）

AttentionField.snapshot()（无消费者）

InternalDynamicsObserver.description（无消费者）
***********************************************
写死占位（我判断为"临时措施，最终内生+自平衡"）：
CloudState.capacity=32 / age<80

CloudCollision.bounce_threshold=0.0

Sampler.w_age/w_activity/w_delta = 0.25/0.35/0.40

PlanetField.size=128 / 0.01

ComputeSystem.capacity=1024 / 0.01

AttentionField.growth=0.2 / decay=0.95 / threshold=0.0

ObservationCache.threshold=0.0

CloudField.capacity=32 / rate=0.95 / release_threshold=0.01 / 0.05

Planet._split_region 四叉分割（结构还是占位，待确认）

_region_hand 的 current + temporal 1:1 权重

_magnitude 对 dict 取 max

_extract_intensity 跳过列表、spatial 叠加/scalar max
***************************************
不确定 1：camera 中间层是"待接"还是"有意绕过"？
main.py 里 camera 路径是：cap.read() → camera_io.encode() → transport.publish() → dynamics.receive() → 广播 CLIPField。

camera_planet / camera_observer / camera_compute 三件都不在路径里。

如果"待接"：当前 camera 的 delta/age/activity、块平均、举手、精算都没做，CLIPField 直接收 raw camera packet 自己 _decode 成 224×224。

如果"有意绕过"：camera 只做封装+广播，所有采样/观察在 CLIPField 内部做（_decode 的 resize 是 CLIP 自己的输入适配）。

这直接决定"采样汇编"里那套采样层（块平均、举手、精算）到底接在哪。
***************************************
不确定 2：CloudField 属于哪个层级？
CloudField 已实现（保留完整 field + Cells + inject_local_response + decay），但 InternalDynamics 里只实例化了 CloudState，没有 CloudField。

CloudState：瞬态容器，receive(relation) → cells

CloudField：瞬态云，receive(field) → 保留 field + inject_local_response → Cell

它们是两个不同的瞬态容器，CloudField 未来接在哪？ 是接在 CLIPField 内部（保留 CLIP cloud），还是接在 InternalDynamics（作为另一个云）
******************************************
不确定 3：Sampler 共享是有意还是方便？
main.py 里 sampler = Sampler()，然后 ComputeSystem 和 CLIPField 共用同一个 sampler 实例。

如果"有意"：采样器经验共享，权重演化同步（未来内生驱动时，两个选择共享同一套权重）

如果"方便"：当前只创建了一个，避免多个实例

这决定"分型"里 Sampler 是"每层独立实例"还是"共享一个实例"。
***********************************************
不确定 4：AttentionField 的产出将来接给谁？
AttentionField 已实现、已接入（_observe() 里 receive + step），但 snapshot() 无消费者。docstring 自认 "consumer: none"。

它是"只记录不消费"的观察场（永远无消费者，只是记录变化累积）？

还是"未来接给 Sampler/Compute"（注意力强度参与选择）？

这决定 AttentionField 是"死产出"还是"待接的选择输入"。
****************************************
不确定 5：InternalDynamicsObserver.describe() 的键不匹配
describe() 找 snapshot["planet"]，但 _observe() 传的是 glimpse["observation"]（含 source/type/level/region/path/exact/age，没有 planet 键）。

所以 description 目前是空 {}。

这是"接口没对齐"（describe 应该改找 glimpse["observation"] 的键）？

还是"未来 glimpse["observation"] 会加 planet 键"？

这决定 description 是"bug 导致空"还是"预留待接"。
********************************************
不确定 6：PlanetField.step() 和 InternalDynamics._planet_step() 的关系
main.py 里 planet = PlanetField(planet_rule)，InternalDynamics(planet=planet, ...)

InternalDynamics._planet_step() 调 self.planet.step() → PlanetField.step() → self.planet.step()（Planet.step()）

两层 step，不是重复（我上一轮确认过）

但 PlanetField.step() 和 InternalDynamics._planet_step() 的职责边界是什么？

PlanetField.step()：Planet.step() + snapshot + previous_state + age

_planet_step()：PlanetField.step() + PlanetField.glimpse() → internal_fields["planet_glimpse"]

glimpse() 在 _planet_step() 里调，不在 PlanetField.step() 里调——所以 PlanetField.step() 只演化，_planet_step() 演化+观察。这个分工是有意的吗？
***********************************************
已完成：

主环跑通（Camera → 广播 → 内部演化 → 观察/选择/提交 → 碰撞 → 承接 → 输出）

Planet 自主动力（PlanetField → Planet）

CLIPField 自持 organ（cloud + budget + forward）

Compute 三合一（筛选 + 选择 + 分配）

CloudCollision 筛选器机制

输出合流（DisplayIO）

待接：

camera 中间层（planet/observer/compute）

CloudField

USBCamera / DisplayDevice

"visual" 订阅

AttentionField 消费者

description 消费者
********************************
┌─────────────────────────────────────────┐
│ 容器（结构状态 + 动力源）                  │
│   Planet / PlanetField / CLIPField / ...  │
│   持有状态，自己演化                       │
└──────────────────┬──────────────────────┘
                   │ 状态/扰动
                   ▼
┌─────────────────────────────────────────┐
│ 采样                                      │
│   全局遍历 → 稀疏递归 → 焦点精算 → 过期压缩补算 │
│   （camera 焦点采样、PlanetField.glimpse、   │
│    CLIPField._sample_matrix_coordinate 都是实例）│
└──────────────────┬──────────────────────┘
                   │ 焦点/扰动
                   ▼
┌─────────────────────────────────────────┐
│ 计算（筛选 + 分配算力）                    │
│   Sampler（筛选）+ ComputeSystem（分配）    │
│   = 把有限注意力放在需要看的地方             │
└──────────────────┬──────────────────────┘
                   │ 机会/资源
                   ▼
┌─────────────────────────────────────────┐
│ IO（传递）                                │
│   取所需 + 写回状态变化 + 打包未使用的      │
│   同构信息流继续传递                       │
└─────────────────────────────────────────┘
四个模块各司其职，通过扰动互动，不改变对方内部规则。
*********************************************
┌──────────────────────────────────────────┐
│ 容器（结构状态 + 动力源）                   │
│   持有状态，自己演化，不理会全局             │
└──────────────────┬───────────────────────┘
                   │ 状态 / 扰动
                   ▼
┌──────────────────────────────────────────┐
│ 采样                                       │
│   全局遍历 → 稀疏递归 → 焦点精算 → 过期压缩补算 │
│   自持 + 内部自动举手 + 按需调用，只做份内工作  │
└──────────────────┬───────────────────────┘
                   │ 焦点 / 扰动
                   ▼
┌──────────────────────────────────────────┐
│ 计算（筛选 + 分配算力）                     │
│   = 把有限注意力放在需要看的地方             │
└──────────────────┬───────────────────────┘
                   │ 机会 / 资源
                   ▼
┌──────────────────────────────────────────┐
│ IO（传递）                                 │
│   取所需 + 写回状态变化 + 打包未使用的        │
│   同构信息流继续传递                        │
└──────────────────────────────────────────┘
四个关键词
各司其职 — 每个模块只做自己的事，不替别人决定

同构分型 — 同一个职能，在不同尺度重复，有各自的内部时序和规则

自持 + 自动举手 + 按需调用 — 不预设数量/管理，被调用时只做份内工作

扰动互动 — 模块间只投递扰动，不改对方内部规则
*********************************************
camera frame
  ↓
level 0：全图范围，稀疏取少数点（比如 4×4 = 16 个点，覆盖全图）
  ↓
自比较 delta（level 0 的点 vs 自身历史）
  ↓
选变化最大的区域
  ↓
level 1：只在选中区域内，再稀疏取点（比如 2×2 = 4 个点）
  ↓
自比较 delta
  ↓
选变化最大的子区域
  ↓
level 2：继续收窄
  ↓
...直到达到焦点精度
  ↓
反向精算：对最细层的焦点坐标附近，集中采样（取更多点/像素）
*********************************
level 0：全图分成 grid_h × grid_w
  ↓
每格采对角线三个点（初始占位）
  ↓
选变化最大的格子
  ↓
level 1：选中的格子，再分成 grid_h × grid_w（同样的分法）
  ↓
每格采对角线三个点
  ↓
选变化最大的子格子
  ↓
level 2：继续
  ↓
...直到不能再分（格子小到 1×1，或内部状态决定够了）
  ↓
焦点精算：最细层格子取原始像素
*********************************
独立采样模块（共享采样逻辑：分层稀疏 + 点数/位置内生）
  ├── camera 采样实例
  ├── PlanetField.glimpse() 实例
  └── CLIPField._sample_matrix_coordinate 实例
        │
        └── 产出：焦点坐标
              │
              ▼
        CloudCollision 反向推演
        （依赖"坐标 = 输入扰动造成的结果"）
*********************
采样模块产出焦点坐标
  ↓
内部模块反向推演（模糊推理）
  ↓
产出：对变化状态的描述（语言层面）
  ↓
这段描述可以是"实相世界"，也可以是"梦境世界"
  ↓
取决于观察者怎么对待它
  ↓
代码里不写"这是实相还是梦境"——保留缺口
********************************
物质层面（无限海洋）
  ↓ 收敛
模块 A 的描述层
  ├── 对外描述（输出接口）
  └── 对内描述（内部状态，A 自己的规则和时序）
  ↓ IO 传递
模块 B 的描述层
  ├── 对外描述
  └── 对内描述（B 自己的规则和时序）
  ↓ IO 传递
模块 C 的描述层
  └── ...
  ↓
最终幻境世界
--------------------------
每一层：都是"描述实相"——对那一层来说，它看到的描述就是"真实"

嵌套：B 看到的"实相"，是 A 的描述层；C 看到的"实相"，是 B 的描述层

同构：每一层都是"对外描述 + 对内描述"，结构相同

模块内部有自己的规则和时序：A 的内部不是"空"，是"有规则和时序"

"嵌套的同构描述实相" = 每一层都是实相（对那一层而言），每层结构相同，层层嵌套。
***************************************
camera frame（原始 BGR）
  ↓
【IO】CameraIO.encode → BitPacket(camera_raw, media.bgr)
  ↓
【采样】分层稀疏：
  level 0：全图分成 grid_h × grid_w（从分辨率派生，cell_px 初始占位）
    每格采对角线三个点（初始占位，点数/位置演化后内生）
    自比较 delta（三点 vs 自身历史）
    选变化最大的格子
  level 1：选中格子再分成 grid_h × grid_w（同分法）
    每格采对角线三个点
    自比较 delta
    选变化最大的子格子
  ...
  直到不能再分（物理 1×1 硬边界，内部状态可提前决定够了）
  ↓
【采样】焦点精算：最细层格子取原始像素（仔细看）
  ↓
【计算】Sampler.select(scores, budget) → top-budget 焦点坐标
  ↓
【IO】焦点坐标 + 粗基线 + 过期压缩，同构打包，继续传递
  ↓
【容器】CLIPField / 内部模块接收，反向推演（模糊推理）→ 结构化描述
-------------------------------
关键约束：

漏点接受，演化后部分弥补（点数/位置内生）

三点是占位，代码留"点数可变"口子

四叉/分法也是占位，未来内生

采样是独立模块，自持 + 举手 + 按需调用

描述层多层嵌套，每层"对外描述 + 对内描述"

代码不写"坐标 = 输入扰动"、不写"假定内部有规则"
*******************************
camera frame（原始 BGR）
  ↓
【IO】CameraIO.encode → BitPacket(camera_raw, media.bgr)
  ↓
【采样】分层稀疏：
  level 0：全图分成 grid_h × grid_w（从分辨率派生，cell_px 初始占位）
    每格采对角线三个点（初始占位，点数/位置演化后内生）
    每点 delta 保留（交给下游），max 聚合用于选 winner
    max 选 winner（采样模块内部，不调 Sampler）
  level 1：选中格子再分成 grid_h × grid_w（同分法）
    每格采对角线三个点
    每点 delta 保留，max 聚合选 winner
  ...
  直到不能再分（物理 1×1 硬边界，内部状态可提前决定够了）
  ↓
【采样】焦点精算：最细层格子取原始像素（仔细看）
  → 需要计算资源时，调 Sampler 分配
  ↓
【采样】粗基线（grid）保留 + 焦点精算叠加
  ↓
【采样】过期焦点压缩：丢弃细节保留轮廓（变化区域边界）
  ↓
【IO】同构打包（取所需、留其余、写回状态变化）
  ↓
【容器/下游模块】接收包裹，用自己的规则演化
************************************
概念校准
四大模块 + 各司其职 + 同构分型：

容器（结构状态 + 动力源）：持有状态，自己演化

采样：全局遍历 → 稀疏递归 → 焦点精算 → 过期压缩补算

计算：筛选 + 分配算力 = 有限注意力

IO：取所需 + 写回状态变化 + 打包未使用的

最简架构：本层容器，上层采样，下层状态：

所有模块都适用这个范式

同一个模块在不同层级是不同分型

逻辑极简，只是要改变思维习惯

Planet = 火种（Spark）：

从无限可能收敛到当前维度时空的桥梁/窗口

中间层，不是最底层

浪漫的称呼，来自《变形金刚》

海洋 → 云 → 冰山：

海洋 = Planet（火种，唯一动力源，永远存在）

云 = field（PlanetField / CloudField，演化后的局部状态）

冰山 = state（Planet.state / CloudState 的 cells）

消融 = 云/冰山会消融（状态衰减，不是演化），海洋永远存在

CLIPField = 人为放入的轻量大模型，模拟演化后的状态表现（不是"冰山"，是"模拟器"）

描述层面：

每个模块产生一次收敛，对外描述 + 对内描述

世界是嵌套的同构描述实相

实相 = 梦境 = 幻象（描述天然片面局部）

时间：

时间本身不存在，是描述先后状态的解释层面工具

时序是运行后自然产生的，不设计时序

逻辑为主，时间戳辅助

放权：

我们只接线，不做大家长

放与不放由模块规则决定

个体只对自己负责，不对全局负责

接口对不上，是 IO 同构传递项目的缺失

系统启动后：

像生命开始，不能拆解

启动后只观察，演化产生什么都是祝福

4. 我的纪律（固化）
不替导航员做方向决策

代码改动只在概念冻结后进行

每读一个文件，先写"它不知道什么"

审计姿态：先问"观察者看得到吗"

手滑清单：中心化调度 / 正向算结果 / 标量压缩 / 删除丢弃 / 全局视角 / 写死常量 / 越权 commit / 观察者驱动演化 / 观察者当控制器 / 上帝视角 / 解释层和模块层混淆 / 做大家长 / 死亡螺旋（纠缠当前层面意义）

区分"待校准"（启动前设计）和"待观察"（启动后演化）
*********************************************
tests/test_spark.py

1. 复制 main.py 的初始化（相机 / transport / dynamics / clip_field / camera_io / camera_observer）
2. 跑 1000 步
3. 每步记录：
   - collision_response_count（幂律雪崩）
   - clip_activity + planet_delta（动态耦合）
   - clip_winner_layer（路径依赖）
   - cloud_state_count（非线性恢复力）
4. 1000 步后统计：
   - 幂律雪崩：response_count 分布 + log-log 图（matplotlib）
   - 动态耦合：clip_activity 和 planet_delta 的 Spearman 相关
   - 路径依赖：winner_layer 的马尔可夫转移矩阵
   - 非线性恢复力：cloud_state_count 序列（看扰动后是否进入新水平）
5. 输出到 C:\temp\cima0_spark_test\（日志 + 图表 + 统计 JSON）
*******************************************
“看原来的代码”：不要急于替代，先看清原始代码是什么

“分工非常精细”：四大模块是概括，原始代码更细

“采样动作在哪里”：采样可能分布在多个模块，不是“一个采样模块”

“设计者只建造环境、制定规则，如何成长让内部按规则进行”：不替模块决定内部规则

“自然界没有全局遍历的浪费做法”：全局遍历是理解世界的失误

“考虑长远影响”：现在费点时间改到采样模块，长远更实用
***********************************
20261028
降维合法，消费端缺失。要补的不是“取消降维”，而是“给一个下游按需消费连续量”，
且消费方式要符合极简（不引入新阈值/新状态）。


