# CIMA0 Phase5_7 Architecture

## 0. Core Principle

CIMA0 Phase5_7 is an internal dynamic system.

External input does not directly become meaning.

The pipeline is:

External disturbance
        |
        v
Internal field interaction
        |
        v
Observation
        |
        v
Selection
        |
        v
Computation
        |
        v
Internal evolution


No module should bypass this structure.

---

# 1. Overall Topology


                    External World
                         |
                         |
                      Camera
                         |
                         v

                  IO / Router Layer

                         |
                         v


              +----------------------+
              |  InternalDynamics    |
              +----------------------+

                         |
        ----------------------------------
        |                |               |
        v                v               v


   PlanetField       Organs          Memory


        |              |
        |              |
        v              v


 Planet Cloud     Organ Cloud


        \             /
         \           /
          \         /
           v       v


             CloudCollision


                   |
                   v


             Collision Signal


                   |
                   v


            AttentionField


                   |
                   v


             ComputeSystem


                   |
                   v


              Sampler


                   |
                   v


          ObservationMemory


                   |
                   |
                   +----------------+
                                    |
                                    v

                         Future Sampling Adaptation



---

# 2. Module Responsibility


## PlanetField

Role:

Internal continuous dynamic field.


Owns:

- internal state
- evolution rule


Does:

- evolve itself
- provide snapshot
- provide projection


Does NOT:

- understand observation
- know camera
- know CLIP


Interface:
snapshot()

collision_projection()

evolve()


---

# 3. Organ System


## CLIPField


Role:

Visual internal organ.


Input:
camera packet

{
bytes,
shape,
dtype
}


Output:

internal visual cloud.


Owns:
self.cloud

self.internal_activity

self.dirty


Does NOT:

- classify image
- produce semantic meaning


Interface:
receive()

step()

collision_projection()

activity()



---

# 4. Cloud Layer


Cloud is not the original field.

Cloud is:

A temporary reduced representation
for interaction.


Example:


PlanetField

(large internal field)

        |
        v

planet_cloud

{
 mean,
 energy,
 variance,
 density
}



CLIPField

(high dimensional feature field)

        |
        v

clip_cloud


Cloud purpose:

- comparison
- interaction
- resource competition


Cloud does NOT replace original field.



---

# 5. CloudCollision


Role:

Relationship calculation.


Input:
planet_cloud

clip_cloud
Output:
collision_result

{
collision,
distance,
interaction
}


Does NOT:

- modify clouds
- select winner
- allocate compute
- interpret meaning



---

# 6. Signal Flow


Collision:
CloudCollision
    |
    v
collision_result	
    |
    v
signals[]
    |
    |
    +------------+
    |            |
    v            v
AttentionField ComputeSystem



---

# 7. AttentionField


Role:

Short term competition field.


Input:

signals


Output:

attention state


Does:

- accumulate importance


Does NOT:

- execute computation
- change organs



---

# 8. ComputeSystem


Role:

Resource allocation.


Input:

signals


Output:

winner / budget


Example:
COMPUTE WINNER: clip


Meaning:

CLIP receives update budget.


Not:

CLIP is superior.



---

# 9. Sampler


Role:

Select local observation positions.


Current:

Static priority:
priority =
age * 0.25
+
activity * 0.35
+
delta * 0.40


Problem:

Weights are externally defined.


Future:

Weights become internal adaptive variables.


---

# 10. ObservationMemory


Location:
core/memory/

NOT:
core/observer/


Reason:


Observer:

"What do I see now?"


ObservationMemory:

"What observations have happened before?"



Stores:
observation events

age history

activity history

delta history

selection history


Does NOT store:

- complete field
- original image
- semantic information



---

# 11. Observer


Location:
core/observer/


Role:

External read-only observer.


Does:
snapshot
extract
package


Does NOT:

- influence evolution
- store adaptive state



---

# 12. Future Adaptive Loop


Target:

Internal Field
  |
  v	
Sampler
  |
  v
Observation Event
  |
  v
ObservationMemory
  |
  v
Parameter Adaptation
  |
  v
Sampler


Future adaptive parameters:

w_age

w_activity

w_delta


They should evolve through:

- usage
- decay
- competition
- feedback


Not fixed constants.



---

# 13. Current Phase5_7 Status


Completed:

[x] Camera -> Router

[x] InternalDynamics container

[x] PlanetField evolution

[x] CLIPField organ

[x] Cloud projection

[x] CloudCollision

[x] Collision -> Signal bridge

[x] Attention integration

[x] Compute competition



Missing:

[ ] ObservationMemory

[ ] Sampler integration

[ ] Adaptive sampling weights

[ ] Long term self-adjustment



---

# 14. Current Development Rule


Before adding a new module:

Answer three questions:


1. Who owns this state?

2. Who can modify this state?

3. Who can only observe this state?


If these are unclear:

Do not add code.
Fix topology first.
collision_projection() 只负责投影，不是压缩内部世界。

PlanetField.state (128,128) 只是当前实现的局部可见截面，不代表内部空间大小。

Sampler 不应该自己产生记忆。

ObservationMemory 是连接“观察”和“未来选择”的桥。  

## State Ownership Table
| 模块                | 拥有状态            | 允许修改 |
| ----------------- | --------------- | ---- |
| PlanetField       | 内部场             | 自己   |
| CLIPField         | visual cloud    | 自己   |
| CloudCollision    | last_result     | 自己   |
| AttentionField    | attention state | 自己   |
| ComputeSystem     | budget state    | 自己   |
| Sampler           | selection state | 自己   |
| Observer          | 无               | 无    |
| ObservationMemory | 观察历史            | 自己   |
ObservationMemory
目前不存在。

它应该是：

core/

    memory/

        observation_memory.py
它和：

observation_cache.py
完全不同。

区别：
|      | Cache      | Memory     |
| ---- | ---------- | ---------- |
| 目的   | 暂存         | 学习历史       |
| 生命周期 | 短          | 长          |
| 是否演化 | 否          | 是          |
| 影响未来 | 否          | 是          |
| 位置   | observer辅助 | internal状态 |
## State Ownership


PlanetField

owns:
    internal field


CLIPField

owns:
    visual cloud


CloudCollision

owns:
    last comparison result


CloudState

owns:
    transient events


AttentionField

owns:
    attention state


ComputeSystem

owns:
    budget allocation


Sampler

owns:
    selection process


ObservationCache

owns:
    temporary snapshot


ObservationMemory

owns:
    historical observation adaptation
