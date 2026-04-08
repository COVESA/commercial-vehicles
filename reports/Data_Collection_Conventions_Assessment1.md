# VSS Data Collection Conventions — Proposed Extensions

**Purpose:** Prescribe how vehicle signal data should be collected to support specific use cases, such that a separate data collector can produce data that is directly usable by a downstream processor without coordination beyond this specification. 

**Basis:**

Drawing from the simple approach of the COVESA Commercial and Fleet Vehicle guidelines for insurance and fleet purposes as well as the glipses into conventions expressed in Ford's proposed extensions to VSS document.

- [COVESA Commercial Vehicles – insurance-output.yaml](https://github.com/COVESA/commercial-vehicles/blob/main/tmp/convert-spreadsheet/insurance-output.yaml) — working example of `importance`, `usecase`, and `sampling` extensions
- [COVESA VSS – Gaps Feb 2025 (Google Doc)](https://docs.google.com/document/d/1OKjlefi6_gGIKYvbZIHdF8Syabj_7AvsiksKBXmT9mc/edit?tab=t.0) — Ford's proposed metadata extensions

---

## Existing Fields (from insurance-output.yaml)

The current YAML uses three extension fields per signal:

```yaml
Vehicle.Speed:
  importance: Must Have
  sampling: 5 Hz
  usecase: SAFETY10
```

| Field | Current vocabulary | Issues |
|-------|--------------------|--------|
| `importance` | `Must Have`, `Should Have`, `.nan` | Inconsistent casing; maps loosely to MoSCoW; needs controlled vocabulary |
| `usecase` | Opaque strings (`SAFETY04`, `MAINTENANCE08`) | Only meaningful with the use case catalogue; should be URIs or bundled |
| `sampling` | Mixed: `CHANGE`, `5Hz`, `20-50 Hz`, `Vehicle.LowVoltageSystemState='START'`, `CHANGE/0.008333f Hz`, `.nan` | Conflates mode, rate, and condition in one string; no formal grammar |

---

## Problem: `sampling` Conflates Three Distinct Concepts

The current `sampling` field mixes:
- **Mode** — *how* the trigger works (change-driven, periodic, conditional, hybrid)
- **Rate** — *how often* (Hz or period)
- **Condition** — *when* (a precondition expression referencing another signal)

Separating these enables machine-parseable specification and removes ambiguity. The sections below propose additional fields that replace the single `sampling` string with a structured set.

---

## Proposed Additional Fields

### 1. `transmission_mode`

Replaces the implicit mode embedded in `sampling`. Controlled vocabulary:

| Value | Meaning | Typical signals |
|-------|---------|----------------|
| `CHANGE` | Transmit on state change only | Boolean/enum states, warnings |
| `PERIODIC` | Transmit at fixed rate regardless of change | Speed, location, acceleration |
| `PERIODIC_RANGE` | Transmit within an adaptive rate range | Obstacle distance, kinematics |
| `CONDITIONAL` | Transmit only when a precondition is met | Signals gated on ignition state |
| `HYBRID` | Transmit on change AND at a minimum periodic rate | Odometric signals (distance) |

```yaml
Vehicle.Speed:
  transmission_mode: PERIODIC
  sampling_rate: 5Hz
  usecase: SAFETY10

Vehicle.Chassis.ParkingBrake.IsEngaged:
  transmission_mode: CONDITIONAL
  sampling_condition: "Vehicle.LowVoltageSystemState == 'START'"
  usecase: SAFETY12

Vehicle.TraveledDistance:
  transmission_mode: HYBRID
  sampling_rate: 0.00833Hz      # minimum periodic heartbeat
  usecase: SAFETY04
```

### 2. `sampling_rate`

An explicit numeric frequency (Hz) or period (s), separate from mode. Only meaningful for `PERIODIC`, `PERIODIC_RANGE`, and `HYBRID` modes. Format should always be normalized as `<float>Hz`.

```yaml
sampling_rate: 5.0Hz          # fixed
sampling_rate: 5.0-10.0Hz     # adaptive range (min-max)
sampling_rate: 0.00333Hz      # ~5 min interval
```

**Note:** A companion field `sampling_period` in seconds may be more readable for slow signals:
```yaml
sampling_rate: 0.00333Hz
sampling_period: 300s         # informative, redundant but human-readable
```

### 3. `sampling_condition`

A machine-parseable precondition expression, replacing the ad hoc string `Vehicle.LowVoltageSystemState='START'`. Uses a signal reference with equality operator:

```yaml
sampling_condition: "Vehicle.LowVoltageSystemState == 'START'"
```

This formalises Ford's proposed `signal_context.operational_conditions` (image 3 of the VSS Gaps document) as a structured expression rather than free text, making it evaluable by a collection agent.

Compound conditions should be supported:
```yaml
sampling_condition: "Vehicle.LowVoltageSystemState == 'START' AND Vehicle.Speed > 0"
```

### 4. `co_sample_group`

Declares that signals must be collected atomically — same timestamp, same collection event. Implements the dependency-chain atomic sampling concept from Ford's `depends_on` / `signal_context.dependencies`.

Signals sharing a `co_sample_group` label must be read together; a collector must not split the group across separate polling intervals.

```yaml
Vehicle.CurrentLocation.Latitude:
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  co_sample_group: location
  usecase: SAFETY09

Vehicle.CurrentLocation.Longitude:
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  co_sample_group: location
  usecase: SAFETY09

Vehicle.CurrentLocation.Altitude:
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  co_sample_group: location
  usecase: SAFETY09

Vehicle.CurrentLocation.Timestamp:
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  co_sample_group: location
  usecase: SAFETY09
```

Similarly, the three acceleration axes and three angular velocity axes should each form a co-sample group (collecting them at slightly different times invalidates vector composition).

### 5. `quality_factor_signal`

References the companion VSS signal that provides the quality/confidence indicator for this measurement. Drawn from Ford's `PlatformTypes.QualityFactor` struct pattern (image 6 of VSS Gaps). A collector should always read and transmit the QF signal alongside the value signal.

```yaml
Vehicle.Powertrain.CombustionEngine.Speed:
  transmission_mode: PERIODIC
  sampling_rate: 0.0333Hz
  quality_factor_signal: Vehicle.Powertrain.CombustionEngine.Speed.QualityFactor
  usecase: SAFETY14
```

Where no QF signal exists in VSS today, this field can be left absent; its absence flags a gap in signal coverage.

### 6. `signal_validity`

Declares the conditions under which a collected value is physically meaningful. Corresponds to Ford's `signal_context.operational_conditions`. Unlike `sampling_condition` (which gates *when* to collect), `signal_validity` describes *what makes the value valid once collected* — useful for flagging samples taken during transient states.

```yaml
Vehicle.Powertrain.CombustionEngine.EOP:
  transmission_mode: PERIODIC
  sampling_rate: 0.00333Hz
  signal_validity: "Vehicle.Powertrain.CombustionEngine.IsRunning == true"
  usecase: SAFETY15
```

A collection agent that cannot evaluate `signal_validity` should transmit the value with a `validity_unknown` flag rather than silently dropping it.

### 7. `signal_type`

Distinguishes cumulative/lifetime signals from instantaneous/real-time signals. Drawn from the structural difference between `AccumulatedBrakingEnergy` and `Range` in image 5 of the VSS Gaps document. This affects valid processing strategies downstream (e.g. a cumulative signal should never be averaged over time).

| Value | Meaning | Examples |
|-------|---------|---------|
| `instantaneous` | Point-in-time measurement | Speed, Temperature, Pressure |
| `cumulative` | Monotonically accumulating total | TraveledDistance, AccumulatedBrakingEnergy |
| `derived` | Computed from other signals | TimeRemaining, Range estimate |
| `state` | Discrete state machine value | Gear, LowVoltageSystemState |
| `event` | One-shot occurrence | Airbag deployment, FaultCode |

```yaml
Vehicle.TraveledDistance:
  signal_type: cumulative
  transmission_mode: HYBRID
  sampling_rate: 0.00833Hz
  usecase: SAFETY04

Vehicle.Speed:
  signal_type: instantaneous
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  usecase: SAFETY10

Vehicle.Cabin.Seat.Row1.DriverSide.Airbag.IsDeployed:
  signal_type: event
  transmission_mode: CHANGE
  usecase: SAFETY03
```

### 8. `privacy_classification`

Classifies the privacy sensitivity of the collected data. Relevant for regulatory compliance (GDPR, CCPA) and for informing `access_control` and `retention_policy`. Location, occupancy, and driver state signals are particularly sensitive.

| Value | Meaning |
|-------|---------|
| `public` | Not personally identifiable |
| `pseudonymous` | Linkable to a vehicle/device ID but not directly to a person |
| `personal` | Directly linkable to a natural person |
| `sensitive` | Special category under GDPR (health, biometric) |

```yaml
Vehicle.CurrentLocation.Latitude:
  privacy_classification: personal    # location history is personal data
  co_sample_group: location

Vehicle.Driver.FatigueLevel:
  privacy_classification: sensitive   # driver health/biometric-adjacent

Vehicle.Speed:
  privacy_classification: pseudonymous  # linkable to vehicle, not person directly
```

### 9. `access_control`

Declares which party or role is permitted to receive the collected signal data. Connects to Ford's cybersecurity metadata category.

| Value | Meaning |
|-------|---------|
| `public` | Any consumer |
| `fleet_operator` | Fleet manager / insurer / telematics provider |
| `oem` | Vehicle manufacturer only |
| `regulator` | Regulatory authority only |
| `owner` | Vehicle owner only |

```yaml
Vehicle.Driver.FatigueLevel:
  privacy_classification: sensitive
  access_control: fleet_operator

Vehicle.CurrentLocation.Latitude:
  privacy_classification: personal
  access_control: fleet_operator
```

### 10. `retention_policy`

Specifies how long collected data may be stored before mandatory deletion or anonymization. Relevant to GDPR Article 5(1)(e) and similar requirements.

```yaml
Vehicle.CurrentLocation.Latitude:
  privacy_classification: personal
  retention_policy: 90d              # delete or anonymize after 90 days

Vehicle.Speed:
  privacy_classification: pseudonymous
  retention_policy: 365d

Vehicle.Cabin.Seat.Row1.DriverSide.Airbag.IsDeployed:
  privacy_classification: pseudonymous
  retention_policy: unlimited        # event records may be retained for liability
```

---

## Complete Extended Example

Applying all proposed fields to a representative set of signals from insurance-output.yaml:

```yaml
# --- Location group: personal data, atomic, medium-frequency ---
Vehicle.CurrentLocation.Latitude:
  importance: Must Have
  usecase: SAFETY09
  signal_type: instantaneous
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  co_sample_group: location
  privacy_classification: personal
  access_control: fleet_operator
  retention_policy: 90d

Vehicle.CurrentLocation.Longitude:
  importance: Must Have
  usecase: SAFETY09
  signal_type: instantaneous
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  co_sample_group: location
  privacy_classification: personal
  access_control: fleet_operator
  retention_policy: 90d

Vehicle.CurrentLocation.Timestamp:
  importance: Must Have
  usecase: SAFETY09
  signal_type: instantaneous
  transmission_mode: PERIODIC
  sampling_rate: 5.0Hz
  co_sample_group: location
  privacy_classification: personal
  access_control: fleet_operator
  retention_policy: 90d

# --- Kinematics group: pseudonymous, atomic, high-frequency ---
Vehicle.Acceleration.Longitudinal:
  importance: Must Have
  usecase: SAFETY02 / SAFETY04
  signal_type: instantaneous
  transmission_mode: PERIODIC_RANGE
  sampling_rate: 20.0-50.0Hz
  co_sample_group: kinematics
  privacy_classification: pseudonymous
  access_control: fleet_operator
  retention_policy: 365d

Vehicle.AngularVelocity.Yaw:
  importance: Must Have
  usecase: SAFETY04
  signal_type: instantaneous
  transmission_mode: PERIODIC_RANGE
  sampling_rate: 20.0-50.0Hz
  co_sample_group: kinematics
  privacy_classification: pseudonymous
  access_control: fleet_operator
  retention_policy: 365d

# --- Odometric: cumulative, hybrid ---
Vehicle.TraveledDistance:
  importance: Must Have
  usecase: SAFETY04
  signal_type: cumulative
  transmission_mode: HYBRID
  sampling_rate: 0.00833Hz
  sampling_period: 120s
  privacy_classification: pseudonymous
  access_control: fleet_operator
  retention_policy: 365d

# --- Safety event: one-shot, no periodic ---
Vehicle.Cabin.Seat.Row1.DriverSide.Airbag.IsDeployed:
  importance: Must Have
  usecase: SAFETY03
  signal_type: event
  transmission_mode: CHANGE
  privacy_classification: pseudonymous
  access_control: fleet_operator
  retention_policy: unlimited

# --- Conditional: only sampled on ignition START ---
Vehicle.Chassis.ParkingBrake.IsEngaged:
  importance: Must Have
  usecase: SAFETY12
  signal_type: state
  transmission_mode: CONDITIONAL
  sampling_condition: "Vehicle.LowVoltageSystemState == 'START'"
  privacy_classification: pseudonymous
  access_control: fleet_operator
  retention_policy: 365d

# --- Driver state: sensitive / biometric-adjacent ---
Vehicle.Driver.FatigueLevel:
  importance: Must Have
  usecase: SAFETY13
  signal_type: derived
  transmission_mode: CHANGE
  privacy_classification: sensitive
  access_control: fleet_operator
  retention_policy: 30d
```

---

## Summary of Proposed Fields

| Field | Replaces / extends | Required? | Notes |
|-------|--------------------|-----------|-------|
| `transmission_mode` | `sampling` (mode component) | Yes | Controlled vocabulary |
| `sampling_rate` | `sampling` (rate component) | When mode is PERIODIC/PERIODIC_RANGE/HYBRID | Normalised as `<float>Hz` or `<float>-<float>Hz` |
| `sampling_period` | — | No | Informative redundant companion to `sampling_rate` for slow signals |
| `sampling_condition` | `sampling` (condition component) | When mode is CONDITIONAL | Formal signal reference expression |
| `co_sample_group` | Ford `depends_on` / `dependencies` | No | Label shared by signals that must be collected atomically |
| `quality_factor_signal` | Ford `QualityFactor` struct pattern | No | VSS path to companion QF signal |
| `signal_validity` | Ford `operational_conditions` | No | Signal reference expression; validity condition post-collection |
| `signal_type` | — | Yes | `instantaneous` / `cumulative` / `derived` / `state` / `event` |
| `privacy_classification` | Ford cybersecurity category | Yes | `public` / `pseudonymous` / `personal` / `sensitive` |
| `access_control` | Ford cybersecurity category | Yes | Role or party permitted to receive data |
| `retention_policy` | Ford cybersecurity + data collection | Yes | Duration or `unlimited` |

---

*Companion to: [COVESA VSS Gaps Feb 2025 Analysis](COVESA_VSS_Gaps_Feb2025_Analysis.md)*
