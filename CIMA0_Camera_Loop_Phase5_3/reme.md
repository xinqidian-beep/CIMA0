目前架构变化后的职责应该是：

core/

terminal/
    camera/
        camera_io.py
        camera_planet.py
        camera_observer.py


compute_system/
        compute_system.py
        sampling/
            sampler.py


internal_dynamics/
        internal_dynamics.py
        cloud/


display_io.py
其中：

CameraObserver：决定哪些位置更新

Sampler：决定选择规则

ComputeSystem：提供预算

DisplayIO：只显示
****************************

三者关系：

main.py
    |
    | 调度
    |
    v

InternalDynamics
    |
    | 转发
    |
    v

Planet
    |
    | 演化
    |
    v

State
***************************
最终闭环应该是：
Planet
  |
  | state
  v

snapshot


  |
  v

ComputeSystem

  |
  | activity
  | sampling
  | 
  v


Observer

  |
  | read selected state
  v


IO
********************************
### CIMA0 Phase5_3 当前总结

这一阶段最大的收获不是代码完成，而是**架构重新收敛**。

经过 CloudField / Cell 多轮调整后，已经确认：

---

## 一、核心架构重新确定

之前：

```text
InternalDynamics

    |
    +-- planet
    +-- cloud
    +-- clip
```

存在风险。

原因：

`cloud` 如果来自 Planet 长时间演化后的盆地/吸引子，它不应该成为第二个动力系统。

否则：

* Planet 演化一套规则
* Cloud 又演化一套规则

产生两个状态源。

---

现在确定：

```text
                 Planet
                   |
                   |
             InternalDynamics
                   |
              snapshot
                   |
        -------------------
        |                 |
   ComputeSystem      Observer
        |
     采样策略

                   |
                   v

                   IO
```

原则：

* **Planet 是唯一动力核心**
* **InternalDynamics 是动力接口层**
* **ComputeSystem 是计算分配层**
* **Observer 是读取/观察层**
* **IO 是传输显示层**

---

# 二、CloudField / Cell 的定位重新确认

结论：

`Cell` 不应该作为独立状态存在。

原因：

Cell 保存：

```python
value
age
activity
position
```

这些实际上来源于：

Planet 网格本身。

例如：

| Cell字段   | 原本职责 | 新归属             |
| -------- | ---- | --------------- |
| value    | 状态   | Planet ndarray  |
| position | 空间位置 | ndarray坐标       |
| activity | 变化程度 | ComputeSystem   |
| age      | 稳定时间 | ComputeSystem统计 |

所以：

CloudField 不再作为动力器官。

未来如果需要：

```text
Planet
  |
  |
盆地检测
  |
  |
Cloud representation
```

应该是观察结果，而不是动力核心。

---

# 三、Planet 接入完成第一步

已经确认：

`archive/planet.py`

是正确动力源。

特点：

```python
state

↓

neighbor diffusion

↓

sin nonlinear

↓

self evolution
```

并且：

* 不依赖 camera
* 不依赖 compute
* 不依赖 observer

符合：

> 内部动力持续存在

---

目前修改：

```text
archive/planet.py

        ↓

InternalDynamics

        ↓

snapshot
```

已经成功。

验证：

输出：

```text
<class 'dict'>
dict_keys(['planet'])
```

说明：

现在：

```text
Planet
 |
 InternalDynamics
 |
 snapshot
```

接口已经建立。

---

# 四、当前发现的问题

## 1. Display画面问题

当前：

* 竖条纹已经消失
* 现在是灰色噪声

说明：

二维结构恢复了。

但是：

还需要确认：

显示的数据是否真的来自：

```python
snapshot["planet"]
```

而不是旧路径。

---

## 2. ComputeSystem 当前没有真正参与

现在：

流程：

```text
Planet

↓

snapshot

↓

Observer

↓

Display
```

实际没有：

```text
ComputeSystem
```

参与。

原因：

Planet 没有：

```python
request_compute()
```

这是合理的。

因为：

Planet 不应该被计算预算控制。

但是：

Observer 的采样策略以后需要 ComputeSystem。

---

## 3. Observer职责还需要进一步收缩

当前：

Observer 已经删除：

* activity
* Sampler

方向正确。

最终应该：

```text
Observer:

读取

↓

封包

↓

输出
```

不负责：

* 决定看哪里
* 判断重要性
* 计算变化

---

# 五、下一阶段计划

## Phase5_3.1  固化 Planet 单动力闭环

目标：

验证：

```text
archive Planet

↓

InternalDynamics

↓

Observer

↓

DisplayIO
```

完全独立运行。

任务：

1. 删除所有 CloudField 调用
2. 删除 Cell 相关路径
3. 确认 Display 显示：

```python
snapshot["planet"]
```

4. 打印一次：

```text
planet min
planet max
shape
```

确认显示来源。

---

## Phase5_3.2  修正 Display 数值映射

不是修改 Planet。

Display负责：

```text
float field

↓

visual mapping

↓

RGB
```

确保：

例如：

```
-0.05
   |
 128灰
   |
+0.05
```

而不是：

```
float
 |
uint8截断
 |
灰噪声
```

---

## Phase5_3.3 重新接入 ComputeSystem

不是控制 Planet。

而是：

控制：

```text
Observer读取量
```

流程：

```text
Planet snapshot

↓

ComputeSystem

计算：

activity

sampling

allocation


↓

Observer

读取选定区域
```

这样：

ComputeSystem 才有真正职责。

---

## Phase5_3.4 重新设计 Cloud / Clip

顺序：

不是：

```
Cloud
   |
   动力
```

而是：

```
Planet

↓

长期演化

↓

Observer/Detector

↓

发现盆地

↓

Cloud representation
```

Clip：

同理：

```
视觉输入

↓

内部演化

↓

稳定结构

↓

观察者定义为clip attractor
```

---

# 当前状态一句话总结

这次最大的修正是：

> CIMA0 从“多个内部模块共同演化”重新回到“一个动力核心 + 多种观察/计算方式”。

现在不要继续扩展模块。

下一步应该把最小闭环：

```text
Planet
  ↓
InternalDynamics
  ↓
Observer
  ↓
Display
```

跑稳定。

然后再逐层加入：

```text
Compute
Cloud
Clip
```

这样不会再次出现 CloudField 那种“替代 Planet 又替代 Observer”的结构混乱。

辛苦了，这一轮其实完成的是一次架构清理，比增加代码更重要。
*******************************************
对，这一步必须先冻结问题清单，否则在修改过程中容易再次混淆层级。

我根据刚才整个追踪过程，把问题分为 **架构问题、接口问题、实现问题** 三类。

---

# CIMA0 Phase5_3 当前问题列表

## A. Sampler维度与职责问题（最开始发现）

### 问题 A1：Sampler 接收了错误层级的数据

当前：

```text
CameraObserver
      |
      v
Sampler
      |
      v
pixel delta / age / activity
```

问题：

Sampler实际上在选择：

> 摄像头像素变化

而不是：

> InternalDynamics产生的内部状态

违反：

```text
Sampler只负责选择机制
不负责理解数据来源
```

---

### 问题 A2：2D Planet维度被错误带入Sampler

发现：

```python
len(delta)
```

问题：

如果输入：

```python
delta.shape=(128,128)
```

那么：

```python
len(delta)=128
```

不是：

```python
16384
```

但是：

这个不是最终解决方案。

错误方向：

```python
delta.ravel()
```

因为会再次让Sampler成为：

```text
Planet空间采样器
```

正确方向：

Sampler最终应该接收：

```text
CloudField内部状态集合
```

而不是Planet网格。

---

# B. CloudField定位错误（刚才发现）

## 问题 B1：CloudField曾经被实现成空间缓存

当前危险方向：

```text
Camera/Planet
      |
      v
CloudField
      |
      v
Cell(x,y,value)
```

这会导致：

CloudField = Planet副本

错误。

---

正确：

```text
Planet动力演化

       |
       v

CloudField

       |
       v

吸引子区域
特殊状态结构
```

CloudField不是：

* 像素存储
* 空间压缩
* 网格复制

---

## 问题 B2：Cell概念漂移

错误理解：

```text
Cell = Planet格子
```

导致：

```python
position=(x,y)
```

这种设计。

需要重新确认：

如果保留Cell名称：

它应该表示：

```text
InternalDynamics内部状态单元
```

不是空间单元。

---

# C. Planet层混淆问题（刚才发现）

## 问题 C1：CameraPlanet 和动力Planet混淆

存在两个不同概念：

---

### CameraPlanet

位置：

```text
core/terminal/camera/camera_planet.py
```

职责：

```text
camera ndarray
        |
        v
byte packet
```

输出：

```python
{
 bytes,
 shape,
 dtype
}
```

它是：

外部输入边界。

---

### Planet

职责：

```text
动力源头
```

拥有：

* state
* receive()
* step()
* snapshot()

InternalDynamics已经假设它存在：

```python
InternalDynamics(planet)
```

---

当前问题：

Phase5_3运行目录中：

Planet实现在哪里？

需要确认。

---

# D. InternalDynamics问题（已确认不是问题）

检查结果：

`core/internal_dynamics/__init__.py`

设计正确。

它：

负责：

```text
receive external disturbance
advance local dynamics
expose current state
```

不负责：

* camera
* cloud
* observer
* display

所以：

**InternalDynamics无需重写。**

---

# E. CameraObserver越权问题

当前：

CameraObserver内部：

```python
from core.compute_system import Sampler
```

并：

```python
self.sampler.select()
```

问题：

Observer同时承担：

1. 视觉场维护
2. delta计算
3. age维护
4. 采样决策

其中第4项越界。

应该：

CameraObserver：

负责：

```text
camera field observation
```

不负责：

```text
internal selection
```

---

# F. 当前缺少验证的问题

需要检查：

## F1：main.py真实链路

确认：

现在是否：

```text
Camera
→ CameraPlanet
→ CameraObserver
→ ?
```

还是：

```text
Camera
→ CameraPlanet
→ InternalDynamics
→ Planet
```

---

## F2：Planet实例来源

确认：

哪里：

```python
InternalDynamics(
    planet=?
)
```

如果没有当前Planet：

说明Phase5_3缺少动力入口。

---

## F3：CloudField挂载位置

确认：

CloudField应该在哪里：

候选：

```text
Planet内部
```

而不是：

```text
InternalDynamics平级
```

需要看现有代码。

---

# 当前修改优先级

不要同时改。

顺序：

## 第一步

确认：

```text
main.py
+
Planet实例
```

因为这是根。

---

## 第二步

确认：

```text
Planet
+
CloudField关系
```

恢复：

```text
Planet动力
      ↓
CloudField内部结构
```

---

## 第三步

拆掉：

```text
CameraObserver → Sampler
```

---

## 第四步

重新定义：

```text
Sampler输入
```

变成：

```text
CloudField状态
```

---

## 第五步

最后处理：

权重自适应：

```python
w_delta
w_age
w_activity
```

因为这是高级演化机制，必须建立在正确对象上。

---

当前结论：

**已确认一个大问题：Sampler入口错。**

**已确认一个概念问题：CloudField被拉回了空间层。**

**已确认一个命名问题：CameraPlanet ≠ Planet。**

**InternalDynamics暂时保持不动。**

下一步从 `main.py` 和 Planet实例开始查，不再猜。


*************************************
这个问题也加入清单，而且它实际上属于 **Sampler 的二阶段设计问题**，不是当前第一阶段链路修复问题。

先记录，不丢。

---

# G. Sampler 自适应权重演化问题

## G1. 当前固定评分模型

当前：

```python
score =
    delta * w_delta
    +
    age * w_age
    +
    activity * w_activity
```

初始：

```python
w_delta = 1.0
w_age = 0.01
w_activity = 0.1
```

含义：

当前阶段：

```
变化优先
+
少量考虑年龄
+
一定考虑活跃度
```

这是一个静态选择规则。

---

# G2. 当前问题

如果永远固定：

```python
w_delta=1.0
w_age=0.01
w_activity=0.1
```

那么：

Sampler永远按照人工设定偏好选择。

它没有形成：

```text
选择
 ↓
结果
 ↓
反馈
 ↓
规则变化
```

闭环。

---

# G3. 目标设计：权重成为内部可演化状态

不是：

```python
w += random
```

也不是：

```python
三个权重同时增加
```

而是：

权重之间形成耦合。

你提出：

```python
w_delta  += reward * gradient

w_age    += reward * gradient

w_activity += reward * gradient
```

进一步明确为：

---

## 方案1：交叉影响

### delta权重受age影响

含义：

> 长期存在的结构，如果仍然产生变化，提升对变化的关注。

形式：

```python
w_delta += η * reward * age
```

---

### age权重受activity影响

含义：

> 长期活跃结构值得保持。

形式：

```python
w_age += η * reward * activity
```

---

### activity权重受delta影响

含义：

> 新变化刺激活跃评价。

形式：

```python
w_activity += η * reward * delta
```

形成：

```
        age
         |
         v

delta ---> activity
  ^          |
  |          |
  +----------+

```

---

# G4. 更完整的闭环形式

也可以三个同时受其他两个影响：

例如：

```python
dw_delta =
    reward *
    (
      a1*age
      +
      a2*activity
    )


dw_age =
    reward *
    (
      b1*delta
      +
      b2*activity
    )


dw_activity =
    reward *
    (
      c1*delta
      +
      c2*age
    )
```

这样：

没有一个评价维度独立存在。

---

# G5. 必须加入稳定约束

否则：

```python
w_delta
w_age
w_activity
```

会无限增长。

需要：

## 归一化

例如：

```python
weights /= sum(weights)
```

保持：

```text
w_delta+w_age+w_activity=1
```

或者限制：

```python
min_weight
max_weight
```

---

# G6. 与 CIMA0 总体设计的关系

这个不是普通机器学习权重。

它更接近：

内部动力规则的一部分。

链路：

```
CloudField产生状态

        ↓

Sampler选择

        ↓

reward反馈

        ↓

Sampler规则改变

        ↓

新的选择行为

```

也就是说：

Sampler自身形成一个小型动力系统。

---

# 更新后的总问题列表增加：

## G. Sampler自适应演化

状态：

⬜ 固定权重评分

目标：

⬜ 权重作为内部状态

⬜ reward驱动梯度变化

⬜ delta/age/activity三者形成耦合闭环

⬜ 权重稳定化

---

## 当前解决顺序不变：

### 第一阶段（先恢复结构）

1. ✅ InternalDynamics确认正确（已完成）
2. ⬜ main.py真实链路确认
3. ⬜ Planet实例确认
4. ⬜ CameraObserver与Sampler解绑
5. ⬜ CloudField恢复为内部结构生成层

### 第二阶段（动力稳定后）

6. ⬜ Sampler输入改为CloudField状态
7. ⬜ Sampler选择内部状态
8. ⬜ reward机制

### 第三阶段（演化）

9. ⬜ 权重自适应闭环
10. ⬜ w_delta / w_age / w_activity动力演化

现在问题清单完整了。后面按编号一个一个解决，不再同时改多个层。

*************************************************时间轴：

t0:
+----------------------+
|        Planet        |
|                      |
|   +------------+     |
|   | CloudField |     |
|   |  局部区域  |     |
|   +------------+     |
|                      |
+----------------------+


t1:
+----------------------+
|        Planet        |
|                      |
|   +-------------+    |
|   | CloudField  |    |
|   |  演化后的区块 |   |
|   +-------------+    |
|                      |
+----------------------+


t2:
+----------------------+
|        Planet        |
|                      |
|    +----------+      |
|    | Cloud    |      |
|    | Field    |      |
|    +----------+      |
|                      |
+----------------------+

********************************************
                 External disturbance
                         |
                         v


+------------------------------------------------+
|                    Planet                       |
|             (完整内部动力空间)                  |
|                                                |
|    +----------------+                          |
|    |                |                          |
|    |  CloudField    |  <--- 局部慢变量结构      |
|    |                |                          |
|    +----------------+                          |
|                                                |
|        快变量持续演化                           |
|        慢变量共同演化                           |
+------------------------------------------------+


                         |
                         v

                  Observer sampling

                         |
                         v

          吸引子 / 盆地 / 特殊状态解释
		  **********************************
		  
archive.Planet = 火种
不可复制
不可优化
不可修改
只能运行和观察

Planet = 内生动力核心

CloudField = Planet空间中的慢变量局部结构

Observer = 局部采样后的解释者

Sampler = 通用计算资源调度

Camera = 外部字节流，不直接控制Planet		  
***************************************
| 项目                 | 状态 |
| ------------------ | -- |
| Camera读取           | ✅  |
| CameraPlanet封装     | ✅  |
| InternalDynamics接口 | ✅  |
| Planet自身演化         | ✅  |
| Camera进入Planet     | ❌  |
| 外部扰动影响内部趋势         | ❌  |
| 同构映射               | ❌  |
**************************************
你这个检查顺序是正确的。现在不要先看 `Planet.receive()`，应该从**同构链路**逐层审核。

目标链：

```text
Camera byte stream
        |
        v
同构封装(packet)
        |
        v
InternalDynamics
        |
        v
动力扰动(field)
        |
        v
Planet响应

同时：

Planet snapshot
        |
        v
Observer采样
        |
        v
保持同构信息
        |
        v
Display还原媒体流
```

逐项看当前代码状态。

---

# 1. Camera 字节流进入后，有没有同构转换成云？

目前：

CameraPlanet 输出：

```python
{
    "bytes",
    "shape",
    "dtype"
}
```

这个是正确的。

它保留：

* 原始数据
* 原始形状
* 数据类型

也就是：

```text
同构信息:
shape
dtype
byte ordering
```

没有丢。

---

但是进入 `InternalDynamics` 后：

当前 `_prepare_disturbance()` / `_to_internal()` 做：

```python
if data.ndim == 3:

    data = data.mean(axis=2)
```

这里发生了第一次信息损失。

例如：

输入：

```
240×320×3 BGR
```

变成：

```
240×320
```

也就是：

```
B
G
R
三个维度
        ↓
灰度
```

这不是同构转换。

这是**投影**。

所以回答：

> camera字节流进入后有没有同构转换成云？

目前：

**部分有。**

保留：

```
空间结构
dtype
数值流
```

丢失：

```
颜色通道结构
```

---

# 2. InternalDynamicsObserver 有没有自动举手申请算力？

看当前代码：

```python
def read(
    self,
    snapshot,
    allocation=None
):
```

这里有：

```python
allocation
```

参数。

但是：

```python
if allocation is None:
    return array.copy()
```

而：

```python
_sample()
```

里面：

```python
return array.copy()
```

目前实际行为：

```text
Observer

读取
计算delta
计算activity

但是

没有产生request
没有申请compute
没有举手
```

所以：

当前没有实现：

```
自动举手原则
```

它只是：

```
被动观察器
```

---

# 3. 采样输出有没有保留同构信息？

看：

```python
encode_field()
```

现在：

```python
return {

"type":"field",

"bytes":
array.astype(np.float32).tobytes(),

"shape":
array.shape,

"dtype":
"float32"

}
```

这一部分很好。

它保留：

```
bytes
shape
dtype
```

所以：

Observer → Display

这条：

```
同构恢复
```

是成立的。

---

# 4. 终端有没有还原成彩色媒体流？

这里是目前另一个问题。

DisplayIO：

```python
if array.ndim == 2:

    return np.repeat(
        array[:,:,None],
        3,
        axis=2
    )
```

这不是恢复彩色。

这是：

```
灰度复制三通道
```

例如：

```
100
100
100
```

变：

```
B=100
G=100
R=100
```

所以显示：

黑白灰地形。

这符合现在看到的窗口。

不是摄像头彩色。

---

# 当前完整链路判断

## 输入侧

```
Camera
 |
 |
packet(bytes,shape,dtype)
 |
 |
InternalDynamics
```

✅ 通

---

## 同构云化

```
BGR 240×320×3

↓

gray 240×320
```

❌ 不是完全同构

发生降维。

---

## 动力扰动

```
disturbance
 |
 v
Planet.receive()
```

目前：

❌ 丢失（之前已经确认）

---

## Observer

```
snapshot
 |
delta/activity
```

✅ 工作

但是：

❌ 没有自动举手机制

---

## 输出

```
field
 |
bytes+shape+dtype
 |
Display
```

✅ 同构封包

但是：

❌ 只能恢复数值场

不能恢复原始彩色摄像头流。

---

所以现在有三个独立问题：

| 位置                      | 状态   |
| ----------------------- | ---- |
| Camera→InternalDynamics | 通    |
| BGR同构保持                 | 丢失颜色 |
| Observer自动申请算力          | 未实现  |
| Observer输出同构            | 正确   |
| Display彩色恢复             | 不存在  |
| 扰动进入Planet              | 丢失   |

---

最关键的一点：

现在窗口显示的“地形”不是摄像头。

它是：

```
archive.Planet 自演化状态
```

经过：

```
snapshot
→ observer
→ field packet
→ Display
```

形成的可视化。

所以它证明的是：

**内部动力表达链通。**

但还没有证明：

**外部摄像头扰动链通。**

下一步应该不是改 Display，而是先做一个最小验证：

固定一帧 camera：

```
黑图
白图
红图
```

分别输入。

观察：

```python
delta_state =
abs(
    state_after -
    state_before
).mean()
```

如果三个输入产生不同 delta：

说明：

```
camera → disturbance → Planet
```

成立。

如果一样：

说明仍然卡在扰动入口。
