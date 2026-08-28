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
			 