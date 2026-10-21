# CIMA0 Topology

## 0. Purpose

`TOPOLOGY.md` describes the **actual structural topology of CIMA0**.

It answers:

* What objects exist?
* Which object owns which state?
* Which object can modify that state?
* Which interfaces connect objects?
* What data crosses each boundary?
* Which dependencies are explicit?
* Which relationships are local?
* Which relationships must not exist?

This document is different from:

* `CONSTITUTION.md` — what must never be violated
* `ARCHITECTURE.md` — architectural principles and conceptual structure
* `DATA_FLOW.md` — movement of data, state, events, and resources
* `STATE_OWNERSHIP.md` — detailed state ownership
* phase documents — historical implementation records

This document describes the **code topology**.

---

# 1. Fundamental Topological Rule

CIMA0 has no God View.

There is no runtime object that is required to know:

* all organs
* all internal states
* all coordinates
* all events
* all observations
* all resource decisions
* all meanings
* all future actions

No object is the universal owner of the system.

The topology is therefore not:

```text
                    Main Controller
                          |
        +-----------------+-----------------+
        |                 |                 |
      Planet            CLIP              Memory
        |                 |                 |
        +-----------------+-----------------+
                          |
                       Decision
                          |
                       Action
```

The topology is composed of locally bounded objects:

```text
                 External Boundary
                        |
                     Camera
                        |
                       IO
                        |
                    Packet
                        |
               +--------+--------+
               |                 |
          Internal Dynamics   Other Boundary
               |
       +-------+--------+
       |                |
   PlanetField       Organs
       |                |
     Planet          CLIPField
       |                |
       +-------+--------+
               |
        Local Interaction
               |
          CloudCollision
               |
        transient result
               |
        resource opportunity
               |
         ComputeSystem
               |
          selected organ
               |
        local computation
```

The diagram is conceptual only.

It does **not** imply that `InternalDynamics` has global knowledge or that every relationship is a permanent linear pipeline.

---

# 2. Repository-Level Topology

The current structural domains are approximately:

```text
core/
│
├── io/
│   └── transport/
│
├── internal_dynamics/
│   │
│   ├── ...
│   │
│   └── organs/
│       └── clip_field.py
│
├── planet/
│   └── archive.py
│
├── observer/
│
├── memory/
│
└── ...
```

The exact file layout may evolve.

The important distinction is between:

```text
module location
```

and:

```text
architectural ownership
```

A file's directory does not automatically give it authority over another object's state.

---

# 3. Core Runtime Objects

The current topology contains several important runtime objects.

## 3.1 InternalDynamics

`InternalDynamics` is the internal runtime boundary/container.

Its responsibility is to provide the local environment in which internal entities interact.

It may hold references to:

* `PlanetField`
* registered organs
* `ComputeSystem`
* collision system
* observation components
* temporary runtime state

It must not become:

* global semantic interpreter
* global state owner
* global observer
* permanent decision maker
* permanent winner
* universal database
* universal coordinate authority

Its references are dependencies, not ownership of every referenced object's state.

---

# 4. Planet Topology

The Planet side contains two conceptually different objects:

```text
Planet
  ^
  |
PlanetField
```

These must not be conflated.

## 4.1 Planet

Planet is the underlying dynamical substrate.

Conceptually:

```text
Planet
├── evolution rules
├── internal dynamics
└── autonomous state
```

Planet owns its own dynamical behavior.

Other components must not:

* replace Planet's rules
* duplicate Planet's rules
* optimize Planet's rules from outside
* turn Planet into a passive array
* directly assume knowledge of its complete internal space

Planet may expose a snapshot or evolution interface.

---

## 4.2 PlanetField

`PlanetField` is an interface/field layer around Planet's evolving state.

Current implementation contains state such as:

```python
state
previous_state
pending_disturbance
age
compute_budget
```

The important ownership relation is:

```text
PlanetField
    |
    +-- owns current field representation
    |
    +-- receives disturbance
    |
    +-- invokes Planet evolution
    |
    +-- exposes local snapshot/projection
```

A disturbance enters through:

```text
PlanetField.receive(disturbance)
```

The disturbance becomes pending state.

Evolution occurs through:

```text
PlanetField.step()
```

The field then delegates evolution to Planet where appropriate.

Therefore:

```text
external disturbance
        |
        v
PlanetField.receive()
        |
        v
pending_disturbance
        |
        v
PlanetField.step()
        |
        v
Planet.evolve(...)
        |
        v
PlanetField.state
```

The above describes an interface relationship, not a global execution authority.

---

# 5. Organ Topology

Organs are independent internal entities.

Current important organ:

```text
CLIPField
```

Organs own their own internal states.

The topology is:

```text
InternalDynamics
      |
      +---- registered organ
                 |
              CLIPField
```

Registration gives `InternalDynamics` a reference.

It does not transfer ownership of the organ's internal state.

---

# 6. CLIPField

`CLIPField` is a local visual internal organ.

Its external boundary is a camera packet.

Conceptually:

```text
Camera Packet
     |
     v
 CLIPField
     |
     +-- input state
     +-- model state
     +-- transformer layers
     +-- complete cloud
     +-- local responses
     +-- transient winner
     +-- compute budget
```

Current cloud representation:

```text
(12, 50, 768)
```

This represents the current internal visual field produced by the CLIP processing path.

The cloud belongs to `CLIPField`.

No other component becomes its owner merely because it receives a projection of it.

---

# 7. CLIPField Input Boundary

The camera packet is structurally represented by information such as:

```text
source
bytes
shape
dtype
```

The packet describes data.

It does not contain semantic interpretation.

The camera boundary therefore remains:

```text
Camera
   |
   v
raw homogeneous byte packet
   |
   v
CLIPField
```

The packet is not:

```text
object
person
meaning
command
decision
```

unless a downstream local component independently derives such information.

---

# 8. CLIPField Internal State

The internal cloud:

```text
cloud.shape == (12, 50, 768)
```

must be treated as CLIPField-owned state.

The complete cloud must not be globally collapsed merely because another component needs a smaller interaction representation.

Therefore:

```text
CLIP internal state
        |
        +------ complete state remains owned by CLIPField
        |
        +------ local response
        |
        +------ interaction projection
```

An interaction projection is not a replacement for the cloud.

---

# 9. CLIP Local Response

CLIPField can derive local response information from its own state.

Current response structure includes:

```text
layer_activity
winner_layer
winner_response
internal_activity
```

The winner is transient.

Topology therefore treats:

```text
winner_layer
```

as an event/result of a local computation opportunity.

It is not:

```text
global winner
permanent focus
system priority
global coordinate
global authority
```

A later interaction may produce another winner.

---

# 10. Compute Budget Inside CLIPField

CLIPField may receive a computation opportunity.

Current local state includes:

```text
compute_budget
```

The topology is:

```text
ComputeSystem
      |
      | resource allocation
      v
  CLIPField
      |
      v
 local computation
```

The allocation does not tell CLIPField what semantic result to produce.

For example:

```python
{"amount": 1.0}
```

means:

```text
computation resource available
```

not:

```text
perform operation X
```

The organ owns the decision about how its own computation proceeds.

---

# 11. ComputeSystem

`ComputeSystem` owns the finite computation resource.

Its topology is:

```text
signals
   |
   v
ComputeSystem
   |
   +-- availability
   +-- selection
   +-- allocation
   +-- consumption
   +-- recovery
```

Current resource behavior includes gradual recovery:

```python
self.available += (
    self.capacity - self.available
) * 0.01
```

The resource system therefore has its own state evolution.

ComputeSystem does not own:

* Planet state
* CLIP state
* collision state
* camera state
* observation truth

---

# 12. Compute Request Boundary

An organ may expose a local request:

```python
{
    "request": "compute"
}
```

This means:

```text
I currently require a computation opportunity.
```

It does not mean:

```text
I am globally important.
```

It does not mean:

```text
I must win.
```

It does not mean:

```text
ComputeSystem should execute my operation.
```

The topology is:

```text
Organ
  |
  | local request
  v
ComputeSystem
  |
  | finite opportunity
  v
Organ
```

This is a resource relationship.

It is not command delegation.

---

# 13. Winner Topology

The result called `winner` exists only within the scope of a particular computation-selection event.

Conceptually:

```text
local requests
      |
      v
selection
      |
      v
temporary winner
      |
      v
resource allocation
```

After the event, the winner has no permanent architectural authority.

Therefore the topology must not be interpreted as:

```text
winner
  |
  v
leader
  |
  v
controller
```

It is:

```text
winner
  |
  v
temporary resource recipient
```

---

# 14. Commit Boundary

The current commit path is a resource handoff.

Conceptually:

```text
selection result
       |
       v
commit
       |
       v
ComputeSystem.consume()
       |
       v
organ.apply_compute()
       |
       v
organ.execute local computation
```

`commit()` must not become a semantic dispatcher.

Its responsibility is limited to transferring an already allocated computation opportunity into the selected local entity.

---

# 15. Collision Topology

Collision is an internal interaction mechanism.

It is not a global controller.

Current conceptual boundary:

```text
Planet local state
        \
         \
          v
     CloudCollision
          ^
         /
        /
CLIP local state
```

The collision object computes local relationships.

It does not own:

* PlanetField state
* CLIPField cloud
* ComputeSystem budget
* ObservationMemory
* semantic interpretation

---

# 16. Collision Primitive Rules

The collision layer currently distinguishes states such as:

```text
EMPTY_SLOT
EMPTY_VALUE
ZERO_VALUE
NONZERO_VALUE
```

and collision relations such as:

```text
PENETRATE
CHANGE
BOUNCE
```

These are local rules.

The collision layer may produce:

```text
candidate_change
collision_result
relations
```

These are interaction results.

They are not automatically committed into the source state.

---

# 17. Critical Collision Boundary

CIMA0 must not implement:

```text
all Planet states
        ×
all CLIP states
```

as a collision topology.

For example:

```text
16,384 Planet values
        ×
76,800 CLIP values
```

would create:

```text
1,258,291,200
```

comparisons.

The problem is not merely computational cost.

The deeper problem is architectural:

> There is no architectural reason for every Planet coordinate to know every CLIP coordinate.

Such a topology would implicitly create a global relationship that CIMA0 explicitly rejects.

---

# 18. No Artificial Coordinate Mapping

Planet and CLIP have different internal topologies.

For example:

```text
Planet
  internal coordinates
        ≠
CLIP
  (layer, token, dimension)
```

The topology must not invent:

```text
Planet[x,y] <-> CLIP[layer,token,dimension]
```

merely because the implementation needs a convenient index.

There is no assumed universal coordinate system.

If interaction occurs, it must arise from a bounded local relationship.

---

# 19. Local Interaction Topology

The intended interaction topology is:

```text
CLIP local event
       |
       v
bounded interaction context
       |
       v
Planet local interaction
       |
       v
collision
       |
       v
changed local state
```

The system does not need to know the complete relationship between the two internal spaces.

Only the locally relevant interaction needs to exist.

---

# 20. Camera as External Homogeneous Source

The camera is an external source.

Its role is:

```text
world
 |
 v
camera
 |
 v
bytes
```

The byte stream is homogeneous external input.

It is not itself meaning.

The camera does not know:

* Planet
* CLIP
* collision
* attention
* compute allocation
* observation
* memory

This keeps the external boundary clean.

---

# 21. Local Event Reconstruction

When an internal event needs to relate back to the physical input, the original homogeneous camera data may be used to derive the bounded local physical region corresponding to that event.

The important distinction is:

```text
homogeneous input
       |
       v
local event
       |
       v
bounded reconstruction
       |
       v
local interaction
```

This is not:

```text
global camera map
       |
       v
global internal coordinate map
```

No permanent global camera-to-internal topology is required.

---

# 22. Changed State and Re-Encoding

A local interaction may produce changed state.

Conceptually:

```text
local interaction
       |
       v
changed internal state
       |
       v
homogeneous representation
```

Re-encoding preserves the external/internal boundary.

It does not mean that the system has acquired a semantic interpretation of the original bytes.

---

# 23. Cloud Topology

Clouds are interaction representations.

They are not automatically:

```text
the world
```

or:

```text
the complete internal state
```

A cloud may be:

```text
source state
    |
    v
interaction projection
```

The source state remains owned by its source entity.

Therefore:

```text
PlanetField state
      |
      +---- projection --> collision

CLIPField cloud
      |
      +---- local projection --> collision
```

Collision must not silently take ownership of either source.

---

# 24. CloudState

`CloudState` is transient.

It may represent:

* local interaction
* temporary relation
* current event
* bounded collision context

It must not silently become:

```text
permanent global state
```

or:

```text
system-wide truth database
```

---

# 25. Attention Topology

Attention is temporary relevance.

It is not a global consciousness object.

An attention field may represent:

```text
current local competition
```

but must not become:

```text
global importance table
```

or:

```text
permanent priority authority
```

Attention may disappear, decay, or be replaced by another local event.

---

# 26. Observation Topology

Observation is downstream of internal events.

The observer is read-only.

Conceptually:

```text
internal state/event
       |
       v
snapshot
       |
       v
observer
       |
       v
description
```

The observer does not:

* modify Planet
* modify CLIP
* allocate compute
* choose a winner
* authorize collision
* determine future causality

Observation describes what has already occurred.

---

# 27. ObservationCache

`ObservationCache` is short-lived.

Its role is:

```text
snapshot
   |
   v
temporary comparison
   |
   v
use
   |
   v
discard
```

It must not become the permanent source of truth.

A cache exists to support a local observation operation.

It is not system memory.

---

# 28. ObservationMemory

`ObservationMemory` is conceptually different from `ObservationCache`.

```text
ObservationCache
    |
    +-- temporary
    +-- use once
    +-- discard

ObservationMemory
    |
    +-- historical
    +-- persistent/adaptive
    +-- supports future adaptation
```

ObservationMemory may eventually retain historical observations and influence future local sampling parameters.

It must not become:

```text
complete system history
```

or:

```text
God View database
```

---

# 29. Sampler Topology

Sampler owns selection behavior.

It does not own memory.

Therefore:

```text
Sampler
   |
   +-- selects local observation target
   |
   +-- uses available local signals
```

and separately:

```text
ObservationMemory
   |
   +-- retains historical observation information
```

The topology must not become:

```text
Sampler
   |
   +-- creates memory
   +-- owns history
   +-- knows complete system
```

---

# 30. Adaptation Topology

Future adaptive behavior should remain local.

Conceptually:

```text
observation history
       |
       v
local adaptation
       |
       v
local parameter
       |
       v
future local selection
```

Adaptation should not require a global optimizer.

For example, a sampler may adapt:

```text
sampling weights
decay rates
local preference
competition parameters
```

without acquiring knowledge of the complete internal system.

---

# 31. Observer vs Memory

These are distinct roles.

```text
Observer
    |
    +-- describes
    +-- read-only
    +-- post-hoc

ObservationMemory
    |
    +-- retains history
    +-- supports adaptation
    +-- has its own state
```

Neither is the global owner of system state.

---

# 32. State Ownership Topology

The primary ownership relationships are:

| State                       | Owner                    | Others may                        |
| --------------------------- | ------------------------ | --------------------------------- |
| Planet dynamical state      | Planet                   | observe/use interface             |
| PlanetField state           | PlanetField              | receive disturbance               |
| pending disturbance         | PlanetField              | none                              |
| CLIP cloud                  | CLIPField                | receive projection                |
| CLIP layer activity         | CLIPField                | observe                           |
| CLIP winner                 | CLIPField                | observe transient result          |
| CLIP compute budget         | CLIPField                | receive allocation                |
| collision result            | CloudCollision           | observe                           |
| temporary cloud interaction | Cloud/interaction layer  | consume locally                   |
| attention state             | AttentionField           | observe/use locally               |
| compute availability        | ComputeSystem            | request/consume                   |
| sampler parameters          | Sampler                  | local adaptation                  |
| observation cache           | ObservationCache         | temporary read                    |
| observation memory          | ObservationMemory        | query/update through its boundary |
| camera packet               | transport/input boundary | consume                           |

No row should be interpreted as granting another object global knowledge.

---

# 33. Dependency Injection

Important runtime dependencies should be explicit.

For example:

```python
self.compute = compute
self.collision = collision
```

Dependencies should be supplied from outside rather than silently reconstructed inside unrelated objects.

This preserves:

* testability
* ownership boundaries
* topology visibility
* local responsibility

It also prevents an object from secretly creating an architectural subsystem that it does not own.

---

# 34. No Hidden Dependency Construction

Avoid patterns such as:

```python
class InternalDynamics:

    def __init__(self):

        self.collision = CloudCollision(...)
        self.compute = ComputeSystem(...)
        self.observer = Observer(...)
```

when those objects are architecturally independent services.

Prefer explicit dependencies:

```python
class InternalDynamics:

    def __init__(
        self,
        compute=None,
        collision=None,
        observer=None
    ):

        self.compute = compute
        self.collision = collision
        self.observer = observer
```

The dependency graph should remain visible.

---

# 35. No Generic Organ Execution

The existence of an `organs` collection does not imply:

```python
for organ in self.organs.values():
    organ.step()
```

This pattern is dangerous because it silently assumes:

```text
all organs
    |
    v
same execution authority
```

It can also cause an entity to evolve twice when its evolution is already handled elsewhere.

Each local evolution path must have a clear owner.

---

# 36. Planet Evolution Boundary

Planet evolution has a specific boundary.

Current relationship:

```text
PlanetField
    |
    v
Planet.step()/Planet.evolve()
```

The surrounding runtime must not additionally execute Planet as a generic organ.

Therefore:

```text
Planet
```

must not simultaneously participate in:

```text
PlanetField.step()
```

and:

```text
generic organ.step()
```

unless a future architecture explicitly defines such dual evolution.

---

# 37. InternalDynamics Topology

`InternalDynamics` coordinates boundaries without becoming a global mind.

A simplified structural representation is:

```text
                 InternalDynamics
                        |
        +---------------+---------------+
        |               |               |
   PlanetField       Organs          Services
        |               |               |
      Planet        CLIPField      ComputeSystem
                                      |
                                resource boundary

        Collision --------------------+
             |
             +---- local interaction

        Observer ---------------------+
             |
             +---- post-hoc description
```

The important property is that the central drawing position does not imply central knowledge.

`InternalDynamics` is a runtime boundary/container, not a God object.

---

# 38. Data Ownership vs Reference Ownership

A reference does not equal state ownership.

For example:

```python
self.compute = compute
```

means:

```text
InternalDynamics has access to ComputeSystem's interface.
```

It does not mean:

```text
InternalDynamics owns ComputeSystem.available.
```

Likewise:

```python
self.organs["clip"] = clip
```

does not mean:

```text
InternalDynamics owns CLIPField.cloud.
```

Ownership follows responsibility, not pointer location.

---

# 39. Event Topology

An event should be understood as:

```text
local state change
      |
      v
boundary crossing
      |
      v
another local entity receives information
```

rather than:

```text
global controller
      |
      v
command
      |
      v
target
```

This distinction is fundamental.

A component should normally react to what it receives through its boundary.

It should not require knowledge of the entire system in order to act.

---

# 40. Causality Topology

The causal relationship should remain local.

For example:

```text
camera bytes
      |
      v
CLIP input state
      |
      v
CLIP computation
      |
      v
local response
      |
      v
local interaction
      |
      v
collision
      |
      v
local changed state
```

At every boundary, the receiving entity only needs the information required to perform its own responsibility.

No global causal graph is required at runtime.

---

# 41. No Global State Bus

There must not be an implicit object equivalent to:

```python
global_state = {
    "planet": ...,
    "clip": ...,
    "camera": ...,
    "attention": ...,
    "memory": ...,
    "compute": ...
}
```

followed by arbitrary modules reading and modifying everything.

Such a structure would effectively recreate God View through a shared dictionary.

Interfaces must remain bounded.

---

# 42. No Hidden Control Channels

A data packet must not secretly become a control channel.

For example:

```text
camera bytes
```

must not secretly encode:

```text
run CLIP
select Planet
allocate compute
choose winner
```

Similarly, an observation result must not secretly mutate internal causality.

Control and data boundaries must remain explicit.

---

# 43. No Permanent Center

The following must not become permanent centers of authority:

```text
InternalDynamics
ComputeSystem
AttentionField
Sampler
Observer
winner
Memory
CloudCollision
```

Each has a local responsibility.

None is the universal decision point.

---

# 44. Local Knowledge Rule

For every runtime object, the following questions should be answerable:

```text
What does it know?

What does it own?

What can it modify?

What does it receive?

What does it expose?

What event causes it to act?
```

If the answer becomes:

```text
it knows everything
```

the topology is probably wrong.

If an object requires complete knowledge to perform a local responsibility, the boundary should be reconsidered.

---

# 45. Topological Independence of Internal Spaces

Planet and CLIP are independent internal spaces.

Conceptually:

```text
Planet space
+-------------------+
|                   |
|     Planet        |
|                   |
+-------------------+

        X

+-------------------+
|       CLIP        |
| layer/token/dim   |
|                   |
+-------------------+
CLIP space
```

The `X` means:

```text
no predefined universal coordinate equivalence
```

Interaction is possible without requiring identity of topology.

---

# 46. Local Interaction Does Not Require Global Mapping

A major architectural property is:

> Two systems can interact without possessing a complete mapping between their entire internal spaces.

Therefore CIMA0 does not require:

```text
Planet coordinate
        ↕
CLIP coordinate
```

for every possible coordinate.

Instead:

```text
current local event
        |
        v
bounded relation
        |
        v
bounded interaction
```

This is sufficient.

---

# 47. Full State vs Interaction State

These are different topological objects.

```text
FULL INTERNAL STATE
        |
        | projection
        v
INTERACTION REPRESENTATION
        |
        v
LOCAL COLLISION
```

The projection does not replace the source state.

This distinction must be preserved throughout the implementation.

---

# 48. Current CLIP Topology

The current CLIP path can be represented as:

```text
camera packet
     |
     v
CLIPField.receive()
     |
     v
input_packet
     |
     v
dirty
     |
     v
compute request
     |
     v
ComputeSystem
     |
     v
allocation
     |
     v
CLIPField.apply_compute()
     |
     v
CLIPField.step()
     |
     v
_decode()
     |
     v
_forward()
     |
     +--------------------+
     |                    |
     v                    v
12 transformer layers    local response
     |                    |
     v                    v
complete cloud       winner_layer
(12,50,768)          winner_response
```

This is a code topology, not a semantic interpretation pipeline.

---

# 49. Current Compute Topology

The current resource relationship is approximately:

```text
CLIPField
   |
   | request="compute"
   v
InternalDynamics._compute()
   |
   v
ComputeSystem.select()
   |
   v
temporary winner
   |
   v
commit()
   |
   v
ComputeSystem.consume()
   |
   v
CLIPField.apply_compute()
```

Planet may expose activity to observation without becoming a compute requester.

Therefore:

```text
Planet activity
```

and:

```text
compute request
```

are different signals.

---

# 50. Current Planet Observation Topology

The Planet side may currently expose:

```text
PlanetField.snapshot()
        |
        v
Observer.describe()
        |
        v
ObservationCache
        |
        v
activity/change
```

This relationship does not grant the observer mutation authority.

The observed activity can be used as information without turning the observer into a controller.

---

# 51. Current Collision Topology

The collision boundary should eventually be:

```text
local CLIP event
       |
       v
CLIP local interaction representation
       |
       +
       |
       v
Planet local interaction representation
       |
       v
CloudCollision
       |
       v
collision result
```

The collision layer must not receive or iterate over the complete Cartesian product of both worlds.

The local context must be bounded before collision.

---

# 52. Collision Result Ownership

`CloudCollision` may own its latest calculation result:

```text
last_result
```

but this does not mean that it owns the state described by that result.

For example:

```text
collision result
       |
       +---- describes possible/change relation
       |
       +---- does not automatically mutate Planet
       |
       +---- does not automatically mutate CLIP
```

A state owner must explicitly accept and apply the relevant change through its own boundary.

---

# 53. State Mutation Rule

A component should mutate only state for which it is responsible.

Examples:

```text
Planet
    -> Planet-owned dynamical state

PlanetField
    -> PlanetField field state

CLIPField
    -> CLIP cloud/input/local response/budget

ComputeSystem
    -> compute availability

ObservationCache
    -> temporary cache state

ObservationMemory
    -> historical observation state

Sampler
    -> sampler-local selection/adaptation state
```

A result crossing a boundary does not automatically grant mutation authority.

---

# 54. Runtime Topology Is Not Execution Order

The existence of a relationship:

```text
A -> B
```

does not necessarily mean:

```text
A always executes before B
```

The topology describes possible interaction and dependency.

Temporal behavior is described separately in:

```text
DATA_FLOW.md
```

and phase/runtime documentation.

This distinction prevents the topology document from becoming another centralized execution script.

---

# 55. Main Program Boundary

`main.py` is an external runtime assembly boundary.

It may:

* construct objects
* inject dependencies
* connect input/output
* start the runtime
* provide process-level lifecycle

It must not become a runtime God object.

In particular, `main.py` should not contain the semantic logic for:

```text
Planet
CLIP
collision
attention
memory
compute
```

It assembles the system; local entities perform their own responsibilities.

---

# 56. Programmer Boundary

The programmer may know the repository globally during development.

Runtime objects must not be designed as if they possess that same knowledge.

This creates two different layers:

```text
DESIGN TIME

programmer
   |
   +-- understands repository
   +-- defines boundaries
   +-- defines local rules
   +-- defines interfaces


RUNTIME

local entity
   |
   +-- knows local state
   +-- receives local event
   +-- executes local rule
   +-- exposes local result
```

The programmer designs the conditions for emergence.

The programmer does not hard-code every emergent relationship.

---

# 57. Forbidden Topologies

The following structures are architecturally forbidden unless explicitly justified and reviewed.

## 57.1 Global State Object

```text
GlobalState
   |
   +-- everything
```

Forbidden.

---

## 57.2 Universal Controller

```text
Controller
   |
   +-- decides all actions
```

Forbidden.

---

## 57.3 Global Observer

```text
Observer
   |
   +-- reads everything
   +-- understands everything
   +-- controls future
```

Forbidden.

---

## 57.4 Global Coordinate System

```text
Planet coordinate
       ↕
CLIP coordinate
       ↕
Camera coordinate
```

as a universal permanent mapping.

Forbidden.

---

## 57.5 Cartesian Collision

```text
every Planet state
        ×
every CLIP state
```

Forbidden.

---

## 57.6 Permanent Winner

```text
winner
  |
  v
system priority
```

Forbidden.

---

## 57.7 Hidden Shared Memory

```text
module A
   \
    +--> global dictionary
   /
module B
```

Forbidden.

---

## 57.8 Generic Universal Step

```python
for entity in everything:
    entity.step()
```

Forbidden as a substitute for explicit local evolution topology.

---

# 58. Topology Review Procedure

Before adding a new module, answer:

### Ownership

```text
What state does it own?
```

### Input

```text
What boundary does it receive?
```

### Knowledge

```text
What local information does it need?
```

### Mutation

```text
What is it allowed to modify?
```

### Output

```text
What does it expose?
```

### Interaction

```text
Who can receive that output?
```

### Resource

```text
Does it consume or own finite resources?
```

### Time

```text
What causes it to act?
```

### Memory

```text
Is its state transient or persistent?
```

### Global knowledge

```text
Does it require information outside its responsibility?
```

If the final answer is yes, the proposed topology must be reconsidered.

---

# 59. Minimal Topological Model

The entire system can be reduced to:

```text
                 EXTERNAL
                    |
                  input
                    |
                    v
              local entity
                    |
              local state
                    |
              local rule
                    |
             local interaction
                    |
              state change
                    |
             boundary event
                    |
                    v
              another entity
```

Resource systems add:

```text
local request
     |
     v
finite resource
     |
     v
temporary opportunity
     |
     v
local computation
```

Observation adds:

```text
state/event
     |
     v
snapshot
     |
     v
post-hoc observation
```

Memory adds:

```text
observation
     |
     v
historical local state
     |
     v
future local adaptation
```

None requires a global mind.

---

# 60. Relationship to CONSTITUTION.md

`CONSTITUTION.md` has higher authority.

If a topology conflicts with the Constitution:

```text
CONSTITUTION.md
        >
TOPOLOGY.md
```

The topology must change.

---

# 61. Relationship to ARCHITECTURE.md

`ARCHITECTURE.md` describes the conceptual structure.

`TOPOLOGY.md` describes how that structure appears in code.

Therefore:

```text
CONSTITUTION
      |
      v
ARCHITECTURE
      |
      v
TOPOLOGY
      |
      v
CODE
```

This is a documentation hierarchy, not a runtime control hierarchy.

---

# 62. Topology and Implementation

Implementation convenience must not silently create architectural authority.

Examples of dangerous convenience:

```text
passing the whole system object
```

```text
passing global dictionaries
```

```text
giving collision access to every state
```

```text
giving observer mutable references
```

```text
using one universal coordinate map
```

```text
letting main.py decide internal behavior
```

The implementation must serve the topology.

The topology must not be rewritten merely to justify an implementation shortcut.

---

# 63. Emergent Topology

Some relationships should emerge from actual runtime interaction.

This does not mean the code has no structure.

The code defines:

```text
entities
interfaces
local rules
resources
boundaries
decay
competition
events
```

Runtime interaction determines:

```text
which local relation becomes active
which state changes
which entity receives an opportunity
which observation becomes relevant
which local adaptation persists
```

Therefore:

```text
fixed local rules
        +
finite resources
        +
local state
        +
events
        +
time
        =
emergent system topology
```

The programmer defines the possibility space, not every future relationship.

---

# 64. Core Architectural Test

A practical topology test is:

> If a hypothetical global observer/controller is removed, can the local entities still perform their own responsibilities?

If the answer is no because:

```text
someone must know everything
```

then a hidden God View probably exists.

If the answer is:

```text
each entity still knows what it needs
and reacts through its local boundary
```

then the topology is consistent with CIMA0.

---

# 65. Final Topology Statement

CIMA0 is composed of locally bounded state owners connected by explicit interfaces.

No object owns the whole system.

No object requires the whole system's knowledge.

Planet owns Planet dynamics.

PlanetField owns its field representation.

Organs own their internal states.

CLIPField owns its visual internal field.

CloudCollision owns collision calculation state.

ComputeSystem owns finite computation resources.

Sampler owns local selection behavior.

ObservationCache owns temporary snapshots.

ObservationMemory owns historical observation state.

Observer owns no internal world state.

`InternalDynamics` provides the runtime boundary without becoming a universal controller.

The resulting system is therefore not:

```text
one program
        +
one global flow
        +
one global controller
```

It is:

```text
many local entities
        +
local state
        +
local rules
        +
explicit boundaries
        +
finite resources
        +
transient events
        +
time
        +
local interaction
```

The topology exists to make those boundaries visible.

The absence of a God View is not an implementation limitation.

It is the topology.
