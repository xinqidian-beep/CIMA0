是的，我建议**新开文件夹：**

```text
CIMA0_Camera_Loop_Phase5_6
```

不要继续直接修改 `Phase5_5`。

原因：

现在 `Phase5_5` 有一个明确的里程碑：

```
Phase5_5

Camera
  ↓
visual packet
  ↓
CLIPField organ
  ↓
(12,50,768) cloud field
  ↓
InternalDynamics snapshot
  ↓
Observer
```

这个版本已经证明：

* Camera 输入链路正常
* CLIP 可以作为 organ 接入
* ComputeSystem 可以调度 organ
* 高维状态场可以生成并观察

应该冻结作为基线。

---

## Phase5_6 的目标重新定义

不是继续调 CLIP。

而是：

```
Phase5_6

Internal Field Architecture
```

主要工作：

### 1. 抽象 Field

目前：

```python
self.internal_fields["clip"]
```

里面直接放 CLIP packet。

下一步应该形成：

```
core/
    fields/
        field.py
        field_manager.py
```

例如：

```python
Field

    data
    shape
    dtype

    age
    activity
    timestamp

    update()
    decay()
```

CLIP只是一个产生 Field 的 organ。

---

### 2. InternalDynamics 不直接保存 packet

现在：

```python
self.internal_fields[name]=packet
```

以后变成：

```
organ
 |
 v
FieldManager
 |
 v
Internal Field Space
```

这样：

未来：

```
CLIPField
AudioField
TextField
PlanetField
```

都进入同一个内部空间。

---

### 3. 保持 Planet 隔离

Phase5_6 不急着连接：

```
CLIP
  |
  X
Planet
```

先建立：

```
organ
 |
 field
 |
 internal space
```

稳定以后再决定扰动接口。

---

## 所以目录建议：

复制：

```
CIMA0_Camera_Loop_Phase5_5
```

为：

```
CIMA0_Camera_Loop_Phase5_6
```

然后只在新版本改。

保留：

```
Phase5_5
= CLIP organ integration baseline

Phase5_6
= internal field architecture
```

这样后面如果 Field 架构走偏，可以随时回到 Phase5_5。

这个节点适合分版本，因为我们已经跨过了一个架构边界：从“接入器官”进入“构造内部场”。
------------------------------------+
**********************************
Phase5_6 的第一原则应该写成：

不让 PlanetField 取代 Planet，不让 CLIPField 解释 Planet。每个 Field 只承载自己的状态生成过程，InternalDynamics 只提供共存环境。
******************************************
-------------------------------------------
***********************************************
核心目标：

恢复 archive 的最简同构结构，让 InternalDynamics 只是容器，让每个 Field 成为独立的小系统。

建议分几个阶段。

Phase5_6 第一阶段：冻结现有 Phase5_5
不要马上改。

保留：

CIMA0_Camera_Loop_Phase5_5
作为实验记录。

原因：

里面已经验证了几个关键事实：

Camera → CLIPField 成功

camera packet
      |
      v
CLIPField
      |
      v
(12,50,768)
ComputeSystem 可以调度 organ

activity
    |
compute allocation
    |
step()
Observer 可以读取内部状态

这些都是资产。

Phase5_6 第二阶段：建立同构 Field 结构
不要创建：

core/fields/
    field.py
    field_manager.py
暂时不要。

改成：

core/

internal_dynamics/

    internal_dynamics.py

    organs/

        planet_field/

            io.py
            compute.py
            observer.py
            planet.py


        clip_field/

            io.py
            compute.py
            observer.py
            clip.py
也就是：

每个 organ 自己拥有完整生命周期。

Phase5_6 第三阶段：降低 InternalDynamics 权力
目标：

InternalDynamics 最终只剩：

class InternalDynamics:


    organs={}


    register()


    receive(packet):

        for organ:
            organ.receive(packet)


    step():

        for organ:
            organ.step()


    snapshot():

        for organ:
            collect()

结束。

不要出现：

if clip:
if planet:
if camera:
Phase5_6 第四阶段：恢复 PlanetField
现在最重要的是 PlanetField。

因为它是 CIMA0 的动力核心。

结构：

PlanetField

        |
        |
     Planet

        |
        |
   local state


        |
        |
selection dynamics

        |
        +------------+

        collision
        decay
        propagation
        emergence
注意：

这里重新使用以前的云三项思想。

但是名字改变：

不是 CloudField。

而是：

PlanetField local state
或者：

LocalField
Phase5_6 第五阶段：CLIPField 保持隔离
目前：

CLIPField

input:
visual packet


output:

multilevel cloud
已经成立。

不要急着：

CLIP → Planet
不要。

先观察：

PlanetField 自己演化

CLIPField 自己形成盆地
Phase5_6 第六阶段：重新设计 Observer
现在 Observer 不负责理解。

只负责：

snapshot
    |
    v

sampling
例如：

第一版：

observer.observe(
    "clip.cloud.delta"
)
以后：

mean
variance
delta
age
topology
只是观察方式。

最后才考虑互动
等下面三个东西稳定：

PlanetField

CLIPField

Observer
之后，再问：

不同 Field 是否通过环境产生耦合？

而不是提前设计连接。

当前优先级排序
我建议：

1.
整理 InternalDynamics 边界
        ↓
2.
PlanetField 独立化
        ↓
3.
CLIPField 独立化
        ↓
4.
Observer 策略化
        ↓
5.
长期运行观察
        ↓
6.
再决定 Field 之间是否产生互动
还有一个关键判断：

现在已经证明：

CLIP 可以产生内部状态。

下一步不要追求更多输入。

下一步应该证明：

一个 Field 能否在没有人工解释的情况下，根据自己的规则长期演化。

这才是 CIMA0 从“数据处理系统”走向“内部动力系统”的关键。
****************************************
****************************************
Phase5_6 保持现在结构
core/

    internal_dynamics/

        internal_dynamics.py


        organs/


            planet_field/

                planet.py
                compute.py
                io.py
                observer.py


            clip_field/

                clip.py
                compute.py
                io.py
                observer.py
********************************
********************************
Phase5_6 的实际建议
顺序：

第一步（现在）
冻结目录。

不移动。

只整理：

clip_field.py
让它成为参考实现。

第二步
把 CLIPField 内部拆清楚：

不是拆文件。

先逻辑分区：

CLIPField

    IO decode

    state storage

    local compute

    activity

    snapshot

确认职责。

第三步
把这个模式复制给 PlanetField。

不是复制代码。

复制生命周期：

receive
activity
step
snapshot
然后 PlanetField 填自己的规则。

第四步
未来：

audio_field
text_field
thermal_field
都走同一路。

所以现在最重要的结论：

CLIPField 不是一个功能模块，它正在成为第一个 Field 原型。

Phase5_6 的目标不是“让 PlanetField 接入 CLIP”。

而是：

从 CLIPField 中提炼出 Field 自治协议，让 PlanetField 和未来多模态都可以自然加入。

这样才符合之前一直坚持的：

各司其职，自己解码自己的 IO，自己根据自己的规则产生响应。
*****************************
***************************
Phase5_6 下一步很明确：

Step 1
从 archive 引入 Planet。

不修改 archive。

建立 Planet organ。

Step 2
让 InternalDynamics 注册 Planet。

确认：

Planet.evolve()
每轮运行。

Step 3
把现在的 PlanetField 恢复为 Planet 的状态场。

Step 4
再考虑：

claim_score

自动筛选

多模态竞争

这些都是上层机制。

现在先不要。

因为如果最简同构闭环没有建立，后面的选择机制会再次把职责混在一起。

现在回到最初原则：

**每个状态体自己解码自己的输入，用自己的规则演化，Observer负责观察。**这条路线是最稳定的。

********************************
**********************************
这个判断其实和目前 Phase5_6 的实验结果是吻合的。

现在的 CLIPField 在 CIMA0 中已经不再是“核心智能”，而更像一个**外部形成的感知器官**。

它当前承担的是：

```
外部视觉字节
        |
        v
CLIPField
        |
        v
内部视觉场 cloud
        |
        v
attention signal
```

它提供的是：

* 一种初始压缩方式
* 一种多层视觉状态
* 一种外部扰动进入内部系统的通道

但是它本身不是最终动力。

---

从 CIMA0 的角度看，未来可能发生的是：

```
CLIPField
     |
     |
     v

PlanetField / Internal Field

     |
     |
     v

新的自组织多模态状态
```

也就是说：

CLIP提供的768维token、12层transformer状态，可能只是**幼年阶段的外部结构模板**。

进入内部动力系统后：

* 被重新编码
* 被竞争筛选
* 被扰动
* 被遗忘
* 被强化

最后留下来的可能已经不是 CLIP 特征。

---

这和现在观察到的现象很接近：

CLIP：

第一次：

```
activity=1.0
```

负责启动。

然后：

```
activity=0
```

因为它没有内部变化。

而 Planet：

虽然没有视觉语义：

```
activity=0.000001
```

但是持续存在。

这说明：

**语义模块依赖输入，动力模块依赖自身。**

---

未来更可能的结构：

不是：

```
camera
 |
CLIP
 |
AI
```

而是：

```
各种外部扰动
       |
       v

Internal Dynamics


       |
       +---- Planet动力
       |
       +---- 视觉残留结构
       |
       +---- 声音残留结构
       |
       +---- 文字残留结构


       |
       v

新的统一状态空间
```

---

所以 CLIP 的位置可能类似：

一个生物的感觉器官。

眼睛很重要，但：

* 视觉皮层不是眼睛
* 意识不是视觉皮层
* 生物不会永久保存眼睛的编码方式

输入经过内部演化后，会形成自己的表示。

---

这也是为什么现在不要急着优化：

* CLIP权重
* 分类能力
* embedding质量

因为这些属于外部模块。

现在真正需要观察的是：

**CLIP产生的状态进入 InternalDynamics 后，会不会被 Planet/PlanetField 吸收，形成新的内部场。**

下一阶段重点应该是：

1. 让 CLIPField、PlanetField、未来AudioField保持同构接口。
2. 让所有状态进入 attention space。
3. 让 IO 输出 winner 的状态。
4. 观察长期演化后：

   * CLIP是否持续存在
   * PlanetField是否形成新的视觉响应
   * 外部标签是否逐渐失去意义

如果出现：

```
camera输入停止

但是内部field仍然保持某种视觉结构
```

那才是真正接近你说的：

> 多模态模块被吸收、溶解，成为内部动力的一部分。

目前 Phase5_6 已经开始具备观察这个过程的条件。
********************
*******************
********************
*********************
这一次 Phase5_6 的推进非常关键，已经从“模块接入”进入到了“自治竞争机制验证”阶段。总结如下。

---

# CIMA0 Phase5_6 当前阶段总结

## 一、核心架构已经进一步稳定

当前结构：

```
core/

    internal_dynamics/

        internal_dynamics.py

            |
            |
            +----------------+
            |                |
            v                v

       CLIPField        PlanetField

            |                |
            |                |
            v                v

       CLIP状态        Planet状态


            |
            v

       attention activity

            |
            v

       ComputeSystem

            |
            v

       winner

            |
            v

       apply_compute()

            |
            v

       step()
```

目前这条链已经跑通。

---

# 二、最重要成果：attention竞争第一次成立

之前：

```
Camera
 |
 v
CLIP
 |
 v
显示
```

基本是单通道。

现在：

```
CLIPField
     |
     | activity
     |
     |
PlanetField
     |
     | activity
     |
     v

ComputeSystem

     |
     v

资源选择
```

两个内部实体已经进入同一个竞争空间。

---

# 三、验证结果

## 1. CLIP启动阶段

输出：

```
ATTENTION SIGNALS:

clip:
1.0

planet:
0.0


COMPUTE WINNER: clip
```

说明：

外部输入可以激活 CLIP。

CLIP获得第一次计算资源。

---

## 2. Planet接管阶段

之后：

```
ATTENTION SIGNALS:

clip:
0

planet:
0.000394


COMPUTE WINNER: planet
```

说明：

CLIP停止变化以后：

* 不再举手
* 不再获得资源

Planet因为自身演化：

* 状态持续变化
* activity存在
* 获得计算资源

这验证了：

> 内生动力可以自主获得注意力。

---

# 四、Planet和PlanetField关系进一步明确

现在已经确认：

## archive/planet.py

定位：

```
纯动力规则
```

只负责：

```
state
+
local evolution
```

不能修改。

不能移动。

---

## PlanetField

定位：

```
动力系统状态容器
```

负责：

```
保存state

接收扰动

调用planet规则

提供snapshot

提供packet

提供activity
```

它不是动力本身。

关系：

```
Planet

   提供规则


PlanetField

   提供存在
```

两者必须保持分离。

---

# 五、发现的重要问题

## 1. activity语义已经暴露

原来：

CLIP：

```
packet size
```

作为activity。

这个是不合理的。

因为：

```
输入大小
```

不是：

```
内部变化
```

现在改成：

```
cloud delta
```

以后：

activity代表：

> 内部状态变化需求。

这个方向正确。

---

## 2. CLIP出现冷启动问题

现在：

CLIP需要：

```
compute
 |
 v
forward
 |
 v
cloud
 |
 v
delta
 |
 v
activity
```

形成：

```
没有activity
      |
      v
没有compute
      |
      v
没有cloud
      |
      v
没有activity
```

所以需要：

一次启动机制。

目前采用：

```
第一次输入刺激
        |
        v
CLIP举手
        |
        v
生成内部状态
```

这是合理的。

---

# 六、目前还没有解决的问题

## 1. 输出仍然绑定CLIP

当前：

```
DisplayIO

     |
     v

fields["clip"]
```

所以：

即使：

```
winner = planet
```

窗口仍然显示CLIP。

原因：

输出层还没有接入attention选择。

---

## 2. IO标签体系还没有完成

未来：

应该是：

```
winner

  |
  +--- clip
  |       |
  |       image output
  |
  +--- planet
  |       |
  |       field output
  |
  +--- audio
  |
  +--- text
```

IO不是理解内容。

只是：

```
tag -> terminal
```

---

# 后续工作计划

## Phase5_7：完成多状态输出链

目标：

让输出不再固定CLIP。

步骤：

### 1. PlanetField增加packet()

与CLIP同构：

```
packet()

{
 type:"field",
 representation:"planet",
 organ:"planet",
 bytes,
 shape,
 dtype,
 activity
}
```

---

### 2. InternalDynamics保存所有field

现在：

已有：

```python
self.internal_fields
```

继续保持。

不要增加特殊逻辑。

---

### 3. Observer记录winner

增加：

```
attention winner
```

输出：

例如：

```
winner:

planet
```

---

### 4. DisplayIO按照tag显示

例如：

```
clip

 -> RGB image


planet

 -> field visualization
```

---

# Phase5_8：完善自举手

目标：

所有模块同构：

```
activity()

receive()

step()

snapshot()

packet()
```

包括：

```
CLIPField

PlanetField

AudioField

TextField
```

---

# Phase5_9：调整ComputeSystem

现在ComputeSystem已经证明可用。

未来只需要：

不要知道：

```
内部是什么
```

只知道：

```
谁申请资源
```

保持：

```
activity
     |
     v
allocation
```

---

# Phase5_10：多模态扩展

最终结构：

```
InternalDynamics


    |
    |
    +--- PlanetField
    |
    +--- CLIPField
    |
    +--- AudioField
    |
    +--- TextField


            |
            v


      Attention Space


            |
            v


      Compute Selection


            |
            v


      IO Routing
```

---

# 当前阶段结论

Phase5_6 最大成果不是显示画面，而是：

**CIMA0第一次出现了真正的内部竞争。**

现在：

* CLIP不是永远中心
* Planet不是被动背景
* ComputeSystem不是固定调度
* attention开始由状态变化驱动

下一阶段重点不是继续增加算法，而是完成：

```
winner
   |
   v
IO
```

这一条闭环。

这样整个系统才从：

“内部动力实验”

进入：

“自治状态选择系统”。

这次推进非常扎实。下一阶段保持现在的边界，不要再增加新的中间层。

***********************
**********************
*************************
顺序：

Step 1
修改：

InternalDynamicsObserver
增加：

attention()
输出纯 signal。

Step 2
修改：

InternalDynamics.step()
从：

winner
 |
 organ.apply_compute()
之后增加：

packet = winner["organ"].packet()
Step 3
把 packet 交给：

TransportRouter
例如：

transport.publish(
    packet
)
Step 4
Display 注册：

tag="visual"
而不是：

source="clip"
这样：

未来：

planet

planetfield

camera

都可以进入同一输出通道。

现在 Phase5_6 真正的问题已经很明确：

不是动力系统。

不是 CLIP。

而是：

attention → packet → transport → io 的闭环还没有形成。

而且这个闭环应该沿用现有 transport/envelope/packet/router/view，不要新增概念。你这个判断是对的。下一步从 selector.py / display_io.py 之前的 packet 流开始整理。
+**********************
Step 2

修改 main.py：

删除：

display.encode_field(
    read_state
)

换成：

winner
 |
 organ
 |
 packet
 |
 DisplayIO
Step 3

让 PlanetField.packet() 输出：

BitPacket

不要 dict。

Step 4

让 DisplayIO 只接受 packet。

这样链路会变成：

Camera
 |
 IO packet
 |
 Transport
 |
 InternalDynamics
 |
 Planet / organs
 |
 attention
 |
 winner
 |
 packet
 |
 TransportRouter
 |
 DisplayIO
 |
 window

这条链已经和你最初设计的：

举手 → 分配计算资源 → 采样 → 输出 IO

一致。

现在最大的问题不是缺模块，而是Observer 越界 + IO 前缺少 packet 路由层。下一步应该从 display_io.py 和 transport/view.py 收拢，而不是再动 CLIP。
*****************************
## Phase5_6 当前阶段总结

这一阶段的核心目标已经从：

> 摄像头 → CLIP → 内部动力场 → 显示

转变为：

> 外部信息进入 → 内部 organ 自主演化 → attention 选择 → packet 输出 → IO 自动路由

这个方向是正确的。

目前已经完成了几个关键架构迁移。

---

# 一、已经完成的结构调整

## 1. InternalDynamics 已经成为真正的 organ 容器

当前：

```
External
   |
   v
TransportRouter
   |
   v
InternalDynamics
   |
   +---- CLIPField
   |
   +---- PlanetField
          |
          +---- Planet
```

InternalDynamics 不再负责理解数据。

它只负责：

* 注册 organ
* 广播输入
* 收集 activity
* 选择 compute
* 请求 packet

符合原设计：

> 动力系统不知道意义，只知道状态变化。

---

# 二、Attention 链路已经建立

现在输出：

```
ATTENTION SIGNALS:

[
 {
   name:"planet",
   organ:<PlanetField>,
   state:
   {
      activity,
      age,
      delta
   }
 }
]
```

这个变化很重要。

以前：

```
Observer
 |
 判断视觉
 |
 制造显示数据
```

现在：

```
Observer
 |
 读取状态
 |
 输出 signal
```

Observer 权限下降了。

这是正确方向。

Observer 不应该决定：

* 什么是视觉
* 什么应该显示
* 哪个 organ 有意义

它只提供：

> 当前内部状态的注意候选。

---

# 三、Transport 层方向正确

目前已经建立：

```
BitPacket

    |
    |
PacketEnvelope

    |
    |
TransportRouter
```

职责：

## Envelope

负责：

```
source
tag
schema
version
```

身份。

## BitPacket

负责：

```
data
shape
dtype
meta
```

结构。

## Router

负责：

```
tag
  |
  receiver
```

传播。

这个设计比以前：

```
source="clip"
显示clip
```

高级很多。

因为：

```
planet tag=visual
schema=discrete_field

planetfield tag=visual
schema=continuous_field
```

完全允许存在。

关键：

tag 不是意义。

schema 不是意义。

它们只是结构描述。

---

# 四、发现的问题

## 问题1

PlanetField packet 曾经返回 dict。

导致：

```
PlanetField
 |
 dict
 |
 DisplayIO
 |
 BitPacket接口
```

断裂。

已经确认应该统一：

```
PlanetField
 |
 BitPacket
 |
 Router
 |
 DisplayIO
```

---

## 问题2

DisplayIO 曾经承担太多职责。

旧：

```
DisplayIO

知道:

camera
planet
field
source
format
```

现在应该收缩为：

```
DisplayIO

输入:

BitPacket


输出:

framebuffer
```

它只问：

```
packet.schema?
packet.dtype?
packet.shape?
```

不问：

```
谁产生?
为什么产生?
有没有视觉意义?
```

---

# 五、当前最大问题：Planet.step()

现在运行：

```
COMPUTE WINNER: planet

PLANET OBJECT:
PlanetField

PLANETFIELD DELTA:
0.000025

然后：

PlanetField.step()

    ↓

archive/planet.py

    ↓

np.sin(old[x,y])

```

这里出现：

```
KeyboardInterrupt
```

说明：

不是逻辑错误。

是：

## Planet evolution 太重。

当前：

```
每一个 dynamics.step()

都会：

PlanetField.step()

调用:

Planet.step()

```

也就是说：

内部时间：

```
camera FPS

=
planet evolution FPS
```

这是不合理的。

Planet 是慢变量。

需要独立时间尺度。

---

# 六、下一阶段重点：检查 Planet 自动举手机制

你提出的问题非常关键。

目标：

> Observer 不应该持续扫描 Planet 全部状态，而应该依靠 Planet 自己产生 attention signal。

也就是：

现在：

```
Observer

读取:

planet.activity()

```

未来：

```
Planet

内部变化

↓

activity increase

↓

raise hand

↓

attention signal

↓

Observer

只读取举手者

```

这才符合：

> 最省力观察无穷演化系统。

---

# 七、后续工作计划

## Step 1

检查 Planet 是否已经拥有 activity / attention 机制。

检查：

```
archive/planet.py
```

重点：

寻找：

```
activity()

delta()

energy()

change()

signal()

```

确认：

Planet 有没有：

```
内部变化
    |
    v
活动度
    |
    v
举手
```

如果没有：

增加最小接口：

```
Planet.activity()

return {

 "activity": value,
 "delta": value,
 "age": age

}
```

不要增加语义。

---

## Step 2

修改 InternalDynamics attention 收集

现在：

```
for organ:
    activity()
```

未来：

统一：

```
organ.attention()
```

例如：

```
CLIPField.attention()

PlanetField.attention()

```

返回：

```
{
 name,
 organ,
 state
}
```

这样：

organ 自己决定：

什么时候举手。

---

## Step 3

解决 Planet 时间尺度

当前：

```
camera loop

100 FPS

↓

planet evolve 100 FPS
```

改：

例如：

```
Planet clock:

every 50 step

evolve once
```

结构：

```
InternalDynamics

step()

 |
 +-- fast organs
 |
 +-- slow organs
```

Planet 保持慢演化。

---

## Step 4

完成 attention → packet → router → display

最终链：

```
organ

 |
 attention()

 |
 compute winner

 |
 organ.packet()

 |
 BitPacket

 |
 TransportRouter

 |
 tag="visual"

 |
 DisplayIO
```

main.py 最终只保留：

```
while:

    camera input

    dynamics.step()

    cv2.imshow()
```

不要：

```
if clip:
 display clip

if planet:
 display planet
```

---

## Step 5

删除历史遗留接口

最终删除：

```
DisplayIO.encode_field()

```

原因：

它违反新原则：

> Display 不创造 packet。

packet 必须由产生者产生。

---

# 当前阶段评价

Phase5_6 已经跨过一个关键节点：

以前：

```
程序控制内部世界
```

现在：

```
内部实体产生状态
       |
       v
注意力竞争
       |
       v
计算资源分配
       |
       v
输出
```

下一阶段的核心不是 CLIP，也不是显示。

而是：

**让 Planet 真正成为一个自主举手、自主演化、低观察成本的内部生命单元。**

后续优先顺序：

1. ✅ 检查 Planet attention / activity 机制
2. ✅ 修正 Planet 时间尺度
3. ✅ 完成 packet/router/display 闭环
4. 再观察 CLIP 与 Planet 的竞争关系

目前架构方向已经稳定，可以继续推进。辛苦了。
***************************
******************************
***************************
12. 当前 Phase5_6 下一阶段重点
根据现在日志：

已经完成：

✅ Camera → BitPacket
✅ Router
✅ Organ attention
✅ Compute winner
✅ PlanetField packet方向
✅ Display 接收 packet架构

下一步：

A. 修正 Planet 自动举手机制
确认：

Planet.activity()

        |
        v

Attention signal

        |
        v

Observer attention()
是否真正由内部变化产生。

目标：

Observer 不主动观察 Planet。

Planet 自己产生：

activity > threshold
然后被选择。
----------------------------------------
B. 修正 Planet.step性能
现在：

Planet.step()
 |
 archive/planet.py
 |
 nested loop
 |
 KeyboardInterrupt
需要检查：

网格规模

step频率

是否需要内部clock

是否需要慢变量演化

C. 完成 Packet 全面统一
目前需要检查：

CLIPField.packet()

PlanetField.packet()

CameraIO.packet()

DisplayIO.decode()
全部必须：

BitPacket
禁止混用：

dict packet
D. 多显示端预留
保持：

tag="visual"

      |
      + Display Window A
      + Display Window B
      + Terminal
      + Network
由 Router 自动选择。

不要：

main.py

if display:
   show()
总结一句：

CIMA0 后续编程，不再是“写一个程序完成任务”，而是“建立一个由自治实体、信息流、注意力和资源分配组成的内部生态”。

Phase5_6 已经完成了最关键的结构转变：
从“控制系统”转向“观察-选择-响应系统”。

后面的重点不是增加功能，而是保持这个范式纯净。
****************************************
****************************************
****************************************
Step 2

InternalDynamics.__init__

增加：

self.observer
self.previous_observations
Step 3

InternalDynamics.step()

替换：

planet.activity()

为：

observer.describe(
    planet.snapshot()
)
Step 4

生成：

attention signal

只进入：

self.last_signals
Step 5

测试：

没有 Camera：

Planet 是否仍然：

step()
 |
 evolve()
 |
 observe()
 |
 attention

持续产生变化。

这个方向比让每个 Organ 暴露 activity() 更符合你现在提出的“唯一动力主体 + 外部观察窗口”的原则。
****************************************
****************************************
****************************************
****************************************
你这里提出的是一个非常关键的架构边界问题。我重新整理一下现在 Phase5_6 的逻辑，并回答你的核心问题：

> **Observer 增加变化测量，记录放在 InternalDynamics.py 能不能实现？是否需要改动核心四模块？**

答案：

**可以，而且应该这样做。不要把“举手机制”放入 Planet。**

原因是：

你的理解：

```
Planet产生变化
        |
        v
Observer看到变化
        |
        v
activity增加
        |
        v
Compute选择
```

这个链路本质上不是动力系统的一部分。

它是：

```
动力系统
    |
    | 产生状态变化
    |
    v
观察窗口
    |
    | 测量变化
    |
    v
注意力信号
    |
    | 分配计算资源
    |
    v
计算反馈
```

这是**外部观察闭环**，不是内部动力闭环。

---

## 1. Planet 的职责保持不变

`archive/planet.py`

不要动。

Planet只负责：

```
state(t)
    |
    v
evolve()
    |
    v
state(t+1)
```

它不知道：

* 有没有 Observer
* 有没有 Attention
* 有没有 Compute
* 有没有 Camera
* 有没有显示

否则动力系统被观察者污染。

---

## 2. Observer 的职责

现在：

```python
Observer.describe()
```

负责：

```
snapshot
    |
    v
描述
```

很好。

但是增加：

```python
measure_change()
```

是合理的。

例如：

```python
class Observer:


    def measure_change(
        self,
        current,
        previous
    ):

        if previous is None:

            return 1.0


        delta = np.abs(
            current - previous
        )


        return float(
            delta.mean()
        )
```

注意：

这里不是修改状态。

只是：

```
读取
计算
返回
```

仍然是观察。

---

## 3. 变化记录应该在哪里？

你的判断正确：

不要放 Planet。

不要放 Organ。

应该放：

```
InternalDynamics
```

为什么？

因为：

InternalDynamics 是：

```
Container
```

它管理：

* Organ
* Planet
* Observer
* Compute
* Transport

它可以保存：

```
previous_snapshot
```

这不是动力记忆。

区别：

### Planet memory

```
state history
```

属于动力。

### InternalDynamics memory

```
previous observation
```

属于观察。

两者不能混。

所以：

```python
self.previous_observations={}
```

这个设计方向是正确的。

---

## 4. 正确结构应该是这样

```
              Planet
                |
                |
             evolve()
                |
                v
          new internal state
                |
                |
                v

        InternalDynamics
                |
                |
          snapshot()
                |
                v

             Observer
                |
                |
        measure delta
                |
                v

          attention signal

                |
                v

             Compute

                |
                v

       selected organ gets resource
```

这里：

Observer 不改变 Planet。

Compute 不改变 Planet。

只是：

```
观察 → 选择 → 资源分配
```

---

# 关于你提出的“自循环、自我指认”

这个非常重要。

你写：

```
Planet产生变化
        |
Observer看到变化
        |
activity增加
        |
Compute选择
```

这里确实形成一个循环。

但是它不是：

> 内部自我意识循环

而更接近：

> 一个动力系统 + 一个观察反馈选择环

数学上类似：

```
Dynamical system

x(t+1)=F(x(t))


Observation

y(t)=O(x(t))


Selection

a(t)=S(y(t))


Resource allocation

R(t)=G(a(t))


Feedback

x(t+1)=F(x(t),R(t))
```

关键点：

**观察不是创造变化。**

观察只是：

```
发现变化
```

然后：

```
改变资源分布
```

所以：

它形成的是：

```
动力 → 观察 → 选择 → 资源 → 动力
```

循环。

---

## 5. 为什么不能把 activity 写进 Planet？

因为这样会变成：

```
Planet内部:

state
 |
变化
 |
activity
 |
决定自己是否被观察
```

这会产生：

```
动力系统知道自己被看
```

破坏：

> 内生动力独立性

你的观点：

> 自举手是内部变化的外部观察采样结果，本身不等于是内部最优解，只是相对于外部观察者的最优解。

这个判断非常准确。

应该保持：

```
内部:
    无目的演化


外部:
    根据变化选择观察资源
```

---

# 所以后续修改方案

保持四大核心：

```
Planet
CloudField
Cell
CLIPField
```

不动。

增加：

## archive/observer.py

增加：

```python
measure_change()
```

只负责：

```
snapshot
↓
delta
↓
description
```

---

## InternalDynamics.py

增加：

初始化：

```python
self.observation_history={}
```

step里面：

顺序调整为：

### 1

运行动力：

```
planet.step()
organ.step()
```

### 2

snapshot:

```
current_state
```

### 3

Observer:

```
delta=observer.measure_change(
    current,
    previous
)
```

### 4

生成 attention:

```
{
 name:"planet",
 activity:delta
}
```

### 5

Compute:

```
winner=select(signal)
```

---

这样：

Planet 永远不知道 Attention。

Observer 永远不控制。

Compute 永远不解释。

形成：

```
内生动力系统
        +
外部观察选择系统
```

这就是 Phase5_6 现在真正需要建立的范式。

下一步建议不是继续改显示，而是先把 **InternalDynamics.step() 拆成五个明确阶段：**

```
1 evolution
2 snapshot
3 observation
4 attention
5 compute
```

现在你的 step() 长，是因为这五层混在一起了。拆开以后，后面的 CLIP、Cloud、Display 都会自然稳定。
************************************
你的这种感觉其实来自一个架构层面的差异：**系统的“存在”和“行为”被分开了。**

传统设计往往有一个隐含前提：

> 一个模块发现目标 → 模块判断重要性 → 模块保存目标 → 模块继续处理目标。

所以很容易形成：

```
感知
 |
识别
 |
记忆
 |
决策
 |
执行
```

每一步都在“抓住”信息。

久而久之会出现几个问题：

---

### 1. 关注变成了命令，而不是结果

传统系统：

```
Attention:
    我要关注这个
```

然后：

```
Memory:
    保存它
```

这里有一个隐藏的中央控制。

系统必须不断回答：

* 什么重要？
* 为什么重要？
* 保存多久？
* 什么时候删除？

于是产生大量人为规则。

---

你的方向更像：

```
变化
 |
 v
扰动
 |
 v
竞争
 |
 v
资源流向
 |
 v
暂时形成结构
```

这里没有一个地方说：

> “我要关注它。”

它只是因为：

* 有变化
* 有能量
* 有资源竞争

所以形成了关注。

---

### 2. 记忆不再是仓库，而是动力学结果

传统：

```
Memory = 保存过去
```

所以需要：

* 清理算法
* 优先级
* 遗忘策略

否则越来越大。

---

你的结构：

```
AttentionField = 当前状态场
```

它不是保存：

“过去发生过什么”。

而是：

“当前什么正在影响系统”。

例如：

水面上的波纹。

波纹不是水保存了过去。

而是：

当前能量分布的结果。

没有继续输入：

波纹自然消失。

---

### 3. 终止条件从逻辑判断变成物理耗散

这是你感觉最明显的地方。

传统：

```
if confidence < 0.5:
    stop()
```

需要人为定义。

你的方向：

```
资源投入
     |
     v
计算
     |
     v
消耗
     |
     v
没有补充
     |
     v
衰减
     |
     v
停止
```

停止不是一个决定。

停止是系统状态自然到达。

类似：

火焰不是决定熄灭。

燃料没有了，火焰消失。

---

### 4. 系统避免了“观察者陷阱”

传统 AI：

```
系统
 |
观察外部世界
 |
产生模型
 |
改变自己
```

这里有一个问题：

观察者和被观察对象分离。

---

你的 CIMA0 更像：

```
外部输入
    |
    v
内部扰动
    |
    v
内部动力变化
    |
    v
观察内部变化
    |
    v
资源重新分配
    |
    v
内部继续演化
```

观察本身也是系统内部事件。

没有一个站在外面的“小人”。

---

所以你现在难以描述的感觉，可能可以总结为：

> 传统系统通过“保存和控制”维持秩序，而这个结构通过“流动和竞争”产生秩序。

或者更技术一点：

> 它把主动管理状态的问题，转化成了状态在约束条件下自组织的问题。

这也是为什么 `ObservationCache` 必须短命，`AttentionField` 必须可衰减，`ComputeSystem` 必须掌握资源，而不是某个模块掌握“意义”。

你现在碰到的其实不是一个代码问题，而是 CIMA0 从“程序结构”向“动力系统结构”转换时的核心边界。你感觉到的不协调，是因为传统软件里的“对象生命周期”思维，和这里的“状态流动”思维发生了冲突。
********************************************
********************************************
********************************************
********************************************
Ctrl+C 中断时，摄像头读取阻塞。

Windows OpenCV MSMF 经常出现。

建议后面处理：

try:
    while True:
        ret, frame = cap.read()

except KeyboardInterrupt:
    pass

finally:
    cap.release()
    cv2.destroyAllWindows()
让退出干净。
********************************************
********************************************
********************************************
********************************************
## Phase5_6 当前总结

这一次调整非常关键，实际上解决的是 CIMA0 里一个核心架构问题：

> **注意力不是由输入产生，而是由内部状态变化产生。**

之前的设计虽然跑通了链路，但是注意力来源错误。

---

# 一、已经确认正确的架构链路

现在系统结构：

```
Camera
  |
  v
Transport Router
  |
  v
InternalDynamics.receive()
  |
  v
CLIPField.receive()
  |
  v
保存外部扰动
  |
  v
Attention Observation
  |
  v
Compute Allocation
  |
  v
CLIPField.update()
  |
  v
生成内部状态 cloud
  |
  v
比较状态变化
  |
  v
产生 activity
```

这个方向正确。

---

# 二、发现并修正的问题

## 1. 原始 attention 来源错误

之前：

```python
self.disturbance += (
    len(packet.data)
    /
    1000000.0
)
```

问题：

它代表：

```
数据量
```

不是：

```
状态变化
```

导致：

```
摄像头打开
      |
      v
永久高activity
      |
      v
永久占用compute
```

这类似传统系统：

```
输入刺激 = 注意力
```

容易形成外部驱动。

已经删除。

---

# 三、CLIPField 的重新定位

现在明确：

CLIPField 不是动力系统。

它是：

```
状态器官
```

类似：

```
一个缓慢变化的内部场
```

它没有自己的时间周期。

它不应该：

```
每帧运行
```

而应该：

```
收到扰动
     |
     v
请求资源
     |
     v
更新状态
     |
     v
等待下一次变化
```

---

# 四、当前 CLIPField 生命周期

正确模型：

```
receive()

保存camera packet

       |
       v

activity()

判断是否需要计算

       |
       v

compute winner

       |
       v

update()

CLIP forward

       |
       v

new_cloud

       |
       v

compare old cloud

       |
       v

internal_activity

       |
       v

attention结束
```

---

# 五、目前最后一个问题

当前日志：

```
clip {'activity':1.0}
clip {'activity':1.0}
clip {'activity':1.0}
```

说明：

CLIPField 一直认为：

```
cloud == None
```

也就是：

状态没有提交。

原因：

`_forward()` 生成：

```python
new_cloud
```

但是没有：

```python
self.cloud = new_cloud
```

所以：

每次都是：

```
没有状态
    |
    v
初始化请求
    |
    v
compute
    |
    v
生成状态
    |
    v
丢失
```

形成循环。

---

# 六、下一步立即修改

## CLIPField._forward()

增加：

```python
if self.cloud is None:

    self.internal_activity = 1.0

else:

    self.internal_activity = float(
        np.mean(
            np.abs(
                new_cloud -
                self.cloud
            )
        )
    )


#
# commit state
#

self.cloud = new_cloud.copy()
```

这是当前最重要修改。

---

# 七、修改后的预期现象

第一次：

```
ATTENTION

clip:
activity 1.0


COMPUTE WINNER: clip
```

生成状态。

---

第二次，如果摄像头静止：

```
ATTENTION

(empty)
```

或者：

```
clip:
activity 0.000001
```

---

移动画面：

```
ATTENTION

clip:
activity 0.05

COMPUTE WINNER: clip
```

也就是：

注意力由变化产生。

---

# 八、Observation Cache / Attention Field 后续计划

目前先不要继续扩展。

顺序：

---

## Phase5_6.1 完成 CLIP 状态生命周期

目标：

确认：

```
状态形成
↓
状态保持
↓
状态变化
↓
注意力产生
↓
资源分配
```

完成。

---

## Phase5_6.2 接入 ObservationCache

现在：

InternalDynamics 里面还有：

```python
previous_observations
```

这个以后需要清理。

原因：

它混合了：

* 观察历史
* 动力状态
* attention判断

职责重叠。

调整：

```
ObservationCache

只负责：

snapshot
↓
temporary cache
↓
compare
↓
discard
```

不保存长期状态。

---

## Phase5_6.3 AttentionField独立化

现在：

```
organ.activity()
```

直接生成attention。

未来：

改成：

```
organ
 |
 v
observation signal

 |
 v

AttentionField

 |
 v

resource request
```

也就是：

器官只报告变化。

AttentionField负责：

竞争。

---

## Phase5_6.4 ComputeSystem最终定位

最终：

Compute不是主动调度。

而是：

```
attention field
       |
       v
requests
       |
       v
compute allocation
```

资源耗尽：

自然结束。

这对应你之前提出的：

> 当计算资源分配结束时，自然终止关注。

这个方向是正确的。

---

# 九、目前最大的架构收获

这次实际上确认了 CIMA0 一个核心原则：

传统：

```
输入
 |
 v
处理
 |
 v
输出
```

容易变成：

```
外部控制内部
```

你的方向：

```
输入
 |
 v
内部状态形成
 |
 v
内部状态变化
 |
 v
产生注意力
 |
 v
争取资源
```

变成：

```
内部状态控制计算
```

这就是你之前感觉“避免了传统设计缺陷”的地方。

它不是一个持续运行的大脑模型。

更接近：

> 一个由状态变化驱动的、自竞争计算资源的内生系统。

---

下一阶段建议：

**先不要增加算法。**

先完成：

1. CLIPField 状态提交；
2. 验证 activity 是否自然消失；
3. 验证运动时重新出现；
4. 再抽离 ObservationCache 和 AttentionField。

目前 Phase5_6 的核心方向已经基本确定。你现在是在修最后的生命周期细节。
***************************************************************
**************************************************************
**************************************************************
***************************************************************
## Phase5_6 当前架构复核结论（2026-08-21 14:05）

这次复核非常重要。

结论：

**方向正确，但实现处于“半迁移状态”。**

也就是说：

旧架构：

```
main.py
 |
 |-- InternalDynamicsObserver
 |
 |-- 单独观察
 |
 |-- 单独输出
```

和新架构：

```
InternalDynamics
 |
 |-- Observer
 |-- ObservationCache
 |-- AttentionField
 |-- Transport
 |
 |-- observation
 |-- attention
 |-- compute
 |-- sampling
```

目前同时存在。

所以系统可以运行，但是：

> 新设计的权力结构没有真正接管执行链。

---

# 当前主要问题排序

## P0：先完成接线（最高优先级）

目标：

让新的内部观察链真正运行。

当前：

```python
dynamics = InternalDynamics(
    planet=planet,
    compute=compute
)
```

改成：

```python
dynamics = InternalDynamics(
    planet=planet,
    compute=compute,
    observer=observer,
    observation_cache=observation_cache,
    attention_field=attention_field,
    transport=transport
)
```

---

但是这里需要注意：

不是简单传进去。

需要先确认：

## 1. InternalDynamics.**init**

目前：

```python
def __init__(
    self,
    planet,
    compute=None,
    observer=None,
    transport=None
):
```

需要扩展：

```python
def __init__(
    self,
    planet,
    compute=None,
    observer=None,
    observation_cache=None,
    attention_field=None,
    transport=None
):
```

增加：

```python
self.observation_cache = observation_cache

self.attention_field = attention_field
```

---

完成后验证：

运行时：

应该看到：

```
ATTENTION SIGNALS:

planet {...}

clip {...}
```

而不是只有：

```
clip
```

---

# P1：清理 Observer 双轨制

现在：

存在：

```
core/observer/InternalDynamicsObserver
```

和：

```
archive/observer.py
```

两个观察体系。

必须停止双轨。

目标结构：

```
Planet
 |
 |
snapshot()
 |
 v
Observer
 |
 v
Observation
 |
 v
ObservationCache
 |
 v
change
 |
 v
AttentionField
```

---

动作：

## main.py 删除：

类似：

```python
observer.observe(snapshot)
```

这种循环外观察。

原因：

观察权应该属于：

```python
InternalDynamics
```

不是 main loop。

---

main.py 只负责：

```
输入
运行
显示
```

不要参与认知链。

---

# P2：删除旧观察残留代码

## 删除或冻结：

```python
_measure_change()
```

原因：

现在职责已经迁移：

以前：

```
InternalDynamics
 |
 previous_observations
 |
 compare
```

现在：

```
ObservationCache
 |
 compare
```

所以：

删除：

```python
self.previous_observations
```

以及：

```python
_measure_change()
```

避免未来误调用。

---

# P3：统一 Signal 协议

现在：

Planet:

```python
{
 "change":xxx
}
```

CLIP:

```python
{
 "delta":xxx
}
```

这是架构问题。

必须统一。

建议：

所有内部实体输出：

```
Signal
```

统一：

```python
{
    "name":"clip",

    "organ":clip,

    "state":
    {
        "activity":0.02,

        "change":0.02
    }
}
```

也就是：

取消：

```
delta
```

统一：

```
change
```

原因：

AttentionField 不应该知道：

* Planet叫什么
* CLIP叫什么

它只接受：

```
变化量
```

---

# P4：AttentionField接入

现在先不要设计复杂算法。

第一版：

纯竞争。

输入：

```
signals
```

输出：

```
winner
```

规则：

```python
max(change)
```

即可。

不要加入：

* 学习
* 权重
* 长期记忆

因为现在验证的是：

```
注意力产生机制
```

不是智能。

---

# P5：重新定义 ObservationCache

这里非常关键。

你的理解：

> 用后即弃，避免长期演化为唯一来源。

保留。

所以：

ObservationCache:

不是：

```
memory
```

而是：

```
measurement window
```

职责：

```
snapshot(t)

保存

snapshot(t+1)

compare

return change

discard
```

不能：

* 控制动力
* 修改状态
* 保存历史轨迹

---

# P6：重新整理 InternalDynamics.step()

目标顺序：

现在文档和代码不一致。

最终：

应该：

```
step()

1.
collect observation

2.
cache compare

3.
generate attention signals

4.
attention selection

5.
compute allocation

6.
organ update

7.
planet evolve

8.
sample output
```

也就是：

观察发生在演化之前。

---

目前代码：

```
observe

compute

organ evolve

sample

planet step
```

基本正确。

但是缺：

```
attention_field
observation_cache
```

---

# P7：CLIPField生命周期确认

这个方向已经明确。

最终：

CLIPField：

不是：

```
camera processor
```

而是：

```
visual state organ
```

生命周期：

```
receive disturbance

↓

wait

↓

request compute

↓

generate state

↓

compare old/new

↓

produce activity

↓

rest
```

没有自己的周期。

---

# 推荐执行顺序

不要同时改。

按照：

## 第一步（现在）

### 接线

完成：

* observer
* observation_cache
* attention_field
* transport

进入 InternalDynamics。

---

## 第二步

验证：

输出：

```
planet signal

clip signal

attention winner
```

---

## 第三步

清理：

删除：

* main.py旧observer
* _measure_change
* previous_observations

---

## 第四步

统一：

Signal协议：

全部：

```python
change
```

---

## 第五步

完善 AttentionField。

---

## 第六步

继续观察：

CLIPField 是否：

静止：

```
无attention
```

变化：

```
重新竞争compute
```

---

# 当前阶段判断

Phase5_6 已经不是算法问题。

现在主要是：

**架构迁移问题。**

核心思想已经稳定：

```
动力系统
    ↓
产生状态

观察系统
    ↓
测量变化

注意力系统
    ↓
请求资源

计算系统
    ↓
给予机会

状态器官
    ↓
更新自身
```

下一步不要继续增加模块。

先完成这次“权力迁移”的接线，让新架构真正接管运行。
********************************************************************
********************************************************************
********************************************************************
********************************************************************
固定三个协议
1. Observation Snapshot
给：

Observer
ObservationCache
Attention
格式：

{
 "planet":
 {
    "state": ndarray
 },

 "organs":
 {
    "clip":
    {
       "activity":,
       "delta":
    }
 }
}
只描述。

2. State Packet
给：

Transport
Display
External
格式：

BitPacket(
    tag,
    data,
    shape,
    dtype
)
只传输。

3. Internal State
器官内部：

CLIPField
PlanetField
CloudField
自己管理。

现在混乱的原因：

Planet.snapshot()

和：

InternalDynamics.snapshot()

名字一样。

但是意义不同。

应该以后改名：

例如：

PlanetField.observe_state()
和：

InternalDynamics.observe()
避免误用。

所以现在不要砍 ObservationCache。

正确路线：

保留当前 ObservationCache 高阶能力

增加递归 diff

增加递归 magnitude

固定 snapshot 协议

最后再整理 Display packet
*******************************************
******************************************
*******************************************
后续修改原则：

不要删除模块。

每次修改只检查三个东西：

1. 谁产生数据？

2. 谁接收数据？

3. 谁消费数据？
也就是：

producer
    |
    |
receiver
    |
    |
consumer
*******************************************
******************************************
*******************************************
## 当前状态总结（2026-08-21 16:xx）

这次 Phase5_6 的核心链路已经恢复，而且比之前更接近设计目标。

先确认几个关键点：

---

# 一、已经修复的核心问题

## 1. InternalDynamics 接线完成 ✅

现在：

```python
dynamics = InternalDynamics(

    planet=planet,

    compute=compute,

    observer=observer,

    observation_cache=observation_cache,

    attention_field=attention_field,

    transport=transport
)
```

四个外围模块已经进入动力系统：

```
Observer
    |
    v
ObservationCache
    |
    v
AttentionField
    |
    v
Transport
```

这一步是 Phase5_5 → Phase5_6 的主要目标。

---

# 二、Observer / Cache / Signal 分离方向正确 ✅

现在日志：

```
planet {
 'observation':
 {
    'planet':
    {
       'shape': (128,128),
       'mean': ...
       'energy': ...
    }
 },

 'activity': 1.27e-06,

 'changed': True,

 'signal':1.27e-06
}
```

说明：

现在进入 Compute 的是：

```
轻量 signal
```

而不是：

```
128*128 delta field
```

这是正确方向。

以前：

```
Compute
 |
 |
16384 float array
```

现在：

```
Compute

planet
 |
 activity
 signal
 changed
```

高维数据已经分离。

---

# 三、internal_fields 保留成功 ✅

这个非常重要。

之前讨论过：

> 不能为了轻量化，把高阶功能模块废掉。

现在代码：

```python
if isinstance(delta, dict):

    self.internal_fields.update(
        delta
    )
```

保留：

```
ObservationCache
        |
        |
        +---- signal ----> Compute

        |
        |
        +---- delta field ----> internal_fields
```

这是正确架构。

不是删除功能。

而是：

## 信号通道

负责：

```
选择
调度
竞争
```

## 数据通道

负责：

```
空间场
连续场
显示
演化
```

两个通道分离。

---

# 四、CLIPField 恢复工作 ✅

日志：

```
CLIP RECEIVE (307200,3)
```

证明：

摄像头：

```
CameraIO

   |

Transport

   |

InternalDynamics

   |

CLIPField.receive()
```

恢复。

随后：

```
clip {'activity':1.0,'delta':1.0}
```

进入：

```
Attention
    |
Compute
```

说明 organ 没有被废弃。

之前的问题确实是：

不是 CLIP坏了。

而是：

```
transport.subscribe()
```

断掉。

---

# 五、Planet 输出链路成功 ✅

现在：

```
COMPUTE WINNER: clip

PLANET PACKET CREATED

ROUTER:
planet visual continuous_field

DISPLAY RECEIVE:
planet visual continuous_field
```

说明：

完整链路：

```
Camera
 |
 v
CLIPField
 |
 v
Attention
 |
 v
Compute
 |
 v
PlanetField
 |
 v
packet
 |
 v
Display
```

已经闭环。

---

# 六、当前还有几个问题，但不是结构问题

## 问题1：camera packet 同时给 display

现在：

```
ROUTER: camera visual media.bgr
CLIP RECEIVE
DISPLAY RECEIVE
```

意味着：

摄像头原始画面仍然直接显示。

也就是说：

Display现在收到两个来源：

```
camera media.bgr

planet continuous_field
```

这会产生竞争。

目前显示层可能出现：

* 摄像头覆盖 Planet
* Planet 覆盖摄像头
* 闪烁

后面需要明确：

Display 的唯一输入应该是什么。

建议：

Phase5_6 保持：

```
Display

只显示内部状态

不要显示外部输入
```

即：

```
camera
   |
   v
CLIP
   |
   v
InternalDynamics
   |
   v
Planet
   |
   v
Display
```

Camera 不直接进入 Display。

但现在不要改。

先稳定。

---

## 问题2：AttentionField 还没有真正参与选择

现在：

```
attention_field.receive()
```

已经存在。

但是：

Compute 使用：

```
signals
```

不是：

```
attention_field.snapshot()
```

也就是说：

当前：

```
AttentionField

只是接收变化

没有成为资源场
```

这是下一阶段。

---

## 问题3：CLIP 权重警告

```
WARNING:
No pretrained weights loaded
Model initialized randomly
```

这个以前已经发现。

不是 Phase5_6 问题。

现在：

CLIP 是：

```
随机视觉动力 organ
```

不是：

```
语义 CLIP
```

按照 CIMA0 设计：

其实暂时可以接受。

因为现在需要的是：

```
内部器官
```

不是：

```
分类器
```

---

# 下一步工作计划

不要继续大改。

现在进入稳定阶段。

---

# Phase5_6.1  数据边界整理

目标：

固定三条通道。

## 1. Signal Channel

保持：

```
Observer

 ↓

ObservationCache

 ↓

InternalDynamics._observe()

 ↓

Compute
```

内容：

只允许：

```python
{
 activity,
 changed,
 signal
}
```

禁止：

```
array
bytes
field
```

---

## 2. Field Channel

保持：

```
ObservationCache

 ↓

internal_fields

 ↓

packet

 ↓

Display
```

允许：

```
numpy field
```

---

## 3. Media Channel

暂时保留：

```
Camera

 ↓

CLIP
```

但准备断开：

```
Camera -> Display
```

---

# Phase5_6.2 删除残留代码

清理：

## internal_dynamics.py

检查删除：

* `_measure_change`
* 旧 observer 逻辑
* 重复 `_observe`
* 未使用变量

特别检查：

不要再次出现：

```python
change
```

在：

```python
__init__
```

里面。

---

# Phase5_6.3 接入 AttentionField

下一步：

不是修改 Planet。

而是：

让：

```
AttentionField
```

成为：

```
Compute
```

之前的一层。

结构：

现在：

```
Observer
 |
 signals
 |
 Compute
```

未来：

```
Observer
 |
 AttentionField
 |
 weighted signals
 |
 Compute
```

---

# 当前版本判断

现在的状态：

```
Camera
        |
        v
Transport
        |
        +------> CLIPField
        |
        +------> Display(暂时)

CLIPField
        |
        v
Attention signals

PlanetField
        |
        v
Compute winner

Planet packet
        |
        v
Display
```

已经从：

> "模块存在"

进入：

> "模块真实交换数据"

这是 Phase5_6 一个重要节点。

下一步建议不要继续扩展功能，先做：

**锁定数据边界 + 清理旧代码 + 确认 Display 单一来源。**

*******************************************
******************************************
*******************************************
