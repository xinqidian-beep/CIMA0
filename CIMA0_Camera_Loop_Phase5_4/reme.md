
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