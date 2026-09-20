Phase5_7 作为已验证基线冻结，Phase5_8 从副本继续演化。 不在 5_7 上继续边改边试，避免把已经跑通的链路弄乱。

建议目录关系：

CIMA0_Camera_Loop_Phase5_7
        │
        │  完整复制
        ▼
CIMA0_Camera_Loop_Phase5_8
        │
        ├── 保留 Camera → InternalDynamics
        ├── 保留 CLIP organ
        ├── 保留 PlanetField
        ├── 保留 Sampler / Memory
        ├── 保留 Router / Display
        │
        └── 新阶段：
             稀疏采样
             ↓
             焦点精算
             ↓
             过期压缩
             ↓
             必要时补算
			 
			 Phase5_8 第一原则
先复制，不改逻辑。

复制完成后第一次运行，只验证：

Camera
  ↓
CameraIO
  ↓
BitPacket
  ↓
InternalDynamics
  ↓
CLIP
  ↓
Planet
  ↓
Sampler
  ↓
Router
  ↓
Display

仍然正常。

确认基线一致以后，我们再开始 Phase5_8 的第一项结构改造：

把“完整 CLIP forward”从默认计算方式，变成由稀疏焦点触发的昂贵计算。

而不是一上来就在 CLIPField 里面堆各种 threshold、frame counter 或时间周期。

5_7 = 基线 / 冻结
5_8 = 稀疏计算动力学实验场

你先完成目录复制。复制后把 Phase5_8 的目录结构 或第一次运行日志贴过来，我们从基线检查开始。

**********************************
Phase5_8 的拓扑应该逐渐变成
                         CAMERA
                           │
                           ▼
                  CameraObserver
                           │
                           ▼
                  ObservationCache
                           │
                           ▼
                    AttentionField
                           │
                 ┌─────────┴─────────┐
                 │                   │
              stable              changed
                 │                   │
              aging               focus
                 │                   │
             compress              │
                 │                 │
                 └──────┐   ┌──────┘
                        ▼   ▼
                    SparseSampler
                          │
                     compute budget
                          │
                          ▼
                      CLIPField
                          │
                          ▼
                  expensive local
                    computation
                          │
                          ▼
                    visual field
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        CloudCollision             Memory
              │                       │
              ▼                       ▼
         PlanetField              history
              │                       │
              └───────────┬───────────┘
                          ▼
                       Signals
                          │
                    ┌─────┴─────┐
                    ▼           ▼
                Attention     Compute
				
				
				*******************************
				*******************************
				*******************************
变化
 ↓
焦点
 ↓
计算
 ↓
结果
 ↓
历史
 ↓
下一次焦点
*******************************
*******************************
*******************************	

整个 Phase5_8 的核心重新固定下来：			
                 Camera
                    │
                    ▼
               CLIPField
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Layer 0     Layer 1     ... Layer 11
        │           │               │
        └───────────┴───────────────┘
                    │
                    ▼
               CLIP Cloud
                    │
                    │
                    ▼
             CloudCollision
                    ▲
                    │
              Planet Cloud
                    │
                    ▼
              PlanetField

*********************************	
CloudCollision
      │
      ▼
碰撞关系
      │
      ▼
哪个 CLIP layer / cloud region
表现出特殊关系？
      │
      ▼
Special Layer / Focus		
这里的 Focus 才有意义。
*****************************  
Internal Dynamics
        │
        ├── evolution
        │
        ├── collision
        │
        ├── focus
        │
        └── sampling
                 │
                 ▼
          Observation Output
                 │
                 ▼
             DisplayIO
			 
显示只是读取系统允许输出的状态。

**********************************
Phase5_8 的正确数据流
                         ┌───────────────┐
Camera ────────────────► │   CLIP 内部   │
                         │               │
                         │ token         │
                         │ transformer   │
                         │ layer 0~11    │
                         └───────┬───────┘
                                 │
                                 ▼
                         CLIP External Adapter
                                 │
                    完整同构 CIMA0 BytePacket
                                 │
                                 ▼
                         ┌───────────────┐
                         │  Cloud System │
                         └───────┬───────┘
                                 │
                 ┌───────────────┼──────────────┐
                 ▼               ▼              ▼
             Collision       Attention       Sampler
                 │               │              │
                 └───────────────┴──────────────┘
                                 │
                                 ▼
                              Compute

而且 Planet/FANET 也走同样的外部流通规则：
CLIP Cloud ──┐
             ├──► 同构流通结构 ──► Collision
Planet Cloud ┘

不同内部系统可以完全不同，但跨系统之后，都必须能够进入同一个状态流通体系。
整个 Phase5_8 的层级就比较清楚了：
                    外部世界
                       │
                       ▼
                    Camera
                       │
                       │ 原始字节流
                       ▼
                 Internal Input
                       │
                       ▼
              ┌─────────────────┐
              │ InternalDynamics │
              │                 │
              │     内部世界     │
              │                 │
              └─────────────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Planet Cloud         CLIP Cloud
             │                   │
             │                   │
             └─────────┬─────────┘
                       ▼
                 CloudCollision
                       │
                       ▼
                结构关系产生
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      special_layers       focus_candidates
             │                   │
             └─────────┬─────────┘
                       ▼
                     Focus
                       │
                       ▼
                    Sampler
					
Internal Dynamics
│
├── PlanetField
│      │
│      └── Planet Cloud
│
└── CLIPField
       │
       └── CLIP Multilevel Cloud
              │
              ├── layer 0
              ├── layer 1
              ├── ...
              └── layer 11
这时候 CLIP Multilevel Cloud 才真正成为“内部云”。

			  
                         EXTERNAL WORLD
                              │
                              ▼
                           Camera
                              │
                              │ raw bytes
                              ▼
                    ┌───────────────────┐
                    │ InternalDynamics  │
                    │                   │
                    │   external input  │
                    └─────────┬─────────┘
                              │
                    internal disturbance
                              │
                              ▼
                    ┌───────────────────┐
                    │  Internal World   │
                    │                   │
                    │ ┌───────────────┐ │
                    │ │  PlanetField  │ │
                    │ │       ↓       │ │
                    │ │ Planet Cloud  │ │
                    │ └───────┬───────┘ │
                    │         │         │
                    │         ↕         │
                    │ ┌───────┴───────┐ │
                    │ │   CLIPField   │ │
                    │ │       ↓       │ │
                    │ │ CLIP Cloud    │ │
                    │ │               │ │
                    │ │ layer 0       │ │
                    │ │ layer 1       │ │
                    │ │ ...           │ │
                    │ │ layer 11      │ │
                    │ └───────┬───────┘ │
                    │         │         │
                    └─────────┼─────────┘
                              │
                              ▼
                       CloudCollision
                              │
                     structural relation
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
         relations     special_layers    focus_candidates
                                                │
                                                ▼
                                              Focus
                                                │
                                                ▼
                                             Sampler
                                                │
                                                ▼
                                      selected structure
                                                │
                                                ▼
                                       homogeneous bytes
                                                │
                                                ▼
                                              Router
                                                │
                                      ┌─────────┴─────────┐
                                      ▼                   ▼
                                   Display              Other
								   
								   
								   
这张图里最重要的一条原则就是：

Camera 在内部云之外。

Camera 是输入源。

Planet 和 CLIP 是内部存在的云。

Collision 是内部云之间的关系机制。

Focus 是碰撞之后产生的短暂关注状态。

Sampler 是从候选结构中取用。

Display 则只是最终同构流的一个消费者。		

                 同构字节流
                     │
                     ▼
              ┌─────────────┐
              │    Module   │
              └─────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
      自己需要的信息         自己不需要的信息
          │                     │
          ▼                     ▼
       取用/处理              不丢弃
          │                     │
          └──────────┬──────────┘
                     ▼
              重新打包成
              同构字节流
                     │
                     ▼
                继续流通						   

Camera 产生一个同构字节流。
这个字节流进入内部。
CLIP 遇到它，因为 CLIP 能处理其中自己认识的部分，于是取用那部分。
CLIP 没有权力删除其它信息。
CLIP 产生自己的内部状态，并把相关信息重新封装进同构字节流。
这个流继续在内部传播。

CLIP Cloud 也要重新理解

                  同构字节流
                       │
                       ▼
                 ┌──────────┐
                 │  CLIP    │
                 └──────────┘
                       │
             取用自己需要的信息
                       │
                       ▼
             CLIP内部12层结构
                       │
                       ▼
                CLIP Multilevel
                     Cloud
                       │
                       │
              保留其它信息
                       │
                       ▼
                同构字节流
                       │
                       ▼
                 继续流通


四条检查代码：

① 模块不知道全局
模块只知道：

我是谁
我能做什么
我的接口是什么
不知道：

数据最终去哪
谁应该赢
谁应该显示
系统整体目的是什么
② 接口永远是同构字节流
不是：

camera_data → CLIPData → CollisionData → FocusData
而是：

        同构字节流
             ↓
        模块取用
             ↓
        局部产生变化
             ↓
        同构字节流
             ↓
        继续流通
③ “不需要” ≠ “删除”
这是最重要的一条。

模块 A 不需要 X
        ≠
模块 A 删除 X
而是：

A 不取用 X
    ↓
X 原样保留
    ↓
继续封装
    ↓
后面的模块仍然可以取用 X
④ 显示也是一个模块
所以显示不是：

CLIP ─────────→ Display
Planet ────────→ Display
而应该是：

                 同构流
                   │
                   ▼
              Display 模块
                   │
          只取自己认识的部分
                   │
                   ▼
                 显示
显示为什么能看到某个东西，不应该由 CLIP 或 Planet 决定。

是因为那个信息沿着同构流走到了 Display，而 Display 恰好认识它。

所以你这次把原始逻辑补充出来以后，Phase5_8 的方向实际上重新清晰了：

                     EXTERNAL
                        │
                     Camera
                        │
                        ▼
                 同构字节流
                        │
                        ▼
              ┌─────────────────┐
              │ Internal Flow   │
              │                 │
              │  Planet         │
              │    ↕            │
              │  CLIP           │
              │    ↕            │
              │  Collision      │
              │    ↕            │
              │  Focus          │
              │    ↕            │
              │  Sampler        │
              │                 │
              └─────────────────┘
                        │
                 同构字节流
                        │
                        ▼
                    Display
但这个图里的 ↕ 不是预设的数据管线。

它表达的是：

同一个同构信息流在内部流动；各模块自主取用、产生变化、重新封装，而不是由中央控制器规定“这个数据必须交给那个模块”。

这才真正符合你说的涌现模型。


① CLIPField
      ↓
   完整 Multilevel Cloud
      ↓
② CloudCollision
      ↓
   relations
   special_layers
   focus_candidates
      ↓
③ Focus
      ↓
④ Sampler				 
而且每一步都必须遵守：
完整信息流
     ↓
模块自主取用
     ↓
产生自己的结果
     ↓
不删除其它信息
     ↓
重新进入同构流
------------------
packet()
    =
同构流通出口

collision_projection()
    =
CloudCollision读取CLIP Cloud的只读接口
************************************
CloudCollision 不能再把 CLIP cloud 压缩成 mean/energy/variance/density 后就结束。

下面这个版本保留：

Planet Cloud

完整 (12, 50, 768) CLIP Multilevel Cloud

12 个 layer

每个 layer 的结构统计

每个 layer 与 Planet 的关系

特殊 layer

特殊 layer 内的 token 候选

不创建 Focus

不选择 winner

不修改任何 cloud

同时把 collision 定义为结构关系是否形成，而不是旧版本的“两个平均统计量是否接近”。
***********************************************
Phase5_8 以后统一采用下面这个概念图：
                         EXTERNAL INPUT
                              │
                              │ raw bytes
                              ▼
                         ┌──────────┐
                         │  Camera  │
                         └────┬─────┘
                              │
                              ▼
                    Internal Dynamics
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        ┌─────────┐      ┌─────────┐      ┌─────────┐
        │CLIPField│      │Planet...│      │ Other   │
        │  organ  │      │  organ  │      │ organs  │
        └────┬────┘      └────┬────┘      └─────────┘
             │                │
             │                │
             ▼                ▼
       CLIP Internal      Planet Internal
           Cloud              Cloud
             │                │
             │                │
             │                │
             │         ┌──────┴──────┐
             │         │             │
             │         │ Cloud State │
             │         │             │
             │         │128 × 128    │
             │         └──────┬──────┘
             │                │
             │                │
             └───────┬────────┘
                     ▼
              Cloud Topology
                     │
                     │
                     ▼
               CloudCollision
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
     penetrate     change       bounce
        │            │            │
        └────────────┼────────────┘
                     ▼
              Collision Structure
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
           special       interaction
           structure
              │
              ▼
        focus candidates
              │
              ▼
       Attention / Focus
	   
************************
***************************	 
Camera 不决定 CLIP Cloud。

而是：

Camera
   ↓
输入扰动
   ↓
CLIPField 内部动力
   ↓
Cloud 自身形成状态

所以更准确地说：

Camera ──► disturbance
                 │
                 ▼
             CLIPField
                 │
          internal dynamics
                 │
                 ▼
             CLIP Cloud
*******************************
*******************************
CloudCollision 的职责也更加清楚,它只面对已经形成的两个内部 Cloud：
        CLIP Cloud
            │
            │
            ▼
       ┌───────────┐
       │           │
       │ Collision │
       │           │
       └───────────┘
            ▲
            │
            │
        Planet Cloud
然后在对位空间里处理：
Cloud A              Cloud B

空位        ↔        空位
空位        ↔        空值
空值        ↔        零值
零值        ↔        非零
非零        ↔        非零
最终才进入：		
穿透
变化
弹开
这也解释了为什么不能把 CLIP (12,50,768) 简单理解成“输入的 12×50×768 个数”12 × 50 × 768 是：

CLIPField 当前形成出来的内部状态结构。
存在：

Internal Dynamics
      +
CLIPField
      +
Cloud state evolution
下一版 CloudCollision 的核心应该非常纯
它的输入应该是：

Planet Cloud
CLIP Cloud
它做：

1. 建立对位拓扑

2. 读取双方 Cloud 状态

3. 判断：
   empty slot
   empty value
   zero
   non-zero

4. 对非零状态进行碰撞计算

5. 产生：
   penetration
   change
   bounce

6. 汇总碰撞结构

7. 提供 interaction

8. 提供 special collision regions
   → 作为后续 Focus 的候选
Phase5_8 的核心思想压缩成一句话
Camera 只提供外部扰动；内部 Cloud 自主决定取用和形成什么状态；Cloud Collision 只对已经形成的异质内部状态进行对位碰撞，并由空位、空值、零值、非零值自然产生穿透、变化与弹开。  
***************************** 
class CloudCollision:

    def analyze(self, clouds):
        """
        判断 cloud 之间是否存在直接碰撞关系。
        """

    def resolve(self, candidates):
        """
        接收 Sampler 已经决定的 winner。
        """

    def commit(self, shared_stream, winner):
        """
        winner 才允许修改自己的区域。
        其他区域原样保留。
        """

    def preserve(self, shared_stream):
        """
        未获选部分保持原样。
        """
******************************
Phase5_8 当前状态
────────────────────────────

① Camera
   480×640×3 BGR
        ✓

② Camera → BitPacket
        ✓

③ InternalDynamics.receive()
        ✓

④ Planet cloud
   128×128
        ✓

⑤ CLIP cloud
   12×50×768
        ✓

⑥ CloudCollision
   heterogeneous
   no direct positional collision
        ✓

⑦ candidate collection
   Planet + CLIP
        ✓

⑧ Sampler
   Planet score = 0.006875
   CLIP   score = 0.076530
        ✓

⑨ Winner
   CLIP
        ✓

⑩ Compute allocation
        ✓

⑪ Winner → shared-flow commit
        ← 当前缺口

⑫ Loser preserve
        ← 随⑪一起完成

⑬ Repack
        ← 随⑪完成

⑭ Router → Display
        ✓（目前仍是并行输出）
*****************************
| 模块               | 职责             |
| ---------------- | -------------- |
| CloudCollision   | 描述 cloud 之间的关系 |
| Compute/Sampler  | 竞争、选唯一赢家       |
| InternalDynamics | 执行赢家写回共享流      |
********************************		
让 _compute() 返回的 winner 进入“共享流写回”，而不是在 _sample() 中再次把各 organ 当成互相独立的输出源。让 _compute() 返回的 winner 进入“共享流写回”，而不是在 _sample() 中再次把各 organ 当成互相独立的输出源。

raw / signals
      │
      ▼
┌──────────────┐
│    step()    │   调度，不做具体动力学
└──────┬───────┘
       ▼
┌──────────────┐
│   _compute() │   计算“谁获得这次动作”
└──────┬───────┘
       ▼
┌──────────────┐
│   commit()   │   把计算结果正式写入内部状态
└──────┬───────┘
       ▼
┌──────────────┐
│   _sample()  │   只读当前已提交状态
└──────┬───────┘
       ▼
    snapshot
	
关键原则是：

_compute() 不修改正式状态

commit() 是唯一的状态提交点

_sample() 绝不反向改变动力学

step() 只是组织生命周期

snapshot 来自 _sample()，而不是直接从 compute 临时结果拿

compute 的“举手/选举”结果和真正的状态改变分离
**************************************
receive() 和这条线不要混在一起。
                 external input
                       │
                       ▼
                 receive(packet)
                       │
                       ▼
                pending disturbance
                       │
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 │
            step()              │
              │                 │
        _compute()              │
              │                 │
           commit() ◄───────────┘
              │
           _sample()
              │
              ▼
          snapshot
也就是说：

receive() 是输入进入系统。

step() 是内部时间推进。

_compute() 是选择。

commit() 是状态改变。

_sample() 是观察。

这五个动作不要再互相越权。	
**********************
把 internal_dynamics.py 收成这个骨架
class InternalDynamics:

    def __init__(self, ...):

        self.organs = {}

        self.compute = None

        self.last_snapshot = None


    def register(
        self,
        name,
        organ
    ):

        self.organs[name] = organ


    def receive(
        self,
        packet
    ):

        # external input only
        # prepare / route / inject pending input

        ...


    def step(self):

        signals = self._collect_signals()

        result = self._compute(
            signals
        )

        self.commit(
            result
        )

        return self._sample()


    def _collect_signals(self):

        signals = []

        for name, organ in self.organs.items():

            if not hasattr(
                organ,
                "activity"
            ):
                continue

            state = organ.activity()

            if state is None:
                continue

            signals.append(
                {
                    "name": name,
                    "organ": organ,
                    "state": state
                }
            )

        return signals


    def _compute(
        self,
        signals
    ):

        ...


    def commit(
        self,
        result
    ):

        ...


    def _sample(self):

        ...


    def snapshot(self):

        if self.last_snapshot is None:
            return None

        return self.last_snapshot.copy()
*************************************
两套 step()
CloudField 自己有：

def step(self):

    self.collision()

    self.decay()

    self.propagation()
而 InternalDynamics 现在有：

def step(self):

    signals = ...

    result = self._compute(signals)

    self.commit(result)

    return self._sample()
这两个 step() 不能混为一谈。

应该是：

InternalDynamics.step()
        │
        ├── _compute()
        │
        ├── commit()
        │
        └── _sample()
而：

CloudField.step()
        │
        ├── collision()
        ├── decay()
        └── propagation()
是 CloudField 自己的局部演化机制。：

InternalDynamics 不应该替 CloudField 决定 collision / decay 的具体规则。
*************************************
                    InternalDynamics
                           │
                    ┌──────▼──────┐
                    │    step     │
                    └──────┬──────┘
                           │
                     request_compute
                           │
                           ▼
                    ┌─────────────┐
                    │   Compute   │
                    └──────┬──────┘
                           │
                       allocation
                           │
                           ▼
                     commit()
                           │
                  execute_compute()
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         collision       decay     propagation
              │            │            │
              └────────────┼────────────┘
                           ▼
                        sample
                           │
                           ▼
                       snapshot
**********************************************
step() 应该重新定义成：
step
 │
 ├── 1. internal dynamical evolution
 │       ├── cloud
 │       ├── planet
 │       └── collision
 │
 ├── 2. collect organ signals
 │
 ├── 3. _compute
 │
 ├── 4. commit
 │
 └── 5. _sample

CloudState 是 InternalDynamics 自己拥有的内部状态。

而：

self.organs = {}
是：

可注册的内部器官。

因此：
Cloud ≠ organ
Planet ≠ organ
Compute ≠ organ
Sampler ≠ organ
这几个层级必须保持。 
那么 step → _compute → commit → _sample 应该这样理解
step()
只负责生命周期调度：
step
 │
 ├── update internal dynamics
 │
 ├── collect signals
 │
 ├── _compute
 │
 ├── commit
 │
 └── _sample
_compute()
只回答：

这一时刻，哪个内部信号值得获得一次计算机会？
**********************************
Phase5_8 的主线明确为：
                    InternalDynamics.step()
                              │
                              ▼
                         _observe()
                              │
                    observation signals
                              │
                              ▼
                         _compute()
                              │
                       selected action
                              │
                              ▼
                          commit()
                              │
                       formal execution
                              │
                              ▼
                         _evolve()
                              │
                              ▼
                         _sample()
						 
********************************************
时间关系应该是：
T(n)

上一轮状态
    │
    ▼
observe
    │
    ▼
evaluate previous decision
    │
    ▼
compute current decision
    │
    ▼
commit current decision
    │
    ▼
evolve
    │
    ▼
sample
    │
    ▼
T(n+1)
******************************************
    def step(self):

        #
        # 1. observe
        #

        signals = self._observe()


        #
        # 2. compute
        #

        result = self._compute(
            signals
        )


        #
        # 3. commit
        #

        self.commit(
            result
        )


        #
        # 4. evolve
        #
        self._planet_step()
        self._evolve()


        #
        # 5. sample
        #

        return self._sample()
*********************************
生命周期归位：
                 EXTERNAL
                    │
                    ▼
                 receive
                    │
                    ▼
              pending input
                    │
                    ▼
                 step()
                    │
             ┌──────┴──────┐
             ▼             │
          observe          │
             │             │
             ▼             │
          signals          │
             │             │
             ▼             │
         _compute          │
             │             │
             ▼             │
           winner          │
             │             │
             ▼             │
          commit           │
             │             │
             ▼             │
          evolve           │
             │             │
             ▼             │
          _sample          │
             │             │
             ▼             │
        last_snapshot      │
                           │
                           ▼
                        snapshot

****************************************
内部动力学拥有自己的时间；观察拥有自己的时间。Planet 的计算复杂度 ≠ Observer 的计算复杂度.先把：

step → _compute → commit → _sample
重新定义成：

observe
   ↓
_compute
   ↓
commit
   ↓
_sample
而内部演化本身不应该被 Sampler 控制。
Compute
不是
“让 Planet 运行”

而是
“决定有限计算资源观察哪里”
无限的是内部状态空间和演化。
有限的是每一次观察。
Sampler 不负责让宇宙演化。
Sampler 只负责回答：
“现在这么多变化里，我看哪一个？”
把 InternalDynamics.step() 的语义彻底改成：

推进/承接无限内部演化 → 观察当前变化 → 计算选择一个最大/最值得的候选 → commit 一次 → sample 一次。
*********************************	
我觉得这里真正解决复杂性的，不是“记住更多代码”，而是**建立一套让任何人都能重新推导出架构的坐标系**。

你现在这个项目已经不是普通的“模块调用关系”了。它同时存在：

* 时间关系
* 状态关系
* 数据关系
* 计算资源关系
* 观察关系
* 选择关系
* 演化关系
* 所有权关系
* 因果关系

如果只看 Python 文件，很容易迷失。

我刚才能把它理清，主要用了下面这套方法。

---

# 1. 第一件事：不从代码开始，而从“谁拥有什么”开始

例如你这里最重要的不是：

```python
self.planet.step()
```

而是先问：

```text
谁拥有 Planet？
谁拥有 Cloud？
谁拥有 Organ？
谁拥有 Observation？
谁拥有 Compute？
谁拥有 Sample？
```

于是马上得到：

```text
InternalDynamics
│
├── Planet
├── Cloud
├── Organs
├── ComputeSystem
├── Observer
├── ObservationCache
├── AttentionField
└── Transport
```

这一步叫：

> **Ownership Map（所有权图）**

只要所有权明确，很多“谁应该调用谁”的问题自然消失。

---

# 2. 第二件事：区分“存在”和“观察”

这是你这个系统最容易被普通软件工程思维误读的地方。

普通程序：

```text
step()
 ↓
计算
 ↓
得到结果
```

你的系统不是。

你的系统更像：

```text
                 内部世界
                    │
             持续 / 无限演化
                    │
          ┌─────────┴─────────┐
          │                   │
       Planet              Organs
          │                   │
          └─────────┬─────────┘
                    │
                  观察
                    │
                    ▼
                 Observer
                    │
                    ▼
              有限 signals
                    │
                    ▼
                 Sampler
```

所以必须建立第二张图：

> **Existence Map（存在图）**

它回答：

> 什么东西自己存在、自己演化？

---

# 3. 第三张图：观察图

然后再单独画：

```text
Planet
   │
   ▼
snapshot / change
   │
   ▼
Observation
   │
   ▼
activity / delta / age
   │
   ▼
Sampler
```

CLIP也是：

```text
Camera
   │
   ▼
CLIPField
   │
   ▼
activity / state
   │
   ▼
Sampler
```

最后：

```text
Planet ──┐
         ├──> candidates ──> Sampler ──> winner
CLIP ────┘
```

这时候复杂度突然下降了。

因为你不再把：

```text Planet
PlanetField
Observer
ObservationCache
Compute
Sampler
```

当成一个整体。

而是分别问：

> 它在“存在图”里干什么？

> 它在“观察图”里干什么？

---

# 4. 第四张图：时间图

这正是刚才 `Planet.step()` 问题出现的地方。

如果没有时间图，很容易得出：

> Planet 太慢，所以不要每帧 step。

但你的思想告诉我们：

```text
Planet time
∞────────────────────────────>

Observer time
    ↑       ↑       ↑       ↑

Sampler time
    ↑       ↑       ↑       ↑
```

于是马上知道：

**两个系统不应该共享同一个时间尺度。**

所以我现在会给这个项目增加一个非常重要的概念：

> **Temporal Ownership（时间所有权）**

谁决定一个东西什么时候演化？

谁决定什么时候观察？

谁决定什么时候采样？

这三个问题必须分开。

---

# 5. 第五张图：资源图

然后再看 ComputeSystem：

```text
Organ
   │
   │ request
   ▼
ComputeSystem
   │
   │ allocate
   ▼
selected activity
```

这里 Compute 不是：

> “宇宙的发动机”

而是：

> **有限计算机会的分配器。**

于是：

```text
内部演化
≠
计算资源分配
```

这也是为什么我们刚才发现：

```python
self.compute.select(signals)
```

和：

```python
self.planet.step()
```

不能简单理解成上下级关系。

---

# 6. 第六张图：因果图

最后我会问：

> 谁改变谁？

目前大概是：

```text
Camera
  │
  ▼
packet
  │
  ▼
CLIPField
  │
  ▼
activity
  │
  ▼
Observation
  │
  ▼
Compute/Sampler
  │
  ▼
winner
  │
  ▼
Commit
  │
  ▼
internal action
  │
  ▼
state evolution
  │
  ▼
next observation
```

这才是真正的：

> **Causal Loop（因果环）**

---

# 7. 这样一来，我实际上不是“读懂了几百行代码”

而是在脑中建立了六张地图：

```text
① Ownership Map
谁拥有谁

② Existence Map
谁自己存在/演化

③ Observation Map
谁观察谁

④ Temporal Map
谁以什么时间尺度运行

⑤ Resource Map
计算机会如何流动

⑥ Causal Map
什么改变什么
```

然后再把六张图叠起来。

这比单纯读代码有效得多。

---

# 8. 所以我认为 CIMA0 现在非常需要一个“架构宪法”

如果以后其他人、另一个 AI、甚至未来的你重新打开项目，不应该要求他们：

> “把几十个 `.py` 文件全部读完。”

而应该让他们先看到一个文件：

```text
CIMA0_ARCHITECTURE.md
```

甚至最好是：

```text
CIMA0/
│
├── ARCHITECTURE.md
├── TOPOLOGY.md
├── PRINCIPLES.md
├── LIFECYCLE.md
└── core/
```

---

# 9. `ARCHITECTURE.md` 只回答五个问题

我建议非常严格：

```text
1. 世界由什么组成？
2. 谁拥有状态？
3. 谁负责演化？
4. 谁负责观察？
5. 谁负责选择？
```

不要把具体代码塞进去。

---

# 10. `TOPOLOGY.md` 只画图

例如：

```text
                         CIMA0
                           │
             ┌─────────────┼─────────────┐
             │             │             │
          EXTERNAL      INTERNAL       OUTPUT
             │             │             │
          Camera        Dynamics       Display
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       Planet            Cloud            Organs
          │                                 │
          │                              CLIP
          │                │                │
          └────────────────┼────────────────┘
                           │
                       Observation
                           │
                         Signals
                           │
                        Compute
                           │
                         Sampler
                           │
                        Winner
                           │
                         Commit
                           │
                      next state
```

一张图就能让新人获得 70% 的方向感。

---

# 11. `LIFECYCLE.md` 则只解释一件事

例如：

```text
EXTERNAL INPUT
      │
      ▼
    receive
      │
      ▼
INTERNAL CONTINUOUS EVOLUTION
      │
      ▼
    observe
      │
      ▼
   candidates
      │
      ▼
    compute
      │
      ▼
    sampler
      │
      ▼
    ONE WINNER
      │
      ▼
    commit
      │
      ▼
    ONE SAMPLE
```

然后明确写：

> **Observation is finite. Internal evolution is not.**

这句话我认为应该成为 CIMA0 的核心架构原则之一。

---

# 12. 最重要的是：每个模块只写“它不知道什么”

你现在的代码其实已经在做这个事情。

例如 `CloudField`：

```text
CloudField knows:
    collision
    decay
    propagation

CloudField does NOT know:
    CPU
    GPU
    scheduler
    external meaning
```

这是非常好的架构文档方式。

以后每一个核心模块都应该采用同样格式：

```text
Planet

KNOWS:
    own state
    own dynamics

DOES NOT KNOW:
    observer
    sampler
    camera
    compute allocation
```

---

# 13. 这样 AI 就非常容易进入项目

如果以后一个新的 AI 接手 CIMA0，我希望它首先拿到的不是：

```text
internal_dynamics.py
```

而是：

```text
                CIMA0 QUICK MAP

WORLD
  ├── Planet
  ├── Cloud
  └── Organs

OBSERVATION
  ├── Observer
  ├── ObservationCache
  └── Activity

SELECTION
  ├── Compute
  └── Sampler

ACTION
  └── Commit

OUTPUT
  └── Sample


CORE RULE

Internal dynamics is continuous/infinite.

Observation is finite.

Sampler selects what is worth observing.

Compute allocates limited opportunity.

No observer owns the world.
No sampler owns the world.
No display owns the world.
```

然后才去看代码。

---

# 14. 我甚至建议给每个核心函数加一个“语义标签”

例如：

```python
def receive(...)
```

标：

```text
ROLE: INPUT BOUNDARY
CHANGES: pending external packets
DOES NOT: interpret
```

`_observe()`：

```text
ROLE: OBSERVATION
CHANGES: observation context only
DOES NOT: evolve
```

`_compute()`：

```text
ROLE: SELECTION
CHANGES: compute decision
DOES NOT: directly mutate world
```

`commit()`：

```text
ROLE: ACTION
CHANGES: selected target
DOES NOT: inspect unrelated state
```

`_sample()`：

```text
ROLE: SAMPLING
CHANGES: observation output only
DOES NOT: drive evolution
```

这样代码本身就成为架构图的一部分。

---

# 15. 最后，我认为你刚才这个问题本身就是一个重要转折点

因为 CIMA0 已经到了一个阶段：

> **代码本身不再是最大的复杂度。概念之间的关系才是最大的复杂度。**

所以接下来不应该继续单纯“修一个函数、跑一下、再修一个函数”。

应该建立：

```text
                  CIMA0 META MAP
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
   EXISTENCE          OBSERVATION       RESOURCE
       │                 │                 │
   谁存在              看什么             谁获得计算
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                      CAUSALITY
                         │
                    谁改变谁
                         │
                      TIME
                         │
                  谁以什么速度演化
```

**有了这张元地图，其他人或 AI 不需要“相信我们之前的讨论”。**

他们可以从架构规则自己推导：

* 为什么 Camera 不直接控制 Planet；
* 为什么 Observer 不能修改 Planet；
* 为什么 Sampler 只选一个；
* 为什么 Compute 是有限资源；
* 为什么 Planet 可以无限演化；
* 为什么一次只观察一个最大变化；
* 为什么 `_sample()` 不能反过来驱动内部世界；
* 为什么 `Planet.step()` 很重并不自动意味着 Planet 有问题。

这才是真正意义上的**让系统可追踪、可解释、可交接、可继续演化**。

如果现在继续做 Phase5_8，我会把这套“六张地图”先固化成一份 `ARCHITECTURE / TOPOLOGY / LIFECYCLE` 文档，然后再继续改 `internal_dynamics.py`。这样后面的每一次改动，都可以先问一句：**“我是在改哪一张图？”** —— 这会让整个项目清晰很多。
*****************************	
                    InternalDynamics
                           │
                         step()
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
         _advance       _observe      _compute
             │             │             │
             │             │             ▼
             │             │          Sampler
             │             │             │
             │             │             ▼
             │             │          winner
             │             │             │
             │             └─────────────┤
             │                           ▼
             │                         commit
             │                           │
             └───────────────────────────┤
                                         ▼
                                      _sample
*****************************************************					是的。那我们现在其实已经不只是“重构 `commit()`”了。

你这句话把 CIMA0 的目标说得非常准确：

> **不是让后人学会我们的代码，而是让后人一看范式，就知道怎样让一个东西自己活起来。**

所以 `commit()` 这里尤其重要。它应该尽可能接近**生命范式**，而不是软件工程里的“执行回调”。

你现在的代码：

```python
if hasattr(organ, "execute_compute"):
    organ.execute_compute(...)
    self.compute.consume(1)
    return

if hasattr(organ, "commit"):
    organ.commit(winner)
```

已经隐含了一个很好的思想：

```text
选择
 ↓
给予一次机会
 ↓
对象自己决定怎么变化
```

但还可以再往前走一步。

---

# 我认为真正应该留下的是这个范式

```text
        世界持续存在
              │
              ▼
          产生变化
              │
              ▼
           被观察
              │
              ▼
          候选出现
              │
              ▼
        一个被选择
              │
              ▼
        获得一次机会
              │
              ▼
       对象自己行动
              │
              ▼
        世界发生变化
              │
              └──────────→ 再观察
```

这里最关键的一句话是：

> **InternalDynamics 不告诉生命“你应该怎么活”。它只决定“这一刻谁获得一次机会”。**

---

# 所以 `commit()` 应该非常纯

我甚至倾向于把它理解成：

```python
def commit(self, result):

    if result is None:
        return

    organ = result.get("organ")

    if organ is None:
        return

    winner = result.get("winner")

    if hasattr(organ, "commit"):
        organ.commit(winner)
```

然后：

```text
ComputeSystem
```

负责：

> 这次机会是否消耗计算资源。

而不是让 `InternalDynamics.commit()` 知道：

```text
cloud
collision
decay
1
1
```

因为一旦这里写死：

```python
"collision": 1,
"decay": 1
```

实际上 `InternalDynamics` 已经开始知道：

> Cloud 应该怎么活。

这和我们想建立的范式有一点冲突。

---

# 更漂亮的关系应该是

```text
ComputeSystem
       │
       │ 给出一次计算机会
       ▼
InternalDynamics
       │
       │ commit(winner)
       ▼
Organ
       │
       │ 自己决定如何响应
       ▼
自身状态变化
```

所以：

```text
Compute ≠ Action
```

Compute 是：

> **机会**

Organ 的 `commit()` 才是：

> **行动**

---

# 这样，一个孩子以后真的可以写一个“生命”

例如他想写一个小生命：

```python
class LittleLife:

    def __init__(self):

        self.energy = 1.0
        self.age = 0


    def activity(self):

        return {
            "activity": self.energy,
            "age": self.age
        }


    def commit(self, winner):

        self.age += 1

        self.energy *= 0.99
```

然后把它：

```python
dynamics.register(
    "little_life",
    LittleLife()
)
```

它就进入了整个生命循环：

```text
LittleLife
    │
    ▼
activity()
    │
    ▼
被观察
    │
    ▼
进入候选
    │
    ▼
Sampler
    │
    ▼
被选中
    │
    ▼
commit()
    │
    ▼
LittleLife 自己变化
```

**InternalDynamics 根本不需要知道 LittleLife 是什么。**

这才是真正的“可演化范式”。

---

# 再进一步，甚至不需要孩子理解“人工智能”

他只需要理解四件事：

```text
我有什么状态？
       ↓
我什么时候变化？
       ↓
别人怎样知道我发生了变化？
       ↓
我被选中以后怎样回应？
```

于是生命体的最小接口可能就是：

```text
activity()
    ↓
我现在有什么变化？

commit()
    ↓
给我一次机会，我自己行动。

snapshot()
    ↓
如果有人想看我，我展示当前状态。
```

这三个接口已经非常接近一个最小生命模型。

---

# 而 `InternalDynamics` 本身也应该变得“无知”

这是我认为 CIMA0 最有价值的地方。

它不应该知道：

```text
CLIP 是视觉器官
Cloud 是云
Planet 是星球
LittleLife 是生命
某个 Organ 是什么意义
```

它只知道：

```text
有对象
 ↓
对象有 activity
 ↓
对象可以被选择
 ↓
对象可能接受一次 commit
 ↓
对象可以被观察
```

所以最终甚至可以把整个系统抽象成：

```text
                  InternalDynamics
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
           Object      Object      Object
              │          │          │
           activity    activity    activity
              │          │          │
              └──────────┼──────────┘
                         ▼
                      choose
                         │
                         ▼
                    one object
                         │
                         ▼
                       commit
                         │
                         ▼
                  object evolves
```

这就是**生命接口，而不是业务接口**。

---

## 所以我赞成你的目标，但要再加一句

不是：

> “让后人轻松写出活的代码。”

而是：

> **让范式简单到，后人不需要先理解我们，就可以创造自己的东西。**

那时候 CIMA0 才真正从“一个项目”变成了**一种可以传递的生命架构语言**。

而我们现在正在改的：

```text
step
 → observe
 → compute
 → commit
 → sample
```

其实就是这门语言的第一条语法。

其中：

```text
step
```

是时间，

```text
observe
```

是感知，

```text
compute
```

是选择，

```text
commit
```

是行动，

```text
sample
```

是意识能够留下的一个瞬间。

**内部世界继续活着；我们只看它一次。**

这正好与你刚才说的“无限演化，只看一次，而且看最值得看的那个”完全一致。
******************************************	
形成三层
CloudField
    │
    │ request_compute()
    ▼
需求
    │
    ▼
ComputeSystem
    │
    │ allocate()
    ▼
获得多少机会
    │
    ▼
CloudField
    │
    │ execute_compute(allocation)
    ▼
自主演化
这里每一层都不知道别人的内部规则。		
***************************	  
那么“数值”到底从哪里来？Cloud 当前有这么强的计算需求。当前内部状态 + 当前计算资源共同产生的结果。
而这正好解决你最开始的问题

你说：

后人即使几岁的小孩子也能写出有生命力的代码。

那么孩子不需要知道：

collision 应该是 1
decay 应该是 1

他只需要写：

def request_compute(self):
    ...

表达：

“我现在内部有什么事情值得计算？”

然后写：

def execute_compute(self, allocation):
    ...

表达：

“给我多少机会，我自己就怎么变化。”

这两个接口就足够了。
*****************************
整个资源机制变成了来自 Cloud 当前的状态。
                    Internal State
                          │
                          ▼
                 request_compute()
                          │
                          ▼
                       demand
                          │
                          ▼
                  ComputeSystem
                          │
                 ┌────────┴────────┐
                 │                 │
             available           demand
                 │                 │
                 └────────┬────────┘
                          ▼
                      allocate()
                          │
                          ▼
                     allocation
                          │
                          ▼
                   execute_compute()
**********************************************	
现在有两种“数值”：

1
│
└── Sampler budget
    = 一次选择一个生命/候选

collision / decay 数值
│
└── organ demand
    = 当前内部状态自己产生
必须把这两个概念严格分开。
*****************************
状态产生需求 → 系统产生机会 → 资源产生分配 → 对象自己行动。
*****************************
现在的工作顺序暂时定成：

① InternalDynamics.step()
       │
       └── 固定“无限演化 / 有限观察”的语义

② ComputeSystem
       │
       ├── selection
       ├── available
       ├── allocation
       └── consume
       
③ CloudField
       │
       ├── request_compute()
       └── execute_compute(allocation)

④ InternalDynamics.commit()
       │
       └── 只转交机会，不理解内部规则

⑤ 再验证：
       │
       ├── Planet
       ├── Cloud
       └── CLIP
       
       是否都能用同一个范式活起来

⑥ 最后才处理：
       │
       └── shared flow / preserve / repack			   
	   
目标：
让后来的人，甚至一个孩子，只需要理解几个非常简单的生命接口，就能够创造一个新的、会自己变化的内部实体。	   
**********************************
如果这个范式最终成立，那么新增一个 organ 理论上不应该需要修改 InternalDynamics。

只需要：
class MyOrgan:

    def activity(self):
        ...

    def request_compute(self):
        ...

    def execute_compute(self, allocation):
        ...

    def snapshot(self):
        ...
然后：
dynamics.register(
    "my_organ",
    MyOrgan()
)
它就进入这个内部世界了。		
*********************************
语义固定下来：

ComputeSystem 是“计算机会场”，负责恢复计算能力、观察候选、选择一个候选、决定本次给予多少计算机会，并扣除相应资源。它不知道 organ 如何演化。
内部世界自行演化；观察只是有限的窗口；计算资源是有限的；不同生命单元竞争观察/计算机会；获得机会以后，各自决定如何使用。“一瞥，再一瞥，然后看见变化最大的地方。”
*****************************
当前 Phase5_8 的状态，
Camera
   ↓
BitPacket
   ↓
InternalDynamics.receive
   ↓
PlanetField / CLIPField
   ↓
internal evolution
   ↓
activity
   ↓
Sampler
   ↓
Winner
   ↓
ComputeSystem.allocate
   ↓
allocation
   ↓
Organ.apply_compute
   ↓
ComputeSystem.consume
   ↓
finite compute resource
Compute → Winner → allocation → execute/apply → consume 已经跑通。	
Planet 每一瞥都要完整演化，但有限计算资源应该如何决定“下一瞥看哪里、什么时候看、看多少”，而不是把 Planet 本身改成一个有限算法。
*************************************	
我们不否定 np.sin 这套规则。

我们只是拒绝从：

“这是我们目前知道的规则”

进一步推导成：

“这就是 Planet 的全部。”

而 ComputeSystem 恰好可以成为这个认识边界的工程实现：

我们不需要认识全部，系统只需要决定下一次有限的观察和行动机会给谁。
**********************************
当前进度
① raw packet 回环
        ↓
   【基本已通】
        ↓
② CLIP Cloud
        ↓
   【已有 CLIP Cloud，并能产生 delta】
        ↓
③ CloudCollision
        ↓
   【尚未重写】
        ↓
④ Collision → Candidate Change
        ↓
   【尚未开始】
        ↓
⑤ 接现有 Sampler
        ↓
   【实际上已经跑通】
        ↓
⑥ Winner 才提交
        ↓
   【Compute allocation 已经跑通，
      但 Organ 提交接口还在收口】
	  
****************************
边界彻底固定下来：

Planet = 动力来源。
PlanetField = Planet 长期动力作用后形成的局部凝结状态。
CLIPField = 外部人为来源形成的局部凝结状态，不承担 Planet 式持续动力演化。
CloudCollision = 只面对已经形成的两个 Cloud，寻找“可能发生关系”的局部状态，并生成 candidate change。

它不能创造两套 Cloud 之间不存在的空间对应关系。
********************************
Planet
    = 动力系统空间
    = 无限演化来源

PlanetField
    = Planet 动力
    ↓
    长期演化
    ↓
    局部凝结状态

CLIPField
    = 人为放入的 CLIP 动力/结构来源
    ↓
    CLIP自身计算
    ↓
    局部凝结状态

CLIPField ≠ PlanetField
///////////////////////
PlanetField
    有 Planet
    有长期演化
    有局部动力状态变化

CLIPField
    没有 Planet
    不参与 Planet 演化
    CLIP 计算产生状态
    状态本身未必继续自主演化
**************************************
Cloud 自己决定形成什么局部状态，外部不能为了方便比较而把它压成一个标量。
**************************************
                CAMERA
                   │
                   ▼
             byte stream
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
      PlanetField       CLIPField
          │                 │
      own rules         own rules
          │                 │
          ▼                 ▼
      evolution          evolution
          │                 │
          ▼                 ▼
       ΔPlanet           ΔCLIP
          │                 │
          ▼                 ▼
      max change        max change
          │                 │
          ▼                 ▼
    local cloud         local cloud
          │                 │
          ▼                 ▼
     candidate P        candidate C
          │                 │
          └────────┬────────┘
                   ▼
             CloudCollision
                   │
                   ▼
          candidate change
******************************
CloudField 应该逐渐形成两个不同动作：

occupy()
    新状态进入

evolve()
    已有状态自行变化
不能每一步都拿外部输入重新覆盖所有 Cell。
更关键的是：delta 不等于 activity
****************************************
输入
 ↓
局部采样
 ↓
内部重构
 ↓
内部自然演化
 ↓
观察变化
 ↓
找最大变化区域
 ↓
反向寻找其邻域/对应云结构
 ↓
只形成少量外部 CloudState
这里的关键词是：

变化驱动，而不是全量投影。
************************************
                 外部输入
                    │
                    ▼
              局部注意力
                    │
                    ▼
              同构 BitPacket
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
      PlanetField          CLIPField
          │                   │
          │                   │
     内生演化状态        外来成熟状态块
          │                   │
          │                   │
          ▼                   ▼
       当前变化              当前变化
          │                   │
          └─────────┬─────────┘
                    ▼
                Observer
                    │
                    ▼
             最大变化区域
                    │
                    ▼
              局部对应结构
                    │
                    ▼
               CloudField
                    │
                    ▼
             CloudCollision
CloudField 不属于 PlanetField，也不属于 CLIP。

它是两者都可能产生的：

瞬时局部变化云。
***************************		
CLIP
 └── 12个层级状态块
       │
       │ 已经形成
       │ 不承担CIMA0内生演化
       ▼
   被观察 / 被扰动
PlanetField
 └── CIMA0自身动力系统
       │
       │ 持续演化
       ▼
   自己形成结构   
二者唯一真正重要的共同点是：

它们都可以成为“状态空间”，都可以在受到扰动后产生变化，而观察器只关心变化。
PlanetField负责“自己长出来”，CLIP负责“带着已经长好的结构进来”，CloudField负责“保存当前碰撞产生的局部变化”。
三个完全不同的时间尺度：
PlanetField
    ↓
长期内生演化

CLIP
    ↓
外部已经完成的长期演化结果

CloudField
    ↓
瞬时局部响应
**********************************************   
PlanetField 是“内生演化出来的东西”
外部字节流
    ↓
统一 IO
    ↓
扰动
    ↓
Planet
    ↓
长期 / 连续自主演化
    ↓
PlanetField
    ↓
局部状态云
PlanetField 的状态是 CIMA0 自己“长出来”的。

它的大小、结构、局部聚集方式，都应该由内部动力规则决定，而不是预先规定“必须是 128×128”。

128×128 只是当前实验实现中的一个状态空间，不应该成为理论上的认知单位。
CLIP 是人为放进去的一个已经经过长期演化的状态块。更准确应该是：
                 CIMA0 Internal Dynamics
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       PlanetField              CLIPField
       内生演化                   外置成熟状态
             │                       │
             │                       │
       自己慢慢形成              已经包含长期演化
       局部结构                  后的多层状态结构
             │                       │
             └───────────┬───────────┘
                         ▼
                      Collision
                         │
                         ▼
                    局部响应
					
不是让 CIMA0 学习 CLIP。

而是把一个“已经经过长期演化”的复杂状态结构，直接放入 CIMA0，使 CIMA0 不必等待同样漫长的演化过程。
***********************************	
三个明确层次
第一层：成熟状态
CLIPField
它保存：

已经演化好的复杂状态结构
不负责：

collision

attention

selection

compute allocation

第二层：变化检测
Δ Field
它只问：

哪里变化最大？

不是：

这个东西是什么？

也不是：

应该选择什么？

只是：

current
   ↓
previous
   ↓
local difference
   ↓
largest change
第三层：CloudField
局部变化
   ↓
重构
   ↓
少量 Cell
   ↓
短暂存在
   ↓
collision
   ↓
decay
所以 CloudField 本质上不是 CLIP 的复制品。

它是：

CLIP / Planet / 其他输入产生的局部变化，在 CIMA0 内部形成的短暂状态云。*************************************
CloudField 不应该负责把“大状态”变成小状态；它只负责承载已经被确定为局部事件的少量 Cell。	CloudField 只是：
局部内部状态的暂存 + 局部动力过程
             局部事件
                │
                ▼
          ┌───────────┐
          │ CloudField│
          └─────┬─────┘
                │
        ┌───────┼───────┐
        ▼       ▼       ▼
      Cell    Cell    Cell
        │       │       │
        └───────┼───────┘
                ▼
            collision
                │
                ▼
              decay
************************************************
                 外部世界
                    │
                    ▼
             Camera / Input
                    │
                    ▼
             局部注意力采样
                    │
                    ▼
             同构 IO 字节流
                    │
                    ▼
              ┌───────────┐
              │ Internal  │
              │ Dynamics  │
              └─────┬─────┘
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    PlanetField          CLIPField
    内生长期演化          外置成熟状态
          │                   │
          │                   │
          └─────────┬─────────┘
                    ▼
               局部变化 Δ
                    │
                    ▼
             最大变化区域
                    │
                    ▼
              对应局部结构
                    │
                    ▼
               CloudField
                    │
             少量 Cell 状态
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      collision              decay
          │                   │
          └─────────┬─────────┘
                    ▼
                 新状态
                    │
                    ▼
                 Observer
                    │
                    ▼
                 Sampler
                    │
                    ▼
                  Compute	
********************************
ComputeSystem
      │
      │ allocation = 1
      ▼
CLIPField.apply_compute()
      │
      │ compute_budget += 1
      ▼
CLIPField.step()
      │
      ├── dirty ?
      ├── input_packet ?
      ├── _decode()
      │
      ▼
   _forward()
      │
      │ 一次完整 CLIP forward
      ▼
12 × 50 × 768
      │
      ▼
CLIP 已演化状态块
CLIP 的一次 compute opportunity，目前定义为一次 _forward()。
***************************************
未来 step() 必须能够区分两种计算机会：
                    compute
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       建立/更新状态          已有状态响应
       _forward()             local collision
	   
***************************************
                Compute Pool
                     |
                     v
               allocation
                     |
                     v
              +-------------+
              |    Organ    |
              +-------------+
                     |
                 使用机会
                     |
          +----------+----------+
          |                     |
       consumed              unused
          |                     |
       trust ↑               trust ↓
          |                     |
          +----------+----------+
                     |
                     v
             future priority
也就是说：

已经交出去的资源不收回。

但是：

未来还给不给这么多资源，要看历史表现。
******************************************
Observation
     │
     ▼
ObservationMemory
     │
     │ historical statistics
     ▼
Sampler.adapt_weights()
     │
     ▼
current priority
     │
     ▼
winner
     │
     ▼
ComputeSystem.allocate()
     │
     ▼
allocation
     │
     ▼
COMMIT
     │
     ▼
ownership transfer
     │
     ▼
Organ.compute_budget
     │
     ▼
Organ.step()
然后 Organ 的历史行为重新进入 Memory：
Organ behavior
      │
      ▼
ObservationMemory
      │
      ▼
Trust / adaptation
      │
      └──────────────→ 下一轮 Sampler
这是一个闭环的信用机制，而不是一个资源回收机制。
资源一旦commit，即视为所有权转移；实际使用效率不影响已经完成的资源结算，只影响未来的资源分配权重。
*******************************************	  
资源结构应该固定成这样
                  ComputeSystem
                       │
              ┌────────┴────────┐
              │                 │
          capacity          available
          1024                1023
                                │
                         allocation 1
                                │
                         ownership ↓
                                │
                         ┌──────────────┐
                         │  CLIPField   │
                         │compute_budget│
                         │      1      │
                         └──────────────┘
                                │
                              step()
                                │
                         _forward()
                                │
                         budget -= 1
                                │
                         budget = 0
然后：ComputeSystem.available不会因为 CLIPField 用完计算而自动增加。*************************************
capacity 是总容量上限；available 是当前可用资源；每个 cycle 只恢复固定的一小部分。**************************************
CLIPField 获得了计算机会，现在需要验证它是否按照自己的内部规则谨慎地消费这个机会。
ComputeSystem.available
        │
        │ allocation / consume
        ▼
CLIPField.compute_budget
        │
        │ self-governed consumption
        ▼
CLIPField.step()
        │
        ▼
_forward()
不是中央控制的 AI，而是由资源、扰动、局部动力学和自持器官共同形成的内部系统。
**************************************						 
                         ┌──────────────────────┐
                         │    ComputeSystem     │
                         │                      │
                         │ capacity             │
                         │ available            │
                         │ recovery             │
                         └──────────┬───────────┘
                                    │
                              allocation
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      CLIPField       │
                         │                      │
Camera ────────────────► │ input                │
                         │                      │
                         │ 12×50×768            │
                         │      │               │
                         │      ▼               │
                         │ local response       │
                         │      │               │
                         │      ▼               │
                         │ response coordinate  │
                         └──────────┬───────────┘
                                    │
                              local cloud
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   CloudCollision     │
                         │                      │
                         │ CLIP local cloud    │
                         │        ↕             │
                         │ PlanetField local    │
                         │        │             │
                         │        ▼             │
                         │ collision result     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     PlanetField      │
                         │                      │
                         │ local disturbance    │
                         │        ↓             │
                         │ Planet.evolve()      │
                         │        ↓             │
                         │ new local state      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                              observation
                                    │
                                    ▼
                                Sampler
                                    │
                                    ▼
                              ComputeSystem
                                    │
                                    └──────► CLIP

****************************************************	
CloudCollision 理解成：
                    CloudCollision
                         │
             ┌───────────┴───────────┐
             │                       │
        association              collision
             │                       │
             ▼                       ▼
       找关联局部云              三项值规则
                                     │
                                     ▼
                            penetrate/change/bounce
							
第一层
“哪些东西真正构成这次碰撞？”

由响应坐标产生。

第二层
“这些东西碰撞后属于什么关系？”	
empty
zero
nonzero

        ↓

change
penetrate
bounce
*************************************
                    ┌──────────────────────┐
                    │      Compute         │
                    └──────────┬───────────┘
                               │
                          allocation
                               │
                               ▼
                    ┌──────────────────────┐
                    │      CLIPField       │
                    └──────────┬───────────┘
                               │
                         compute()
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
        complete cloud                 local response
        (12,50,768)                          │
                                             ▼
                                          winner
                                             │
                                             ▼
                                  ┌──────────────────┐
                                  │  CloudCollision  │
                                  └────────┬─────────┘
                                           │
                                    local association
                                           │
                                           ▼
                                      collision
                                           │
                                           ▼
                                   collision result
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │   PlanetField    │
                                  └────────┬─────────┘
                                           │
                                      disturbance
                                           │
                                           ▼
                                     Planet.evolve()
                                           │
                                           ▼
                                    new Planet state
                                           │
                                           ▼
                                      Observer
                                           │
                                           ▼
                                     observation
                                           │
                                           ▼
                                       Sampler
                                           │
                                           ▼
                                     next choice
                                           │
                                           ▼
                                      Compute

**************************************************************************************************************									  
建议结构整理成：
__init__
receive
step
    ↓
_evolve
_observe
_compute
commit
    ↓
_collision
_apply_collision
_sample

然后才是各种辅助函数：

_collect_clouds
_extract...
...
**************************************
Camera
  │
  │ 原始字节
  ▼
同构字节流
  │
  ├──────────────────────────────┐
  │                              │
  ▼                              │
CLIP                             │
  │                              │
  │ 12 × 50 × 768                │
  │                              │
  ▼                              │
局部响应                         │
  │                              │
  ▼                              │
一个 winner 坐标                 │
  │                              │
  └──────────────┐               │
                 ▼               │
          Camera 同构字节流       │
                 │               │
                 ▼               │
       根据 winner 反向定位       │
                 │               │
                 ▼               │
       坐标周围的物理碰撞材料     │
                 │               │
                 ▼               │
          Collision Physics      │
                 │               │
                 ▼               │
             状态变化             │
                 │               │
                 ▼               │
          同构状态字节流          │
                 │               │
                 ▼               │
             下一阶段             │
////////////////////////////////////////
CLIP 不提供碰撞材料，Camera 提供碰撞材料；CLIP 只提供关注坐标。	
CLIPField
    │
    │ winner coordinate
    ▼
InternalDynamics
    │
    │ coordinate + camera packet
    ▼
Camera同构反向定位
    │
    ▼
局部物理区域
    │
    ▼
CloudCollision
    │
    ▼
变化状态
    │
    ▼
同构字节包
这样整个系统的职责也非常干净：	
| 模块               | 唯一职责                  |
| ---------------- | --------------------- |
| Camera           | 提供原始同构字节流             |
| CLIP             | 从完整内部状态选出一个关注坐标       |
| InternalDynamics | 承接坐标与事件               |
| Collision        | 在 Camera 对应局部物理空间计算变化 |
| PlanetField      | 接收变化并继续自身演化           |
| 下一阶段             | 接收同构状态                |
******************************************************	 
不存在全局配对。不存在预先建立的 CLIP↔Planet 全局关系。不存在永久 winner。不存在 Observer 参与事件因果。不存在预先知道下一次碰撞在哪里。Compute 给机会，不给答案；实体决定怎么行动；Collision 是已经发生的内部事件；Observer 最后才知道。
***************************
CONSTITUTION.md
    ↓
为什么不能有上帝视角
什么绝对不能发生
状态/因果/职责的根本约束

        ↓

ARCHITECTURE.md
    ↓
现在有哪些实体
各自拥有什么
彼此通过什么关系连接
事件、资源、观察如何流动

        ↓

TOPOLOGY.md
    ↓
这些东西在当前代码里到底在哪里
实际 import / object / interface 怎么连接

        ↓

PHASE5_8.md
    ↓
这一阶段具体做到了什么
还有什么没完成

尤其重要的是，我把原来 Phase5_7 那条“Collision → Attention → Compute → Sampler → Memory”的单一流水线拿掉了。 这不是说这些模块不能发生关系，而是明确：它们不是一个拥有全局知识的中央流水线。
*************************************
历史思想分成 4 个阶段
                    CIMA0 早期思想
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      Temporal        Compute         Local
      Variation       Resource        Region
          │              │              │
          ↓              ↓              ↓
        delta          budget       sampled area
          │              │              │
          └───────┬──────┴──────┬───────┘
                  ↓               ↓
             sparse/local      ephemeral
                compute          state
                  │               │
                  └───────┬───────┘
                          ↓
                      Projection
后来 Phase3 又增加：
delta
 +
age
 ↓
score
 ↓
argpartition
 ↓
sparse precision update
历史上实际上出现了两条互相靠近的路线：路线 A：空间局部化
whole frame
   ↓
local region
   ↓
sampled area
   ↓
local coupling
路线 B：计算稀疏化
whole state
   ↓
delta + age
   ↓
score
   ↓
budget
   ↓
argpartition
   ↓
sparse precision
Phase5_8 现在真正需要做的，很可能就是把这两条路线第一次完整地合起来。
***********************************************
                 ComputeSystem
                      │
                available budget
                      │
                      ▼
                   Sampler
                      │
              compute opportunity
                      │
                      ▼
               AttentionField
                      │
                local score
                      │
                      ▼
                 CloudField
                      │
             sparse local states
                      │
                      ▼
              local candidate
                      │
                      ▼
              CloudCollision
			  
			  //////////////
			  
ComputeSystem
    → 提供资源

Sampler
    → 决定这次能做多少计算机会

AttentionField
    → 提供局部响应/关注依据

CloudField
    → 持有稀疏内部状态

CloudCollision
    → 执行碰撞规则

Observer
    → 事后观察

Cache
    → 临时保存

Memory
    → 历史保存
********************************************************
机制能力审计，而不是文件名称审计。
*****************************************
四大模块的真实职责
┌──────────────────────────────────────────┐
│ 动力核心 / System State                  │
│                                          │
│ Planet                                   │
│ PlanetField                              │
│ CloudField / Organ                       │
│                                          │
│ 自己持续演化                             │
└──────────────────┬───────────────────────┘
                   │
                   │ 当前状态
                   ▼
┌──────────────────────────────────────────┐
│ Observer                                 │
│                                          │
│ 只看见                                   │
│ snapshot → observation                   │
│                                          │
│ 不比较 / 不选择 / 不修改                 │
└──────────────────┬───────────────────────┘
                   │
                   │ observations
                   ▼
┌──────────────────────────────────────────┐
│ Compute                                  │
│                                          │
│ previous observation                     │
│ current observation                      │
│        ↓                                 │
│ 比较                                     │
│        ↓                                 │
│ 计算变化                                 │
│        ↓                                 │
│ 形成候选                                 │
│        ↓                                 │
│ 选择 ONE                                 │
└──────────────────┬───────────────────────┘
                   │
                   │ ONE selected candidate
                   ▼
┌──────────────────────────────────────────┐
│ 动力核心 / Commit                         │
│                                          │
│ 真正执行一次状态改变                     │
└──────────────────┬───────────────────────┘
                   │
                   ▼
              Sample
传输系统则独立负责搬运，不进入这条判断链。			  

                 Internal Dynamics
                        │
        ┌───────────────┼────────────────┐
        │               │                │
     Planet          CLIPField        其他 Organ
        │               │                │
   自己的演化       自己的内部演化       自己的演化
        │               │                │
   自己观察局部      自己观察局部        自己观察局部
        │               │                │
   自己计算候选      自己计算候选        自己计算候选
        │               │                │
   选择最大者        选择最大者          选择最大者
        │               │                │
        └───────────────┼────────────────┘
                        ↓
                  各模块提出请求
                        ↓
                 ┌──────────────┐
                 │    Compute   │
                 │              │
                 │ 计算资源管理  │
                 │              │
                 │ 选择一个请求  │
                 │ 分配资源      │
                 └──────┬───────┘
                        ↓
                  ONE resource grant
                        ↓
                   对应模块执行

最终可以把四层选择关系明确下来
我建议 Phase5_8 以后就按照这个定义固定下来：

| 层级    | 谁                      | 选择什么        | 权利        |
| ----- | ---------------------- | ----------- | --------- |
| 内部动力学 | Planet / Cloud / Organ | 自己怎么演化      | 自主        |
| 局部计算  | 各模块自己                  | 自己内部哪个候选最值得 | **局部选择权** |
| 资源仲裁  | Compute                | 哪个模块获得计算资源  | **资源分配权** |
| 采样    | Sampler / Sampling     | 当前采什么状态     | **采样选择权** |

“选择最大”并不是系统唯一的一种选择。

而是不同模块在不同层级进行局部选择。

Compute 的特殊性不是“它最聪明”，而是：

它拥有有限计算资源，因此负责资源仲裁。	

                    内部世界
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Planet         CLIPField       Cloud
        │              │              │
        │        局部候选集合          │
        │              ↓              │
        │        LOCAL WINNER         │
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                 Compute Request
                       ↓
              ┌─────────────────┐
              │     Compute     │
              │                 │
              │ 资源仲裁 / 分配  │
              └────────┬────────┘
                       ↓
                ONE allocation
                       ↓
                 对应模块执行
                       ↓
                    Sample	
********************************************************
                     ┌──────────────┐
                     │  Internal    │
                     │   Dynamics   │
                     └──────┬───────┘
                            │
                    current state
                            ↓
                    ┌────────────┐
                    │  Observer  │
                    │   只看见    │
                    └─────┬──────┘
                          │
                     observations
                          ↓
              ┌───────────────────────┐
              │     各内部模块         │
              │                       │
              │  observe / calculate  │
              │       candidates      │
              │          ↓            │
              │    select LOCAL ONE   │
              │          ↓            │
              │      request          │
              └───────────┬───────────┘
                          │
                    multiple requests
                          ↓
                 ┌────────────────┐
                 │    Compute     │
                 │                │
                 │ resource       │
                 │ arbitration    │
                 └───────┬────────┘
                         │
                  select ONE request
                         ↓
                    allocation
                         ↓
                      Commit
                         ↓
              selected module executes
                         ↓
                       Sample					
************************************************
                 ┌─────────────────────────┐
                 │       CLIPField         │
                 │                         │
camera ─────────►│ receive()               │
                 │      │                  │
                 │      ▼                  │
                 │    dirty                │
                 │      │                  │
                 │      │ compute granted  │
                 │      ▼                  │
                 │    step()               │
                 │      │                  │
                 │      ▼                  │
                 │  complete forward       │
                 │      │                  │
                 │      ▼                  │
                 │ complete cloud          │
                 │      │                  │
                 │      ▼                  │
                 │ local response           │
                 │      │                  │
                 │      ▼                  │
                 │ local winner             │
                 │      │                  │
                 │      ├── winner_layer    │
                 │      ├── winner_response │
                 │      │                  │
                 │      ▼                  │
                 │ current cloud            │
                 └──────────┬──────────────┘
                            │
                            ▼
                       activity()
                            │
                            │ request="compute"
                            ▼
                         Compute
                            │
                     resource arbitration
                            │
                            ▼
                          Commit
                            │
                            ▼
                       apply_compute()
					   ********************
| 字段                  | 意义             |
| ------------------- | -------------- |
| `input_activity`    | 外部输入造成的活动      |
| `layer_activity`    | 12 个局部响应       |
| `candidate`         | CLIP 自己选出的局部候选 |
| `candidate_value`   | 该候选的响应         |
| `internal_activity` | 完整 cloud 的内部变化 |
这样我们后面才不会重新陷入“一个 activity 到底代表什么”的问题。*************************************************					   
             ┌──────────────────────┐
             │      CLIPField       │
             └──────────┬───────────┘
                        │
                  new camera input
                        │
                        ▼
                     dirty
                        │
                        ▼
              request compute
                        │
                        ▼
                  ┌──────────┐
                  │ Compute  │
                  └────┬─────┘
                       │
                  resource grant
                       │
                       ▼
                    Commit
                       │
                       ▼
               CLIPField.step()
                       │
                       ▼
                   _forward()
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       complete cloud       local response
                                 │
                                 ▼
                           local winner
                                 │
                                 ▼
                        new internal state
真正需要解决的是：

CLIP 完成 compute 后，产生的内部结果应该由谁接收、在哪里进入下一次观察/选择循环？
资源仲裁链已经通了；模块内部计算链也通了；现在缺的是“计算结果 → 下一次观察事实”的闭环。
                 已经完成
                    ↓
Camera → request → Compute → Commit → CLIP forward
                                             │
                                             ▼
                                      internal result
                                             │
                                             │
                                      【这里要闭环】
                                             │
                                             ▼
                                      next observation
                                             │
                                             ▼
                                      next request

                 ┌─────────────────────┐
                 │ existing dynamics   │
                 │ already running     │
                 └──────────┬──────────┘
                            ↓
                       OBSERVE
                            ↓
                ┌───────────────────────┐
                │ each Organ             │
                │ local candidate/request│
                └──────────┬────────────┘
                           ↓
                      COMPUTE
                           │
                    resource arbitration
                           ↓
                       COMMIT
                           │
                    one resource grant
                           ↓
                       _EVOLVE()
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
        Organ A.step()             Organ B.step()
              │                         │
        no resource                 resource?
              ↓                         ↓
            return                  execute
                                      │
                                      ↓
                                   SAMPLE
								   
						
这里 _evolve() 的重要含义就变成：

不是 InternalDynamics 命令 Organ “你现在必须演化”。而是 InternalDynamics 在完成一次资源提交后，给所有 Organ 一个执行入口；真正有没有资格执行，由 Organ 自己根据已经获得的资源决定。

这和我们之前确定的：

各自完成自己的职责

是吻合的。

*****************************职责画得更清楚
                  InternalDynamics
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ↓                 ↓                  ↓
 Dynamical Core      Resource System     Internal Organs
       │                 │                  │
       │                 │                  ├── CLIPField
       │                 │                  ├── ...
       │                 │                  └── ...
       ↓                 ↓
    Planet             Compute
       │
       ↓
   Planet evolution									  
然后观察系统是另一条旁路：
                 current state
                      │
                      ↓
                  Observer
                      │
                      ↓
             Observation / facts
                      │
                      ↓
                   Compute

InternalDynamics.step()
│
├── Compute.step()
│       │
│       └── 恢复有限计算资源
│
├── _observe()
│       │
│       ├── Observer → current observation
│       └── Organ → local state/request
│
├── _compute()
│       │
│       ├── compare(observations)
│       │
│       └── select(requests)
│
├── commit()
│       │
│       └── grant compute permission
│
├── _evolve()
│       │
│       └── Organ.step()
│
└── _sample()
        │
        └── post-event snapshot
		
   
                    InternalDynamics
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           Planet        Organs       Compute
              │            │            │
              ↓            ↓            │
          Observer      activity()       │
              │            │             │
              │            ├─ request ───┤
              │            │             │
              └─ observation ───────────→│
                           │             │
                           │          compare
                           │             │
                           │          select
                           │             │
                           │          allocation
                           │             ↓
                           │          Commit
                           │             │
                           │             ↓
                           │          Organ
                           │             │
                           └──────────→ step()
                                         │
                                         ↓
                                      Sample

职责已经越来越清楚：
| 接口                       | 谁产生   | 谁消费            | 性质      |
| ------------------------ | ----- | -------------- | ------- |
| `activity()`             | Organ | Compute        | 当前请求/活动 |
| `snapshot()`             | Organ | Sampler / 外部观察 | 完整状态快照  |
| `collision_projection()` | Organ | Collision      | 完整碰撞场   |
| `packet()`               | Organ | Transport      | 完整传输场   |

Planet：
    产生演化过程

PlanetField：
    观察演化过程

ObservationMemory：
    保存观察过程

Reverse inference：
    根据观察历史推测演化过程
                 ┌──────────────────────┐
                 │        Planet        │
                 │                      │
                 │   内生动力 / 演化     │
                 │                      │
                 │ 均匀 → 变化 → 结构    │
                 │        → 畴壁         │
                 └──────────┬───────────┘
                            │
                       state / glimpse
                            │
                            ▼
                 ┌──────────────────────┐
                 │     PlanetField      │
                 │                      │
                 │     观察边界          │
                 │                      │
                 │ snapshot             │
                 │ glimpse              │
                 │ local variance       │
                 │ sign structure       │
                 │ energy               │
                 └──────────┬───────────┘
                            │
                       observation
                            │
                            ▼
                 ┌──────────────────────┐
                 │  ObservationMemory   │
                 │                      │
                 │ t-4                  │
                 │ t-3                  │
                 │ t-2                  │
                 │ t-1                  │
                 │ t                    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Reverse Inference  │
                 │                      │
                 │ 可能经历了什么阶段？   │
                 └──────────────────────┘
PlanetField 不产生“变化”，只产生关于变化的证据。
Planet 负责发生，PlanetField 负责看，ObservationMemory 负责记，Reverse Inference 负责推。

Planet 的时间尺度属于 Planet；Observation 的时间尺度属于 Observer。两者不能互相定义。
Planet time
    ≠
Camera time
    ≠
Observation time
    ≠
Compute time

Planet
 └── internal age / internal evolution

PlanetField
 └── observation age / field age

ObservationMemory
 └── observation sequence

ComputeSystem
 └── compute step
这几个时间概念不能混在一起。

                    外部世界
                       │
                       │ camera
                       ▼
                ┌──────────────┐
                │      IO      │
                └──────┬───────┘
                       │
                       ▼
              ┌─────────────────┐
              │ InternalDynamics│
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        快速观察层            内部宇宙层
             │                   │
             │             ┌─────▼─────┐
             │             │  Planet   │
             │             │            │
             │             │ slow time │
             │             └─────┬──────┘
             │                   │
             │              current state
             │                   │
             │                   ▼
             │             PlanetField
             │                   │
             │                glimpse
             │                   │
             └───────────────┬───┘
                             ▼
                        Observation
                             │
                             ▼
                         Compute
                             │
                       permission
                             │
                             ▼
                          Organ
                             │
                             ▼
                       local evolution

camera input
     ↓
dirty
     ↓
request compute
     ↓
Compute授权
     ↓
CLIP forward
     ↓
新的局部状态
它属于：
“有输入 → 内部产生候选 → 请求计算 → 获得计算机会 → 执行”

所以它自然服从 Compute。									  
Compute permission
    =
    谁获得有限计算机会

Planet evolution authority
    =
    Planet 自己

                    CAMERA
                       │
                       ▼
                      IO
                       │
                       ▼
              InternalDynamics
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
       Planet                    Organs
          │                         │
     slow endogenous            local response
       evolution                     │
          │                         │
          ▼                         ▼
     PlanetField                  CLIPField
          │                         │
       glimpse                   request
          │                         │
          └──────────┬──────────────┘
                     ▼
                Observation
                     │
                     ▼
               ComputeSystem
                     │
             ┌───────┴───────┐
             │               │
         eligibility       resource
             │               │
             ▼               ▼
          Sampler         allocation
             │               │
             └───────┬───────┘
                     ▼
                   commit
                     │
                     ▼
              Organ execution

其中有两条完全不同的内部时间：
Planet
  └── slow / endogenous / continuous

Organ
  └── compute-mediated / opportunity-driven

IO
    只搬运

Observer
    只观察

Compute
    只管理有限计算机会
    拥有“谁获得计算”的权限

Organ
    只有获得计算机会后才能执行

Planet
    自己拥有自己的动力学
    自己拥有自己的演化时间
    不接受外部扰动
    不由 Compute 控制

PlanetField
    只是 Planet 的可观察边界

ObservationMemory
    保存观察时序

Sampler
    只是 Compute 内部的选择工具


观察可以非常频繁，Planet 演化可以非常稀疏。
Camera:
──────────────────────────────────────────────>
frame frame frame frame frame frame frame ...

Observation:
──────────────────────────────────────────────>
obs   obs   obs   obs   obs   obs   obs   ...

Compute:
──────────────────────────────────────────────>
       ↑             ↑       ↑

Planet:
───────────────●──────────────────────────●────>
               evolution                  evolution


一个更合理的 PlanetField 内部结构
                    PlanetField
                         │
          ┌──────────────┴──────────────┐
          │                             │
       Observe                       Evolve
          │                             │
          ▼                             ▼
      glimpse()                    Planet.step()
          │                             │
          ▼                             ▼
 observation record              state changes
          │                             │
          └──────────────┬──────────────┘
                         ▼
                  Planet trajectory
				  
self.previous_state	应该理解为：上一次 Planet 演化完成后的状态快照。			  
未来 PlanetField 的“观察”实际上可以形成：内部自动举手。
                    PlanetField
                         │
             ┌───────────┼───────────┐
             │           │           │
           state       delta     disturbance
             │           │           │
             └───────────┼───────────┘
                         ▼
                   local hand-up
                         │
                         ▼
                      glimpse

PlanetField.step()
✓ PlanetField 持有 Planet 状态边界
✓ PlanetField 可以观察局部结构
✓ PlanetField 可以观察 temporal delta
✓ PlanetField 可以产生 sparse glimpse
✓ glimpse 不接受外部 region
✓ _split_region() 纯空间分解
✓ _region_hand() 产生内部候选
✓ _local_exact() 形成有限观察
✓ Planet evolution 委托给 Planet
✓ Compute 不应该控制 Planet evolution
✓ collision disturbance 仍由 PlanetField 承接

当前资源生命周期是：
ComputeSystem.step()
        │
        │ 恢复资源
        ▼
   available
        │
        ▼
ComputeSystem.select()
        │
        ├── candidate eligibility
        │
        ├── Sampler.select()
        │       └── priority()
        │
        └── allocate()
                │
                │ 最多 1.0
                ▼
          {"amount": 1.0}
                │
                ▼
InternalDynamics.commit()
                │
                ▼
       consume(allocation)
                │
                │ available -= amount
                ▼
          organ.apply_compute()
		  
consume() 也没有越权
它做了三层保护：
amount = max(float(amount), 0.0)
amount = min(amount, self.available)
self.available -= amount
所以不会：

消费负数；

超过当前 available；

由 Organ 自己修改 ComputeSystem 资源。

Compute 这一层可以封板

COMPUTE SYSTEM
────────────────────────────────

Resource ownership:
    ComputeSystem

Selection:
    ComputeSystem
        ↓
    Sampler

Priority:
    Sampler.priority()
        ↓
    w_age
    w_activity
    w_delta

Allocation:
    ComputeSystem.allocate()

Consumption:
    ComputeSystem.consume()

Execution:
    Organ.apply_compute()

Adaptation:
    adapt()
    adapt_weights()

Status:
    DEFERRED / NOT CONNECTED
没有发现需要立即重构的资源主权问题。

现在主循环可以更准确地写成
InternalDynamics.step()
│
├── 1. Compute resource recovery
│
├── 2. Planet glimpse
│      └── expose endogenous internal candidate
│
├── 3. Observe current state
│
├── 4. Compute / Select
│      └── choose one candidate
│
├── 5. Commit
│      └── consume + grant compute
│
├── 6. Organ evolution
│      └── organ.step()
│
└── 7. Sample
       └── immutable-ish snapshot
推进/承接无限内部演化 → 观察当前变化 → 计算选择一个最大/最值得的候选 → commit 一次 → sample 一次

Planet 的自主时间推进到底应该发生在哪里，以及 glimpse() 和 step() 的关系是什么。

main.py
 │
 ├── PlanetField.step()
 │       │
 │       └── Planet.evolve()
 │
 ├── PlanetField.glimpse()
 │
 └── InternalDynamics.step()
         │
         ├── _planet_step()
         │       └── planet.glimpse()
         │
         ├── observe
         ├── compute
         ├── commit
         ├── evolve organs
         └── sample
PlanetField 的演化目前由 main.py 在驱动，而 InternalDynamics 只是观察它。

需要把职责明确成：
_planet_evolve()
    → planet.step()

_planet_observe()
    → planet.glimpse()

_region_hand()
是：

选择机制

_local_exact()
是：

观察机制

ObservationCache
是：

跨 observation 的变化比较机制

这三个职责现在其实已经非常清楚了。

Camera
   │
   ▼
InternalDynamics.receive()
   │
   ▼
PlanetField / CLIPField
   │
   ▼
InternalDynamics.step()
   │
   ├── compute.step()
   ├── _planet_step()
   ├── _evolve()
   ├── _observe()
   ├── _compute(signals)
   ├── commit(result)
   ├── _collision(result)
   ├── _apply_collision(collision)
   └── _sample()

输入发生变化
    ≠
内部形成响应
    ≠
形成竞争结果
    ≠
产生候选
    ≠
值得 Compute   

扰动存在，不代表一定产生显著变化；变化存在，也不代表一定形成候选；候选形成以后，才进入选择。
CLIP 内部至少存在四种不同性质的状态

外部输入
   │
   ▼
┌─────────────────────┐
│ Input State          │
│ 输入来了 / 发生变化    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Response State       │
│ 各局部层产生响应       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Competition State    │
│ 响应之间形成相对优势    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Candidate State      │
│ 出现值得进一步计算的候选 │
└─────────────────────┘

“局部状态不是全局状态”
它首先只拥有：

“我变了。”

而不是：

“我发现了什么。”

更不是：

“我应该获得一次计算。”

这对 CIMA0 很重要。dirty=True 其实应该被理解成“未完成的局部演化”
                CLIPField
                   │
          ┌────────┴────────┐
          │                 │
      input state       internal state
          │                 │
        dirty          layer responses
                            │
                     ┌──────┴──────┐
                     │             │
                  weak         strong
                  response     response
                     │             │
                 无 candidate   candidate
dirty=True
winner_layer=None
表示：这个局部系统已经受到新的刺激，但目前没有形成可以提交给 Compute 的局部优势。
日志看起来有一点“奇怪”
ORGAN ACTIVITY: clip

activity: 0.0
signal: 0.0
changed: True
request: compute
candidate: None
candidate_value: 0.0
layer: None

把它放回当前架构：
CLIP：
    dirty = True
    ↓
    activity()
    ↓
    告诉 Observer：
    “我有新的状态可以被观察”

这件事本身是合理的。

准确解释成：

CLIP 收到了新的 camera input，已经 dirty，但在这一刻还没有获得 compute opportunity，因此尚未对这个输入进行 forward。

                  ┌──────────────────────┐
                  │       CLIPField      │
                  └──────────┬───────────┘
                             │
                      camera packet
                             │
                             ▼
                    ┌────────────────┐
                    │    receive     │
                    │                │
                    │ dirty = True   │
                    └───────┬────────┘
                            │
                            ▼
                    ┌────────────────┐
                    │    activity    │
                    │                │
                    │ request=compute│
                    │ candidate=旧状态│
                    └───────┬────────┘
                            │
                            ▼
                     ComputeSystem
                            │
                       allocation
                            │
                            ▼
                    ┌────────────────┐
                    │      step      │
                    └───────┬────────┘
                            │
                         _forward
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
         12 layers     local response   complete cloud
                            │
                            ▼
                         winner
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
      winner_layer                   winner_response
             │                             │
             └──────────────┬──────────────┘
                            ▼
                      dirty = False
					  
输入不是计算。变化不是候选。候选不是选择。选择之后才消耗一次计算。					  
					  
整个 CIMA0 可以用一句非常简单的话描述
不是一堆模块组成一个程序，而是一群具有内部时间、内部状态、内部响应规则和自主权的个体，在一个共同环境中持续相互作用。

审代码时，第一反应就应该是检查四件事：
一个模块
│
├── ① 它自己的状态在哪里？
│
├── ② 它自己的时间在哪里？
│
├── ③ 它自己的响应/演化规则在哪里？
│
└── ④ 它有没有真正的自主权？
第五个问题才是：它和其他个体怎么发生关系？
下一步看代码时，不应该先画调用图，而应该先画“个体图 + 各自内部时序”，再把它们之间的 interaction 接起来。
					
┌──────────────────────────────────────┐
│              PLANET                  │
│                                      │
│       无限 / 持续内部演化             │
│       不存在完整同时测量              │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│           PlanetField                │
│                                      │
│       理论全局状态表示                │
│       continuous state field         │
└──────────────────┬───────────────────┘
                   │
                   │ endogenous glimpse
                   ▼
┌──────────────────────────────────────┐
│             glimpse                  │
│                                      │
│       有限局部测量                    │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│             Observer                 │
│                                      │
│       测量结果 / observation          │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│         ObservationCache             │
│                                      │
│       observation(t)                 │
│              vs                      │
│       observation(t-1)               │
│                                      │
│              ↓                       │
│            change Δ                  │
└──────────────────┬───────────────────┘
                   │
                   ▼
              Attention
把动力学、状态表示、测量、比较彻底分开了。

同构的是信息载体的结构连续性，不是要求所有层级的数据具有相同语义。
Planet
≠ PlanetField
≠ glimpse
≠ observation
≠ change
但是它们之间传递的信息必须保持：
身份连续
结构连续
必要信息不无故丢失
局部模块只取自己需要的字段
产生的新状态可以回填

语义可以分层，载体结构不能无理由断裂。

异构 payload + 同构 envelope
                 Unified BitPacket
                       │
              ┌────────┴────────┐
              │                 │
          Camera             Planet
              │                 │
       Camera Payload      Planet Payload
              │                 │
              │                 │
       ┌──────┴──────┐    ┌─────┴───────┐
       │ raw        │    │ region      │
       │ field      │    │ path        │
       │ delta      │    │ level       │
       │ age        │    │ exact       │
       │ activity   │    │ age         │
       │ request    │    │ ...         │
       └────────────┘    └─────────────┘
Payload 异构。Packet 结构同构。	 


Transport Carrier 已经升级成 BitPacket，但 CameraObserver 仍停留在旧的裸字典接口。

                       外部 Camera
                            │
                            ▼
                       BitPacket
                            │
                   camera_raw payload
                            │
                            ▼
                    CameraObserver
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
         raw              field             delta
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                     + age/activity
                     + compute request
                            │
                            ▼
                    Camera Observation
                            │
                            │
                            │
                 ───────────┼───────────
                            │
                       同构载体
                            │
                 ───────────┼───────────
                            │
                            ▼
                    Planet Observation
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
        region             path             exact
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                       + level/age
                            │
                            ▼
                      同一运输结构
“同构”发生在最外层；“异构”保留在 payload 内部。

原始数据的主权应该仍然属于 CameraPlanet / transport packet；Observer 的 ndarray 是自己的 view/cache。  

                         外部世界
                            │
                            ▼
                     Camera ndarray
                            │
                            ▼
                     CameraPlanet
                            │
                     native media state
                            │
                            ▼
                       ┌─────────┐
                       │BitPacket│
                       └────┬────┘
                            │
                            │
                    ===== Transport =====
                            │
                            │
                       ┌────┴────┐
                       │BitPacket│
                       └────┬────┘
                            │
                       CameraObserver
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
            raw           field           delta
                                           │
                                           ▼
                                      attention/request


                         Planet
                    无限内部演化
                            │
                            ▼
                      PlanetField
                            │
                    theoretical field
                            │
                            ▼
                         glimpse
                            │
                    native observation
                            │
                            ▼
                       ┌─────────┐
                       │BitPacket│
                       └────┬────┘
                            │
                    ===== Transport =====
                            │
                            ▼
                         Observer

两个世界的内容不对称
Camera → media
Planet → internal glimpse
但两个世界的运输方式应该对称
Camera payload → BitPacket
Planet payload → BitPacket
这就是我们真正想要的“同构”。同构保证“可传递”，而不是保证“必须使用”。
传递 ≠ 观察 ≠ 生效。

简单的模块审计表：
| 模块           | 输入                 | 自己负责    | 输出/回填           | 是否越权 | 是否丢数据 |
| ------------ | ------------------ | ------- | --------------- | ---- | ----- |
| Camera       | 外部世界               | 局部采样    | Camera payload  |      |       |
| CameraPlanet | frame              | 原生封装    | media packet    |      |       |
| Router       | BitPacket          | 传递      | 原 packet        |      |       |
| Planet       | disturbance        | 无限演化    | PlanetField     |      |       |
| PlanetField  | Planet state       | glimpse | glimpse payload |      |       |
| Observer     | glimpse            | 当前观察    | observation     |      |       |
| Cache        | observation        | diff    | change          |      |       |
| Attention    | change             | 注意场     | attention state |      |       |
| Compute      | candidates         | 竞争/资源   | winner          |      |       |
| CLIP         | input + allocation | 精算      | CLIPCloud       |      |       |

外部世界
   │
   ▼
Camera
   │
   │ 生物式局部采样
   ▼
CameraPlanet
   │
   │ 忠实封装
   ▼
BitPacket
   │
   │ 只是进入内部
   ▼
InternalDynamics
   │
   │ 可被取用
   ▼
┌─────────────────────────────┐
│       Internal Space        │
│                             │
│  Planet     CLIP     Organ  │
│    │         │        │     │
│    │         │        │     │
│    └──────┬──┴────────┘     │
│           │                 │
│       各自决定是否需要        │
└───────────┬─────────────────┘
            │
            ▼
        真正的内部作用

ObservationCache 正确地产生了一个“整个 observation 的结构变化”，而 AttentionField 是否应该把这个结构变化解释为 attention intensity，需要由 AttentionField 自己的职责决定。

                         Observation
                              │
             ┌────────────────┼────────────────┐
             │                │                │
           region            path             exact
             │                │                │
       空间位置变化       选择路径变化       局部内容变化
             │                │                │
             └────────────────┼────────────────┘
                              │
                              ▼
                         ObservationCache
                              │
                              ▼
                         signed Change
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
     region Δ             path Δ             exact Δ
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                       AttentionField
                              │
                    自己决定取什么
这才符合我们现在确定的模块自治原则。					
					
                    PlanetField                     CLIPField
                    ──────────                     ─────────
自身状态               state                         cloud/layers/...
自身时间               age + step                    无自主连续时间
自身演化               planet.evolve()              无
外部触发               disturbance                  camera/input packet
compute_budget         非动力机制                    真正的执行门槛
compute allocation     inert                         必须获得
step()                 自主执行                      有 budget 才执行
演化结束               继续存在                      dirty → false
下一次演化              自动继续                      等待新的输入					
					
PHASE5_8 OUTPUT CHECKPOINT

Camera → Display          ✓
Planet → Display          ✓

Planet internal evolution ✓
Planet observation        ✓
Planet packet             ✓
Transport routing         ✓
Display reception         ✓

CLIP                      ⏸
Compute                   ⏸
Commit                    ⏸
Collision                 ⏸
Memory / Sampler          ⏸
Output fusion             ⏸					


while True
│
├─ Camera
│    ↓
│  CameraIO.encode()
│    ↓
│  Transport.publish(camera_raw)
│    ├──────────────→ DisplayIO
│    │
│    └──────────────→ InternalDynamics.receive()
│
├─ dynamics.step()
│    │
│    ├─ ComputeSystem.step()       ← 暂时保留，但不处理
│    │
│    ├─ Planet clock
│    │    ↓
│    │  PlanetField.step()
│    │    ↓
│    │  PlanetField.glimpse()
│    │    ↓
│    │  planet_glimpse
│    │
│    ├─ Observer
│    │    ↓
│    │  ObservationCache
│    │    ↓
│    │  AttentionField
│    │
│    ├─ CLIP activity              ← 暂停研究
│    ├─ Compute winner             ← 暂停研究
│    ├─ CLIP step                  ← 暂停研究
│    └─ Collision                  ← 暂停研究
│
├─ planet.packet()
│    ↓
│  Transport.publish(visual)
│    ↓
│  DisplayIO.receive()
│
└─ cv2.imshow()
其中两条输出路径真的在跑。

Phase A — 固定当前基线Phase5_8 Planet + Camera Runtime Baseline
Planet 线路不再修改
Camera 线路不再修改
Display 边界不再修改
archive/planet.py 不动
之后如果 Compute / CLIP 出现问题，不能回头改 Planet 来配合它们。

多个独立信息流已经到达输出边界，但“输出端合流规则”尚未设计。内部不合流，输出才合流。
所以未来可以研究 Display 的最终输出策略，但现在不新增 FusionEngine、ColorField、OutputAdapter 等模块。

Phase B：下一条只接 Compute
CLIP.receive()
    ↓
dirty=True
    ↓
activity()
    ↓
request="compute"
candidate=None
    ↓
ComputeSystem.select()
    ↓
None
    ↓
allocation=None
    ↓
CLIP.compute_budget=0
    ↓
CLIP.step()
    ↓
无法 forward
    ↓
candidate 仍然 None
CLIP被外部状态云冲撞后产生局部快速响应的结构。 第一次局部响应到底应该由什么真实的内部状态/外部状态触发？

最后再重新打开 Collision	
Planet local state
       ↕
   CloudCollision
       ↕
CLIP local state
最后才重新打开 Memory / Sampler
Planet ✓
Camera ✓
Display ✓
      ↓
Compute
      ↓
CLIP response
      ↓
Collision
      ↓
Memory / Sampler

当前最重要的架构原则
Planet
    自己演化
    自己产生 glimpse
    自己产生 visual packet

Observer
    只观察

ObservationCache
    只保存/比较观察变化

AttentionField
    接收变化

ComputeSystem
    将来负责计算资源选择/分配

CLIP
    局部快速响应
    不成为第二个 Planet

Collision
    将来负责已有状态之间的相互作用

Display
    只负责输出边界
数据原则：

取所需。留其余。产生响应。重新封装，继续传递。
和：
模块拥有局部使用权，不拥有全局删除权。				

ComputeSystem 并没有拒绝一个已经形成的 candidate；它是在 candidate 尚未形成的时候，把 request 挡在了竞争场之外。

CLIP 当前有没有另一条“不需要 Compute 权限”的外部状态入口，可以自然产生第一次局部状态。

Planet time
──────────────────────────────────────→
 P1 → P2 → P3 → P4 → P5 → P6 → ...

Camera time
──────────────────────────────────────→
 C1 → C2 → C3 → C4 → C5 → C6 → ...

CLIP compute time
──────────────────────────────────────→
       F1          F2              F3
       ↑           ↑               ↑
    allocation  allocation      allocation
这三个时间不能混成一个 step。尤其：Planet 不应该因为 CLIP 没有 compute budget 就停止。
	
Planet
  │
  │ 自己演化
  ▼
Planet state
  │
  │ 对内部环境产生影响
  ▼
某种状态进入/作用于 CLIP
  │
  ▼
CLIP 获得局部状态
  │
  ▼
local response
  │
  ▼
candidate
然后：
candidate
   ↓
ComputeSystem
   ↓
allocation
   ↓
CLIP forward
   ↓
新的 cloud
   ↓
新的 response
第一次“状态产生”和后续“计算机会”可能是两个不同层次。
	
① Planet 自主演化

        ↓

② 外部/内部状态进入某个响应体

        ↓

③ 响应体产生自己的局部 response

        ↓

④ response 成为 candidate

        ↓

⑤ ComputeSystem 分配有限计算

        ↓

⑥ CLIP forward

        ↓

⑦ CLIP cloud

        ↓

⑧ CloudCollision

        ↓

⑨ collision result

        ↓

⑩ 后续内部变化	


                    ┌──────────────┐
                    │    Planet    │
                    │ 自主演化     │
                    └──────┬───────┘
                           │
                           ▼
                    Planet local state
                           │
                           │
Camera ───────────────────┤
                           ▼
                    ┌──────────────┐
                    │     CLIP     │
                    │ 局部响应体    │
                    └──────┬───────┘
                           │
                      local response
                           │
                           ▼
                       candidate
                           │
                           ▼
                    ┌──────────────┐
                    │ ComputeSystem │
                    └──────┬───────┘
                           │
                       allocation
                           │
                           ▼
                       CLIP forward
                           │
                           ▼
                     complete cloud
                           │
                           ▼
                    CloudCollision
                           │
                           ▼
                    collision result
                           │
                           ▼
                    Planet disturbance
                           │
                           ▼
                    Planet继续演化
Planet 有自己的时间。CLIP 没有自己的时间。ComputeSystem 有自己的有限资源时间。
Collision 是关系发生时才出现。这四个时间/机制终于分开了。					
					
                    Planet
                      │
                持续自主演化
                      │
                      ▼
                当前完整状态
                      │
                      ▼
              ┌──────────────┐
              │ Planet内部筛选 │
              └──────┬───────┘
                     │
                 candidate
                     │
                 local region
                     │
                     ▼
              Planet local cloud
                     │
                     │
                     ▼
                   CLIP
                     │
              local response
                     │
                     ▼
                winner/candidate
                     │
                     ▼
               ComputeSystem
                     │
                 allocation
                     │
                     ▼
                CLIP forward
                     │
                     ▼
                complete cloud
                     │
                     ▼
              CloudCollision
                     │
                     ▼
              local relation
                     │
                     ▼
              local disturbance
                     │
                     ▼
                 PlanetField
                     │
                     ▼
                继续演化

Planet产生动力。
持续演化
Planet 内部筛选,减少需要暴露/交互的状态空间。
全场
 ↓
局部
 ↓
更局部
 ↓
candidate
CLIP对被作用的状态产生局部响应。
不是自主动力系统。
ComputeSystem
只决定有限计算机会给谁。不是动力来源。
***************************----------------**********************
最终 collision 要成为真正的局部动力学交互，那么以后	
region
+
local state
+
local temporal state
+
local disturbance	
这里现在不要改。因为我们还没有审完 interaction 的实际需求。	
***************************----------------**********************
整个结构可以重新理解成四个不同的“时间”
Planet time
    ↓
连续 endogenous evolution
    ↓
glimpse
    ↓
内部空间筛选


Camera time
    ↓
外部输入到达
    ↓
CLIP dirty


CLIP response time
    ↓
获得 compute opportunity
    ↓
forward
    ↓
local response


Compute time
    ↓
Sampler
    ↓
选择谁获得有限计算
四个时间不能压成一个 step 的意义。

Planet 已经拥有自己的内部筛选机制，但这个筛选机制目前只产生 observation，还没有成为内部 interaction 的局部入口。
现在：

Planet
 ├── evolve
 ├── glimpse ─────→ Observer
 └── state ───────→ Collision   ← 绕过 glimpse


应该逐渐形成：

Planet
 └── evolve
       ↓
    glimpse
       ↓
 internal selection
       ↓
  local Planet state
       ↓
   interaction
       ↓
      CLIP
       ↓
    response
       ↓
   Compute/Sampler
       ↓
      commit
       ↓
 Planet continues
这里没有必要新增模块。

PlanetField--"committed": True, TODO：删除/重新定义 committed=True，避免 Collision 声称自己已经 commit。先不要动，
 
 审计顺序
① Planet glimpse
      ↓
② exact 到底应该暴露什么
      ↓
③ collision 需要什么最小 Planet material
      ↓
④ _extract_planet_local_states()
      ↓
⑤ CloudCollision.collide()
      ↓
⑥ collision_result
      ↓
⑦ PlanetField._apply_collision()

让同一个 glimpse 快照同时携带“描述”和“状态材料”。
glimpse snapshot
│
├── region
├── path
├── age
│
├── observation
│    └── statistics
│
└── local_state
     └── raw local Planet state

整个数据生命周期可以画成
                         PlanetField
                             │
                         self.state
                             │
                    唯一持续内部状态
                             │
                    ┌────────┴────────┐
                    │                 │
               Planet.step()      glimpse()
                    │                 │
                    │          endogenous selection
                    │                 │
                    │          selected region
                    │                 │
                    │          local snapshot
                    │                 │
                    │       ┌─────────┴─────────┐
                    │       │                   │
                    │   observation          local_state
                    │       │                   │
                    │       ▼                   ▼
                    │    Observer          Collision
                    │                           │
                    │                           │
                    └───────────────┐           │
                                    │           │
                              continue          │
                              evolution         │
                                                ▼
                                      Planet local ×
                                      CLIP local
                                                │
                                                ▼
                                           collision
                                                │
                                                ▼
                                         disturbance
                                                │是唯一重新进入 Planet 的地方。
                                                ▼
                                           PlanetField


| 部分                             | 当前状态               | 判断 |
| ------------------------------ | ------------------ | -- |
| Planet.step                    | 内生演化               | ✅  |
| Planet.glimpse                 | Planet 自己选择局部      | ✅  |
| glimpse → Observer             | 当前观察               | ✅  |
| glimpse → Collision            | **尚未接上**           | ⚠️ |
| Collision → CLIP               | 12层局部状态            | ✅  |
| CLIP × Planet                  | Cartesian relation | ✅  |
| Collision → candidate          | 关系产生               | ✅  |
| candidate → scalar disturbance | **过早压缩**           | ⚠️ |
| scalar → 整个 Planet             | **全局广播**           | ⚠️ |

真实结构非常干净：
PlanetField
    └── endogenous Planet state


CLIP
    └── 12 image-layer state clouds


CloudField
    └── local Cell state
    └── collision() 生命周期入口
    └── inject_local_response() 结果承接入口


Sampler
    └── 从大量候选中竞争有限注意力


ComputeSystem
    └── 有限计算资源

暂时把架构原则写成这样
CIMA0 Attention Principle

1. Internal state may be large and continuously evolving.

2. Existence does not imply observation.

3. Observation is local and limited.

4. Unobserved state continues to evolve.

5. Potential relations remain open;
   they are not globally pre-filtered.

6. Only currently contacted states enter actual observation.

7. Compute is finite and selective.

8. Commit is the only explicit state-changing decision.

9. Temporary observations and collision material
   do not become independent long-term state sources.	
   
CIMA0 的“注意力有限”不是性能优化。
它是认识世界的方式。永远只能接触一小部分，而系统的长期演化决定下一次可能接触哪里。
是一个有限注意力参与其中的持续动力系统。   


CIMA0 当前的方向浓缩成一句话
状态可以巨大而持续演化，潜在关系保持开放，但有限注意力只能接触极小的一部分，有限 Compute 再从这些实际接触中产生一次改变。

或者更简洁：无限状态，开放关系，有限注意力，有限计算。

                  时间
                   →
                   →
Planet ─────────────────────────
        演化    演化    演化

CLIP   ────────────────► 状态进入

                   ↓
              当前异常/胜出
                   ↓
                glimpse
                   ↓
             扩大观察范围
                   ↓
        ┌──────────┴──────────┐
        ↓                     ↓
   当前状态痕迹          历史变化痕迹
        │                     │
        └──────────┬──────────┘
                   ↓
             后验状态形成
                   ↓
             AttentionField
                   ↓
             状态 / 云 / 场
                   ↓
              开放关系空间
                   ↓
                collision
                   ↓
             候选变化
                   ↓
             有限采样/计算
系统先产生历史，再从当前胜出点向后观察历史，并把后验观察逐渐形成新的状态。			 
			 
一个核心原则写成：
动力属于 Planet，状态属于 PlanetField，
碰撞属于状态之间的关系，扰动只是状态变化的输入，
观察只描述状态，计算只提供有限机会；没有任何这些东西可以自行成为第二个 Planet。

现在的 CIMA0 状态
| 部分                     | 当前状态          | 真正还没解决的问题          |
| ---------------------- | ------------- | ------------------ |
| **Planet 内部动力学**       | 基本稳定          | 保持其自主性             |
| **Camera → 内部状态**      | 框架已经存在        | 继续完成状态化后的内部路径      |
| **CLIP 预形成状态**         | 已经存在          | 明确它作为“已有状态”的位置     |
| **Planet ↔ CLIP 碰撞**   | **实验阶段，反复推翻** | 什么才算真正的状态互动、响应如何产生 |
| **Observer / glimpse** | 基本成形          | 保持只观察              |
| **Compute / Sampler**  | 框架存在          | 让选择机制真正利用历史        |
| **Memory**             | **被动记录**      | 过去如何改变未来选择         |
| **整体自演化闭环**            | 尚未完成          | 让上述部分自然闭合          |


“状态 ≠ 动力”
| 对象           | 是什么          | 自己产生动力？   |
| ------------ | ------------ | --------- |
| Planet       | 大海 / 动力核心    | **是**     |
| PlanetField  | 局部海水状态       | 不独立产生     |
| CloudField   | 粘稠/凝固倾向的局部状态 | 不作为第二动力核心 |
| CLIP         | 预形成状态        | 否         |
| Camera cloud | 外部输入形成的内部状态  | 否         |
| Collision    | 状态关系         | 否         |
| Observer     | 观察关系         | 否         |
| Memory       | 历史状态记录/关系    | 否         |

                    ┌──────────────────┐
                    │      Planet      │
                    │  唯一动力来源    │
                    └────────┬─────────┘
                             │
                         evolves/step
                             │
                             ▼
                    ┌──────────────────┐
                    │   PlanetField    │
                    │   局部状态空间   │
                    └────────┬─────────┘
                             │
                         glimpse
                             │
                             ▼
                    ┌──────────────────┐
                    │ CloudCollision   │
                    │   状态关系机制   │
                    └────────┬─────────┘
                             │
                      collision response
                             │
                             ▼
                    ┌──────────────────┐
                    │   PlanetField    │
                    │ receive(disturb.)│
                    └────────┬─────────┘
                             │
                     pending_disturbance
                             │
                             ▼
                    ┌──────────────────┐
                    │      Planet      │
                    │ 下一次动力演化    │
                    └──────────────────┘
                             ↺
							 
              已确认
                 │
                 ▼
Planet ─── 唯一动力源
  │
  ▼
PlanetField ─── 状态承接
  │
  ▼
CloudCollision ─── 状态关系
  │
  ▼
collision response
  │
  ▼
PlanetField.receive()
  │
  ▼
pending_disturbance							 
							 
                 ┌──────────────────────┐
                 │       Planet         │
                 │                      │
                 │  唯一内部动力来源    │
                 │  state + local rule  │
                 └──────────┬───────────┘
                            │
                          step()
                            │
                            ▼
                 ┌──────────────────────┐
                 │     PlanetField      │
                 │                      │
                 │   Planet evolved     │
                 │      local state     │
                 └──────────┬───────────┘
                            │
                     glimpse / state
                            │
                            ▼
                 ┌──────────────────────┐
                 │   CloudCollision     │
                 │                      │
                 │   state relation     │
                 │   response relation  │
                 └──────────┬───────────┘
                            │
                      transient response
                            │
                            ▼
                 ┌──────────────────────┐
                 │     PlanetField      │
                 │ pending_disturbance  │
                 └──────────┬───────────┘
                            │
                    observation / effect
                            │
                            ▼
                         discard

| 层                                           | 当前状态          |
| ------------------------------------------- | ------------- |
| CLIP 完整 cloud                               | ✅ 保留          |
| winner 作为入口                                 | ✅ 正确          |
| CLIP 局部状态提取                                 | ✅ 保留拓扑        |
| Planet 状态提取                                 | ✅ 保留自身坐标      |
| Cartesian relation                          | ✅ 暂时保留        |
| relation 集合                                 | ✅ 核心碰撞材料      |
| `_make_candidate()`                         | ⚠️ 响应语义需要重新定义 |
| `committed=True`                            | ❌ 语义错误        |
| `_build_collision_result()` 的 `mean()`      | ⚠️ 第一次明显信息压缩  |
| `_apply_collision()` scalar → uniform field | ⚠️ 第二次明显信息压缩  |
| Planet 自身动力规则                               | ✅ 不应修改        |

当前 CloudCollision 画出真实职责图：
                    ┌─────────────────────┐
                    │   CLIP complete     │
                    │      state          │
                    └──────────┬──────────┘
                               │
                               │
                               ▼
                    ┌─────────────────────┐
                    │  local state pair   │
                    │     relation        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ _collision_type()   │
                    │                     │
                    │ zero/nonzero        │
                    │ same/opposite sign  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ _make_candidate()   │
                    │                     │
                    │ hand-written        │
                    │ response formula    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ relations[]         │
                    │                     │
                    │ actually rich       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ _build_collision_   │
                    │ result()            │
                    │                     │
                    │ MEAN → scalar       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ _apply_collision()  │
                    │                     │
                    │ scalar → full field│
                    └──────────┬──────────┘
                               │
                               ▼
                         PlanetField

CLIP
│
└── 提供完整 CLIP state
        │
        ▼
CloudCollision
│
├── 认识 CLIP topology
├── 认识 Planet topology
├── 产生 state relations
└── 产生 candidate responses
        │
        ▼
Planet-shaped response
        │
        ▼
PlanetField
│
├── receive disturbance
├── 保存 pending state
├── glimpse local state
└── 承接 Planet dynamics
        │
        ▼
Planet
└── 唯一 dynamics source
InternalDynamics应该只是：调用,传递,承接

CloudCollision 实际上已经分成了三个层次
第一层：发现状态
────────────────────────
CLIP cloud
    ↓
_extract_clip_local_states()

Planet local state
    ↓
_extract_planet_local_states()


第二层：建立关系
────────────────────────
CLIP state × Planet state
    ↓
_collision_type()
    ↓
relations[]


第三层：产生响应
────────────────────────
relations[]
    ↓
_make_candidate()
    ↓
proposed_value
    ↓
_build_collision_result()
    ↓
一个 disturbance scalar


CloudCollision
────────────────────
负责：

CLIP state
+
Planet state
        ↓
state relation
        ↓
candidate response
        ↓
Planet-compatible response material
-------------------
PlanetField
────────────────────
负责：

接收 disturbance
        ↓
保存 pending disturbance
        ↓
交给 Planet dynamics
        ↓
产生下一状态		
---------------
InternalDynamics
────────────────────
只负责：

调用
 ↓
传递
 ↓
承接		

完整 CLIP Cloud
12 × 50 × 768
        │
        │
        ▼
┌─────────────────────┐
│ Level 1             │
│ Layer Response      │
│                     │
│ 12 个 layer scalar  │
└──────────┬──────────┘
           │
           ▼
      winner_layer
           │
           │
           ▼
┌─────────────────────┐
│ Level 2             │
│ Matrix Cloud        │
│ Response            │
│                     │
│ 50 × 768            │
└──────────┬──────────┘
           │
           ▼
   matrix coordinate
   (token, dimension)
           │
           │
           ▼
┌─────────────────────┐
│ Level 3             │
│ Posterior           │
│                     │
│ perturbation cloud  │
│ + collision         │
│ + state change      │
└──────────┬──────────┘
           │
           ▼
      reverse calculation
	  
                    CLIP 完整状态云
                    12 × 50 × 768
                           │
                           │
                    【第一次采样】
                           │
                           ↓
                    12 个 layer response
                           │
                           ↓
                       winner_layer
                           │
                           │
                    【第二次采样】
                           │
                           ↓
                 winner layer 的 50×768
                           │
                           ↓
                   matrix coordinate
                      (token, dim)
                           │
                           │
                    【后验回溯】
                           │
                           ↓
                 扰动云参数 / 碰撞关系
                           │
                           ↓
                    反向计算
                           │
                           ↓
                 相关局部状态	  
	  
main.py
   │
   ▼
Sampler
  ├──────────────► ComputeSystem
  │                    │
  │                    └── compute selection
  │
  └──────────────► CLIPField
                       │
                       └── matrix coordinate selection

ComputeSystem
    └── sampler
         └── ObservationMemory

CLIPField
    └── sampler

CLIPField
   │
   ├── winner_layer
   │
   └── matrix_coordinate
             │
             ↓
       CloudCollision
             │
             │ 关系计算
             ↓
       candidate response
             │
             ↓
       后验回溯所需证据

Camera perturbation cloud
          │
          └──────────────┐
                         ↓
                  CloudCollision
                         ↑
                         │
                 matrix coordinate
                         ↑
                         │
                    CLIP state

这样就很漂亮：Camera 是动力来源之一。Planet 是动力来源之一。Collision 只是关系。
CLIP 是预形成状态。Matrix coordinate 是观察入口。Memory 是历史证据。
没有谁突然变成“大脑”。

Planet
  ✓ 唯一内部动力源
  ✓ 自己的 clock
  ✓ evolve(state, disturbance)

PlanetField
  ✓ 保存当前 state
  ✓ 保存 previous_state
  ✓ 接收 pending disturbance
  ✓ 产生 sparse glimpse
  ✓ 粗→细→精确观察
  ✓ 不负责解释

CLIPField
  ✓ 12-layer response
  ✓ winner layer
  ✓ 50×768 matrix coordinate
  ✓ 保留 current / previous / delta

CloudCollision
  ✓ 1 CLIP local state
  ✓ 1 Planet local state
  ✓ 产生 relation
  ✓ candidate → disturbance
  ✓ 不拥有 dynamics

InternalDynamics
  ✓ 局部模块连接
  ✓ Planet clock 不被强制改变
  ✓ collision disturbance 延迟到下一次 Planet evolve

Posterior
  ? 等待确认已有 local evidence
  
              状态
               │
        ┌──────┴──────┐
        │             │
      Planet         CLIP
        │             │
   region response  layer response
        │             │
   winner region    winner layer
        │             │
   exact local     matrix coordinate
        │             │
   current/prev    current/prev
   delta           delta
        │             │
        └──────┬──────┘
               │
          posterior  
  
Planet                          CLIP
──────                          ────

previous_state                  previous_cloud
       │                              │
       ▼                              ▼
current_state                   current_cloud
       │                              │
       ▼                              ▼
local delta                     layer delta
       │                              │
       ▼                              ▼
winner region                   winner layer
       │                              │
       ▼                              ▼
exact local                     matrix coordinate  
  
两个局部系统各自通过自己的规则，从完整状态中产生稀疏观察坐标。  
  
当 Planet 自己在下一时刻产生新的状态变化时，从新的局部状态及其时间差中回看“刚才发生了什么”。  
t
────────────────────────────

CLIP matrix coordinate
        ↓
collision
        ↓
disturbance


t+1
────────────────────────────

Planet.evolve(
    previous state,
    disturbance
)
        ↓
new state
        ↓
previous_state
+
current state
        ↓
local delta
        ↓
glimpse
        ↓
观察 winner   “胜出的坐标，引导观察者回溯那里发生的事情。”

 InternalDynamics 不保存“发生了什么”；PlanetField 只保存自己的时间状态；
 CloudCollision 只保存关系结果；Observer 只发现变化。
 后验应从这些局部证据的自然交汇中产生，而不是由一个新模块统一解释。 
 
Planet
  = 唯一内部动力源

Camera
  = 外部动力/扰动源

CLIP
  = 预形成状态

CloudCollision
  = 状态关系

PlanetField
  = Planet 的局部状态 + 自己的时间 + 自己的观察

Observer
  = 发现变化

Sampler
  = 选择关注点

InternalDynamics
  = 承接各模块，不拥有它们的历史

ObservationCache
  = 快照比较，不成为世界的唯一来源
------------------
自指链开始显现：
Planet
 ↓
状态变化
 ↓
PlanetField 自己观察自己
 ↓
找到局部变化
 ↓
外部/内部状态关系进入
 ↓
产生扰动
 ↓
Planet 再次演化
 ↓
新的状态再次成为观察对象
 ↺


CLIP 一侧
winner_layer
matrix_coordinate
current
previous
delta
Collision 一侧
planet position
planet value
clip position
clip value
collision type
candidate
proposed_value
PlanetField 一侧
previous_state
state
delta
glimpse region
local_state
local_exact

collision
   │
   ▼
receive()
   │
   ▼
pending_disturbance
   │
   │ 等待 Planet 时钟
   ▼
Planet.evolve()
   │
   ├──────────────► previous_state = 演化前
   │
   └──────────────► state = 演化后
                         │
                         ▼
                 pending_disturbance 清空
扰动只能改变状态，不能改变动力系统规则。

真正架构升级是
以前我们说：

Planet 是封闭动力系统。

现在应该改成：

Planet 是自主动力系统，但观察上并不等于封闭系统。

再进一步：

Observer 的唯一性制造了“封闭”的假象。	
			 
Interaction may alter the state trajectory, but never defines the dynamics rule.
交互可以改变状态轨迹，但不能定义动力学规则。

CIMA0 可以第一次画出一个非常清楚的“时间拓扑”
                  REAL DYNAMICS
                       │
                       ▼
                ┌─────────────┐
                │   Planet    │
                │ own dynamics│
                └──────┬──────┘
                       │
                 Planet clock
                       │
                       ▼
                ┌─────────────┐
                │ PlanetField │
                │ observation │
                │    window   │
                └──────┬──────┘
                       │
                       │ sampled
                       ▼
                ┌─────────────┐
                │  Observer   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Sampler   │
                │   winner    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Compute   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │    Organ    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │ Interaction │
                │ / Collision │
                └──────┬──────┘
                       │
                       ▼
                  disturbance
                       │
                       ▼
                pending interaction
                       │
                       │ next Planet tick
                       ▼
                    Planet

| 环节               | 当前实际职责                               |
| ---------------- | ------------------------------------ |
| Planet           | 自身演化                                 |
| Observer / Cache | 观察与变化比较                              |
| ComputeSystem    | selection / allocation / consumption |
| commit           | 把计算资源交给 Organ                        |
| Organ            | 消费计算机会、推进自身                          |
| Collision        | 产生 disturbance                       |
| `_sample()`      | 当前状态快照                               |



					