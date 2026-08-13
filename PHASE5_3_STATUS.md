下面整理为：

```text
CIMA0/PHASE5_3_STATUS.md
```

定位：

* 记录 **当前阶段真实状态**
* 不解释理论（理论放 `CORE_LAWS.md` / `ARCHITECTURE.md`）
* 只记录：完成、确认、问题、下一步

---

# CIMA0 Phase5_3 Status

## 0. Phase Definition

Phase5_3目标：

建立 CIMA0 内部动力闭环。

核心方向：

```
External byte stream

        |

        v

Internal disturbance coupling

        |

        v

Planet internal dynamics

        |

        v

CloudField persistent structures

        |

        v

Observer local interpretation
```

---

# 1. Confirmed Completed

---

## 1.1 InternalDynamics Interface

Status:

```
CONFIRMED
```

Location:

```
core/internal_dynamics/
```

Role:

连接：

```
external system

        |

        v

internal dynamics
```

---

Responsibilities:

* receive external disturbance
* advance internal evolution
* expose snapshot

---

Does NOT know:

```
camera

cloud

observer meaning

display
```

---

Current conclusion:

```
InternalDynamics boundary is correct.
```

No redesign required.

---

# 2. Main Loop Status

Status:

```
CONFIRMED
```

Current main flow:

```
Camera

  |

  v

CameraPlanet

  |

  v

packet(bytes, shape, dtype)

  |

  v

InternalDynamics.receive()

  |

  v

Planet

  |

  v

InternalDynamics.step()

  |

  v

Planet evolution

  |

  v

snapshot

  |

  v

Observer

  |

  v

Display
```

---

Confirmed:

* Camera does not directly control display
* Camera does not directly replace internal state
* InternalDynamics remains the boundary

---

# 3. Planet Status

Status:

```
LOCKED
```

Location:

```
archive/planet.py
```

---

Definition:

```
CIMA0 seed
```

---

Rules:

```
DO NOT MODIFY

DO NOT OPTIMIZE

DO NOT REPLACE

DO NOT DUPLICATE
```

---

Allowed:

```
run

snapshot

observe
```

---

Current properties:

* self-existing
* self-evolving
* independent

---

Planet role:

```
internal dynamical core
```

Answers:

```
How does the internal field move now?
```

---

# 4. Planet Runtime Usage

Current situation:

There are runtime implementations such as:

```
PlanetField
```

Need clarification:

They are not replacements.

Relationship:

```
archive.Planet

        |

        v

reference / runtime usage
```

---

Pending decision:

Confirm whether runtime optimized versions are:

* temporary test implementation

or

* forbidden duplication

Current principle:

```
archive.Planet remains the only source.
```

---

# 5. Camera Status

## CameraPlanet

Status:

```
CONFIRMED
```

Role:

Physical input boundary.

Input:

```
BGR frame
```

Output:

```
{
 bytes,
 shape,
 dtype
}
```

---

CameraPlanet does NOT:

* resize
* sample
* interpret
* extract features

---

# 6. CameraObserver Status

Status:

```
PENDING CLEANUP
```

Current issue:

Old design:

```
Camera

 |

v

CameraObserver

 |

v

Sampler
```

contains:

* visual sampling logic
* compute scheduling coupling

---

Current architecture:

```
Camera

 |

v

Internal Coupling

 |

v

Planet / CloudField
```

---

Need decision:

CameraObserver should become:

* pure observation module

or

* removed from active path

---

# 7. Sampler Status

Status:

```
PARTIALLY CONFIRMED
```

Role:

General compute resource scheduler.

---

Sampler knows:

```
delta

age

activity

budget
```

---

Sampler does NOT know:

```
camera meaning

semantic importance

Planet structure

CloudField meaning
```

---

Pending:

Current scoring mechanism:

```
score =
delta*w_delta
+
age*w_age
+
activity*w_activity
```

Initial:

```
w_delta = 1.0
w_age = 0.01
w_activity = 0.1
```

Future:

adaptive weight evolution:

```
w_delta += reward * gradient

w_age += reward * gradient

w_activity += reward * gradient
```

Need define:

* gradient source
* reward source
* update location

---

# 8. CloudField Status

Status:

```
NOT COMPLETED
```

Current problem:

Previous implementations mixed concepts:

Incorrect:

```
CloudField = external cache

CloudField = image compression

CloudField = Planet copy
```

---

Current definition:

```
CloudField ⊂ Planet space
```

---

CloudField should represent:

* slow variables
* persistent structures
* local stable regions
* long-term relationships

---

CloudField is:

```
internal structure generation layer
```

---

Need redesign:

Current questions:

1. How does CloudField observe Planet?
2. How does CloudField maintain persistence?
3. How does external disturbance influence CloudField?
4. How does CloudField produce structures without becoming another Planet?

---

# 9. External Disturbance Coupling

Status:

```
NOT COMPLETED
```

Current problem:

Previous:

```
Camera -> Planet.receive()
```

is too direct.

---

Required:

```
External bytes

       |

       v

Internal coupling

       |

       v

Planet + CloudField evolution
```

---

Need design:

Internal collision mechanism:

* empty state
* empty position
* negative value
* zero value

External input becomes:

```
disturbance
```

not:

```
control signal
```

---

# 10. Current Architecture Problems

## Problem 1

CloudField old design still contains:

```
external field processing logic
```

Need remove.

---

## Problem 2

CameraObserver still contains:

```
Sampler coupling
```

Need separate.

---

## Problem 3

Planet runtime duplication risk.

Need ensure:

```
archive.Planet = only source
```

---

## Problem 4

Need establish:

```
Internal Coupling Layer
```

between external stream and internal world.

---

# 11. Current Priority Order

## Priority 1

Complete CloudField redesign.

Goal:

```
Planet internal local persistent structure
```

---

## Priority 2

Create Internal Coupling Layer.

Goal:

```
camera bytes

        |

        v

internal disturbance
```

---

## Priority 3

Clean CameraObserver.

Goal:

remove:

```
camera meaning

sampling decision

compute allocation
```

---

## Priority 4

Finalize Sampler adaptive mechanism.

Goal:

generic resource evolution.

---

# 12. Current Frozen Decisions

```
archive.Planet is locked.

InternalDynamics design is correct.

Camera does not control Planet.

CloudField is not Planet copy.

Observer never knows global internal state.

Sampler does not understand meaning.
```

---

# Current Phase5_3 Position

```
          LOCKED

       archive.Planet

            |

            v


       InternalDynamics

            |

            v


       (missing)

 Internal Coupling Layer

            |

            v


       CloudField

            |

            v


       Observer
```

---

# Next Development Target

## CloudField redesign

Before writing code, answer:

```
What is the minimum state CloudField must keep
to represent a persistent local structure inside Planet?
```

---

这份作为每天启动时看的状态文件即可。打开它以后，不需要重新回忆前面的推导，只需要从 **CloudField redesign** 继续。
