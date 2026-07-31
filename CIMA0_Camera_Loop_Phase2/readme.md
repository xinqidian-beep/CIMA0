usb_camera.py
=
硬件设备层


camera_io.py
=
边界流转层


camera_planet.py
=
外部世界局部投影

***************
现在这个版本已经完成了一个重要节点：**CIMA0_Camera_Loop 第一条真实硬件闭环基线。**

先总结当前状态，再规划后续。

---

# 一、当前冻结版本总结

版本建议名称：

```text
camera_loop_baseline_v1
```

核心目标：

> 验证“外部世界输入 → 内部模块流动 → 输出”的最小闭环。

当前已验证：

```text
USB Camera
    ↓
CameraIO
    ↓
CameraPlanet
    ↓
CameraObserver
    ↓
CameraCompute
    ↓
DisplayIO
    ↓
OpenCV Window
```

---

## 已解决的问题

### 1. 摄像头入口

已通过：

```text
MSMF backend
Camera index 0
```

确认：

* USB 摄像头可访问；
* OpenCV 接口正常。

---

### 2. 显示链

最终确认：

问题不是摄像头。

问题是：

```python
cv2.imshow()
```

之后缺少：

```python
cv2.waitKey()
```

GUI 事件循环没有推进。

修复后：

* 窗口正常；
* 图像正常刷新。

---

### 3. 模块边界重新明确

最终确定：

## CameraPlanet

只负责：

```text
外部帧 → 外部状态
```

不负责：

* 采样；
* 计算；
* 分配资源；
* 视觉理解。

---

## CameraObserver

负责：

```text
当前状态
      ↓
瞬时变化
```

只产生：

```text
delta_ephemeral
```

---

## CameraCompute

负责：

```text
计算资源状态
```

包括：

* 自恢复；
* 临时额度发放。

不理解任务。

---

## CameraIO / DisplayIO

保持边界透明。

---

# 二、为什么需要另开文件夹

建议：

**不要继续在 CIMA0_Camera_Loop 上直接开发。**

原因：

这个目录现在的价值已经改变：

它不是实验场。

它是：

> 已验证硬件闭环基准。

---

建议结构：

```text
CIMA0/
│
├── CIMA0_Camera_Loop/
│       |
│       └── camera_loop_baseline_v1
│
├── CIMA0_Camera_Loop_Phase2/
│
├── CIMA0_Camera_Loop_Phase3/
│
└── archive/
```

---

# 三、下一阶段建议

## Phase2：外部状态扰动链

新目录：

```text
CIMA0_Camera_Loop_Phase2
```

目标：

不改变显示。

增加：

```text
CameraPlanet
        |
        ↓
external_state

CameraObserver
        |
        ↓
delta_ephemeral
```

观察：

* 摄像头移动；
* 光照变化；
* 手进入画面；

是否产生稳定扰动。

输出：

只打印：

```python
{
 delta_mean,
 delta_std
}
```

不影响显示。

---

## Phase3：计算资源耦合

增加：

```text
Observer
      ↓
request

Compute
      ↓
grant
```

验证：

变化越大：

* 请求增加；
* 资源消耗；
* 自恢复。

仍然不改变图像。

---

## Phase4：临时采样

这里才重新引入：

之前删除的：

```python
sample_ephemeral()
```

但是建议不要放回 Planet。

新模块：

例如：

```text
core/ephemeral_sampler.py
```

职责：

```text
external_state
+
delta
+
compute_slots

↓

temporary samples
```

这样边界清晰。

---

## Phase5：扰动云 / 投影输出

最后才考虑：

```text
sample
    ↓
projection
    ↓
display
```

此时显示的不再是：

摄像头原图。

而是：

内部状态重建后的外部投影。

---

# 四、当前不要做的事情

冻结期间禁止：

? 修改 Planet 职责
? 增加 camera_field
? 增加语义层
? 引入模型
? 加复杂视觉算法
? 重构整个目录

因为现在最宝贵的是：

**已经有一个真实运行闭环。**

---

# 五、推荐下一步操作

现在：

1. 提交：

```powershell
git add main.py
git commit -m "Freeze camera loop baseline: hardware display chain working"
```

2. 打 tag：

```powershell
git tag camera_loop_baseline_v1
```

3. 新建分支：

```powershell
git checkout -b phase2_external_state
```

或者复制目录：

```text
CIMA0_Camera_Loop_Phase2
```

---

我的建议：

对于这个项目，**复制文件夹比 Git 分支更符合你的开发方式**。

原因：

你的实验经常涉及架构边界变化。

独立目录：

* 不污染；
* 可以随时回看；
* 可以并行实验。

所以：

```
CIMA0_Camera_Loop
        ↓
冻结

CIMA0_Camera_Loop_Phase2
        ↓
继续演化
```

这是目前最稳的路线。
