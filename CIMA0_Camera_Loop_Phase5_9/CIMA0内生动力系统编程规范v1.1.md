根据前面 Phase5_6 的重构过程，我们实际上已经逐渐形成了一套不同于传统“功能堆叠式”的编程方式。核心变化是：

**程序不再围绕任务执行，而围绕“自主存在的内部实体 + 信息流 + 注意力选择 + 最小干预”组织。**

因此后续 CIMA0 编程规范需要从传统软件工程规范，转向“内生动力系统编程范式”。

下面整理一版后续开发规则。

---

# CIMA0 内生动力系统编程规范 v1.0

## 0. 总原则

### 第一原则：实体自治

任何内部实体（Organ）必须：

* 拥有自己的状态
* 拥有自己的演化规则
* 拥有自己的输出方式

外部模块：

* 不修改实体内部状态
* 不解释实体意义
* 不替实体决策

即：

```
Organ

  state
    |
    v
 internal evolution
    |
    v
 packet output
```

而不是：

```
Controller
    |
    v
 modify Organ
```

---

# 1. 模块职责原则

每个模块只有一个核心职责。

禁止：

一个模块同时负责：

* 数据解释
* 状态修改
* 决策
* 显示
* 优化

---

## 1.1 Organ

例如：

```
PlanetField
CLIPField
CloudField
Cell
```

职责：

拥有内部动力。

允许：

```
receive()
step()
activity()
packet()
snapshot()
```

禁止：

```
display()
select()
route()
interpret()
```

Organ 不知道：

* 谁观察它
* 谁显示它
* 为什么选择它

---

# 2. Information Packet 原则

所有信息必须封装为 Packet。

禁止：

模块之间直接传递：

```
dict
numpy array
raw bytes
```

必须：

```
BitPacket
    |
    + Envelope
    |
    + Payload
```

结构：

```
Packet

Identity
    |
    + source
    + tag
    + schema


Structure
    |
    + shape
    + dtype


Data
    |
    + bytes
```

---

## Packet 规则

Packet 只描述：

“它是什么结构”

不描述：

“它是什么意思”

例如：

正确：

```
source="planet"

tag="visual"

schema="continuous_field"
```

错误：

```
this_is_a_planet_picture=True
```

---

# 3. Envelope 原则

Envelope 是不可删除的信息身份层。

```
Packet

      Envelope
          |
          + source
          + tag
          + schema


      Data
```

任何转换：

```
Packet
 |
 View
 |
 PacketView
```

必须保留：

```
source
tag
schema
```

---

# 4. Router 原则

Router 只负责运输。

例如：

```
Camera

 |
 BitPacket

 |
 TransportRouter

 |
 CLIP
Planet
Display
```

Router：

知道：

```
tag
```

不知道：

```
内容意义
```

禁止：

```
if packet.source=="planet":
    do something
```

允许：

```
if packet.tag=="visual":
    send()
```

---

# 5. Observer 原则

Observer 是只读观察者。

禁止：

Observer：

* 修改状态
* 生成新状态
* 解释意义

Observer 只能：

```
snapshot

    |
    v

observe

    |
    v

attention
```

---

## Attention 原则

Attention 是资源分配机制。

不是：

识别。

不是：

理解。

不是：

分类。

输入：

```
signal list
```

例如：

```
[
 {
 name:"planet",
 organ:PlanetField,
 state:
 {
   activity,
   age,
   delta
 }
 }
]
```

输出：

```
winner signal
```

保持同构。

---

# 6. Compute 原则

Compute 不创造动力。

Compute 只是：

提供有限资源。

流程：

```
attention

   |
   v

winner

   |
   v

compute allocation

   |
   v

organ.apply_compute()
```

禁止：

Compute：

* 修改规则
* 优化目标
* 学习参数

---

# 7. DisplayIO 原则

Display 是 IO 端口。

Display 不理解：

* planet
* clip
* camera

只接受：

```
Packet
```

流程：

```
Organ

 |
 packet

 |
 Router

 |
 DisplayIO

 |
 framebuffer
```

禁止：

旧方式：

```
display.encode_field(
    planet_state
)
```

因为：

Display 侵入内部结构。

---

# 8. 同构原则（非常重要）

输入输出保持结构对应。

例如：

输入：

```
camera

tag=visual

schema=media.bgr
```

输出：

```
planet

tag=visual

schema=continuous_field
```

它们都是：

```
visual information
```

但：

状态不同。

不要提前假设：

```
visual = image
```

正确：

```
visual
 |
 + media
 |
 + discrete_field
 |
 + continuous_field
```

---

# 9. 三层分离原则

CIMA0 后续严格保持：

## IO层

负责：

信息进入/出去

```
camera
display
network
```

---

## Dynamics层

负责：

内部演化

```
Planet
Cloud
CLIP
Cell
```

---

## Observation层

负责：

读取和选择

```
Observer
Attention
Sampling
```

三层不能互相穿透。

---

# 10. 禁止事项

以后代码审查优先检查：

---

## 禁止1

外部修改 Organ

错误：

```python
planet.state += x
```

正确：

```python
planet.receive(packet)
```

---

## 禁止2

Display读取内部变量

错误：

```python
display.show(planet.state)
```

正确：

```python
display.receive(packet)
```

---

## 禁止3

Observer生成视觉数据

错误：

```python
observer.create_image()
```

正确：

```
observer.select(packet source)
```

---

## 禁止4

隐藏异常

禁止：

```python
except:
    return None
```

必须：

```python
except Exception as e:
    log(e)
```

否则会产生：

“系统没有错误，但是没有结果”

---

# 11. 新开发流程

以后增加任何模块：

第一步：

定义它是什么实体。

例如：

```
NewOrgan
```

回答：

```
它自己的状态是什么？
它如何演化？
它输出什么packet？
```

第二步：

定义 Packet：

```
source
tag
schema
shape
dtype
```

第三步：

接入 Router。

第四步：

加入 Attention。

第五步：

加入 Display 或其他 IO。

---

# 12. 当前 Phase5_6 下一阶段重点

根据现在日志：

已经完成：

✅ Camera → BitPacket
✅ Router
✅ Organ attention
✅ Compute winner
✅ PlanetField packet方向
✅ Display 接收 packet架构

下一步：

## A. 修正 Planet 自动举手机制

确认：

```
Planet.activity()

        |
        v

Attention signal

        |
        v

Observer attention()
```

是否真正由内部变化产生。

目标：

Observer 不主动观察 Planet。

Planet 自己产生：

```
activity > threshold
```

然后被选择。

---

## B. 修正 Planet.step性能

现在：

```
Planet.step()
 |
 archive/planet.py
 |
 nested loop
 |
 KeyboardInterrupt
```

需要检查：

* 网格规模
* step频率
* 是否需要内部clock
* 是否需要慢变量演化

---

## C. 完成 Packet 全面统一

目前需要检查：

```
CLIPField.packet()

PlanetField.packet()

CameraIO.packet()

DisplayIO.decode()
```

全部必须：

```
BitPacket
```

禁止混用：

```
dict packet
```

---

## D. 多显示端预留

保持：

```
tag="visual"

      |
      + Display Window A
      + Display Window B
      + Terminal
      + Network
```

由 Router 自动选择。

不要：

```
main.py

if display:
   show()
```

---

总结一句：

> CIMA0 后续编程，不再是“写一个程序完成任务”，而是“建立一个由自治实体、信息流、注意力和资源分配组成的内部生态”。

Phase5_6 已经完成了最关键的结构转变：
从“控制系统”转向“观察-选择-响应系统”。

后面的重点不是增加功能，而是保持这个范式纯净。
******************************************
*********************************************


*******************************************
*****************************************
你的这几个修正非常关键。前面那版规范仍然带有传统软件“模块自治”的影子，把 **Organ 当成独立动力主体**，这和我们在 Phase5_6 逐渐形成的理解并不完全一致。

现在需要重新调整抽象层级。

核心变化：

> **只有一个内部动力系统（Internal Dynamics）。Organ 不是动力系统，而是内部动力系统中的局部状态观察单元。**

这会解决几个混淆点。

---

# CIMA0 编程范式修正版 v1.1

## 0. 顶层结构

不是：

```
Organ1
  |
  自己动力

Organ2
  |
  自己动力

Organ3
  |
  自己动力
```

而是：

```
                 Internal Dynamics
                       |
        --------------------------------
        |              |              |
    PlanetField    CLIPField     CloudField
        |
    局部状态
```

整个系统：

只有一个内部动力规则。

---

# 1. Internal Dynamics（唯一动力主体）

职责：

拥有：

* 内部时间
* 状态演化
* 动力规则
* 状态转移

它保证：

```
不死
不崩
不重复
持续运动
```

即：

```
Internal State(t)

       |
       v

Dynamics Rule

       |
       v

Internal State(t+1)
```

---

内部动力系统不负责：

* 显示
* 观察
* 选择
* 解释

---

# 2. Organ 定义修正

## Organ 不是动力主体

更准确：

> Organ 是 Internal Dynamics 内部的局部状态区域 / 局部观察接口。

例如：

---

## PlanetField

不是：

“一个有自己动力的 Planet”

而是：

```
Internal Dynamics

      |
      |
      +---- PlanetField

             保存：

             planet局部状态
```

---

## CLIPField

不是：

“CLIP自己演化”

而是：

```
Internal Dynamics

      |
      |
      +---- CLIPField

             保存：

             视觉输入形成的局部内部状态
```

---

## CloudField

不是：

“云有动力”

而是：

```
Internal Dynamics

      |
      |
      +---- CloudField

             保存：

             稀疏状态结构
```

---

所以 Organ 的统一职责：

```
拥有局部内部状态

提供：

receive()
activity()
snapshot()
packet()
```

---

不负责：

```
最终解释
最终选择
最终输出意义
```

---

# 3. Attention 和 Compute 边界重新定义

之前混淆原因：

把 attention 看成“选择器”。

实际上：

Attention 不是选择。

Attention 是：

## 状态显著性报告

流程：

```
Organ

  |
  |
 activity()

  |
  v

Signal

{
 name,
 organ,
 state
}

```

它只是回答：

> “哪些局部状态目前变化明显？”

---

例如：

```
Planet:

activity=0.0001


CLIP:

activity=0.8
```

Attention:

报告：

```
CLIP 当前变化大
```

但是：

Attention 不决定：

“我要处理CLIP”。

---

# 4. Compute 的真正职责

Compute 是：

## 有限内部资源分配器

流程：

```
Attention

   |
   v

candidate signals


   |
   v


Compute

   |
   v

给某个局部状态一次演化机会

```

所以：

Attention:

发现变化。

Compute:

分配资源。

区别：

|      | Attention | Compute |
| ---- | --------- | ------- |
| 输入   | 状态信号      | 候选列表    |
| 作用   | 测量显著性     | 分配资源    |
| 修改状态 | 否         | 否       |
| 提供资源 | 否         | 是       |
| 产生动力 | 否         | 否       |

---

所以：

```
Attention ≠ Controller

Compute ≠ Brain

```

它们都是：

内部动力系统的辅助机制。

---

# 5. Observer重新定义

之前：

> Observer 不生成视觉数据

这个还不够准确。

更准确：

> Observer 不知道终端意义。

Observer做：

```
Internal Dynamics

        |
        v

Snapshot

        |
        v

Observer

        |
        v

selected packet

```

它只知道：

* 状态
* 变化
* 标签

不知道：

```
visual是什么意思
image是什么意思
planet是什么意思
```

---

例如：

收到：

```
tag="visual"

schema="continuous_field"

source="planet"
```

Observer：

不应该认为：

“这是图像”。

它只是：

```
选择一个信息流
```

---

# 6. Terminal / Display 修正

之前：

Display负责显示。

更准确：

Display只是：

## 信息终端

它不拥有意义。

流程：

```
Packet

   |
   v

Terminal

   |
   v

human perception
```

意义产生在：

观察者。

所以：

```
Display:

不知道：

这是地图
这是星球
这是视觉

```

它只知道：

```
packet结构
```

---

# 7. 新职责层级

```
                 Internal Dynamics
                       |
                       |
                 (唯一动力)
                       |
        --------------------------------
        |
        |
      Organ
        |
        |
    局部状态接口


        |
        v


     Attention

     状态显著性


        |
        v


     Compute

     资源分配



        |
        v


     Observer

     选择观察对象



        |
        v


      Router

      信息运输



        |
        v


     Terminal

     外部接口

```

---

# 8. 新版禁止事项

## 禁止1

Organ拥有独立动力规则

错误：

```
PlanetField.step()
自己定义宇宙规则
```

正确：

```
PlanetField

提供局部状态

InternalDynamics

推动演化
```

---

## 禁止2

Attention控制系统

错误：

```
Attention:
执行某个动作
```

正确：

```
Attention:
报告状态
```

---

## 禁止3

Observer解释意义

错误：

```
if tag=="visual":
    create_image()
```

正确：

```
Observer:

返回packet引用
```

---

## 禁止4

Terminal解释意义

错误：

```
planet packet -> planet image
```

正确：

```
packet -> framebuffer
```

---

# 对当前 Phase5_6 的影响

这意味着后续代码检查重点变成：

### 1.

确认：

```
PlanetField.step()
```

是不是实际上绕过了 InternalDynamics。

现在日志：

```
InternalDynamics.step()

      |
      v

PlanetField.step()

      |
      v

archive/planet.step()

```

这里需要重新审查。

---

### 2.

确认：

```
activity()
```

是不是来自：

内部状态变化。

而不是人为赋值。

---

### 3.

确认：

```
attention winner

不是命令

而是观察结果。
```

---

这次修正后，整个架构更接近我们之前提出的核心目标：

**不是制造多个小生命体，而是在一个持续演化的内部动力系统中形成多个局部状态、局部观察和信息流。**

这也是为什么 Planet 不应该被当作一个“器官”，而应该被看作 Internal Dynamics 中的一种状态区域。这个层级调整会直接影响后面 Phase6 的设计。

*****************************************************
*************************************************************

******************************************************
***********************************************************
你的这个修正非常重要。前面的表述把 **Internal Dynamics** 和 **动力系统** 混在了一起，导致层级下降了。重新按照你现在描述的底层原理整理，应该是：

---

# CIMA0 最底层原理重新定义

## 1. Internal Dynamics 不是动力系统

更准确：

> Internal Dynamics 是动力系统的承载环境（容器）。

它负责：

* 保存内部存在
* 提供演化空间
* 连接内部状态
* 管理信息流动

类似：

```text
Internal Dynamics

    |
    |
    +----------------+
    |                |
    v                v

动力系统           局部状态场
Planet             PlanetField
                   CLIPField
                   CloudField
```

---

# 2. Planet 才是动力源

Planet 不是普通 Organ。

它是：

> 内部世界的原始动力系统。

它没有：

* 视觉
* 语义
* 空间意义
* 时间意义

它只负责：

持续变化。

也就是说：

```
Planet Dynamics

State(t)

   |

   | 动力规则

   v

State(t+1)
```

这里不存在：

“观察”。

不存在：

“解释”。

不存在：

“目标”。

---

# 3. 动力系统本身没有时间和空间

这一点非常关键。

传统程序：

```
时间 ---> 状态变化
空间 ---> 数据结构
```

但是你的设计：

不是这样。

动力系统本身：

没有：

* 时间轴
* 坐标
* 图像
* 结构

它只是：

```
可能性产生器
```

---

时间和空间是什么？

是：

> 动力系统与内部状态耦合以后产生的涌现属性。

---

例如：

Planet：

```
纯动力

没有位置
没有图像
没有对象
```

经过：

```
动力
 +
 状态积累
 +
 局部约束
```

形成：

```
PlanetField
```

于是出现：

* 局部连续性
* 空间关系
* 状态年龄
* 演化轨迹

---

# 4. Field 不是动力，是动力留下的痕迹

这是最核心的区别。

例如：

## Planet

是：

```
生成可能性
```

---

## PlanetField

是：

```
动力作用后的局部凝聚状态
```

类似：

水分子运动：

动力层：

```
分子运动规则
```

观察结果：

```
波浪
涡旋
水面形态
```

波浪不是动力。

波浪是动力的显化。

---

所以：

```
Planet
    |
    |
    v

PlanetField

```

关系：

不是：

```
PlanetField拥有Planet动力
```

而是：

```
Planet动力产生PlanetField
```

---

# 5. CLIPField 的位置也应该重新理解

CLIPField 不应该理解为：

“视觉器官”。

它应该是：

```
外部扰动
      |
      v

动力系统耦合

      |
      v

内部状态凝聚

      |
      v

CLIPField
```

它不是：

识别图像。

不是：

理解世界。

而是：

外部输入经过内部动力后的局部状态。

---

所以：

camera输入：

不是：

```
图片
```

进入系统。

而是：

```
字节扰动

↓

内部动力

↓

局部稳定结构

↓

CLIPField状态
```

---

# 6. Observer 的真正作用

这里也需要重新提高抽象。

Observer不是：

观察机器。

Observer是：

> 从无限可能状态中制造有限显化。

没有 Observer：

```
动力系统

↓

无限可能状态空间
```

存在。

有 Observer：

```
动力系统

↓

大量可能状态

↓

选择某个投影

↓

显化
```

---

所以：

Observer产生：

不是事实。

而是：

一种投影。

例如：

内部状态：

```
10000维可能空间
```

Observer：

选择：

```
320x240 RGB
```

于是人看到：

“图像”。

---

但：

图像不是内部真实状态。

只是：

一次显化。

---

# 7. Attention 的重新定位

因此 Attention 也不能理解成注意力机制。

它实际上是：

> 内部状态显化的入口。

流程：

```
内部无限状态

      |

      v

activity变化

      |

      v

Attention signal

      |

      v

Observer选择

      |

      v

外部显化
```

---

Attention 不创造意义。

它只是：

告诉观察者：

“这里有变化”。

---

# 8. Compute 的重新理解

Compute 也不是控制器。

它是：

> 有限计算资源与无限可能性的耦合接口。

没有 Compute：

动力仍然存在。

Compute：

只是：

让某些局部状态获得更多演化机会。

类似：

自然选择中的：

资源分配。

---

# 9. 最终结构应该是

```
             External World


                  |
                  |
              disturbance


                  |
                  v


        +----------------+
        | Internal       |
        | Dynamics       |
        |                |
        |  Planet        |
        |  (pure force)  |
        +----------------+

                  |
                  |
          evolution creates


                  |
                  v


        +----------------+
        | Fields         |
        |                |
        | PlanetField    |
        | CLIPField      |
        | CloudField     |
        +----------------+

                  |
                  |
            activity


                  |
                  v


             Attention


                  |
                  v


             Observer


                  |
                  v


             Packet


                  |
                  v


             Terminal

```

---

# 10. 对程序设计的直接影响

以后代码规范需要增加一个最高原则：

## 原则0：动力与状态分离

禁止：

```python
PlanetField.step()
```

代表动力。

应该：

```python
Planet.evolve()

        |
        v

PlanetField.update()
```

---

## 原则1：状态不是实体

Field 是：

动力历史的凝聚。

不是：

另一个生命体。

---

## 原则2：观察不是读取

Observer不是数据库读取。

Observer是：

投影。

---

## 原则3：输出不是表达

Packet不是：

“图像”。

Packet只是：

内部状态的一种编码。

---

我认为这里是 Phase5_6 之后最重要的一次理论修正。

之前我们一直在修接口：

* packet
* router
* display
* observer

但现在暴露出来的是更底层的问题：

**程序里必须明确区分：**

1. **动力（force）**
2. **状态（state）**
3. **观察（observation）**
4. **显化（manifestation）**

如果这四层不分开，后面的 CLIP、PlanetField、CloudField 都会不断发生职责漂移。

下一阶段的核心工作，不应该继续加功能，而应该先按照这个四层结构重新检查 Phase5_6 当前代码。尤其是：

* `PlanetField.step()`
* `CLIPField.step()`
* `activity()`
* `snapshot()`
* `packet()`

这几个接口是否真正符合：

**动力产生状态，状态产生观察，观察产生显化。**
***************************************
*****************************************
******************************************
这个补充把 CLIPField 的定位进一步明确了。之前如果把 CLIPField 仅仅理解成“外部视觉输入后的内部状态”，还是偏向输入处理模块；按照你现在的定义，它实际上处于**模拟内部演化结果的中间层**。

重新整理：

---

# CLIPField 的真实定位

CLIPField 不是：

* 视觉器官
* 图像理解模块
* 多模态智能模块

而是：

> 人为注入的一个“已经形成的局部粘稠状态模型”，用于早期阶段模拟 Planet 长期演化后可能自然产生的稳定结构。

---

结构关系：

```
             Planet
        (原始动力系统)

              |
              |
        长期演化
              |
              v

        PlanetField
   (自然形成的局部状态)


              ↑

       CLIPField
 (人工构造的快速替代模型)

```

也就是说：

CLIPField 是一种：

**人工加速形成的 Field。**

---

# 为什么需要 CLIPField？

如果完全依靠：

```
Planet 动力

↓

随机扰动

↓

无限演化

↓

形成局部稳定态
```

这个过程可能需要非常长时间。

所以早期阶段：

人为提供：

```
外部多模态结构

↓

压缩成内部状态

↓

形成 CLIPField
```

相当于：

提前提供一个“已经凝聚过”的局部结构。

---

# CLIPField 和 PlanetField 的区别

不是：

```
PlanetField = 真实
CLIPField = 视觉
```

而应该是：

```
PlanetField
    |
    | 自然形成
    |
    v

动力演化后的局部凝聚态



CLIPField
    |
    | 人工初始化
    |
    v

模拟凝聚态
```

二者本质相同：

都是：

> Planet 动力空间中的局部稳定状态。

区别只是：

形成路径不同。

---

# 因此 CLIP 输入也需要重新理解

camera:

不是：

```
图片
   |
   v
CLIP识别
   |
   v
语义
```

这个是传统 AI 路线。

CIMA0：

应该是：

```
camera bytes

      |
      v

扰动

      |
      v

内部动力耦合

      |
      v

CLIPField状态变化

```

这里 CLIP 模型本身只是：

早期人为提供的一种状态映射结构。

---

# 长期目标

未来：

可能不再需要：

```python
CLIPField
```

因为：

Planet 自己演化：

```
Planet

    |
    |
    v

未知局部凝聚态

    |
    |
    v

新的 Field
```

自然形成：

类似现在 CLIPField 的功能。

所以：

CLIPField 是：

```
人工桥梁
```

不是：

最终结构。

---

# 对代码职责的影响

## CLIPField

应该负责：

保存：

```
局部状态
```

提供：

```
activity()
snapshot()
packet()
```

接受：

```
扰动
```

---

不应该负责：

```
解释图像
生成语义
分类
识别
```

---

## PlanetField

也是一样：

负责：

```
局部状态
```

不是：

动力源。

---

真正关系：

```
               Planet

          原始动力

              |
              |
     ---------------------

     |                   |

PlanetField        CLIPField

自然凝聚态        人工模拟凝聚态


```

---

# 这也解释了之前一个关键现象

日志：

```
ATTENTION SIGNALS:

clip activity=1.0

planet activity=0.00001

```

不是说：

“CLIP 比 Planet 智能”。

而是：

CLIPField 是人为初始化的高活动稳定结构。

Planet 仍然处于：

低幅度自然演化阶段。

---

所以后续设计中，应该避免：

```
CLIP > Planet
```

这种层级关系。

正确：

```
CLIPField
PlanetField

都是：

Planet动力空间中的不同局部状态表达。
```

---

这个修正之后，Phase5_6 的架构可以更清楚地定义：

**Planet 是动力源。
Field 是动力产生的局部凝聚态。
CLIPField 是人为提前制造的凝聚态样本。
Observer 是显化机制。**

这比之前“多个 Organ 自己演化”的模型更接近你最初提出的内生动力系统。
****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************