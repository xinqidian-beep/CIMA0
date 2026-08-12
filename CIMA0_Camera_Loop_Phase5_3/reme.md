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
