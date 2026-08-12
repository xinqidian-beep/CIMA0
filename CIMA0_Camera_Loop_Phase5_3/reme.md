第二步
增加一个极小的内部注入规则：

例如：

每step:

输入fragment寻找最匹配cell

规则：

空cell优先

否则：

activity最低者竞争
第三步
观察：

不是看“像不像摄像头”。

看：

输入变化
        |
        v
cell状态变化
        |
        v
collision/decay
        |
        v
稳定结构


第一步
合并认领机制：

删除 _select_cell

改：

target = self._claim(value)
第二步
限制 receive 注入量。

例如：

inject_budget=128
让：

一帧
↓
最多128个内部事件
而不是：

921600次覆盖
第三步
观察：

运行200步：

看：

active cell:
?
不是看画面。

先确认：

云是否稳定。

另外关于黑屏：

目前不要修改 DisplayIO。

因为：

如果：

cloud输出
shape:(1,)
DisplayIO 黑屏是合理结果。

它只是忠实显示。

当前 Phase5_3 的核心问题已经从：

“怎么显示”

转移成：

“输入如何进入云而不破坏自组织”。

这才是正确的问题。

现在最重要的是恢复：

byte
 ↓
cloud
 ↓
byte
中间没有：

mean
resize
固定空间解释
同时也不能：

逐字节暴力覆盖
下一步应该只改 cloud_field.py，不要扩散到 Observer/main。

***************************************************

## CIMA0 Phase5_3 当前总结

这一次定位到了一个比较关键的架构问题：**不是显示问题，也不是 CLIP 问题，而是内部动力边界的问题。**

---

# 一、已经确认的问题

## 1. 最大错误：外部解释进入了内部

之前：

```
Camera bytes

↓

CloudField.receive()

↓

np.mean()

↓

一个标量

↓

cell
```

结果：

* 空间信息丢失
* 颜色信息丢失
* 时间被伪装为空间
* 输出出现 4×8 黑白灰条纹

这个现象已经解释清楚。

根因不是 DisplayIO。

---

## 2. 字节流本身没有问题

CameraPlanet 输出：

```python
{
    "bytes",
    "shape",
    "dtype"
}
```

这个设计正确。

它应该保持：

```
摄像头
 ↓
原始packet
 ↓
内部
```

不能在入口处解释。

---

## 3. Cell设计出现职责冲突

当前：

```
Cell

value
age
activity

collision()
decay()
selection()
```

问题：

Cell变成了小型动力系统。

同时：

```
Planet

也有动力规则
```

形成：

```
Planet动力
     +
Cell动力

```

两个地方决定状态。

导致：

* 状态来源不唯一
* 演化规则冲突
* 内部自组织被外部规则干扰

---

# 二、重新冻结架构

现在 InternalDynamics 只有两个核心：

```
InternalDynamics

      |
      |
 +----------+
 |          |
 v          v

Planet    CLIPField

动力系统    结构状态云

```

---

# 三、Planet定位

Planet：

负责：

* 状态演化
* 动力规则
* 稳定
* 衰减
* 碰撞
* 传播

内部可以有：

```
cells
```

但是：

Cell只是：

```
value
age
activity
```

状态。

不是规则。

---

变成：

```
Planet

    cells

       value
       age
       activity


    dynamics:

       collision()
       decay()
       propagation()

```

---

# 四、CLIPField定位

CLIPField保持：

```
bytes

↓

visual transformer layers

↓

visual cloud

```

不做：

* 分类
* 语义解释
* 控制

它提供：

长期演化后的视觉结构状态。

---

# 五、Observer重新定位

Observer：

只做：

```
snapshot

↓

activity estimation

↓

budget sampling

↓

packet

```

不做：

* 理解
* 重建内部
* 决定结构

---

# 六、DisplayIO冻结

DisplayIO不用改。

职责：

```
packet

↓

numpy frame

↓

cv2.imshow
```

它不应该知道：

* camera
* planet
* clip
* cloud

---

# 七、下一阶段计划

## Phase5_3.1  清理内部动力边界

目标：

去掉：

```
cloud_field.py
```

中的：

* 外部解释
* mean压缩
* 固定采样
* 独立collision
* 独立decay

保留：

状态结构。

---

## Phase5_3.2  Planet接管状态演化

整理：

```
core/internal_dynamics/

    planet/

        planet.py
        cell.py

    clip/

        clip_field.py

```

其中：

cell.py：

只保存状态。

---

## Phase5_3.3 重新测试最小链路

先不用摄像头。

测试：

```
packet
  |
  v
Planet.receive()
  |
  v
Planet.step()
  |
  v
snapshot()
  |
  v
Observer
  |
  v
Display packet
```

确认：

* 无解释
* 无丢失
* 有输出

---

## Phase5_3.4 再接CameraPlanet

确认：

```
camera bytes

↓

Planet

↓

state

↓

Observer

↓

Display

```

观察是否自然出现：

* 连续流
* 模糊对应
* 状态变化

---

## Phase5_3.5 最后接CLIPField

CLIP作为第二状态空间：

```
Planet state
+
CLIP visual state

↓

InternalDynamics snapshot

```

观察两种动力是否形成互补。

---

# 当前冻结原则

后续代码不要再加入：

❌ 外部空间解释
❌ 固定RGB拆分
❌ 固定cell对应像素
❌ 人工语义映射
❌ 新的中间模块

保持：

```
输入:
字节流

内部:
自组织动力

输出:
字节流
```

---

下一步最合理的是：

**先重构 Planet + Cell，把 CloudField 降级或者移除，然后跑最小内部动力链测试。**

这一步完成后，后面 Camera → InternalDynamics → Observer → Display 才是真正闭环。
