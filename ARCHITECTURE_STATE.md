下面整理为：

```text
CIMA0/ARCHITECTURE.md
```

定位：

* 不是最高公理（最高公理在 `CORE_LAWS.md`）
* 是架构关系说明
* 用于恢复系统理解
* 指导代码边界设计

---

# CIMA0 Architecture

## 0. Purpose

CIMA0 is not an input-output mapping system.

It is an internally existing dynamical system.

The system first maintains its own existence and evolution.

External inputs do not create the internal world.

They only participate as disturbances that influence an already-running internal process.

The fundamental relationship:

```
Internal existence
        |
        v
Continuous evolution
        |
        v
External disturbance coupling
        |
        v
Local observation
        |
        v
Interpretation
```

---

# 1. Overall Architecture

```
                 External World

                       |
                       |
                       v


              Camera / External Stream

                       |
                       |
                       v


              Internal Coupling Layer

                       |
                       |
                       v


        +--------------------------------+
        |                                |
        |             Planet             |
        |                                |
        |       Internal Dynamics Core   |
        |                                |
        +--------------------------------+

                       |
                       |
              Continuous evolution

                       |
                       |
                       v


        +--------------------------------+
        |                                |
        |          CloudField            |
        |                                |
        |    Internal Slow Structures    |
        |                                |
        +--------------------------------+

                       |
                       |
                       v


                  Observer

                       |
                       |
                       v


             Local Interpretation
```

---

# 2. Planet Architecture

## 2.1 Definition

Planet is the internal dynamical core.

Location:

```
archive/planet.py
```

Planet is the CIMA0 seed.

It represents:

```
the internal world itself
```

---

## 2.2 Planet Responsibilities

Planet only knows:

```
state

local interaction

evolution
```

Planet answers:

> How does the internal field move now?

---

Planet provides:

* continuous internal evolution
* local interaction
* self-maintenance
* non-repeating dynamics
* stable long-term existence

---

## 2.3 Planet Independence

Planet must continue running without:

```
camera

observer

display

compute allocation

external input
```

The existence of Planet does not depend on observation.

---

## 2.4 Planet and External Input

External input is not control.

Wrong:

```
Camera
 |
 v
Planet.state overwrite
```

Correct:

```
External stream

       |
       v

Internal coupling

       |
       v

Planet tendency change
```

External input can:

* perturb
* influence evolution direction
* modify future trajectory

External input cannot:

* replace state
* control evolution
* define internal rules

---

# 3. CloudField Architecture

## 3.1 Definition

CloudField is an internal slow-variable structure.

It is not:

* Planet copy
* Planet snapshot storage
* external feature map
* image representation

---

CloudField represents:

```
persistent local structures
inside Planet space
```

---

# 3.2 Planet and CloudField Relationship

## Time relationship

Planet and CloudField coexist.

Not:

```
Planet(t)

    |

    v

CloudField(t+100)
```

Correct:

```
t0:

Planet + CloudField


t1:

Planet + CloudField


t2:

Planet + CloudField
```

They continuously co-evolve.

---

## Spatial relationship

CloudField is a subset of Planet space.

```
Planet
+--------------------------------+
|                                |
|                                |
|       +--------------+         |
|       |              |         |
|       | CloudField   |         |
|       |              |         |
|       +--------------+         |
|                                |
+--------------------------------+
```

Relationship:

```
CloudField ⊂ Planet space
```

---

CloudField is not the whole Planet.

It represents local regions where long-term relationships emerge.

---

# 3.3 CloudField Formation

CloudField emerges from:

```
Planet continuous evolution

+

internal interaction

+

external disturbance
```

Long-term effects create:

* persistent states
* sticky regions
* local stable structures
* correlated areas

---

# 3.4 CloudField Responsibilities

CloudField manages:

```
slow variables

persistent structures

local stability

long-term relationships
```

CloudField answers:

> Which structures persist inside this continuously evolving system?

---

# 3.5 CloudField Interpretation

CloudField itself does not contain meanings.

It does not store:

```
attractor

basin

object

concept
```

Those are Observer interpretations.

Actual existence:

```
CloudField state structure
```

Interpretation:

```
"this looks like a basin"

"this behaves like an attractor"
```

belongs to Observer.

---

# 4. External Input Architecture

## 4.1 Camera Role

Camera is an external boundary.

Camera provides:

```
byte stream
```

Camera does not provide:

```
meaning

objects

features

semantics
```

---

Camera pipeline:

```
Camera

   |

   v

CameraPlanet

   |

   v

Raw packet

(bytes, shape, dtype)
```

---

## 4.2 Input Principle

External data enters as disturbance.

Not as instruction.

Not as replacement.

Not as world definition.

---

Correct:

```
byte stream

      |

      v

internal collision / coupling

      |

      v

change internal tendency
```

---

# 5. Observer Architecture

## 5.1 Definition

Observer is a readonly observation system.

Observer does not create the internal world.

Observer only samples the existing world.

---

## 5.2 Observer Input

Observer receives:

```
local snapshot
```

Not:

```
complete internal state
```

---

Relationship:

```
Internal World

       |
       |
       v

snapshot()

       |
       v

Observer
```

---

# 5.3 Observer Limitation

Observer can never know the complete internal state.

Because:

```
Internal state:

P


Observation:

O = f(P)
```

The mapping:

```
f
```

is not one-to-one.

Therefore:

Different internal states can produce similar observations.

---

Observer does not know:

* complete history
* complete space
* complete future trajectory

---

# 5.4 Observer Interpretation

Observer may describe:

* basin
* attractor
* special region
* pattern
* structure

But these are:

```
interpretations of observation
```

not:

```
absolute internal labels
```

---

# 6. Compute System and Sampler

## 6.1 Role

Sampler is a general resource scheduling system.

It knows:

```
task

resource

budget

priority
```

---

Sampler does not know:

```
camera meaning

Planet meaning

CloudField meaning

semantic importance
```

---

Sampler answers:

> Which computation should receive available resources?

Not:

> Which internal structure is meaningful?

---

# 7. Module Boundary Rules

## Planet

Knows:

```
state
interaction
evolution
```

Does not know:

```
camera
cloud
observer
display
```

---

## CloudField

Knows:

```
internal structure
slow variables
local persistence
```

Does not know:

```
semantic meaning
display
external interpretation
```

---

## Observer

Knows:

```
observation
sampling
measurement
```

Does not know:

```
how to control evolution
```

---

## Camera

Knows:

```
physical acquisition
```

Does not know:

```
internal meaning
```

---

# 8. Final Conceptual Model

```
                 External World


                       |
                       v


              External Disturbance


                       |
                       v


        +--------------------------------+
        |                                |
        |             Planet             |
        |                                |
        |       Fast Internal Dynamics   |
        |                                |
        +--------------------------------+


                       |
                       |
                long evolution


                       v


        +--------------------------------+
        |                                |
        |          CloudField            |
        |                                |
        |      Slow Internal Structures  |
        |                                |
        +--------------------------------+


                       |
                       v


                  Observer


                       |
                       v


              Local Interpretation
```

---

# Core Statement

> Planet maintains the existence and movement of the internal world. CloudField represents persistent local structures formed inside that world. Observer can only interpret local projections of the internal world and can never possess the complete internal reality.

---

这份作为 `ARCHITECTURE.md`，后续代码评审时可以直接作为边界依据。
