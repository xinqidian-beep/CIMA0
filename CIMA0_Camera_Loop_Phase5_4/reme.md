
************************************
### CIMA0 Phase5_3 当前状态总结

这阶段主要完成了**同构链路和职责边界重新梳理**。目前系统现象：

> 显示窗口仍然是黑白灰渐变地形，并且缓慢变化。

这个现象说明：

* `Planet` 基础动力系统仍然在运行；
* `Planet snapshot → Observer → DisplayIO` 链路仍然有效；
* 显示的是内部动力状态，不是摄像头媒体流；
* Camera 扰动目前还没有形成明显可见影响。

---

## 一、已经确认的问题

### 1. Planet 自演化正常

当前黑白灰渐变：

不是显示错误。

它来自：

```text
Planet
 |
 | step()
 |
 v
state
 |
 v
InternalDynamicsObserver
 |
 v
DisplayIO
```

Planet 本身没有：

* 颜色
* BGR
* 图像语义

所以显示成灰度场是符合设计的。

---

### 2. Camera媒体同构链重新设计完成方向

目标链路：

```text
CameraPlanet

BGR packet

{
 bytes,
 shape,
 dtype,
 format=BGR,
 channels=3
}


        ↓


CameraObserver

保存完整BGR field

计算:

delta
age
activity


产生:

compute_request


        ↓


CameraCompute

执行采样


        ↓


CameraIO

重新封装媒体packet


        ↓


DisplayIO

按packet标签恢复
```

原则：

> 摄像头进入系统后，不允许因为采样、计算、观察而丢失媒体同构信息。

---

### 3. Observer职责重新划分

确定：

Observer：

负责：

* 读取状态
* 计算变化
* 举手请求

不负责：

* 选择采样点
* 分配算力

结构：

```text
Observer

产生:

score

        ↓

ComputeSystem

分配:

budget

        ↓

Sampler

执行:

selection
```

---

### 4. Sampler重新定位

Sampler：

纯执行器。

输入：

```text
score
budget
```

输出：

```text
indices
```

不理解：

* camera
* planet
* cloud
* CLIP

---

## 二、当前未完成部分

### 1. Camera链路还没有最终接入主循环

虽然四模块方向已经明确：

```text
camera_planet
camera_observer
camera_compute
camera_io
```

但还需要检查：

main.py 当前调用是否仍然走旧路径。

重点：

确认：

```python
camera frame
    ↓
CameraPlanet.step()
    ↓
CameraObserver.observe()
    ↓
CameraCompute
    ↓
CameraIO
    ↓
DisplayIO
```

是否真的成为显示来源。

现在显示仍然是：

```text
Planet field
```

说明：

```text
CameraIO输出
        ↓
DisplayIO
```

可能还没有接管。

---

### 2. InternalDynamics链需要继续同构审核

下一阶段：

审核：

```text
InternalDynamics
        |
        v
InternalDynamicsObserver
        |
        v
ComputeSystem
        |
        v
Sampler
        |
        v
DisplayIO
```

重点检查：

#### InternalDynamics

必须：

* 接收扰动
* 不解释媒体
* 保留状态结构

不能：

* 变成CameraAdapter

---

#### InternalDynamicsObserver

需要补：

自动举手：

```python
score =
    w_delta * delta
    +
    w_age * age
    +
    w_activity * activity
```

输出：

```python
{
 type:"compute_request",
 score,
 shape
}
```

---

#### encode_field()

需要携带：

```python
{
 type:"field",
 field_type:"planet_state",
 representation:"scalar_field",
 dtype:"float32"
}
```

避免DisplayIO猜测。

---

## 三、下一阶段计划

### Phase5_3.1

完成 Camera 显示闭环

目标：

验证：

```text
Camera输入

↓

彩色packet

↓

DisplayIO

↓

彩色输出
```

不是：

```text
Planet灰度场
```

---

### Phase5_3.2

完成 InternalDynamicsObserver 重构

加入：

* 举手机制
* score生成
* compute request

保持：

Observer只观察。

---

### Phase5_3.3

审核 InternalDynamics.receive()

目标：

确认：

```text
camera disturbance

↓

internal disturbance

↓

planet response
```

真实存在。

重点：

不能丢：

* shape
* dtype
* field身份

---

### Phase5_3.4

最终统一：

两条同构链：

#### 外部视觉：

```text
Camera

媒体场

Observer

Compute

Sampler

IO

Display
```

#### 内部动力：

```text
Planet

动力场

Observer

Compute

Sampler

IO

Display
```

二者共享：

* 举手机制
* 算力分配
* 采样原则

但不共享：

* 数据含义
* 动力规则
* 表达形式

---

## 当前最重要判断

现在黑白灰渐变不是失败。

它证明：

> Planet 基础动力已经脱离摄像头独立存在，并且可以持续演化。

下一步不是修改 Planet，而是确认：

**Camera 的媒体场是否已经成为另一个可观察、可采样、可输出的同构场。**

后续工作顺序：

1. 接通 CameraIO → DisplayIO 显示路径
2. 重写 InternalDynamicsObserver 举手机制
3. 审核 InternalDynamics.receive 扰动进入
4. 最后再观察 Camera扰动对Planet盆地形成的长期影响

这样不会破坏已经稳定的动力核心。
***********************************************
# CIMA0 Phase5_4 当前阶段总结

## 一、架构状态确认

Phase5_4 相比 Phase5_3 最大变化：

**外部输入不再直接驱动 Planet。**

---

### Phase5_3

旧结构：

```
Camera
  |
  v
InternalDynamics
  |
  v
Planet.state
  |
  v
Planet evolution
```

特点：

* 摄像头扰动直接进入 Planet
* Planet 被外部输入修改
* camera 与内部动力强耦合

---

### Phase5_4

新结构：

```
                 Camera packet
                       |
                       v

              InternalDynamics
                       |
        +--------------+-------------+
        |                            |
        v                            v

    Planet                    Organs
    (自主动力)                (内部器官)

        |                       |
        |                       |
        v                       v

   fast dynamics          CLIPField cloud
                             
                             
                   

                       |
                       v

                 Observer
                       |
                       v

                  Display
```

当前确认：

* Planet 不知道 camera
* Planet 不知道 CLIP
* CLIPField 不知道 Planet
* CLIPField 不知道 Display
* Observer 只负责读取

这个方向符合原始设计原则：

> 模块只知道自己，只做自己的事情。

---

# 二、当前已经完成

## 1. 目录重新冻结

Phase5_4 独立：

```
CIMA0_Camera_Loop_Phase5_4
```

旧版本保留：

```
archive
```

避免继续破坏稳定版本。

---

## 2. Organ层建立

现在：

```
core
|
+-- organs
|      |
|      +-- clip_field.py
```

CLIPField 已经从内部动力中分离。

这是正确方向。

---

## 3. CLIPField加载成功

已经验证：

```
CLIP visual missing: 0
CLIP visual unexpected: 0
```

说明：

* 权重加载正常
* visual backbone匹配
* 模型初始化完成

---

## 4. Camera → CLIP链路成功

已经看到：

```
CLIP receive:
(480,640,3) uint8
```

说明：

```
CameraPlanet
        |
        v
packet
        |
        v
InternalDynamics
        |
        v
CLIPField.receive()
```

已经通。

---

## 5. ComputeSystem / Sampler开始恢复

发现并修复：

* ComputeSystem 缺少 numpy import
* step接口缺失

现在计算资源分配方向重新接回。

---

# 三、发现的重要问题

## 问题1：当前显示来源未知

snapshot结构：

预计：

```python
{
    "planet": ...,

    "organs":
    {
        "clip":
        {
            "cloud": ...
        }
    }
}
```

但是：

```
Observer
```

还没有确认读取哪一个。

所以当前窗口：

可能显示：

1. Planet状态

或者：

2. CLIP内部云

或者：

3. 两者融合

必须检查：

```
core/internal_dynamics/internal_dynamics_observer.py
```

---

# 四、重要架构调整方向

## 1. 不再把CLIP看成视觉

确认：

CLIPField不是视觉模块。

它是：

```
已经进化完成的内部器官
```

类似：

```
CloudField
```

区别：

普通Cloud：

```
稀疏状态
局部响应
```

CLIP：

```
多层级稳定盆地
特殊特征响应
```

---

## 2. 不采用固定12层输出

当前：

```
12层全部采集
```

这是错误方向。

原因：

* 浪费计算
* 没有自适应
* 违背计算资源模型

未来：

```
CLIP layer response

        |
        v

compute request

        |
        v

ComputeSystem

        |
        v

Sampler

        |
        v

selected layers
```

由内部竞争决定：

哪些层保留。

---

## 3. 保留同构标签

不能因为不用颜色语义就删除。

必须保留：

例如：

```python
channels:
{
    order:
        ["B","G","R"],

    location:
    {
        "B":0,
        "G":1,
        "R":2
    },

    content:
    {
        "B":None,
        "G":None,
        "R":None
    }
}
```

原因：

未来需要：

```
byte
 |
 v
state
 |
 v
another system
```

仍然可以解码。

---

# 五、下一阶段计划

## Phase5_4-A：先稳定闭环

目标：

```
Camera
 |
 v
CLIPField
 |
 v
cloud
 |
 v
snapshot
 |
 v
observer
 |
 v
display
```

先不要碰复杂演化。

任务：

### 1.

检查：

```
internal_dynamics_observer.py
```

确认显示来源。

---

### 2.

完善：

```
InternalDynamics.snapshot()
```

统一：

```python
{
 "planet":,

 "organs":
 {
    "clip":
 }
}
```

格式。

---

### 3.

确认CLIP输出：

必须看到：

```
CLIP cloud shape:

(12,50,768)
```

---

# Phase5_4-B：恢复计算闭环

目录：

```
core

+-- compute_system
       |
       +-- compute_system.py
       |
       +-- sampling
              |
              +-- sampler.py
```

职责：

ComputeSystem：

```
谁需要计算
 |
 v
分配预算
```

Sampler：

```
哪里值得计算
 |
 v
选择位置/层
```

不能混合。

---

# Phase5_4-C：建立器官碰撞层

最终结构：

```
             Organ Cloud

        CLIPField
             |
             |
             v

       collision sampler

             |
             |
             v

        PlanetField


Planet:

fast variable

Cloud:

slow variable
```

符合：

> planet与cloud同时存在，是不同状态。

---

# Phase5_4-D：多模态扩展

以后：

```
core/organs

    clip_field.py

    whisper_field.py

    emotion_field.py

    embedding_field.py
```

统一：

```
organ interface:

receive()
step()
packet()
snapshot()
```

---

# 当前判断

Phase5_4 最大的变化不是代码，而是模型变化：

以前：

```
输入 → 动力系统
```

现在：

```
输入 → 器官 → 内部状态 → 动力系统
```

这是更接近 CIMA0 原始目标的结构。

下一步重点：

**先检查 observer，确认当前窗口到底显示 Planet 还是 CLIP cloud。**

然后再补：

**organ → compute → collision → Planet 的完整闭环。**

目前方向正确，不建议再回退到 Phase5_3 的 camera 直接扰动 Planet。
**************************************


********************************************


Planet 代码：这里的问题是重复最多的问题。还是要摒弃习惯写法。这里采样调用计算模块来接手，planet只提演化规则。

最终改造优先级
排序：

顺序	文件	原因
1	internal_dynamics.py	整个调度中心
2	clip_field.py	验证预算闭环
3	Planetfield.py	慢变量系统接入
4	Display	最后观察

**************************************对，这里需要进一步修正“最小模块”的定义。

刚才说的 `BitTransport` 如果理解成一个很小的传输类，会过度简化。你指出的更准确：

> 最小的不是功能最少，而是**核心约束最少、扩展空间最大**。

因为 CIMA0 面向的是多模态、多终端、分布式环境，所以传输层天然要面对：

* 图像（camera / video）
* 声音（audio stream）
* 网络输入
* 传感器
* 其他终端状态
* 外部设备协议
* 未来未知模态

所以它不能设计成：

```text
camera_packet
clip_packet
audio_packet
```

这种越来越多的专用接口。

应该是：

```text
统一状态流接口
```

---

# 重新定义 Transport Layer

它不是：

```
bytes搬运工具
```

而是：

```
同构状态交换层
```

核心只保证：

1. 能携带信息
2. 能标记来源
3. 能描述结构
4. 不解释内容

---

例如：

```python
Packet
{
    header,
    payload
}
```

---

## header

负责：

```
这个东西是什么
```

例如：

```python
{
    "source": "camera01",

    "tag": "visual",

    "version": 1,

    "timestamp": ...,

    "shape": (480,640,3),

    "dtype": "uint8",

    "encoding": "raw"
}
```

---

## payload

只有：

```python
bytes
```

例如：

图像：

```
BGR bytes
```

声音：

```
PCM bytes
```

网络：

```
serialized bytes
```

甚至：

```
None
```

也可以成立。

---

# 关键：Transport 不知道 CLIP

例如：

现在：

```
Camera
 |
 v
CLIPField
```

以后应该：

```
Camera
 |
 v
Transport
 |
 +------------+
 |            |
 v            v

CLIP       AudioField

```

Transport 不知道：

* 这是视觉
* 这是声音
* 这是文本

它只知道：

```
有一个状态包
```

---

# 模块接口应该统一

所有内部模块：

```python
class Organ:

    def receive(packet):
        pass


    def tick():
        pass


    def emit():
        pass

```

---

注意：

这里没有：

```python
compute_request()
```

没有：

```python
apply_compute()
```

因为这些都是具体实现层。

---

例如：

## CLIP

收到：

```
visual packet
```

自己决定：

```
是否编码
什么时候编码
编码多少
```

---

## Audio

收到：

```
audio packet
```

自己决定：

```
频谱
memory
prediction
```

---

## PlanetField

收到：

```
state disturbance packet
```

自己决定：

```
collision
selection
propagation
```

---

# 那 ComputeSystem 放哪里？

这里也需要重新定位。

不是删除。

而是从：

```
控制器
```

变成：

```
资源场
```

例如：

```
ComputeField

    available_energy

    thermal_limit

    memory_limit

    latency
```

模块可以读取：

```
当前计算环境
```

然后自己决定。

---

类似生物：

不是大脑说：

```
心脏，你现在跳60次
```

而是：

```
身体环境改变
器官自己响应
```

---

# InternalDynamics 的角色也需要调整

它不应该是：

```
scheduler
```

而应该：

```
internal medium
```

类似：

```
空间
```

职责：

保存：

```
organ集合

transport

state snapshot
```

提供：

```
连接
```

不提供：

```
控制
```

---

最终结构：

```
                 External World

                       |
                       v

              Bit Transport Layer

                       |
        --------------------------------

        |              |              |

     Visual         Audio          Network

     CLIP           AudioOrg       NetOrg


        |              |              |

        --------------------------------

                 Internal Space

                       |

                 PlanetField

                       |

                  Planet

```

---

所以你说：

> 可以保留接口，随时根据需要补充。

这个是关键。

接口应该稳定：

```text
packet
receive()
emit()
tick()
snapshot()
```

内容可以增长：

今天：

```
visual
```

明天：

```
audio
```

后天：

```
robot sensor
```

甚至：

```
未知智能体
```

都不需要修改核心。

---

这也解释了为什么之前 `InternalDynamics` 里不断增加：

* compute_request
* allocation
* source匹配
* budget分发

最后会越来越复杂。

因为它承担了本来应该属于：

```
transport + environment
```

的职责。

我认为 Phase5_4 现在应该停在这里重新整理边界：

**先建立通用状态交换层，再让 CLIP / Audio / PlanetField 成为自治模块。**

这样后续增加多模态，不需要继续修改内部动力核心。
****************************************************
******************************************************
这个总结抓到了 CIMA0 这套设计最核心的工程原则。

之前 Phase5_4 出现大量接口问题，本质原因不是代码量增加，而是**逐渐引入了人为中心控制逻辑**：

```text
InternalDynamics
        |
        +-- 告诉 Planet 什么时候运行
        |
        +-- 告诉 CLIP 什么时候计算
        |
        +-- 告诉 Cloud 如何分配预算
```

于是系统开始需要维护：

* 谁调用谁
* 谁先运行
* 谁申请资源
* 谁拥有权限
* 谁知道谁

复杂度自然爆炸。

---

回到你的原则：

## 1. 模块化

每个模块有明确边界：

例如：

```text
Planet

职责：
    自己的状态
    自己的动力规则
    自己的演化

不知道：
    CLIP
    Camera
    Audio
```

---

```text
CLIPField

职责：
    视觉状态转换
    自己的内部表示

不知道：
    Planet怎么演化
    Cloud怎么传播
```

---

```text
Transport

职责：
    信息交换

不知道：
    信息是什么意义
```

---

## 2. 同构化

所有模块遵守类似接口：

```python
receive(packet)

tick()

snapshot()
```

或者：

```python
input()

evolve()

output()
```

这样新增模块：

Audio：

```text
AudioField
```

Network：

```text
NetworkField
```

Robot：

```text
RobotField
```

都不需要修改核心。

---

## 3. 嵌套化

大的结构由小结构组成：

例如：

```text
CIMA0

    InternalDynamics

        Planet

        Organs

            CLIP

            Audio

            Memory

        CloudField

```

每一层只关心自己的下一层。

---

类似：

细胞：

```text
细胞
 |
器官
 |
个体
 |
群体
```

每层都有自己的规则。

---

## 4. 不引入人为控制

这是最关键的一点。

不要：

```python
if clip:
    run_planet()

if planet:
    give_clip_budget()
```

这种逻辑。

因为它假设：

> 一个中心知道所有模块需要什么。

而自治系统不应该这样。

正确：

```text
模块感知环境

        ↓

模块根据自身规则响应

        ↓

产生状态变化
```

---

例如：

CLIP：

```text
收到视觉流

检查自身状态

决定：
    是否更新
    更新多少
```

Planet：

```text
收到扰动

检查自身状态

决定：
    是否演化
```

Cloud：

```text
收到状态

决定：
    collision
    decay
    propagation
```

---

## 5. 外界工作互不干扰

这里不是“完全隔离”。

而是：

**只通过统一信息流产生影响。**

例如：

错误方式：

```text
CLIP
 |
调用
 |
Planet.step()
```

正确方式：

```text
CLIP

产生状态包

      ↓

Transport

      ↓

Planet.receive()

      ↓

Planet自己决定
```

---

这也是为什么：

`packet / transport`

这一层很重要。

它把：

```
影响
```

和：

```
控制
```

分离。

---

最终 CIMA0 的核心结构可以浓缩为：

```text
                 Information Flow

                       |
                       v

        +--------------+--------------+

        |              |              |

      Planet        CLIP          Cloud

        |              |              |

        +--------------+--------------+

                       |

                 Internal Space


每个模块：

拥有自己的时间

拥有自己的规则

拥有自己的状态

只接受信息，不接受命令

```

---

所以后续开发原则应该冻结为：

1. **archive 是不可污染的最小基元**
2. **模块只拥有自己的状态和规则**
3. **模块之间只交换同构信息**
4. **Transport 负责流动，不负责解释**
5. **InternalDynamics 负责承载，不负责调度**
6. **Observer 只观察，不影响**
7. **Compute 是环境，不是管理员**

这样代码反而会越来越简单。

复杂度来自“协调”，而不是来自“模块数量”。去掉中心协调以后，多模态、多终端、多节点扩展反而会更容易。
