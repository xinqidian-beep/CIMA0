# CIMA0 Architecture

## Current System Architecture

**Status:** Current architectural model
**Scope:** CIMA0 internal dynamic system
**Normative constraints:** See `CONSTITUTION.md`

---

# 0. Architectural Overview

CIMA0 is composed of multiple locally bounded entities.

There is no central entity that understands or controls the complete system.

The architecture therefore does not describe a single global execution pipeline.

Instead, it describes:

* local state ownership
* local responsibilities
* explicit interfaces
* event relationships
* resource relationships
* observation relationships
* temporal relationships

The system operates through these local relationships.

---

# 1. Fundamental Structure

The current architecture can be understood through five interacting domains:

```text
External Input
      |
      v
Input / Transport
      |
      v
Internal Dynamics
      |
      +--------------------+
      |                    |
      v                    v
Autonomous Fields       Internal Organs
      |                    |
      |                    |
      +---------+----------+
                |
                v
        Local Interaction
                |
                v
          Changed State
                |
                v
       Subsequent Internal Event


Compute Resource
        |
        v
 Computation Opportunity
        |
        v
   Local Organ


Observation
        |
        v
Observation History
        |
        v
Future Local Adaptation
```

These are relationships, not a centralized control flow.

No component at the center is assumed to know all of them simultaneously.

---

# 2. Architectural Domains

CIMA0 currently contains the following major domains:

```text
core/
│
├── io/
│
├── internal_dynamics/
│
├── organs/
│
├── collision/
│
├── observer/
│
├── memory/
│
└── ...
```

The exact filesystem may evolve.

The architectural responsibilities must remain stable even if implementation locations change.

---

# 3. Input / Transport Domain

## Responsibility

Receive external disturbances and transport them into the internal system without assigning them semantic meaning prematurely.

Current example:

```text
External World
      |
      v
Camera
      |
      v
Camera Packet
{
    bytes,
    shape,
    dtype
}
```

The input layer owns transport concerns.

It does not decide:

* what the image means
* what CLIP should think
* what Planet should do
* what should receive compute

---

# 4. InternalDynamics

## Responsibility

InternalDynamics is the architectural container and coordination boundary for internal components.

It provides the environment through which internal entities can:

* receive appropriate input
* advance their local dynamics
* expose local observations
* request computation
* participate in defined interactions

InternalDynamics is **not**:

* a global controller
* a global observer
* a semantic interpreter
* a global state database
* a permanent decision maker

Its purpose is to provide the structure in which local entities operate.

---

# 5. PlanetField

## Responsibility

PlanetField owns the continuously evolving planetary internal field.

```text
PlanetField
    |
    +-- internal state
    |
    +-- evolution
    |
    +-- snapshot
    |
    +-- interaction projection
```

PlanetField is autonomous with respect to its internal dynamics.

It does not need to understand:

* Camera
* CLIP
* Observer
* Sampler
* global attention
* global meaning

---

## 5.1 Planet

Planet is the underlying dynamical substrate.

Planet owns its own evolution rules.

The architecture must not turn Planet into a passive data container controlled by another module.

Planet may expose:

```text
snapshot
projection
evolution interface
```

without transferring ownership of its internal dynamics.

---

# 6. Internal Organ Domain

Internal organs are autonomous components that maintain their own internal states.

An organ:

* receives defined input
* maintains its own state
* performs its own internal processing
* reports appropriate local activity
* may request finite compute
* decides how to use compute it receives

An organ does not need knowledge of the entire system.

---

# 7. CLIPField

## Responsibility

CLIPField is a visual internal organ.

Input:

```text
Camera Packet
{
    bytes,
    shape,
    dtype
}
```

Internal processing produces a visual internal state.

Current implementation may expose a complete visual cloud with shape:

```text
(12, 50, 768)
```

This represents the current CLIP internal representation.

It is not defined as:

* the complete system state
* semantic truth
* Planet topology
* a global coordinate system

---

## 7.1 CLIPField State

CLIPField owns:

```text
cloud
internal_activity
dirty state
compute state
local response state
```

The organ is responsible for its own internal computation.

It does not receive a command such as:

```text
"compute this exact result"
```

Instead, it receives a finite computation opportunity.

---

# 8. Complete Internal State vs Interaction Projection

CIMA0 distinguishes between:

```text
internal state
```

and:

```text
interaction representation
```

The internal state remains owned by its component.

A projection is generated for a specific interaction.

```text
Complete Internal State
          |
          | projection
          v
Interaction Representation
```

Projection does not mean:

```text
compress internal world
```

and does not mean:

```text
replace original state
```

---

# 9. Cloud

Cloud is an interaction representation.

It exists to expose the information required by an interaction without transferring ownership of the original state.

Conceptually:

```text
Source Field / Organ State
          |
          v
      Projection
          |
          v
        Cloud
          |
          v
   Local Interaction
```

A cloud is therefore contextual.

It does not automatically represent the complete internal world.

---

# 10. CloudState

CloudState represents transient interaction-related information.

It may contain:

* local states
* local positions
* local values
* event-related information
* temporary interaction context

CloudState should remain bounded by the event that created it.

It must not become a hidden global database.

---

# 11. Local Interaction

CIMA0 does not assume that all internal states must interact with all other internal states.

Interaction is local.

A component participating in an interaction receives the information necessary for that interaction.

It does not automatically receive every state owned by every other component.

---

# 12. CloudCollision

## Responsibility

CloudCollision performs local collision / relationship rules on interaction representations.

Its responsibility is limited to determining the interaction defined by the states it receives.

It may determine:

```text
collision type
local relationship
changed value
interaction result
```

It does not:

* select a global winner
* allocate compute
* interpret semantic meaning
* control Planet
* control CLIP
* observe the entire system

---

# 13. Collision Is an Event

Collision is an internal event.

The conceptual relationship is:

```text
Local State
    +
Local State
    |
    v
Interaction Rule
    |
    v
Collision Event
    |
    v
Changed State
```

The collision result is not merely a candidate waiting for a global controller.

If the local collision rule determines that an interaction occurs, that interaction is an internal event.

---

# 14. Locality of Collision

Collision must remain bounded.

The architecture must not construct:

```text
all CLIP states
        ×
all Planet states
```

merely because both representations are available.

The existence of two internal spaces does not imply complete cross-product interaction.

---

# 15. Independent Topologies

Different internal spaces retain their own topology.

For example:

```text
CLIP topology:
(layer, token, dimension)

Planet topology:
(field-specific coordinates)
```

There is no architectural assumption that these coordinates correspond directly.

No global mapping is defined merely to simplify implementation.

A relationship may be established only when the local interaction rules and available information justify it.

---

# 16. Transient Local Focus

A local internal response may identify one current coordinate or point of interest.

Conceptually:

```text
Complete Local Internal State
          |
          v
     local response
          |
          v
  one transient point
```

This point is temporary.

It is not:

* global attention
* permanent focus
* permanent winner
* global coordinate authority
* semantic identity

A subsequent event may produce another point.

---

# 17. Camera as Primary External Stream

Camera data enters as a homogeneous external byte stream.

The stream is transformed internally by the receiving organ.

Conceptually:

```text
Camera
  |
  v
homogeneous bytes
  |
  v
CLIP internal processing
  |
  v
complete internal visual state
  |
  v
local response
  |
  v
transient local point
```

The camera does not directly become semantic meaning.

---

# 18. Local Event Reconstruction / Derivation

When an internal local event requires a relationship with external-origin data, the system may derive the necessary local interaction material from the available homogeneous input representation.

This is not a global coordinate mapping.

It is not a precomputed CLIP-to-Planet map.

It is not a requirement for either side to understand the entire other's topology.

The purpose is only to recover the local material required by the current interaction.

---

# 19. Changed State

An interaction may produce:

```text
changed state
```

The changed state remains owned by the component whose state was changed.

A changed state may subsequently be represented as homogeneous bytes:

```text
Changed State
      |
      v
Homogeneous Representation
      |
      v
Next Internal Stage
```

This allows internal events to become subsequent disturbances without introducing a global state authority.

---

# 20. ComputeSystem

## Responsibility

ComputeSystem owns finite computation resources.

Its responsibilities are:

```text
maintain resource state
recover resource
receive eligible requests
select a computation opportunity
transfer finite resource
```

ComputeSystem does not decide what the selected organ computes.

---

# 21. Compute Request

A component may request compute when its own local condition requires computation.

Conceptually:

```text
Organ
  |
  | request
  v
ComputeSystem
```

The request does not mean:

```text
"Compute this result for me."
```

It means:

```text
"I currently require a computation opportunity."
```

---

# 22. Computation Opportunity

The computation selection process is temporary.

```text
eligible requests
       |
       v
selection
       |
       v
current winner
       |
       v
finite allocation
       |
       v
selected organ
```

`winner` is local to this computation event.

It has no permanent authority.

---

# 23. Resource Ownership

ComputeSystem owns:

```text
available compute
capacity
recovery
allocation
```

The organ owns:

```text
how the computation is performed
how the result is formed
how the result affects its internal state
```

This is a resource boundary, not a control hierarchy.

---

# 24. AttentionField

AttentionField, when present, represents temporary competition or relevance among signals presented to it.

It owns its own temporary attention state.

It does not become:

* global consciousness
* global controller
* permanent focus
* semantic authority

Attention is a local mechanism, not a system-wide mind.

---

# 25. Sampler

Sampler owns the observation-selection process.

Its responsibility is to select among states or signals presented to it.

Sampler does not:

* own observation history
* become permanent memory
* know the complete system
* define global importance

Selection is always relative to the information and opportunity currently presented to Sampler.

---

# 26. ObservationCache

ObservationCache is temporary.

Its lifecycle is:

```text
snapshot
    |
    v
use
    |
    v
discard / expire
```

It is not a permanent source of truth.

It is not long-term memory.

It is not an adaptive model.

---

# 27. ObservationMemory

ObservationMemory belongs to the memory domain.

Its responsibility is historical observation state.

```text
Observation
      |
      v
ObservationMemory
      |
      v
Historical information
      |
      v
Future adaptation
```

It may retain:

* observation events
* age history
* activity history
* delta history
* selection history

It does not own the complete state of the observed entities.

---

# 28. Observer

Observer is a read-only observation interface.

Its conceptual operation is:

```text
Existing Internal State
        |
        v
Snapshot
        |
        v
Observer
        |
        v
Description / Observation
```

Observer does not initiate the observed event.

Observer does not authorize it.

Observer does not modify the source state.

Observer does not become a global interpreter.

---

# 29. Observation Is Downstream

The architectural ordering is:

```text
Internal event
      |
      v
State change
      |
      v
Observable representation
      |
      v
Observation
```

not:

```text
Observation
      |
      v
Permission
      |
      v
Internal event
```

This distinction is fundamental.

---

# 30. Observation and Memory Are Different

The architecture separates:

```text
Observer
    sees

ObservationCache
    temporarily holds

ObservationMemory
    historically retains
```

These three responsibilities must not collapse into one module.

---

# 31. Adaptation

Future adaptation may connect historical observation to future sampling behavior.

Conceptually:

```text
Internal Events
      |
      v
Observation
      |
      v
ObservationMemory
      |
      v
Adaptation
      |
      v
Future Sampling
```

Adaptation is not global intelligence.

It modifies only the adaptive state owned by the relevant component.

---

# 32. Data Ownership Flow

A simplified ownership flow is:

```text
Camera
  owns external camera data
       |
       v
Input / Router
  owns transport packet
       |
       v
CLIPField
  owns visual internal state
       |
       v
Projection
  exposes interaction representation
       |
       v
CloudCollision
  owns interaction result
       |
       v
Changed State
  remains with its state owner
```

At no point does the representation itself create a global owner.

---

# 33. Resource Flow

Resource flow is separate from state flow.

```text
ComputeSystem
      |
      | finite compute
      v
Selected Organ
      |
      | local computation
      v
Organ State Change
```

Compute resource does not carry global semantic authority.

---

# 34. Observation Flow

Observation flow is separate from computation flow.

```text
Internal State / Event
        |
        v
Observable Representation
        |
        v
Observer
        |
        v
Observation Event
        |
        v
ObservationMemory
```

Observation does not control the source.

---

# 35. Event Flow

The general event relationship is:

```text
disturbance
    |
    v
local internal processing
    |
    v
local response
    |
    v
local interaction
    |
    v
changed state
    |
    v
subsequent event
```

There is no requirement for a global interpreter between every stage.

---

# 36. InternalDynamics Step Boundary

InternalDynamics may provide a temporal opportunity for local components to advance.

However, a generic:

```python
for organ in all_organs:
    organ.step()
```

must not be treated as the architectural definition of the system.

A component advances when its own lifecycle and the current event/resource conditions require it.

The container must not assume that every component should execute merely because a global cycle occurred.

---

# 37. No Global Execution Script

The architecture must not depend on a hidden master sequence such as:

```text
Planet
→ CLIP
→ Collision
→ Attention
→ Compute
→ Sampler
→ Memory
```

as though these were stages of one centrally understood algorithm.

They are different responsibilities connected by particular relationships.

Some relationships are:

* temporal
* causal
* observational
* resource-based
* event-based
* representational

They are not necessarily one universal sequence.

---

# 38. State Ownership Table

| Module            | Owns                        | May Modify              | Others May                        |
| ----------------- | --------------------------- | ----------------------- | --------------------------------- |
| PlanetField       | planetary field             | its own field           | observe / receive projection      |
| Planet            | planetary dynamics          | its own dynamics        | invoke defined interface          |
| CLIPField         | visual internal state       | its own state           | observe / receive projection      |
| CloudCollision    | local interaction result    | its own result          | consume result                    |
| CloudState        | transient interaction state | its own state           | consume exposed representation    |
| AttentionField    | temporary attention state   | its own state           | provide signals                   |
| ComputeSystem     | compute resources           | its own resources       | request / receive allocation      |
| Sampler           | selection process           | its own selection state | provide candidates                |
| ObservationCache  | temporary snapshot          | its own cache           | read temporarily                  |
| ObservationMemory | observation history         | its own memory          | provide historical information    |
| Observer          | no system state             | none                    | receive observable representation |

---

# 39. Interface Principle

Every interface should expose only what the receiving responsibility requires.

An interface should answer:

```text
What does the receiver need?
```

not:

```text
What information can we expose?
```

Full internal state should not be exported merely because exporting it is convenient.

---

# 40. Current Architectural Invariants

The following invariants must remain true:

```text
1. No God View.

2. No global controller.

3. No global observer.

4. No permanent winner.

5. No permanent focus.

6. No global coordinate authority.

7. No assumed CLIP ↔ Planet coordinate mapping.

8. No all-state Cartesian collision by default.

9. Planet retains its own dynamics.

10. CLIP retains its complete internal state.

11. Projection does not replace source state.

12. Compute owns compute resources.

13. Organ owns its computation.

14. Observer is read-only and post-hoc.

15. Cache is temporary.

16. Memory owns historical observation.

17. Sampler owns selection, not memory.

18. Collision owns collision rules, not selection.

19. State ownership is explicit.

20. Relationships are local and event-dependent.
```

---

# 41. Architectural Reading Rule

When reading the CIMA0 architecture, do not ask:

> “Which module is the brain?”

There is no such module.

Instead ask:

> “What does this entity know?”

> “What does it own?”

> “What event can reach it?”

> “What can it change?”

> “What does it expose?”

> “What happens after that local change?”

This is the intended way to understand CIMA0.

---

# 42. Relationship With CONSTITUTION.md

`CONSTITUTION.md` defines the architectural laws.

`ARCHITECTURE.md` describes the current structural realization of those laws.

Therefore:

```text
CONSTITUTION.md
        |
        v
architectural constraints
        |
        v
ARCHITECTURE.md
        |
        v
current topology
        |
        v
implementation
```

If the implementation conflicts with the Constitution, the implementation must be treated as incorrect or transitional.

If the current architecture changes, `ARCHITECTURE.md` should be updated.

Historical implementations belong in phase documentation.

---

# 43. Architecture in One Diagram

The current architecture can be summarized as:

```text
                         EXTERNAL WORLD
                               |
                               v
                            CAMERA
                               |
                               v
                     HOMOGENEOUS BYTE STREAM
                               |
                               v
                         INPUT / ROUTER
                               |
                               v
                    +-----------------------+
                    |    INTERNAL DYNAMICS |
                    +-----------------------+
                       |                |
                       |                |
                       v                v
                +------------+    +-------------+
                | PlanetField|    | CLIPField   |
                |            |    |             |
                | autonomous |    | visual      |
                | dynamics   |    | internal    |
                +-----+------+    | state       |
                      |           +------+------+
                      |                  |
                      |                  v
                      |           local response
                      |                  |
                      |                  v
                      |          transient point
                      |                  |
                      +--------+---------+
                               |
                               v
                     LOCAL INTERACTION
                               |
                               v
                       CLOUD COLLISION
                               |
                               v
                        CHANGED STATE
                               |
                               v
                    HOMOGENEOUS REPRESENTATION
                               |
                               v
                         NEXT EVENT


        COMPUTE RESOURCE DOMAIN
        ------------------------

                 +----------------+
                 | ComputeSystem  |
                 +-------+--------+
                         |
                  finite opportunity
                         |
                         v
                    selected organ
                         |
                         v
                  organ computation


        OBSERVATION DOMAIN
        ------------------

               internal event/state
                        |
                        v
                    snapshot
                        |
                        v
                     Observer
                        |
                        v
                observation event
                        |
                        v
              ObservationMemory
                        |
                        v
               future adaptation
                        |
                        v
                     Sampler
```

The diagram intentionally contains no central intelligence.

The center is an **interaction boundary**, not a brain.

---

# 44. Final Architectural Statement

CIMA0 is not a single algorithm executed by a globally informed controller.

It is an internal dynamic architecture composed of locally bounded entities.

Each entity:

```text
owns local state
knows local information
follows local rules
uses local resources
produces local events
exposes local representations
```

The complete behavior of the system is the result of these interactions over time.

No component is required to understand the whole.

No component is granted authority over the whole.

The architecture therefore remains valid even when the final system behavior cannot be predicted in advance.

**CIMA0 is structured so that local entities can operate without a God View, while system-level behavior emerges from their actual interaction.**
