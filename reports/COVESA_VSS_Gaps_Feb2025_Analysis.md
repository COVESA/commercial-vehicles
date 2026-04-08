# COVESA VSS Gaps – Feb 2025: Proposed Extensions Analysis

Source: [COVESA VSS – Gaps Feb 2025 (Google Doc)](https://docs.google.com/document/d/1OKjlefi6_gGIKYvbZIHdF8Syabj_7AvsiksKBXmT9mc/edit?tab=t.0)

Contributor: Ford

---

## Summary of Proposed VSS Extensions

### 1. Signal Relationships (Slides 1–2)

Ford proposes an overlay/dependency mechanism to express how signals relate to one another, enabling cross-signal analytics and diagnostics.

**Proposed overlay syntax (image 2):**
```yaml
analytics.engine_temperature:
  description: >
    engine temperature is indirectly proportionate to engine coolant level
    and directly proportionate to engine coolant pressure and quality factor
  relationship: dependency
  signal: Vehicle.Powertrain.EngineCoolant.Temperature
  depends_on:
    - Vehicle.Powertrain.EngineCoolant.Level
    - Vehicle.Powertrain.EngineCoolant.Pressure
    - Vehicle.Powertrain.EngineCoolant.QualityFactor
```

**Motivating use cases:**
- Engine temperature rise correlated with oil pressure drop → lubrication failure warning
- Engine temperature rise correlated with low coolant level → cooling system fault
- Quality factor (QF) of temperature sensor affects interpretation of temperature data

---

### 2. Signal Metadata Extensions (Slides 3–4)

Ford identifies that the current VSS signal definition is too sparse for cross-functional use. The existing baseline (image 4) contains only:

```yaml
Temperature:
  datatype: float
  type: sensor
  unit: celsius
  description: Engine coolant temperature.
```

**Proposed addition — `signal_context` block (image 3):**
```yaml
Vehicle.Powertrain.EngineCoolant.Temperature:
  description: >
    engine temperature is indirectly proportionate to engine coolant level
    and directly proportionate to engine coolant pressure and quality factor
  type: sensor
  datatype: float32
  signal_context:
    operational_conditions: "Normal operation, not during engine startup"
    dependencies:
      - Vehicle.Powertrain.EngineCoolant.Level
      - Vehicle.Powertrain.EngineCoolant.Pressure
```

**Additional metadata fields listed in slide text (not shown in images):**

| Proposed Field | Purpose |
|----------------|---------|
| `unique_identifier` | Signal identity across systems and OEM toolchains |
| `init_value` | Baseline/default value at collection start |
| `update_period` | Sampling rate / update frequency |
| `e2e_properties` | End-to-end transmission properties (pipeline integrity) |
| `operational_conditions` | When the signal is valid / preconditions for sampling |
| `dependencies` | Other signals this signal depends on |

Cross-functional concerns motivating these additions: cybersecurity, functional safety, data collection, network serialization.

---

### 3. Complex / Nested Datatype Definitions (Slides 5–6)

Ford proposes two syntactic approaches for defining nested struct types in VSS.

**Option A — Flat path notation (image 5):**
```yaml
PowerTrainInfoSignalGroup.PowerTrainInfoStruct:
  type: struct
  description: "A struct with datatype property defined."

PowerTrainInfoSignalGroup.PowerTrainInfoStruct.AccumulatedBrakingEnergy:
  datatype: float
  type: property
  unit: kWh
  description: The accumulated energy from regenerative braking over lifetime.

PowerTrainInfoSignalGroup.PowerTrainInfoStruct.Range:
  datatype: uint32
  type: property
  unit: m
  description: Remaining range in meters using all energy sources available in the vehicle.

PowerTrainInfoSignalGroup.PowerTrainInfoStruct.time:
  type: struct
  description: "nested struct"

PowerTrainInfoSignalGroup.PowerTrainInfoStruct.time.TimeRemaining:
  datatype: uint32
  type: property
  unit: s
  description: Time remaining in seconds before all energy sources available in the vehicle are empty.
```

**Option B — Inline `elements:` syntax (image 6):**
```yaml
PowerTrainInfoStruct:
  description: "Represents the overall vehicle system."
  type: struct
  elements:
    - AccumulatedBrakingEnergyStruct:
        description: " "
        type: struct
        elements:
          - Value: PowerTrain.AccumulatedBrakingEnergy
          - QualityFactor: PlatformTypes.QualityFactor
    - TimeRemaining: PowerTrain.Time
```

**Problems with the current VSS approach that motivate this:**
- Defining nested structs via branching is cumbersome
- Limited reuse of nested struct definitions
- Generated file formats are flat; IDL output does not accurately represent intended struct definitions

---

## Data Collection / Sampling Subset

The following proposed extensions are most directly relevant to **how and when signals are sampled, transmitted, governed, and retained**. Fields are grouped by concern.

### Sampling / Collection Conditions

| Field | Source | Relevance |
|-------|--------|-----------|
| `update_period` | Slide 3–4 text | Sampling rate / cadence (e.g. 100ms, on-change) |
| `init_value` | Slide 3–4 text | Baseline/default value at collection start |
| `operational_conditions` | image 3 (`signal_context`) | Preconditions under which signal is valid for collection (e.g. "Normal operation, not during engine startup") |
| `dependencies` | image 3 (`signal_context`) | Co-sampling relationships — signals that must be observed together for valid interpretation |

### Transmission

| Field | Source | Relevance |
|-------|--------|-----------|
| `transmission_mode` | Implied by slide 3–4 (`e2e_properties`, Network Serialization) | How signal values are sent: periodic, event-driven (on-change), or on-request/pull |
| `e2e_properties` | Slide 3–4 text | End-to-end transmission properties — integrity, latency, ordering guarantees from sensor to consumer |

### Privacy and Access Control

Ford's slide 3 identifies **cybersecurity** as one of the four cross-functional metadata categories alongside data collection. The following fields elaborate that concern as it applies to sampled signal data:

| Field | Source | Relevance |
|-------|--------|-----------|
| `privacy_consideration` | Cybersecurity category (slide 3–4) | Whether sampled values require consent, anonymization, or pseudonymization (e.g. location, biometric-adjacent signals) |
| `access_control` | Cybersecurity category (slide 3–4) | Role or party allowed to read sampled data — e.g. OEM-only, fleet operator, public |

### Retention

| Field | Source | Relevance |
|-------|--------|-----------|
| `retention_policy` | Implied by data collection + cybersecurity (slide 3–4) | How long sampled data may be stored before mandatory deletion or anonymization; relevant to GDPR and regional regulatory compliance |

### Additional Collection Guidelines Derived from Image Patterns

Beyond the named metadata fields, the image examples reveal several implicit conventions that should inform data collection design:

#### 1. Quality Factor (QF) as a Mandatory Companion

Image 2 lists `Vehicle.Powertrain.EngineCoolant.QualityFactor` as a `depends_on` entry for temperature — not just a related signal but a precondition for valid interpretation. Image 6 makes this structural: `AccumulatedBrakingEnergyStruct` bundles `Value` and `QualityFactor` as siblings using `PlatformTypes.QualityFactor` as a standardized type.

**Guideline:** Sampled values should be paired with a quality factor as a typed struct. Collection systems should evaluate QF before transmitting or acting on a sample. A low QF should suppress downstream analytics or trigger a sensor-health alert, not silently propagate a bad reading.

```yaml
# Implied standard pattern from image 6:
AccumulatedBrakingEnergyStruct:
  type: struct
  elements:
    - Value: PowerTrain.AccumulatedBrakingEnergy   # the measurement
    - QualityFactor: PlatformTypes.QualityFactor   # confidence in the measurement
```

#### 2. Atomic Sampling of Dependency Chains

Image 2's `depends_on` list and image 3's `dependencies` block both express that certain signals are only meaningful when observed together. Sampling them at different timestamps invalidates the declared relationship (e.g. a temperature reading correlated against stale coolant pressure data).

**Guideline:** Signals sharing a `depends_on` / `dependencies` relationship should be sampled atomically — same timestamp, same collection event. Individual signal polling intervals should not break apart a declared dependency group.

#### 3. Operational Validity Gating

Image 3 shows `operational_conditions: "Normal operation, not during engine startup"`. This is not merely informational — it defines when a sample is physically meaningful.

**Guideline:** Collection pipelines should evaluate `operational_conditions` before recording or transmitting a sample. Samples collected outside valid conditions should either be:
- suppressed (not transmitted), or
- flagged with a validity/status bit alongside the value

This connects directly to `init_value`: a value recorded before operational conditions are met may be an artefact of startup state, not a real measurement.

#### 4. Cumulative vs. Instantaneous Signal Distinction

Image 5 shows two structurally different signals in the same struct:
- `AccumulatedBrakingEnergy` (float, kWh) — a lifetime aggregate, increases monotonically
- `Range` (uint32, m) — an instantaneous estimate, changes continuously

These require fundamentally different collection strategies:

| Signal type | Example | Appropriate cadence |
|-------------|---------|---------------------|
| Cumulative / lifetime | `AccumulatedBrakingEnergy` | On significant delta, or periodic low-frequency |
| Instantaneous / real-time | `Range`, `Temperature` | Periodic or on-change with threshold |
| Remaining / derived | `TimeRemaining` | On-change with threshold |

**Guideline:** Signal metadata should declare whether a value is cumulative or instantaneous, as this determines valid sampling strategies. Treating a lifetime aggregate as a real-time signal wastes bandwidth and creates false change events.

#### 5. Struct-Based Transmission Units

Images 5 and 6 both propose grouping related signals into structs rather than transmitting them individually. This has direct data collection implications:

**Guideline:** Logically related signals (same subsystem, same validity window, same dependency group) should be collected and transmitted as a unit. This:
- prevents partial-state inconsistencies (consumer receives some signals but not their dependents)
- enables atomic QF evaluation across the group
- reduces per-signal framing overhead

The `time` nested struct in image 5 (`PowerTrainInfoStruct.time.TimeRemaining`) further suggests that **temporal metadata should be a first-class struct member**, not an out-of-band convention.

### Notes on Source Attribution

- `operational_conditions` and `dependencies` are explicitly shown in image 3 with example syntax.
- `QualityFactor` as a value companion is shown in image 6 struct definition; as a dependency in image 2.
- `update_period`, `init_value`, and `e2e_properties` are named in slide text without accompanying example syntax.
- `transmission_mode`, `privacy_consideration`, `access_control`, and `retention_policy` are not named verbatim in the document but are directly implied by Ford's four stated metadata categories (cybersecurity, functional safety, data collection, network serialization) and are pertinent additions for a complete data collection/sampling metadata model.
- Guidelines for atomic sampling, validity gating, cumulative vs. instantaneous distinction, and struct-based transmission units are derived from patterns in the image examples, not stated explicitly in the document.

---

## Ford Next Steps (from slide 7 text)

1. Enhance signal completeness by adding new signals to VSS spec
2. Investigate and extend tooling support to generate C/C++ bindings from the spec
3. Participate in working sessions to address the gaps highlighted

---

*Analysis based on embedded images and slide text extracted from source document.*
