# CIMA0 Phase5_4 架构备忘录

写给工程师，说明这轮讨论定下来的设计结论和依据。目的是让接下来的实现有一份共同参照，不用重新对齐理解。

---

## 一、核心发现：`archive/` 下的四个文件是最简同构种子

路径：`CIMA0_Camera_Loop_Phase5_4/archive/{planet.py, io.py, observer.py, compute.py}`

这四个文件都只有一二十行，读完之后能确认一件事：**整个系统不是"四个各管一段、越往上越复杂的模块"，而是同一个极简模式在不同物理量上的重复实例化。**

每个文件都遵循同一个骨架：

- 只持有极少的局部状态（`Planet.state`，`ComputeSystem.available`）
- 只有一条局部更新规则（扩散公式、衰减回充公式）
- 输入输出极简，不携带"我是谁""你是谁"这类身份信息
- 文档字符串明确写了"不做什么"（Observer 明确写着不请求、不控制、不存历史；ComputeSystem 明确写着不认识 organ、不认识 meaning）

**这意味着**：之前几轮讨论、逐步长出来的"CLIP 向 ComputeSystem 提交带 `source` 字段的请求列表，ComputeSystem 按 `source` 分组做比例分配"那一整套协议，**不是对这四个种子文件的同构复制，是另起炉灶设计出来的复杂机制**，方向上偏了。

结论：接下来的实现应该以这四个文件的极简程度为标准，不是以之前那份协议表为标准。协议表可以废弃。

---

## 二、`archive/compute.py` 揭示的关键性质：没有公平性机制

实测过（不是猜测）：

**单个使用者持续高强度索取**：不会永久枯竭到 0，但会长期卡在很低水平反复打转（`decay` 回充速度追不上被一次性掏空的速度）。

**多个使用者共用同一个 `ComputeSystem` 实例**：结构上是"先到先得"——先调用 `allocate()` 的一方吃满，后调用的一方经常拿到 0。这不是概率问题，是这份极简实现天生没有公平性/优先级逻辑导致的必然结果。

---

## 三、设计结论：唯一注意力 + Sampler 作为 ComputeSystem 的私有员工

甲方（产品侧）给出的原则：**生物不是并发计算，只拥有唯一注意力**。这解释了"先到先得"不是需要修的 bug，而是提示了正确的模型应该是"每一轮只有一个赢家"，不是"雨露均沾按比例分配"。

具体机制（组合的是已有的、复用过三次的机制，不是新发明）：

1. 每个 organ 各自算出一个局部信号（`delta` 变化量 / `age` 距上次被选中的轮数 / `activity` 活跃度）——这三个量正是 `Sampler.select()` 一直在用的输入，之前在 CloudField 碰撞调度、Observer 读取 array/cell 列表时已经复用过三次。
2. 所有 organ 的这三个数字交给 `Sampler.select(..., budget=1)` ——`budget=1` 就是"唯一注意力"的字面实现，不是新逻辑，是把"选一批"的用法收窄成"只选一个"。
3. **关键的层级决定**：`Sampler` 不应该是和 `ComputeSystem` 平级的第五个模块，也不应该被 `Observer` 或任何其他模块直接 `import` 使用。它应该是 `ComputeSystem` 内部私有雇佣的员工——`ComputeSystem.__init__` 里 `self.sampler = Sampler()`，外部 organ 只认 `ComputeSystem` 这一个"老板"，感觉不到 `Sampler` 的存在。
4. 只有 `Sampler` 选中的赢家，才会真正被算 budget、拿到 `allocation`，调用自己的 `apply_compute()`；没被选中的 organ 本轮拿到空结果，`age` 计数器 +1，下一轮重新参与竞争（这就是"过期补算"——长期没被选中的 organ 会因为 `age` 分量持续增长，早晚会被拉回来）。
***************
Sampler
 |
提供一次机会
 |
ComputeSystem
 |
提供计算能量
 |
organ
 |
决定如何使用
***************

---

## 四、现状核查：两处"老板"实现不一致，需要统一

代码库里实际存在两个独立的、各自领域的 ComputeSystem 角色，这是对的（每个领域各自隔离，互不共享同一个实例）：

| 文件 | 角色 | 当前是否符合"雇 Sampler 当员工，选唯一赢家"模式 |
|---|---|---|
| `core/terminal/camera/camera_compute.py` | 摄像头边界领域的老板 | ✅ 已经是对的写法，`self.sampler = Sampler()`，`execute()` 处理单个 request |
| `core/compute_system/compute_system.py` | internal_dynamics 主线的老板 | ❌ 还是旧版本：`submit()` 累积列表 + `allocate()` 按 `source` 比例分配，完全没有 `Sampler`，没有"选唯一赢家"这一步 |

**`core/compute_system/compute_system.py` 需要重写**，参照 `camera_compute.py` 已经验证过的模式，同时保留 `archive/compute.py` 的"自己局部回血"的电池性质（`step()` 让 `available` 按 `decay` 速率回充，不依赖任何人来"申请"）。

新版大致形状（工程师落地时可以按实际接口调整，这里只给设计骨架）：

```python
class ComputeSystem:
    def __init__(self, capacity=1.0, decay=0.01):
        self.capacity = capacity
        self.available = capacity
        self.decay = decay
        self.sampler = Sampler()          # 私有员工，不对外暴露

    def step(self):
        # 电池自己局部回血，不依赖外部触发
        self.available += (self.capacity - self.available) * self.decay
        self.available = min(self.available, self.capacity)

    def allocate(self, candidates):
        """
        candidates: 多个 organ 各自的 (delta, age, activity) 信号
        每轮只选出唯一赢家，只给赢家算 budget
        """
        winner_index = self.sampler.select(
            deltas, ages, activities, budget=1
        )
        # 只对赢家计算 budget，其余 organ 拿到空结果
        ...
```
*****************
class ComputeSystem:


    def __init__(self):

        self.available = capacity

        self.sampler = Sampler()



    def step(self):

        self.available += recovery



    def request(
        self,
        candidates
    ):

        winner = self.sampler.select(
            candidates,
            budget=1
        )


        if winner is None:

            return None


        return {
            "energy":
                self.available
        }
		
重点：

ComputeSystem 不知道：

clip.apply_compute()
也不知道：

planet.step()		
**********************
---

## 五、顺手发现的两处代码碎屑（现在的 `core/compute_system/compute_system.py` 里）

- 第 44 行：忘删的调试 `print("submit:", request)`
- 第 183-186 行：`return result` 之后还有一段永远执行不到的死代码（`print("allocation result:", allocation)`，且 `allocation` 变量在这里根本没定义过，若真执行到会直接报错，只是因为在 `return` 之后所以从未触发）

重写时一并清掉。

---

## 六、分工建议

- **产品/架构侧（甲方 + 我）**：负责确认"唯一注意力"这类设计原则、判定某个实现是否符合"同构"精神、发现协议表和最简种子之间的偏差。
- **工程师**：负责按上面第四节的骨架，把 `core/compute_system/compute_system.py` 重写为符合 `archive/compute.py` + `camera_compute.py` 双重参照的版本，并清理第五节提到的碎屑。

如果工程师在实现过程中发现骨架里有没考虑到的边界情况（比如所有 organ 本轮信号都是 0 时怎么处理、`Sampler.select(budget=1)` 返回空数组时怎么处理），建议先把具体场景发回来讨论，不要自行假设，这也是这次几十轮沟通里反复验证过的教训——接口不对齐、假设不确认，会导致连续几轮的返工。
*****************
source 是人为标签。

新的思想：

状态自己竞争。

*******
archive 四文件的精神：

planet.py
    状态 + 规则


compute.py
    能量 + 回充


io.py
    流动


observer.py
    测量
*********
organ 接口统一
以后所有 organ：

必须有：

receive(packet)

step()

snapshot()

activity()

apply_compute()
但是不是强制全部存在。
********************
