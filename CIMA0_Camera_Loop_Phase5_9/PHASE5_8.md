# CIMA0 Phase5_8

## 0. Phase Definition

Phase5_8 is the stage in which CIMA0 begins to enforce the principle:

> **There is no God View.**

The purpose of this phase is not to add a larger controller or to complete a centralized pipeline.

The purpose is to make the existing internal entities increasingly independent:

* each entity owns its own state
* each entity knows only local information
* each entity acts only within its responsibility
* computation is a finite resource
* collision is a local interaction
* observation is post-hoc
* memory is not global truth
* topology is not predetermined by a universal mapping

Phase5_8 therefore represents a structural transition.

The system is moving from:

```text
centralized execution flow
        |
        v
global coordination
        |
        v
global selection
```

toward:

```text
local state
    +
local rule
    +
local event
    +
local resource
    +
local interaction
    +
time
```

with no global entity required to understand the whole system.

---

# 1. Phase5_8 Main Objective

The primary objective is:

> **Remove hidden God View from the internal architecture.**

This includes both explicit and implicit forms.

A God View may appear as:

```text
global controller
global state dictionary
global observer
global coordinate map
global collision matrix
global winner
global semantic interpreter
generic universal execution loop
```

Even if these are implemented in different modules, they produce the same architecture if one component effectively knows everything.

Phase5_8 therefore focuses on **knowledge boundaries**, not merely module boundaries.

---

# 2. Architectural Shift

Earlier Phase5 development tended to be understood as a pipeline:

```text
Camera
  |
  v
InternalDynamics
  |
  v
Planet / CLIP
  |
  v
Cloud
  |
  v
Collision
  |
  v
Attention
  |
  v
Compute
  |
  v
Sampler
  |
  v
ObservationMemory
```

This representation is useful historically.

However, if interpreted literally, it introduces an unintended assumption:

> one central process knows the complete sequence and decides who acts next.

Phase5_8 rejects that interpretation.

The current model is:

```text
                     External Boundary
                            |
                         Camera
                            |
                         Packet
                            |
              +-------------+-------------+
              |                           |
         local entity                local entity
              |                           |
          CLIPField                 PlanetField
              |                           |
       local internal state       local internal state
              |                           |
              +-------- local ----------+
                       interaction
                            |
                       collision
                            |
                     local event/result

              ComputeSystem
                    |
             finite opportunity
                    |
             requesting entity

              Observer
                    |
             post-hoc observation

              Memory
                    |
             historical adaptation
```

No central node is required to possess the complete picture.

---

# 3. Phase5_8 Completed Structural Work

Phase5_8 established or reinforced the following:

1. explicit ComputeSystem ownership
2. explicit compute requests
3. temporary winner semantics
4. resource consumption and recovery
5. CLIP local computation
6. CLIP complete internal cloud
7. CLIP local response
8. separation between response and compute request
9. Planet independent evolution
10. removal of generic duplicate Planet execution
11. dependency injection for collision and compute
12. separation of collision from compute selection
13. recognition of collision as local interaction
14. rejection of Cartesian collision
15. rejection of artificial coordinate mapping
16. observation as post-hoc
17. ObservationCache as temporary
18. distinction between ObservationCache and ObservationMemory
19. Sampler separated from memory ownership
20. root architecture documentation rewritten around local knowledge
21. no-God-View principle elevated to constitutional level

---

# 4. ComputeSystem

## 4.1 Ownership

`ComputeSystem` owns the finite computation resource.

Current conceptual state:

```text
capacity
available
```

Current recovery behavior is gradual:

```python
self.available += (
    self.capacity - self.available
) * 0.01
```

This behavior must remain.

It must not be replaced with:

```python
self.available = self.capacity
```

because that removes resource scarcity.

---

# 5. Compute Request

An internal entity may expose:

```python
{
    "request": "compute"
}
```

This means:

> the entity currently requires a computation opportunity.

It does not mean:

> this entity is globally important.

It does not mean:

> this entity must win.

It does not specify the semantic result.

The topology is:

```text
entity
   |
   | request
   v
ComputeSystem
```

---

# 6. Current Compute Selection

`InternalDynamics._compute()` now filters signals for explicit compute requests.

Conceptually:

```python
requests = []

for signal in signals:

    state = signal.get("state", {})

    request = state.get("request")

    if request == "compute":

        requests.append(signal)
```

Only explicit requests enter computation competition.

This is an important separation.

For example:

```text
Planet activity
```

may be observable without automatically becoming:

```text
Planet compute request
```

---

# 7. Planet Observation vs Compute Request

The current system distinguishes:

```text
observation signal
```

from:

```text
compute request
```

Planet may report:

```python
{
    "activity": ...,
    "signal": ...,
    "request": False
}
```

while CLIP may report:

```python
{
    "activity": ...,
    "signal": ...,
    "request": "compute"
}
```

Therefore:

```text
activity != request
```

This is structurally important.

An entity being active does not automatically give it a claim on finite computation.

---

# 8. Winner Semantics

`winner` is temporary.

The current meaning is:

```text
winner
   |
   v
temporary recipient of computation opportunity
```

It does not mean:

```text
leader
most important entity
permanent focus
global priority
system controller
```

A later computation opportunity may select another entity.

---

# 9. Compute Commit

The current commit boundary is:

```text
selection
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
local execution
```

The important principle is:

> ComputeSystem transfers resource; it does not perform the organ's work.

The allocation:

```python
{
    "amount": 1.0
}
```

is a resource transfer.

It is not an instruction.

---

# 10. CLIPField

Phase5_8 successfully established the CLIPField local processing path.

Current conceptual topology:

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
decode
      |
      v
forward
```

---

# 11. CLIP Complete Internal Cloud

The current CLIP cloud is:

```text
(12, 50, 768)
```

This is a complete internal representation produced by the current CLIP processing path.

It belongs to `CLIPField`.

It must not be globally compressed simply because collision needs a smaller local interaction representation.

The distinction is:

```text
CLIPField.cloud
        |
        | projection
        v
interaction representation
```

Projection does not replace the cloud.

---

# 12. CLIP Local Response

The local response mechanism was corrected so that:

```text
layer_activity
```

is the authoritative response storage.

The current response is calculated from:

```text
new_cloud
previous_cloud
```

and produces local activity values for transformer layers.

A current result may look conceptually like:

```text
layer 0  -> response
layer 1  -> response
...
layer 11 -> response
```

The highest local response becomes:

```text
winner_layer
```

This is a transient local result.

---

# 13. Response vs Input Demand

A critical Phase5_8 distinction is:

```text
input_activity
```

versus:

```text
winner_response
```

They are not the same concept.

`input_activity` answers:

> Is new input currently demanding processing?

`winner_response` answers:

> What was the local response after processing?

Therefore `activity()` may expose both local information and an explicit request:

```python
{
    "activity": ...,
    "signal": ...,
    "changed": True,
    "source": "clip",
    "request": "compute",
    "layer": ...
}
```

This prevents historical response from being accidentally used as a computation request.

---

# 14. CLIP Compute Budget

CLIPField owns:

```text
compute_budget
```

When ComputeSystem grants a computation opportunity:

```text
ComputeSystem
      |
      | amount
      v
CLIPField.compute_budget
```

CLIPField consumes that opportunity locally.

If no budget exists, it does not perform the computation.

This establishes actual resource causality.

---

# 15. PlanetField

PlanetField remains responsible for the current Planet field representation.

Important current state includes:

```text
state
previous_state
pending_disturbance
age
compute_budget
```

PlanetField receives disturbance through:

```python
receive(disturbance)
```

and evolves through:

```python
step()
```

---

# 16. Planet Sovereignty

Planet remains an independent dynamical substrate.

The surrounding architecture does not redefine Planet's internal evolution.

The relationship is:

```text
PlanetField
      |
      v
Planet evolution
      |
      v
new PlanetField state
```

Planet must not simultaneously be evolved by:

```text
PlanetField.step()
```

and:

```text
generic organ.step()
```

because this creates duplicate causal evolution.

The generic organ execution path was therefore removed.

---

# 17. InternalDynamics Responsibility

`InternalDynamics` remains a runtime boundary.

It may hold references to:

```text
PlanetField
organs
ComputeSystem
collision
observer
observation cache
```

but it must not become the owner of all their states.

The distinction is:

```text
reference
    !=
ownership
```

For example:

```python
self.compute = compute
```

does not mean:

```text
InternalDynamics owns compute.available
```

---

# 18. Dependency Injection

Phase5_8 explicitly keeps:

```python
self.compute = compute
self.collision = collision
```

as injected dependencies.

This avoids hidden subsystem construction.

The topology remains externally visible.

A local component should not secretly instantiate an architectural subsystem merely for convenience.

---

# 19. Collision

Collision is now treated as a genuine internal interaction layer.

Its responsibility is:

```text
local state
   +
local state
   |
   v
relationship
   |
   v
collision result
```

It does not:

* allocate compute
* select a global winner
* modify source state automatically
* interpret semantics
* observe the entire system

---

# 20. Existing Collision Rules

The current collision primitive distinguishes:

```text
EMPTY_SLOT
EMPTY_VALUE
ZERO_VALUE
NONZERO_VALUE
```

and:

```text
PENETRATE
CHANGE
BOUNCE
```

The rules are approximately:

```text
empty + anything
    -> no collision

zero + zero
    -> no collision

zero + nonzero
    -> CHANGE

nonzero + nonzero, same sign
    -> PENETRATE

nonzero + nonzero, opposite sign
    -> BOUNCE
```

These primitive rules remain useful.

The problem is not the local collision rule itself.

The problem is the topology used to decide which states are allowed to collide.

---

# 21. Cartesian Collision Failure

An earlier local collision implementation expanded:

```text
all CLIP states
        ×
all Planet states
```

With:

```text
CLIP = 12 × 50 × 768
     = 460,800
```

when fully materialized at the scalar level, or other reduced representations depending on extraction.

Combined with Planet states, this can reach enormous comparison counts.

The exact numerical explosion is implementation-dependent.

The architectural problem is invariant:

> **CIMA0 must not define collision as every state against every other state.**

This is not primarily an optimization issue.

It is a knowledge-boundary violation.

A collision object should not require complete knowledge of two unrelated internal spaces.

---

# 22. No Artificial CLIP ↔ Planet Mapping

Planet and CLIP have different internal coordinate systems.

CLIP:

```text
layer
token
dimension
```

Planet:

```text
its own internal coordinates
```

Phase5_8 rejects creating:

```text
Planet[x,y]
       ↕
CLIP[layer,token,dimension]
```

merely to make collision implementation easier.

There is no universal coordinate identity.

---

# 23. Correct Local Collision Direction

The intended direction is:

```text
current local event
       |
       v
bounded local context
       |
       v
local interaction
       |
       v
collision
```

not:

```text
Planet complete state
       ×
CLIP complete state
       |
       v
global collision
```

The complete internal states remain sovereign.

Only a bounded interaction context participates in a local event.

---

# 24. Local Event Selection

The current CLIP system already produces a transient layer response:

```text
winner_layer
```

Future collision topology must refine this from:

```text
winner layer
```

toward a sufficiently local event representation.

Potentially:

```text
(layer, token, dimension)
```

or another local coordinate produced by CLIP's actual local response.

The important constraint is:

> The coordinate must arise from local state and local response.

It must not be invented solely to create a convenient global mapping to Planet.

---

# 25. Camera as Primary External Source

The camera remains the primary external homogeneous input.

Its transport form is approximately:

```text
{
    bytes,
    shape,
    dtype
}
```

The input is not semantically interpreted at the transport boundary.

The camera provides:

```text
physical byte stream
```

not:

```text
meaning
```

---

# 26. Full Input Preservation

Phase5_8 preserves the principle:

> External camera input must not be arbitrarily reduced at the transport boundary.

The complete camera frame remains available as homogeneous bytes.

Model-specific preprocessing, such as resizing required by CLIP's input interface, is an internal processing operation.

It is not equivalent to silently replacing the external source with a reduced transport representation.

---

# 27. Local Physical Reconstruction

When a local internal event must interact with the original physical input, the original camera byte field may be used to derive the bounded local physical region relevant to that event.

The intended conceptual structure is:

```text
camera homogeneous bytes
          |
          v
     local event
          |
          v
 bounded physical context
          |
          v
 internal interaction
```

This is not a permanent global mapping.

---

# 28. Changed State Re-Encoding

A collision may produce changed internal state.

That state may later be represented again as homogeneous bytes.

Conceptually:

```text
local interaction
       |
       v
changed state
       |
       v
homogeneous bytes
```

The purpose is to preserve the boundary between physical representation and internal dynamics.

---

# 29. Observation

Observation remains downstream and read-only.

The observer may receive a snapshot:

```python
{
    "planet": ...
}
```

and describe it.

It does not:

```text
predict
authorize
select
allocate
mutate
```

Observation is:

> post-hoc.

It describes what already happened.

---

# 30. ObservationCache

`ObservationCache` is a temporary mechanism.

Its lifecycle is:

```text
snapshot
   |
   v
cache
   |
   v
compare
   |
   v
use
   |
   v
discard/replace
```

It must not become the permanent truth of the system.

---

# 31. ObservationMemory

`ObservationMemory` is conceptually separate.

Its purpose is long-term historical observation and possible future adaptation.

It may retain:

```text
past observations
selection history
local relevance history
adaptive information
```

It must not become:

```text
complete system state
```

or:

```text
global world model
```

---

# 32. Sampler

Sampler owns the local selection process.

It does not create or own ObservationMemory.

The topology remains:

```text
Sampler
   |
   +-- selection
   |
   +-- local parameters


ObservationMemory
   |
   +-- historical observation
```

Future adaptation may allow memory-derived information to influence sampler parameters.

That influence must remain bounded.

---

# 33. Attention

Attention is a temporary local relevance mechanism.

It must not become a global consciousness object.

Attention may:

```text
accumulate
decay
compete
disappear
```

It must not become:

```text
permanent importance
global control
global truth
```

---

# 34. No God View

This is the defining Phase5_8 architectural rule.

No runtime component may require:

```text
all Planet state
all CLIP state
all camera state
all collision state
all attention state
all memory
all resource state
```

in order to perform its responsibility.

The system should remain valid when viewed locally.

For example:

```text
CLIPField
```

needs its own input and compute opportunity.

It does not need to understand the complete Planet.

Likewise:

```text
Planet
```

does not need to understand the complete CLIP cloud.

Likewise:

```text
Observer
```

does not need mutation authority.

---

# 35. Programmer Boundary

The programmer may understand the complete repository during development.

That does not mean runtime entities should be given the same knowledge.

The programmer defines:

```text
entities
interfaces
local rules
resource constraints
boundaries
```

The programmer does not hard-code every future relationship.

This distinction is central to the emergence model.

---

# 36. Why This Is Different from Traditional Programming

Traditional application architecture often looks like:

```text
main()
 |
 +-- decide
 |
 +-- call A
 |
 +-- call B
 |
 +-- call C
 |
 +-- collect results
 |
 +-- decide next action
```

Phase5_8 moves toward:

```text
A owns A-state
B owns B-state
C owns C-state

A reacts locally
B reacts locally
C reacts locally

events cross boundaries
resources are finite
relationships emerge over time
```

The system therefore becomes less like:

```text
a centrally executed algorithm
```

and more like:

```text
an ecology of interacting local entities
```

---

# 37. Runtime Topology

The current runtime should be understood approximately as:

```text
                         CAMERA
                           |
                           v
                       raw packet
                           |
                           v
                    +---------------+
                    | CLIPField     |
                    |               |
                    | input         |
                    | cloud         |
                    | response      |
                    +-------+-------+
                            |
                       compute request
                            |
                            v
                     ComputeSystem
                            |
                     finite resource
                            |
                            v
                       CLIPField


                    +---------------+
                    | PlanetField   |
                    |               |
                    | field state   |
                    | disturbance   |
                    +-------+-------+
                            |
                            v
                         Planet
                            |
                       local evolution


                  CLIP local event
                            |
                            v
                     bounded context
                            |
                            v
                     CloudCollision
                            |
                            v
                      local result


                  internal state/event
                            |
                            v
                         snapshot
                            |
                            v
                        Observer
                            |
                            v
                       observation


                     observation
                            |
                            v
                  ObservationMemory
                            |
                            v
                   local adaptation
```

This diagram must not be interpreted as a single mandatory sequential pipeline.

---

# 38. What Phase5_8 Does Not Complete

Phase5_8 does not yet complete the final emergent topology.

Remaining work includes:

1. define the exact local collision event representation
2. select a bounded CLIP local coordinate
3. derive the corresponding bounded physical context
4. derive a bounded Planet interaction context
5. remove all remaining accidental global collision extraction
6. perform collision only within the local context
7. apply collision results through explicit state-owner boundaries
8. establish changed-state re-encoding
9. complete the observation/sampling relationship
10. introduce ObservationMemory only when its ownership boundary is clear
11. develop local adaptation without creating global memory
12. verify the system without a hidden central controller
13. build topology tests that detect accidental global knowledge

---

# 39. Immediate Technical Priority

The highest-priority technical problem remaining from the current implementation is:

> **Replace the current all-state collision extraction with bounded local interaction.**

The problematic pattern is conceptually:

```python
for clip in all_clip_states:

    for planet in all_planet_states:

        collide(clip, planet)
```

This must not be repaired by merely optimizing the loops.

It must be replaced structurally.

The correct question is:

```text
Which local event exists now?
        |
        v
What bounded local state participates?
        |
        v
What local collision rule applies?
```

---

# 40. Do Not Solve Collision by Index Matching

The following is not an acceptable shortcut:

```text
clip_state[i]
    ↕
planet_state[i]
```

because it creates an artificial topology.

Likewise:

```text
clip layer 11
    ↕
planet row 11
```

is not valid unless the relationship is independently produced by an actual local rule.

The topology must emerge from local interaction, not from matching array indices.

---

# 41. Locality Test

Every future collision implementation should answer:

```text
Why these CLIP states?

Why these Planet states?

What event caused them to become related?

What is the maximum interaction radius?

Who owns the selected local context?

What happens after the collision?
```

If the answer is:

```text
because they are all available
```

the topology is wrong.

If the answer is:

```text
because a current local event caused this bounded relationship
```

the topology is consistent with Phase5_8.

---

# 42. Resource Test

Every computation path should answer:

```text
Who requested computation?

Who owns the resource?

How much was allocated?

Who consumed it?

What local operation happened?
```

A system should never perform unlimited hidden computation simply because an object exists.

This makes computation a physical-like finite resource inside the architecture.

---

# 43. Observation Test

Every observation path should answer:

```text
What happened first?

What snapshot was taken?

What is being described?

Who owns the described state?

Can the observer modify it?
```

The correct answer to the final question must be:

```text
No.
```

---

# 44. Memory Test

Every persistent information structure should answer:

```text
What is remembered?

Who owns the memory?

Why is it retained?

How does it decay or adapt?

Does it represent the complete system?
```

The final answer must not become:

```text
yes
```

---

# 45. Topology Test

For every module:

```text
KNOWS
  |
  v
local information

OWNS
  |
  v
local state

RECEIVES
  |
  v
bounded input

ACTS
  |
  v
local rule

EXPOSES
  |
  v
bounded result
```

The module should not need:

```text
everything
```

---

# 46. Phase5_8 Completion Criteria

Phase5_8 can be considered structurally complete when:

### Compute

* finite resource exists
* resource recovers gradually
* explicit requests exist
* winner is temporary
* allocation is resource, not command
* selected organ executes locally

### Planet

* Planet remains sovereign
* PlanetField owns its field representation
* disturbance enters through explicit boundary
* Planet is not generically stepped twice

### CLIP

* camera packet remains homogeneous
* CLIP receives packet locally
* compute is required for forward processing
* complete cloud exists
* local response exists
* response is distinct from compute demand
* winner is transient

### Collision

* no Cartesian product
* no artificial coordinate mapping
* local event determines interaction context
* collision remains a local rule system
* collision does not own source state
* changed state returns through state-owner boundaries

### Observation

* observer is read-only
* observation is post-hoc
* cache is temporary
* memory is distinct from cache
* sampler does not own memory

### Architecture

* no global state object
* no universal controller
* no global observer
* no permanent winner
* no universal coordinate system
* no hidden control channel
* no generic universal execution loop

---

# 47. Phase5_8 Architectural Statement

Phase5_8 is not the phase in which CIMA0 becomes a larger centralized system.

It is the phase in which CIMA0 becomes less centralized.

The primary achievement is not the number of modules.

It is the increasingly strict separation of:

```text
knowledge
state
responsibility
resource
event
observation
memory
```

Each remains local.

The system therefore moves from:

```text
"How does the central program make everything happen?"
```

toward:

```text
"What local conditions allow something to happen?"
```

---

# 48. Final Phase Principle

The most important Phase5_8 rule is:

> **No entity, including InternalDynamics and the programmer-defined runtime, should need a complete view of the system in order for local behavior to occur.**

The programmer defines the boundaries.

The entities own their states.

Events cross boundaries.

Resources are finite.

Collisions are local.

Observation is post-hoc.

Memory is historical.

Adaptation is local.

Time allows relationships to emerge.

Therefore:

```text
No God View.
No global owner.
No universal controller.
No universal coordinate system.

Only local entities,
local knowledge,
local rules,
local resources,
local interactions,
and time.
```

This is the defining state of CIMA0 Phase5_8.
