# CIMA0 Constitution

## Architecture Constitution

**Status:** Normative
**Scope:** Entire CIMA0 system
**Priority:** Higher than implementation, phase design, optimization, and convenience

---

# 0. Preamble

CIMA0 is an internal dynamic system.

CIMA0 is not designed around a global controller, a global observer, a global semantic interpreter, or a centralized representation of the whole system.

No runtime entity possesses complete knowledge of CIMA0.

No runtime entity is required to understand the complete system in order for the system to operate.

The system is formed from local states, local rules, local resources, local interactions, and events occurring through time.

The overall behavior of the system is not prescribed as a complete sequence by any single component.

The architecture defines boundaries and responsibilities.

The running system produces the actual relationships between those boundaries.

---

# 1. Fundamental Principle — No God View

## 1.1 No Global Knowledge

CIMA0 shall contain no runtime component whose responsibility is to know the complete internal state of the system.

There shall be no:

* global state interpreter
* global observer
* global controller
* global semantic authority
* global coordinate authority
* global event authority
* global decision maker

A component may know the state required for its own responsibility.

It must not require knowledge of unrelated internal states merely because that knowledge is convenient.

---

## 1.2 No Global Interpretation

No component may claim to know what the entire system means.

A local state is not automatically a global meaning.

A local response is not automatically a system-level intention.

A selected state is not automatically the most important state in the system.

An observed change is not automatically a cause.

Interpretation must remain bounded by the responsibility and information available to the component performing it.

---

## 1.3 No Permanent Center

CIMA0 has no permanent:

* center
* king
* winner
* focus
* attention point
* preferred organ
* privileged coordinate

A winner, focus, or selected point exists only within the local event or computation opportunity in which it was produced.

When that event ends, its authority ends.

---

# 2. Local Knowledge Principle

Every component shall operate from local knowledge.

For every component, the architecture must be able to answer:

1. What state does it know?
2. Why does it need that state?
3. What state does it own?
4. What state may it modify?
5. What state may it only observe?
6. What information is explicitly outside its responsibility?

If these boundaries cannot be answered clearly, the topology is incomplete.

The correct response is to repair the topology before adding implementation.

---

# 3. State Sovereignty

Every persistent state belongs to an identifiable owner.

The owner is responsible for:

* creating the state
* evolving the state
* validating the state
* exposing permitted representations of the state
* deciding when the state changes

Other components may receive an exposed representation.

They do not thereby acquire ownership.

---

## 3.1 State Ownership

The general ownership model is:

```text
PlanetField
    owns internal planetary field state

CLIPField
    owns visual internal state

CloudCollision
    owns its local comparison/event result

AttentionField
    owns temporary attention state

ComputeSystem
    owns compute/resource state

Sampler
    owns selection-process state

ObservationCache
    owns temporary snapshots

ObservationMemory
    owns historical observation state

Observer
    owns no internal system state
```

This table is architectural, not merely descriptive.

---

## 3.2 No Shared Ownership

A state shall not have multiple independent owners.

If multiple components need access to a state, the owning component must expose an appropriate interface or representation.

Do not solve ownership ambiguity by creating a global shared state.

---

# 4. Responsibility Boundary

Every module shall have one clearly bounded primary responsibility.

A module may perform internal operations necessary to fulfill that responsibility.

A module shall not silently acquire responsibilities belonging to another module.

Examples:

```text
ComputeSystem
    allocates compute resources

Organ
    decides how to use allocated compute

Observer
    observes

Collision
    performs collision rules

Sampler
    selects

Memory
    stores historical observation

Planet
    evolves according to its own dynamics
```

No component should become a hidden controller merely because it has access to another component's interface.

---

# 5. Causality

CIMA0 distinguishes between:

```text
cause
event
observation
selection
computation
consequence
```

These must not be collapsed into one operation.

An observation of an event does not cause that event.

A selection made after an event does not authorize that event.

A computation opportunity does not determine its result.

A result does not retroactively become the cause of the event that produced it.

---

# 6. Observation Is Post-Hoc

Observation is fundamentally retrospective.

An observer can observe a state or change only after that state or change exists in an observable form.

The Observer shall not:

* authorize an event
* approve an event
* predict an event
* prevent an event
* choose an event
* allocate compute
* modify the observed state
* establish causality

The Observer describes what has already happened.

Therefore:

```text
Internal event
      |
      v
Observable state/change
      |
      v
Observer
```

not:

```text
Observer
      |
      v
decision
      |
      v
Internal event
```

---

# 7. Observer Has No God View

The Observer is not a privileged entity outside the system that understands everything.

The Observer is itself constrained by the information made available to it.

It may observe only an exposed snapshot or representation.

It does not receive automatic access to all internal states.

The Observer's inability to see an internal state is not an error.

It is part of the architecture.

---

# 8. Planet Sovereignty

Planet is an autonomous dynamical substrate.

Planet:

* owns its own dynamics
* evolves according to its own rules
* maintains its own state
* may expose snapshots or projections

Planet shall not become subordinate to:

* Observer
* ComputeSystem
* Sampler
* AttentionField
* CLIPField
* Display
* global controller

No external module may rewrite Planet's fundamental dynamical rules for convenience.

---

# 9. PlanetField

PlanetField is an interface layer around the planetary internal dynamic field.

PlanetField may:

* hold the current field representation
* provide a snapshot
* accept an appropriate disturbance
* advance the field
* provide an interaction projection

PlanetField does not thereby acquire knowledge of:

* camera semantics
* CLIP semantics
* global attention
* future selection
* system-wide meaning

---

# 10. Organ Autonomy

An organ is responsible for its own internal operation.

Receiving compute does not tell an organ what result to produce.

The resource contract is:

```text
ComputeSystem
      |
      | finite opportunity
      v
Organ
      |
      | organ decides
      v
Internal computation
```

Not:

```text
ComputeSystem
      |
      | instruction
      v
Organ
```

The organ determines how to use the resource within its own responsibility.

---

# 11. Compute Is a Resource System

ComputeSystem owns compute resources.

Its responsibility is to:

* maintain available compute
* recover compute according to its own rules
* receive eligible compute requests
* select a computation opportunity
* transfer finite compute capacity

ComputeSystem does not own the internal meaning of an organ.

ComputeSystem does not decide what an organ computes.

ComputeSystem does not interpret the result.

---

## 11.1 Compute Opportunity

A selection result is an opportunity, not an authority.

A winner means:

> This entity receives the current computation opportunity.

It does not mean:

> This entity is globally important.

It does not mean:

> This entity should always be selected.

It does not mean:

> This entity controls the next event.

---

## 11.2 Winner Is Ephemeral

`winner` is valid only within the computation-selection event that produced it.

It shall not become:

* permanent focus
* permanent attention
* global priority
* global coordinate
* global controller
* persistent authority

---

# 12. Resource Recovery

Compute resource recovery belongs to ComputeSystem.

An organ does not manufacture additional global compute merely because it requires more computation.

An organ may request another computation opportunity through the defined resource protocol.

This preserves finite-resource behavior.

The intended pattern is:

```text
request
   |
   v
receive finite resource
   |
   v
perform internal computation
   |
   v
resource exhausted
   |
   v
request again when appropriate
```

---

# 13. Collision Is an Internal Event

Collision is not merely a candidate-generation stage.

Collision represents an actual interaction between local states under defined local rules.

Collision shall not:

* select a global winner
* allocate compute
* interpret meaning
* modify unrelated state
* require knowledge of the complete system

Collision consumes only the local interaction material required for the event.

---

# 14. No Cartesian Explosion by Architecture

CIMA0 shall not construct global interaction sets merely because two states are available.

In particular, the architecture shall not assume:

```text
every CLIP state
    ×
every Planet state
```

must be compared.

Such a Cartesian product is not a valid default representation of interaction.

Interaction must be bounded by the actual local event, local relation, or local physical neighborhood required by the rules.

Performance constraints alone are not sufficient justification.

The topology itself must prevent unnecessary global interaction.

---

# 15. No Artificial Cross-Topology Mapping

Different internal spaces do not automatically possess corresponding coordinates.

For example:

```text
CLIP:
(layer, token, dimension)

Planet:
(x, y)
```

must not be assumed to have a predefined one-to-one mapping.

A mapping shall not be introduced merely because it makes implementation easier.

If a relationship emerges through an actual interaction, that relationship must arise from the interaction rules and available local information.

The programmer must not invent a global correspondence simply to connect otherwise independent topologies.

---

# 16. CLIP Internal State Sovereignty

CLIPField owns its complete visual internal state.

The existence of an external projection does not imply that the internal state has been compressed.

For the current implementation, the complete visual cloud may be represented as:

```text
(12, 50, 768)
```

This is an implementation-level representation of the current internal state.

It must not automatically be interpreted as:

* global meaning
* semantic classification
* universal coordinate space
* collision space
* Planet space

---

# 17. Projection Is Not Compression

A projection is an interaction representation.

It is not the replacement of the source state.

Conceptually:

```text
Internal State
      |
      | projection
      v
Interaction Representation
```

not:

```text
Internal State
      |
      | compression
      v
New World State
```

`collision_projection()` exposes a representation suitable for a particular interaction.

It does not redefine the internal world.

---

# 18. Local Focus

A local response may produce a current point of attention.

That point is temporary.

It is not:

* a permanent winner
* a global coordinate
* a global command
* a semantic label
* a permanent memory

The focus exists only as long as it is relevant to the current local process.

When the process changes, a different point may emerge.

---

# 19. Camera and Homogeneous Input

Camera input is treated first as an external disturbance / homogeneous byte stream.

The byte stream does not contain predetermined semantic meaning for the internal system.

The internal system may transform the stream through its own local rules.

The camera does not directly prescribe internal meaning.

---

# 20. No Semantic Shortcut

External input shall not bypass internal dynamics by directly becoming:

* semantic meaning
* decision
* command
* classification
* global state

The intended principle is:

```text
External disturbance
        |
        v
Internal interaction
        |
        v
Internal change
        |
        v
Observation
```

Any interpretation must arise through the responsibilities of the relevant internal components.

---

# 21. Changed State and Homogeneous Re-encoding

When an internal interaction produces a changed state, that state may be represented again as an appropriate homogeneous data stream for the next stage.

Conceptually:

```text
homogeneous input
       |
       v
local internal processing
       |
       v
local interaction
       |
       v
changed state
       |
       v
homogeneous representation
       |
       v
next stage
```

The re-encoding does not erase the ownership of the state that produced it.

---

# 22. Cloud Principle

Cloud is an interaction representation.

Cloud is not automatically:

* the original field
* the complete internal world
* the permanent memory of a field
* the semantic meaning of a field

A cloud may expose information required for a local interaction.

The original owner retains sovereignty over the underlying state.

---

# 23. CloudState

CloudState represents transient interaction/event state.

It should not become a hidden global database.

Transient interaction information should have a bounded lifetime appropriate to the event that created it.

A temporary event must not silently become permanent system knowledge.

---

# 24. Attention Is Temporary

AttentionField, where present, is a short-term competition mechanism.

Attention does not become:

* global consciousness
* permanent memory
* global control
* semantic authority

Attention represents temporary relevance within the information presented to it.

Its state is local to its responsibility.

---

# 25. Sampler

Sampler owns the selection process.

Sampler may:

* receive eligible observation states
* calculate selection scores
* select among provided states
* maintain selection-related state required by its own algorithm

Sampler does not own observation history.

Sampler does not become a global memory.

Sampler does not invent information that was not provided to it.

---

# 26. Sampler Does Not Create Memory

Sampler and ObservationMemory are separate responsibilities.

```text
Sampler
    selects

ObservationMemory
    remembers observations
```

Sampler must not silently accumulate historical observations merely because historical data would improve its selection.

Historical adaptation belongs to the memory/adaptation architecture.

---

# 27. ObservationCache

ObservationCache is temporary.

Its purpose is:

> preserve a short-lived snapshot long enough for the immediate observation operation.

It is not:

* permanent truth
* long-term memory
* learning memory
* global state
* canonical source of the system

The intended lifecycle is:

```text
snapshot
   |
   v
use
   |
   v
discard / expire
```

A cache must not evolve into an accidental permanent source of truth.

---

# 28. ObservationMemory

ObservationMemory is different from ObservationCache.

ObservationMemory exists to retain historical observation information that may participate in future adaptation.

Conceptually:

```text
Observation
      |
      v
ObservationMemory
      |
      v
Future adaptation
```

ObservationMemory may own:

* observation history
* activity history
* delta history
* selection history
* age/history required for adaptation

It does not own:

* complete Planet state
* complete CLIP state
* original camera data
* global semantic interpretation

---

# 29. Memory Does Not Become a God View

Historical knowledge is still local knowledge.

ObservationMemory may know the history that it owns.

It does not thereby acquire the history of the entire system.

Long-term memory must not become a hidden global controller.

---

# 30. Adaptation

Future adaptive behavior may emerge from:

```text
usage
decay
competition
feedback
historical observation
```

Adaptive parameters may evolve internally.

Examples include:

```text
w_age
w_activity
w_delta
```

However, adaptation must remain within the responsibility of the component that owns the adaptive state.

No global adaptation mechanism may silently rewrite unrelated modules.

---

# 31. Time

Time is part of the architecture.

States may differ because:

* they are new
* they are old
* they have changed
* they have decayed
* they have recently been active
* they have not been used

Age and decay therefore belong to the local state owner that defines their meaning.

A global clock must not be introduced merely to make unrelated modules appear synchronized unless synchronization itself is an explicit architectural requirement.

---

# 32. No Hidden State Transfer

Passing a representation does not transfer ownership.

For example:

```text
CLIPField
    |
    | projection
    v
Collision
```

does not mean Collision now owns the CLIP cloud.

Likewise:

```text
Observer
    |
    | snapshot
    v
external output
```

does not mean the external output becomes the authoritative internal state.

Ownership remains with the original owner.

---

# 33. No Hidden Control Channels

A module shall not influence another module through undocumented side effects.

Avoid:

* hidden global variables
* implicit callbacks
* mutation of another module's state
* undocumented singleton state
* accidental shared references
* observer-triggered mutations
* logging paths that secretly become control paths

Control relationships must be explicit.

---

# 34. Interfaces Are Boundaries

An interface defines what another component is allowed to know or request.

Interfaces should expose the minimum representation required for the responsibility.

An interface must not be used as an excuse to expose the entire internal state of a component.

The question is not:

> “What can we expose?”

The question is:

> “What does the receiving component legitimately need?”

---

# 35. No Convenience Architecture

The following are not valid architectural justifications by themselves:

* easier implementation
* easier debugging
* easier visualization
* fewer lines of code
* faster prototype development
* convenient coordinate mapping
* convenient global state
* convenient caching
* convenient centralized control

Convenience may influence implementation only after ownership, causality, and responsibility remain correct.

---

# 36. Programmer Boundary

The programmer defines:

* local rules
* interfaces
* state ownership
* resource boundaries
* allowed transitions
* topology constraints

The programmer does not define the complete runtime interpretation of the system.

The programmer must not introduce an architecture that requires runtime components to possess information that only the programmer has.

The system must be able to operate from its own local rules.

---

# 37. Programmer Must Not Become Runtime God

The fact that a programmer can inspect the entire repository does not justify creating a runtime component that behaves as if it knows the repository.

Programmer knowledge is design-time knowledge.

Runtime knowledge must remain local.

This distinction is fundamental:

```text
Design time:
    programmer may understand architecture

Runtime:
    entities do not possess that understanding
```

---

# 38. Emergence

The system-level behavior of CIMA0 is not required to be explicitly represented by one module.

Higher-level structure may emerge from:

```text
local state
+
local rules
+
interaction
+
finite resources
+
time
+
decay
+
feedback
```

The architecture should preserve the possibility of such emergence.

A new module that attempts to directly encode the complete emergent behavior should be treated as an architectural warning.

---

# 39. Implementation Does Not Define Reality

The current shape, array size, tensor size, cache size, or buffer size is an implementation detail unless explicitly declared otherwise.

For example:

```text
PlanetField.state = (128,128)
```

does not mean:

```text
Planet's complete internal space = 128 × 128
```

Likewise:

```text
CLIP cloud = (12,50,768)
```

does not mean:

```text
the entire system exists in CLIP's coordinate system
```

Implementation representations must not silently become ontological definitions.

---

# 40. Phase Documents Are Subordinate

Phase documents describe:

* current implementation
* experiments
* temporary structures
* known limitations
* migration steps

They do not override this Constitution.

If a phase implementation conflicts with this Constitution, the implementation is considered transitional or incorrect until the conflict is explicitly resolved.

Historical phase documents remain valuable as history.

They are not automatically current architectural authority.

---

# 41. Architecture Review Rule

Before adding or substantially modifying a module, answer:

### 1. Who owns this state?

### 2. Who can modify this state?

### 3. Who can only observe this state?

Then answer:

### 4. What local knowledge does this module require?

### 5. What knowledge must remain unavailable to it?

### 6. What causal event activates it?

### 7. What responsibility ends when its operation ends?

### 8. Does the module introduce a hidden global view?

### 9. Does it create a permanent center, winner, focus, or mapping?

### 10. Could the same result be achieved without violating local responsibility?

If these questions cannot be answered clearly:

**Do not add code. Fix the topology first.**

---

# 42. Architecture Violation Indicators

The following are warning signs that a design may have introduced a God View:

```text
global_state
global_controller
global_observer
global_context
global_attention
global_focus
global_coordinate_map
global_interpreter
global winner
all-to-all comparison
complete-state aggregation
hidden shared memory
observer-driven mutation
central semantic decision
module A deciding what module B should compute
```

Any such mechanism requires explicit architectural justification.

In most cases, the correct solution is to restore local responsibility rather than expand the global mechanism.

---

# 43. Minimal Causality Model

CIMA0 should be understandable through local causality:

```text
local state
    |
    v
local rule
    |
    v
local event
    |
    v
local change
    |
    v
observable consequence
```

Other components may subsequently react if their own local rules and interfaces allow them to do so.

No global interpreter is required to make the system operate.

---

# 44. Core Architectural Test

A proposed design should pass the following test:

> Remove the hypothetical global observer.

If the system can no longer operate because some component must know what the entire system is doing, the architecture has probably introduced a hidden God View.

Likewise:

> Remove the hypothetical global controller.

If the system can no longer operate because one component must tell every other component what to do, the architecture has probably violated local autonomy.

---

# 45. Final Principle

CIMA0 does not attempt to construct a machine that knows everything.

CIMA0 constructs a system in which:

```text
no entity knows everything
```

yet:

```text
each entity knows enough
to perform its own responsibility.
```

The system is therefore not defined by a single mind.

It is defined by the interaction of limited entities.

The architecture must preserve that limitation.

---

# 46. One-Sentence Constitution

> **CIMA0 is a system without a God View: every entity knows only what its local responsibility requires, owns only its own state, acts only within its own boundary, and the behavior of the whole system emerges from their actual interactions rather than from a globally informed controller.**
