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

The following proposed extensions are most directly relevant to **how and when signals are sampled**:

| Field | Location | Relevance |
|-------|----------|-----------|
| `update_period` | Slide 3–4 text | Sampling rate / cadence |
| `init_value` | Slide 3–4 text | Value at collection start / baseline |
| `operational_conditions` | image 3 (`signal_context`) | Preconditions under which signal is valid for collection |
| `e2e_properties` | Slide 3–4 text | Transmission integrity from sensor to consumer |
| `dependencies` | image 3 (`signal_context`) | Co-sampling relationships — signals that must be read together |

The `signal_context.operational_conditions` field is the only one visually demonstrated in an image. The others (`update_period`, `init_value`, `e2e_properties`) are named in slide text without accompanying example syntax.

---

## Ford Next Steps (from slide 7 text)

1. Enhance signal completeness by adding new signals to VSS spec
2. Investigate and extend tooling support to generate C/C++ bindings from the spec
3. Participate in working sessions to address the gaps highlighted

---

*Analysis based on embedded images and slide text extracted from source document.*
