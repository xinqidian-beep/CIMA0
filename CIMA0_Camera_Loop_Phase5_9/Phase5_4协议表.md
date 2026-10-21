明白。这里需要修正前面的理解：

`PlanetField.py` 不是当前 `archive/planet.py` 的替代品，而是 **InternalDynamics 内部演化后的状态场（slow variable field）**。

它的职责不是“参与计算经济申请预算”，而是：

* 接收进入内部系统的状态云
* 按自身动力规则演化
* 通过碰撞、衰减、传播筛选状态
* 输出内部状态场快照

因此它属于：

```text
InternalDynamics
        |
        +--- PlanetField (slow field)
        |
        +--- ComputeSystem
                |
                +--- CLIPField
                +--- Cloud organs
```

下面重新建立 Phase5_4 协议表。

---

# CIMA0 Phase5_4 Internal Dynamics Protocol v1.0

## 0. 总体架构

```text
                  External World
                       |
                       |
                    Camera
                       |
                       v

                 CameraPacket
                       |
                       v

                  CLIPField
              (visual organ)
                       |
                       |
              compute_request()
                       |
                       v

              InternalDynamics
              (scheduler/router)

          +------------+-------------+
          |                          |
          v                          v

   ComputeSystem              PlanetField
   (resource)                (slow field)
          |
          |
   allocation
          |
          v

      CLIPField
      apply_compute()

          |
          v

      CLIPField.step()

          |
          v

   visual internal state


PlanetField:

state cloud
    |
    v
collision
    |
    v
selection
    |
    v
slow evolution
```

---

# 一、模块职责协议

| 模块               | 文件                                            | 职责         | 禁止职责         |
| ---------------- | --------------------------------------------- | ---------- | ------------ |
| InternalDynamics | `core/internal_dynamics/internal_dynamics.py` | 内部组织、路由、调度 | 不创造状态、不解释输入  |
| ComputeSystem    | `core/compute_system/compute_system.py`       | 计算资源分配     | 不读取organ内部状态 |
| Sampler          | `core/compute_system/sampling/sampler.py`     | 采样、计算辅助    | 不决定演化方向      |
| CLIPField        | `core/organs/clip_field.py`                   | 视觉状态organ  | 不管理全局资源      |
| PlanetField      | `core/internal_dynamics/cloud/Planetfield.py` | 慢变量状态场     | 不申请计算预算      |
| archive Planet   | `archive/planet.py`                           | 基础动力基底     | Phase5_4不改   |

---

# 二、输入数据协议

## Camera → InternalDynamics

格式：

```python
{
    "bytes": bytes,

    "shape": (
        height,
        width,
        channels
    ),

    "dtype": "uint8"
}
```

含义：

完整外部状态流。

---

# 三、Organ接口协议

参与计算经济的organ：

必须实现：

```python
compute_request()
```

和：

```python
apply_compute()
```

---

不参与计算经济的slow field：

例如：

```python
PlanetField
```

只需要：

```python
receive()
step()
snapshot()
```

---

# 四、compute_request协议

## 方向

```text
CLIPField
       |
       v
InternalDynamics
       |
       v
ComputeSystem
```

---

格式：

```python
{
    "type":
    "compute_request",

    "source":
    "clip",

    "score":
    float,

    "activity":
    float,

    "metadata":
    {}
}
```

---

字段：

| 字段       | 说明     |
| -------- | ------ |
| type     | 固定协议名  |
| source   | 请求来源   |
| score    | 资源优先级  |
| activity | 当前活动程度 |
| metadata | 扩展信息   |

---

# 五、InternalDynamics请求收集协议

## 输入：

organ列表：

```python
self.organs
```

---

流程：

```python
for organ in organs:

    request = organ.compute_request()

    requests.append(request)
```

---

输出：

必须是：

```python
list
```

例如：

```python
[
 {
  "type":"compute_request",
  "source":"clip",
  "score":0.7
 }
]
```

禁止：

```python
{
 "clip":{}
}
```

---

# 六、ComputeSystem协议

## 输入：

```python
requests
```

格式：

```python
[
 request1,
 request2
]
```

---

内部流程：

```text
submit()
   |
   |
allocate()
   |
   v
allocation
```

---

或者：

快捷：

```python
step(requests)
```

等价：

```python
for r in requests:
    submit(r)

allocate()
```

---

# 七、allocation协议

方向：

```text
ComputeSystem

       |

       v

InternalDynamics

       |

       v

Organ
```

---

实际格式：

```python
{
    "clip":
    {
        "source":
        "clip",

        "budget":
        512,

        "shape":
        None
    }
}
```

---

注意：

不包含：

```python
ratio
```

原因：

ratio属于ComputeSystem内部策略。

organ无需知道。

---

# 八、apply_compute协议

## CLIPField

输入：

```python
{
    "budget":512
}
```

执行：

```python
self.compute_budget=512
```

---

协议：

```python
def apply_compute(
    allocation
):
    pass
```

---

# 九、budget消费协议

这是之前缺失的一层。

## Organ必须定义：

预算如何影响step。

---

CLIPField：

```text
compute_budget

       |

       v

计算次数
/更新频率
/采样深度

       |

       v

状态变化
```

---

例如：

```python
iterations = budget // cost
```

---

禁止：

```python
budget存储后不用
```

---

# 十、PlanetField协议

## 定位：

slow variable field。

不是organ。

不参与：

```text
compute_request
```

不参与：

```text
allocation
```

---

输入：

状态云：

```python
{
    "value": float,

    "age": int,

    "activity": float
}
```

---

核心行为：

```text
receive()

      |

      v

collision()

      |

      v

selection()

      |

      v

propagation()

      |

      v

slow evolution
```

---

PlanetField作用：

```text
撞入状态云
       |
       v
碰撞筛选
       |
       v
保留稳定模式
       |
       v
形成慢变量地形
```

---

输出：

```python
snapshot()
```

例如：

```python
{
 "state": ndarray,

 "activity": float
}
```

---

# 十一、完整step时序

InternalDynamics：

```text
step()

 |
 |
 +--> observe_requests()

 |
 |
 +--> ComputeSystem.step()

 |
 |
 +--> apply_compute()

 |
 |
 +--> organs.step()

 |
 |
 +--> PlanetField.step()

 |
 |
 +--> snapshot()
```

---

# 十二、Phase5_4冻结规则

## 允许变化：

* CLIPField内部算法
* ComputeSystem分配策略
* PlanetField动力规则

---

## 禁止变化：

### archive/planet.py

保持：

```text
基础动力源
```

---

### 协议字段

冻结：

```python
compute_request

allocation

apply_compute
```

---

# 十三、最终闭环验收

日志必须出现：

```text
CLIP receive:
(480,640,3)

CLIP compute_request:
score=x

ComputeSystem allocation:
clip budget=x

CLIP apply_compute:
budget=x

CLIP step:
updated


PlanetField:

receive cloud

collision

selection

state changed
```

达到这个状态：

说明 Phase5_4 的核心目标完成：

> 外部输入进入内部器官，器官提出计算需求，计算资源被分配，状态场自主筛选并演化。

这才是 Phase5_4 从“数据管线”进入“内部动力系统”的分界点。
