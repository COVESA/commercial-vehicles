# EU Battery Passport → COVESA VSS Signal Mapping

**Source:** [BatteryPassDataModel](https://github.com/batterypass/BatteryPassDataModel) v1.2.0
**Regulation:** EU Battery Regulation 2023/1542 | DIN DKE Spec 99100:2025-02
**VSS Reference:** COVESA Vehicle Signal Specification v6.0
**VSS Prefix:** `Vehicle.Powertrain.TractionBattery` (abbreviated as `TB` below)
**Date:** 2026-04-07
**Author:** Ted Guild, Geotab / COVESA

---

## Scope and Methodology

The Battery Passport defines 7 data modules. This document maps each data point
to an existing VSS signal where one exists, and drafts SUGGESTION entries for
signals a vehicle's Battery Management System (BMS) is capable of reporting but
that are absent from VSS v6.0.

**Excluded by scope:** `MaterialComposition` (chemical composition of battery
cells — not vehicle-reportable signals).

**Key distinction:** Battery Passport data splits into two categories:

- **Static/manufacturer data** — set at production time, not observable from a
  running vehicle (e.g., manufacturing place, warranty period, carbon footprint
  study URI, supply chain due diligence report). These cannot be VSS signals.
- **Dynamic/BMS-reportable data** — values the BMS measures or accumulates
  during operation (SoC, SoH, cycle count, temperature history, internal
  resistance, etc.). These can and should be VSS signals.

This mapping focuses on the second category.

---

## Module 1: GeneralProductInformation

| Battery Passport Field | VSS Signal | Status |
|---|---|---|
| `productIdentifier` (array of IDs) | `TB.Id` | Partial — VSS has a single battery ID string |
| `batteryPassportIdentifier` (UUID) | — | SUGGESTION — see below |
| `manufacturingDate` | `TB.ProductionDate` | **Match** — ISO 8601 date |
| `batteryCategory` (lmt/ev/industrial/stationary) | — | Not needed as a BMS signal; known from vehicle type |
| `batteryStatus` (Original/Repurposed/Reused/Remanufactured/Waste) | — | SUGGESTION — see below |
| `batteryMass` (kg) | — | SUGGESTION — see below |
| `manufacturerInformation` | — | Static manufacturer record, not a BMS signal |
| `manufacturingPlace` | — | Static, not a BMS signal |
| `operatorInformation` | — | Fleet/operator record, not a BMS signal |
| `puttingIntoService` | — | Could map to first activation date — no VSS signal |
| `warrantyPeriod` | — | Contract data, not a BMS signal |

---

## Module 2: CarbonFootprint

Carbon footprint values are manufacturing declarations (kg CO₂e per kWh
over the battery's expected service life). They are set at production and do
not change during vehicle operation. A vehicle *can* store and surface these
as static attributes accessible via VISS.

| Battery Passport Field | VSS Signal | Status |
|---|---|---|
| `batteryCarbonFootprint` (kg CO₂e / kWh) | — | SUGGESTION — see below |
| `carbonFootprintPerLifecycleStage` | — | Too granular for a BMS signal; reference URI preferred |
| `carbonFootprintPerformanceClass` (A–Z label) | — | SUGGESTION — see below |
| `carbonFootprintStudy` (URI) | — | Reference document, not a sensor value |
| `absoluteCarbonFootprint` (kg CO₂e, optional) | — | SUGGESTION — see below |

---

## Module 3: Performance and Durability

This is the richest module for VSS alignment. It splits into:
- **Technical specifications** — static design parameters set at manufacture
- **Battery condition** — dynamic values measured and updated by the BMS

### 3a. Technical Specifications (Static Design Parameters)

| Battery Passport Field | VSS Signal | Status |
|---|---|---|
| `nominalVoltage` (V) | `TB.NominalVoltage` | **Match** |
| `maximumVoltage` (V) | `TB.MaxVoltage` | **Match** |
| `minimumVoltage` (V) | — | SUGGESTION — see below |
| `ratedCapacity` (Ah) | `TB.GrossCapacity` (kWh) | Partial — different unit (Ah vs kWh); both needed |
| `ratedEnergy` (kWh) | `TB.NetCapacity` | **Match** |
| `ratedMaximumPower` (W) | — | SUGGESTION — see below |
| `temperatureRangeIdleState` (°C range) | — | SUGGESTION — see below |
| `expectedNumberOfCycles` | — | SUGGESTION — see below |
| `expectedLifetime` (years or cycles) | — | SUGGESTION — see below |
| `initialSelfDischarge` (% / month) | — | SUGGESTION — see below |
| `roundtripEfficiency` (%, initial) | — | SUGGESTION — see below |
| `initialInternalResistance` [{component, Ω}] | — | SUGGESTION — see below |
| `cRate` (C-rate at rated capacity) | — | SUGGESTION — see below |
| `cRateLifeCycleTest` | — | Test parameter, not a BMS signal |
| `powerCapabilityRatio` | — | SUGGESTION — see below |
| `capacityThresholdForExhaustion` (%) | — | SUGGESTION — see below |
| `lifetimeReferenceTest` (URI) | — | Reference document, not a sensor value |

### 3b. Battery Condition (Dynamic — BMS-Reported)

| Battery Passport Field | VSS Signal | Status |
|---|---|---|
| `stateOfCharge` | `TB.StateOfCharge.Current` | **Match** |
| `remainingEnergy` (Wh) | `TB.StateOfCharge.CurrentEnergy` | **Match** |
| `remainingCapacity` (Ah) | `TB.StateOfHealth` | Partial — SoH (%) captures fade; remaining Ah is not a separate signal |
| `capacityFade` (%) | — | SUGGESTION — see below |
| `stateOfCertifiedEnergy` (UBE remaining, Wh) | — | SUGGESTION — see below |
| `energyThroughput` (Wh accumulated) | `TB.AccumulatedConsumedEnergy` | **Match** |
| `capacityThroughput` (Ah accumulated) | `TB.AccumulatedConsumedThroughput` | **Match** |
| `numberOfFullCycles` | — | SUGGESTION — see below |
| `temperatureInformation.timeExtremeHighTemp` | — | SUGGESTION — see below |
| `temperatureInformation.timeExtremeLowTemp` | — | SUGGESTION — see below |
| `temperatureInformation.timeExtremeHighTempCharging` | — | SUGGESTION — see below |
| `temperatureInformation.timeExtremeLowTempCharging` | — | SUGGESTION — see below |
| `currentSelfDischargingRate` | — | SUGGESTION — see below |
| `evolutionOfSelfDischarge` (trend) | — | SUGGESTION — see below |
| `internalResistanceIncrease` [{component, Ω, timestamp}] | — | SUGGESTION — see below |
| `remainingPowerCapability` [{atSoC, powerAt}] | — | SUGGESTION — see below |
| `powerFade` (%) | — | SUGGESTION — see below |
| `roundTripEfficiencyFade` (%) | — | SUGGESTION — see below |
| `remainingRoundTripEnergyEfficiency` (%) | — | SUGGESTION — see below |
| `roundTripEfficiencyAt50PerCentCycleLife` (%) | — | SUGGESTION — see below |
| `negativeEvents` [{event, timestamp}] | — | SUGGESTION — see below |

---

## Module 4: Circularity

Circularity data is almost entirely manufacturer/EOL declarations, not
vehicle-observable signals. Exception: some safety data (extinguishing agents,
instructions) is potentially useful for emergency services via VISS.

| Battery Passport Field | VSS Signal | Status |
|---|---|---|
| `renewableContent` (% renewable materials) | — | Manufacturer declaration, not BMS signal |
| `recycledContent` [{material, preConsumer%, postConsumer%}] | — | Manufacturer declaration, not BMS signal |
| `dismantlingAndRemovalInformation` [documents] | — | Reference documents |
| `safetyInstructions` (URI) | — | Reference document |
| `extinguishingAgent` (list) | — | Reference data; useful for emergency response |
| `endOfLifeInformation` (URIs) | — | Reference documents |
| `sourceForSpareParts` / `sparePartSources` | — | Supply chain data |

---

## Module 5: Labels

Compliance documentation. Not vehicle-reportable BMS signals.

| Battery Passport Field | VSS Signal | Status |
|---|---|---|
| `euDeclarationOfConformityId` | — | Compliance identifier; SUGGESTION as attribute |
| `declarationOfConformity` (URI) | — | Reference document |
| `resultOfTestReport` (URI) | — | Reference document |
| `materialSymbols` | — | Label/marking data |
| `separateCollection` | — | Label/marking data |

---

## Module 6: SupplyChainDueDiligence

Entirely supply chain documentation URLs and ESG scores. Not vehicle-observable.

| Battery Passport Field | VSS Signal | Status |
|---|---|---|
| `supplyChainDueDiligenceReport` (URI) | — | Policy document, not BMS signal |
| `thirdPartyAssurances` (URI) | — | Certification document |
| `supplyChainIndicies` (ESG+ score) | — | SUGGESTION as static attribute |

---

## VSS SUGGESTION Entries

These are draft VSS signal additions for data a vehicle's BMS can measure and
report but that are absent from VSS v6.0. Format follows VSS .vspec YAML.
Signals are proposed under `Vehicle.Powertrain.TractionBattery` unless noted.

### Battery Identity and Status

```yaml
#
# SUGGESTION: Battery Passport identifier (EU Regulation 2023/1542 Art. 77)
#
Vehicle.Powertrain.TractionBattery.BatteryPassportId:
  datatype: string
  type: attribute
  description: >
    Unique identifier of the EU Battery Passport associated with this battery
    pack. Enables cross-referencing of vehicle signals with the battery's
    regulatory passport record. EU Battery Regulation 2023/1542, Art. 77.

#
# SUGGESTION: Battery lifecycle status
#
Vehicle.Powertrain.TractionBattery.LifecycleStatus:
  datatype: string
  type: attribute
  allowed: ['Original', 'Repurposed', 'Reused', 'Remanufactured', 'Waste']
  description: >
    Lifecycle status of the battery pack as defined by the EU Battery Passport.
    'Original' = first use in a vehicle. 'Repurposed' = new application
    (e.g., stationary storage). 'Reused' = same application after
    redeployment. 'Remanufactured' = rebuilt to original spec.
    EU Battery Regulation 2023/1542, Art. 2.

#
# SUGGESTION: Battery mass
#
Vehicle.Powertrain.TractionBattery.Mass:
  datatype: float
  type: attribute
  unit: kg
  description: >
    Mass of the complete battery pack in kilograms, as declared in the
    Battery Passport. EU Battery Regulation 2023/1542, Annex XIII.
```

### Carbon Footprint (Static Attributes from Passport)

```yaml
#
# SUGGESTION: Battery carbon footprint (functional unit)
#
Vehicle.Powertrain.TractionBattery.CarbonFootprint:
  datatype: float
  type: attribute
  unit: kg/kWh
  description: >
    Carbon footprint of the battery calculated as kg of CO2 equivalent per
    one kWh of total energy provided over the expected service life, as
    declared in the Battery Carbon Footprint Declaration.
    EU Battery Regulation 2023/1542, Art. 7 | DIN DKE Spec 99100: 6.3.2.

#
# SUGGESTION: Carbon footprint performance class
#
Vehicle.Powertrain.TractionBattery.CarbonFootprintPerformanceClass:
  datatype: string
  type: attribute
  description: >
    Carbon footprint performance class label (A = best / lowest footprint)
    assigned to the battery model per manufacturing plant.
    EU Battery Regulation 2023/1542, Art. 7(2) | DIN DKE Spec 99100: 6.3.7.

#
# SUGGESTION: Absolute carbon footprint
#
Vehicle.Powertrain.TractionBattery.AbsoluteCarbonFootprint:
  datatype: float
  type: attribute
  unit: kg
  description: >
    Total carbon footprint of the battery in kg CO2 equivalent (without
    normalization to functional unit). Optional per EU Battery Regulation.
    DIN DKE Spec 99100: 6.3.10.
```

### Performance: Static Design Specifications

```yaml
#
# SUGGESTION: Minimum design voltage
#
Vehicle.Powertrain.TractionBattery.MinVoltage:
  datatype: float
  type: attribute
  unit: V
  description: >
    Minimum permissible voltage of the battery pack (cut-off voltage).
    Complement to the existing MaxVoltage attribute.
    EU Battery Regulation 2023/1542, Annex XIII | DIN DKE Spec 99100: 6.2.5.

#
# SUGGESTION: Rated capacity in Ampere-hours
#
Vehicle.Powertrain.TractionBattery.RatedCapacityAh:
  datatype: float
  type: attribute
  unit: Ah
  description: >
    Rated capacity of the battery pack in Ampere-hours (Ah) at standard
    conditions. Complements GrossCapacity (kWh). The Battery Passport
    requires Ah; the current VSS provides only kWh.
    DIN DKE Spec 99100: 6.2.2.

#
# SUGGESTION: Rated maximum power
#
Vehicle.Powertrain.TractionBattery.RatedMaximumPower:
  datatype: float
  type: attribute
  unit: W
  description: >
    Maximum power the battery pack can deliver under rated conditions,
    as specified at manufacture. EU Battery Regulation 2023/1542, Annex XIII
    | DIN DKE Spec 99100: 6.2.7.

#
# SUGGESTION: Operating temperature range (idle)
#
Vehicle.Powertrain.TractionBattery.TemperatureRangeIdleMin:
  datatype: float
  type: attribute
  unit: celsius
  description: >
    Lower bound of the battery pack's permissible idle operating temperature
    range in degrees Celsius. DIN DKE Spec 99100: 6.2.10.

Vehicle.Powertrain.TractionBattery.TemperatureRangeIdleMax:
  datatype: float
  type: attribute
  unit: celsius
  description: >
    Upper bound of the battery pack's permissible idle operating temperature
    range in degrees Celsius. DIN DKE Spec 99100: 6.2.10.

#
# SUGGESTION: Expected number of charge/discharge cycles
#
Vehicle.Powertrain.TractionBattery.ExpectedNumberOfCycles:
  datatype: uint32
  type: attribute
  description: >
    Expected number of full charge/discharge cycles over the battery's
    lifetime under standard conditions at the rated C-rate.
    EU Battery Regulation 2023/1542, Annex XIII | DIN DKE Spec 99100: 6.2.11.

#
# SUGGESTION: Expected lifetime in years
#
Vehicle.Powertrain.TractionBattery.ExpectedLifetimeYears:
  datatype: float
  type: attribute
  unit: years
  description: >
    Expected calendar lifetime of the battery pack in years under typical
    operating conditions. EU Battery Regulation 2023/1542, Annex XIII.

#
# SUGGESTION: Initial self-discharge rate
#
Vehicle.Powertrain.TractionBattery.InitialSelfDischargeRate:
  datatype: float
  type: attribute
  unit: percent/month
  description: >
    Self-discharge rate of the battery at time of manufacture, expressed
    as percentage of rated capacity lost per month at standard temperature.
    DIN DKE Spec 99100: 6.2.14.

#
# SUGGESTION: Initial roundtrip energy efficiency
#
Vehicle.Powertrain.TractionBattery.InitialRoundTripEfficiency:
  datatype: float
  type: attribute
  unit: percent
  description: >
    Energy roundtrip efficiency of the battery at time of manufacture,
    expressed as percentage of energy returned on discharge relative to
    energy input on charge under standard conditions.
    DIN DKE Spec 99100: 6.2.13.

#
# SUGGESTION: Initial internal resistance (pack-level)
#
Vehicle.Powertrain.TractionBattery.InitialInternalResistance:
  datatype: float
  type: attribute
  unit: ohm
  description: >
    DC internal resistance of the battery pack at time of manufacture,
    in ohms. DIN DKE Spec 99100: 6.2.15.

#
# SUGGESTION: C-rate at rated capacity
#
Vehicle.Powertrain.TractionBattery.CRate:
  datatype: float
  type: attribute
  description: >
    C-rate value used to define the rated capacity and expected cycle life.
    Dimensionless ratio of discharge/charge current to rated capacity.
    DIN DKE Spec 99100: 6.2.3.

#
# SUGGESTION: Power capability ratio
#
Vehicle.Powertrain.TractionBattery.PowerCapabilityRatio:
  datatype: float
  type: attribute
  description: >
    Ratio of power capability at 80% SoC to power capability at 20% SoC,
    indicating flatness of the power delivery curve.
    EU Battery Regulation 2023/1542, Annex XIII.

#
# SUGGESTION: Capacity threshold for exhaustion
#
Vehicle.Powertrain.TractionBattery.CapacityThresholdForExhaustion:
  datatype: float
  type: attribute
  unit: percent
  description: >
    Minimum state of certified energy (SoCE) threshold below which the
    battery is considered exhausted for warranty and second-life purposes.
    DIN DKE Spec 99100: 6.2.8.
```

### Performance: Dynamic Battery Condition (BMS-Reported)

```yaml
#
# SUGGESTION: Number of full charge/discharge cycles accumulated
#
Vehicle.Powertrain.TractionBattery.StateOfCharge.NumberOfFullCycles:
  datatype: uint32
  type: sensor
  description: >
    Accumulated number of equivalent full charge/discharge cycles since
    battery manufacture. Updated by the BMS. Required by EU Battery Passport.
    DIN DKE Spec 99100: 6.2.11 (dynamic attribute).

#
# SUGGESTION: Capacity fade
#
Vehicle.Powertrain.TractionBattery.StateOfCharge.CapacityFade:
  datatype: float
  type: sensor
  unit: percent
  description: >
    Reduction in usable capacity relative to rated capacity, expressed as
    percentage. Complement to StateOfHealth. BMS-measured.
    EU Battery Regulation 2023/1542, Annex XIII | DIN DKE Spec 99100: 6.2.12.

#
# SUGGESTION: State of Certified Energy (UBE remaining)
#
Vehicle.Powertrain.TractionBattery.StateOfCertifiedEnergy:
  datatype: float
  type: sensor
  unit: kWh
  description: >
    Usable Battery Energy (UBE) remaining, i.e., the energy the battery can
    deliver from current state to the capacity exhaustion threshold under
    standard discharge conditions. EU Battery Regulation 2023/1542, Annex XIII
    | DIN DKE Spec 99100: 6.2.9.

#
# SUGGESTION: Power fade
#
Vehicle.Powertrain.TractionBattery.PowerFade:
  datatype: float
  type: sensor
  unit: percent
  description: >
    Reduction in peak power capability relative to original rated maximum
    power, expressed as percentage. BMS-measured.
    EU Battery Regulation 2023/1542, Annex XIII.

#
# SUGGESTION: Current internal resistance (pack-level)
#
Vehicle.Powertrain.TractionBattery.CurrentInternalResistance:
  datatype: float
  type: sensor
  unit: ohm
  description: >
    Current DC internal resistance of the battery pack measured by the BMS,
    in ohms. Enables calculation of internal resistance increase (IR fade).
    DIN DKE Spec 99100: 6.2.15 (dynamic attribute).

#
# SUGGESTION: Internal resistance increase
#
Vehicle.Powertrain.TractionBattery.InternalResistanceIncrease:
  datatype: float
  type: sensor
  unit: percent
  description: >
    Increase in internal resistance relative to initial value at manufacture,
    expressed as percentage. Indicator of battery aging.
    EU Battery Regulation 2023/1542, Annex XIII | DIN DKE Spec 99100: 6.2.16.

#
# SUGGESTION: Current self-discharge rate
#
Vehicle.Powertrain.TractionBattery.SelfDischargeRate:
  datatype: float
  type: sensor
  unit: percent/month
  description: >
    Current self-discharge rate measured by the BMS, expressed as percentage
    of remaining capacity lost per month. Increases with aging.
    DIN DKE Spec 99100: 6.2.14 (dynamic attribute).

#
# SUGGESTION: Current roundtrip energy efficiency
#
Vehicle.Powertrain.TractionBattery.RoundTripEfficiency:
  datatype: float
  type: sensor
  unit: percent
  description: >
    Current energy roundtrip efficiency of the battery pack measured by the
    BMS. Decreases with aging. EU Battery Regulation 2023/1542, Annex XIII
    | DIN DKE Spec 99100: 6.2.13 (dynamic attribute).

#
# SUGGESTION: Roundtrip efficiency fade
#
Vehicle.Powertrain.TractionBattery.RoundTripEfficiencyFade:
  datatype: float
  type: sensor
  unit: percent
  description: >
    Reduction in roundtrip energy efficiency relative to initial value at
    manufacture, expressed as percentage. BMS-measured.
    EU Battery Regulation 2023/1542, Annex XIII.

#
# SUGGESTION: Time spent above extreme high temperature threshold
#
Vehicle.Powertrain.TractionBattery.TemperatureExtremeHighDuration:
  datatype: float
  type: sensor
  unit: h
  description: >
    Cumulative time the battery has spent above an extreme high temperature
    threshold (BMS-defined), in hours. Indicator of thermal stress history.
    EU Battery Regulation 2023/1542, Annex XIII | DIN DKE Spec 99100: 6.2.18.

#
# SUGGESTION: Time spent below extreme low temperature threshold
#
Vehicle.Powertrain.TractionBattery.TemperatureExtremeLowDuration:
  datatype: float
  type: sensor
  unit: h
  description: >
    Cumulative time the battery has spent below an extreme low temperature
    threshold (BMS-defined), in hours. Indicator of cold stress history.
    DIN DKE Spec 99100: 6.2.18.

#
# SUGGESTION: Time spent above extreme high temperature during charging
#
Vehicle.Powertrain.TractionBattery.Charging.TemperatureExtremeHighDuration:
  datatype: float
  type: sensor
  unit: h
  description: >
    Cumulative time the battery has spent above an extreme high temperature
    threshold during charging events. EU Battery Regulation 2023/1542.

#
# SUGGESTION: Time spent below extreme low temperature during charging
#
Vehicle.Powertrain.TractionBattery.Charging.TemperatureExtremeLowDuration:
  datatype: float
  type: sensor
  unit: h
  description: >
    Cumulative time the battery has spent below an extreme low temperature
    threshold during charging events. EU Battery Regulation 2023/1542.

#
# SUGGESTION: Negative events log
#
Vehicle.Powertrain.TractionBattery.NegativeEvents:
  datatype: string[]
  type: sensor
  description: >
    List of negative events recorded by the BMS (e.g., deep discharge,
    overcurrent, overtemperature, external short circuit). Each entry is
    an event code or description string. EU Battery Regulation 2023/1542,
    Annex XIII | DIN DKE Spec 99100: 6.2.19.

#
# SUGGESTION: Power capability at current SoC
#
Vehicle.Powertrain.TractionBattery.PowerCapabilityAtCurrentSoC:
  datatype: float
  type: sensor
  unit: W
  description: >
    Maximum power the battery pack can deliver or accept at the current
    state of charge, as measured by the BMS. Enables the EU Battery Passport
    requirement for power capability curves expressed at specific SoC points.
    EU Battery Regulation 2023/1542, Annex XIII.
```

---

## Summary Table: Coverage by Module

| Module | Total Fields | Maps to VSS | New SUGGESTION | Not a BMS Signal |
|---|---|---|---|---|
| GeneralProductInformation | 11 | 2 | 3 | 6 |
| CarbonFootprint | 5 | 0 | 3 | 2 |
| Performance — Static | 14 | 3 | 11 | 0 |
| Performance — Dynamic | 19 | 5 | 14 | 0 |
| Circularity | 7 | 0 | 0 | 7 |
| Labels | 5 | 0 | 1 (EU conformity ID) | 4 |
| SupplyChainDueDiligence | 3 | 0 | 0 | 3 |
| **Total** | **64** | **10** | **32** | **22** |

---

## Existing VSS Signals That Cover Battery Passport Requirements

| VSS Signal | Battery Passport Field | Module |
|---|---|---|
| `TB.Id` | `productIdentifier` | GeneralProductInformation |
| `TB.ProductionDate` | `manufacturingDate` | GeneralProductInformation |
| `TB.NominalVoltage` | `nominalVoltage` | Performance (Static) |
| `TB.MaxVoltage` | `maximumVoltage` | Performance (Static) |
| `TB.GrossCapacity` | `ratedCapacity` (Ah — unit mismatch) | Performance (Static) |
| `TB.NetCapacity` | `ratedEnergy` (kWh) | Performance (Static) |
| `TB.StateOfCharge.Current` | `stateOfCharge` | Performance (Dynamic) |
| `TB.StateOfCharge.CurrentEnergy` | `remainingEnergy` | Performance (Dynamic) |
| `TB.AccumulatedConsumedEnergy` | `energyThroughput` | Performance (Dynamic) |
| `TB.AccumulatedConsumedThroughput` | `capacityThroughput` | Performance (Dynamic) |
| `TB.StateOfHealth` | `remainingCapacity` (capacity fade proxy) | Performance (Dynamic) |
| `TB.Temperature.{Min,Max,Average}` | `temperatureInformation` (partial) | Performance (Dynamic) |
| `TB.AccumulatedChargedEnergy` | Complements energy throughput | Performance (Dynamic) |
| `TB.AccumulatedChargedThroughput` | Complements capacity throughput | Performance (Dynamic) |

---

## Notes and Recommendations

1. **Unit gap for capacity:** The Battery Passport requires capacity in **Ah**
   (`ratedCapacity`). VSS `GrossCapacity` / `NetCapacity` use **kWh**. Both
   representations are needed. `RatedCapacityAh` should be added as a separate
   attribute rather than changing the existing signal.

2. **Power capability curves:** The Battery Passport requires power capability
   expressed at multiple SoC operating points (e.g., power at 20%, 50%, 80%
   SoC). VSS has no mechanism for this. Options: (a) add a single
   `PowerCapabilityAtCurrentSoC` sensor, or (b) define a curve representation
   as a structured attribute. The former is simpler and sufficient for
   real-time telemetry.

3. **Negative events:** The Battery Passport's `negativeEvents` list is a
   regulatory requirement (tracking abuse/fault history). VSS has no fault
   history log for the traction battery. A `string[]` sensor is the minimal
   viable approach; a structured approach with timestamps would be preferable.

4. **State of Certified Energy (SoCE):** This is a new EU concept — the
   Usable Battery Energy (UBE) at a given state of health, normalized to the
   capacity exhaustion threshold. It is distinct from `StateOfCharge` and
   from `StateOfHealth`. It deserves its own VSS signal.

5. **Temperature stress history:** The four temperature duration signals
   (high/low during operation and charging) are audit-trail data rather than
   instantaneous sensors. VSS currently has instantaneous temperature
   (Average, Min, Max) but no cumulative stress history. These are important
   for second-life battery assessment.

6. **Carbon footprint and passport identifier as attributes:** These are
   static values set at manufacture and could be delivered via VISS as
   `type: attribute` signals stored in the battery's BMS flash, rather than
   requiring a network call to the passport registry. This enables offline
   inspection by emergency services or maintenance technicians.

7. **Circularity and supply chain data:** These modules are entirely
   documentary — URIs pointing to external records. They cannot be expressed
   as VSS signals. The appropriate mechanism is the Battery Passport portal
   itself, with the battery ID as the key to look up these records.

---

## References

- [EU Battery Regulation 2023/1542](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R1542)
- [DIN DKE Spec 99100:2025-02](https://www.dke.de/de/arbeitsfelder/energy/battery-pass)
- [BatteryPassDataModel GitHub](https://github.com/batterypass/BatteryPassDataModel)
- [COVESA VSS v6.0](https://github.com/COVESA/vehicle_signal_specification)
- [VSS TractionBattery spec](https://covesa.github.io/vehicle_signal_specification/spec/Powertrain/TractionBattery/)
- [W3C VISS (Vehicle Information Service Specification)](https://www.w3.org/TR/viss2-core/)
