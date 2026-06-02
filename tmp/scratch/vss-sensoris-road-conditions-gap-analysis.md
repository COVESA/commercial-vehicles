# VSS ↔ SENSORIS Road Conditions and Visibility Gap Analysis

**Author:** Ted Guild (edwardguild@geotab.com) — Geotab / COVESA
**Date:** June 2026
**Purpose:** Identify SENSORIS v1.6.0 signals for road conditions, visibility, and weather that are absent from or partially covered by the current Vehicle Signal Specification (VSS), and draft candidate vspec definitions for missing signals.

**References:**
- SENSORIS v1.6.0 protobuf spec: `/home/edwardguild/doc/covesa/fleet/sensoris-specification-v1.6.0-public/`
- VSS main branch Exterior.vspec: `spec/Vehicle/Exterior.vspec` (GitHub: `COVESA/vehicle_signal_specification`)
- VSS Safety.vspec: `spec/Safety/Safety.vspec`
- Road.vspec scratch file: `/home/edwardguild/doc/covesa/fleet/commercial-vehicles/tmp/scratch/Road.vspec`
- PR #906 (open): `feat(safety): add Whiteout + RoadIcingState derived-assessment signals`
- PR #892 (merged 2026-05-05): Added `Vehicle.Exterior.RoadSurfaceCondition`
- PR #894 (merged 2026-05-05): Added `Vehicle.Safety.IsFire`, `IsSubmersed`, `Rollover`

---

## 1. Current VSS Signals: Road, Weather, Visibility

### Vehicle.Exterior (spec/Vehicle/Exterior.vspec)
| Signal | Datatype | Notes |
|--------|----------|-------|
| AirTemperature | float (°C) | Exists |
| Humidity | float (%) | Exists |
| LightIntensity | float (%) | Exists |
| RoadSurfaceCondition | string enum | Merged PR #892; DRY/WET/SNOW/ICE/SLUSH/WET_ICE/LOOSE_GRAVEL/UNKNOWN |

### Vehicle.Body.Raindetection
| Signal | Datatype | Notes |
|--------|----------|-------|
| Intensity | uint8 (%) | Exists; 0=Dry, 100=Covered |

### Vehicle.Body.Windshield.[Front|Rear].Wiping
| Signal | Datatype | Notes |
|--------|----------|-------|
| Mode | string enum | OFF/SLOW/MEDIUM/FAST/INTERVAL/RAIN_SENSOR |
| Intensity | uint8 | Interval/rain-sensor sensitivity |
| System.Frequency | uint8 (cpm) | Exists |
| WiperWear | uint8 (%) | Exists |

### Vehicle.ADAS.ESC.RoadFriction
| Signal | Datatype | Notes |
|--------|----------|-------|
| MostProbable | float (%) | Exists |
| LowerBound | float (%) | Exists |
| UpperBound | float (%) | Exists |

### Vehicle.Safety (spec/Safety/Safety.vspec)
| Signal | Datatype | Notes |
|--------|----------|-------|
| IsFire | boolean | Merged PR #894 |
| IsSubmersed | boolean | Merged PR #894 |
| Rollover | string enum (UNKNOWN/NONE/RISK/DETECTED) | Merged PR #894 |
| Whiteout | string enum (UNKNOWN/NONE/RISK/DETECTED) | PR #906, open |
| RoadIcingState | string enum (UNKNOWN/NONE/RISK/DETECTED) | PR #906, open |

---

## 2. SENSORIS v1.6.0 Signal Inventory (Road, Weather, Visibility)

### weather.proto

#### VisibilityCondition
- `type_and_confidence.type`: CLEAR / MIST / LOW_HEAVY_RAIN / LOW_HEAVY_SNOW / LOW_SMOKE / LOW_FOG / LOW_SUN_GLARE
- `visible_distance_and_accuracy` (meters)
- `sensor_detection_distance_and_accuracy` (meters)

#### Precipitation
- `type_and_confidence.type`: NONE / RAIN / MIXED_RAIN_SNOW / SNOW / HAIL
- `relative_intensity_and_accuracy` (%, 0–100)
- `absolute_intensity_and_accuracy` (mm/hr)

#### AtmosphereCondition
- `outside_air_temperature` (°C) → **covered** by `Vehicle.Exterior.AirTemperature`
- `relative_humidity` (%, 0–100) → **covered** by `Vehicle.Exterior.Humidity`
- `static_air_pressure` (hPa) → **missing from VSS**

#### WindCondition
- `type_and_confidence.type`: VARIABLE / STRONG / STRONG_CROSS / STORM
- `speed_and_accuracy` (m/s)
- `direction_and_accuracy` (degrees, 0–360)

#### LightIntensity
- `relative_intensity_and_accuracy` (%) → **covered** by `Vehicle.Exterior.LightIntensity`

### traffic_events.proto

#### RoadWeatherCondition (TPEG-TEC compliant, hazard-grade events)
- `type_and_confidence.type`: SNOW / ICE / FREEZING_RAIN (black ice) / FROST / HYDROPLANING / FLOODING / WATER (wet surface)
- `depth_and_accuracy` (mm) — water/snow depth measurement

#### RoadSurfaceCondition (TPEG-TEC, non-weather hazards)
- `type_and_confidence.type`: MUD / CHIPPINGS / OIL / FUEL
- Note: VSS `RoadSurfaceCondition` covers weather states (ICE, SNOW, WET…); SENSORIS has a separate message for non-weather surface contaminants.

#### RoadObstructionCondition
- `type_and_confidence.type`: TREE / AVALANCHE / ROCKFALLS / SHED_LOAD / LAND_SLIP / ANIMAL / ANIMAL_LARGE / ANIMAL_HERD
- No VSS equivalent exists.

#### RoadFriction
- `most_probable` (%, 0–100, resolution 0.01) → **covered** by `Vehicle.ADAS.ESC.RoadFriction.MostProbable`
- `lower_bound` / `upper_bound` → **covered** by `Vehicle.ADAS.ESC.RoadFriction.LowerBound` / `UpperBound`

#### Hazard (weather-related subset)
- SLIPPERY_ROAD / EXCEPTIONAL_CONDITION_LOW_VISIBILITY / EXCEPTIONAL_CONDITION_PRECIPITATION / EXCEPTIONAL_CONDITION_WIND / EXCEPTIONAL_CONDITION_ROAD_SURFACE
- Hazard-level roll-up signal — **no VSS equivalent exists**

### road_attribution.proto

#### SurfaceAttribution
- `material_and_confidence.type`: ASPHALT / CONCRETE / COMPOSITE_PAVEMENT / RECYCLING / GRAVEL / COBBLESTONE
- `road_roughness_and_accuracy` (IRI, mm/km) — International Roughness Index
- `inclination_and_curvature` → partially in `Vehicle.AngularVelocity`, `Vehicle.Orientation`

#### InclinationAndCurvature
- `longitudinal_inclination_and_accuracy` (slope, degrees) → **partially covered** by `Vehicle.Orientation.Pitch` (vehicle attitude, not road geometry)
- `lateral_inclination_and_accuracy` (cross-fall, degrees)
- `horizontal_curvature_and_accuracy` (1/km)

### vehicle_device.proto

#### WiperStatus
- `speed_type`: OFF / SLOW / MEDIUM / FAST / AUTOMATIC / WASHING / SINGLE
- `speed_and_accuracy` (RPM)
- VSS covers Mode (with RAIN_SENSOR) and Frequency (cpm) — **AUTOMATIC** mode not in VSS Mode enum; RPM measurement not in VSS

---

## 3. Gap Summary

| SENSORIS Signal / Concept | VSS Coverage | Gap Assessment |
|---------------------------|-------------|----------------|
| VisibilityCondition.type (CLEAR/MIST/LOW_FOG/LOW_HEAVY_RAIN/LOW_HEAVY_SNOW/LOW_SMOKE/LOW_SUN_GLARE) | None | **Missing** |
| VisibilityCondition.visible_distance (meters) | None | **Missing** |
| VisibilityCondition.sensor_detection_distance (meters) | None | **Missing** |
| Precipitation.type (NONE/RAIN/MIXED_RAIN_SNOW/SNOW/HAIL) | Body.Raindetection.Intensity (rain only, no type) | **Partial** — no type discrimination, no snow/hail |
| Precipitation.relative_intensity (%) | Body.Raindetection.Intensity | **Covered** (rain only) |
| Precipitation.absolute_intensity (mm/hr) | None | **Missing** |
| AtmosphereCondition.static_air_pressure (hPa) | None | **Missing** |
| WindCondition.type (VARIABLE/STRONG/STRONG_CROSS/STORM) | None | **Missing** |
| WindCondition.speed (m/s) | None | **Missing** |
| WindCondition.direction (degrees) | None | **Missing** |
| RoadWeatherCondition.type (SNOW/ICE/FREEZING_RAIN/FROST/HYDROPLANING/FLOODING/WATER) | Exterior.RoadSurfaceCondition covers ICE/SNOW/WET partially; PR #906 adds RoadIcingState | **Partial** — HYDROPLANING, FLOODING, FROST not covered |
| RoadWeatherCondition.depth (mm) | None | **Missing** |
| RoadSurfaceCondition.type (MUD/CHIPPINGS/OIL/FUEL) | None — VSS RoadSurfaceCondition is weather states only | **Missing** (non-weather contaminants) |
| RoadObstructionCondition (TREE/AVALANCHE/ROCKFALLS/ANIMAL/SHED_LOAD…) | None | **Missing** |
| Hazard (weather roll-up: LOW_VISIBILITY/PRECIPITATION/WIND/ROAD_SURFACE) | Safety.Whiteout + Safety.RoadIcingState (PR #906) cover two cases | **Partial** |
| SurfaceAttribution.material (ASPHALT/CONCRETE/GRAVEL/COBBLESTONE…) | None | **Missing** (road material classification) |
| SurfaceAttribution.road_roughness (IRI, mm/km) | None | **Missing** |
| Road geometry: longitudinal slope, lateral cross-fall, horizontal curvature | Orientation.Pitch/Roll are vehicle attitude, not road geometry | **Distinct gap** |
| WiperStatus.AUTOMATIC mode | Wiping.Mode has RAIN_SENSOR but not AUTOMATIC | **Minor gap** |
| WiperStatus.speed (RPM) | Wiping.System.Frequency (cpm) — different unit, conceptually equivalent | **Covered** with unit translation |
| AirTemperature | Exterior.AirTemperature | **Covered** |
| Humidity | Exterior.Humidity | **Covered** |
| LightIntensity | Exterior.LightIntensity | **Covered** |
| RoadFriction | ADAS.ESC.RoadFriction | **Covered** |

---

## 4. Prioritization for VSS Contribution

### Priority 1 — High value, well-defined, no blockers

These signals map cleanly from SENSORIS to VSS and fill gaps that matter for connected safety, fleet telematics (VEDS), and navigation:

1. **Vehicle.Exterior.VisibilityCondition** — type enum + visible distance
2. **Vehicle.Exterior.PrecipitationType** — discriminated precipitation type (extends Raindetection)
3. **Vehicle.Exterior.PrecipitationIntensity.AbsoluteRate** — mm/hr measurement
4. **Vehicle.Exterior.WindSpeed** and **WindDirection**
5. **Vehicle.Exterior.AirPressure** — atmospheric pressure

### Priority 2 — Useful but needs architectural decision

These require discussion of where in the VSS tree they belong (Exterior? Safety? Road? ADAS?):

6. **Vehicle.Exterior.RoadSurfaceContaminant** — non-weather surface hazards (MUD/OIL/FUEL/CHIPPINGS), distinct from weather-state `RoadSurfaceCondition`
7. **Vehicle.Exterior.RoadObstruction** — detected road obstructions (ANIMAL/TREE/AVALANCHE/ROCKFALLS…)
8. **Vehicle.Road.Geometry** — slope, cross-fall, curvature (road geometry distinct from vehicle attitude)
9. **Vehicle.Road.SurfaceMaterial** — ASPHALT/CONCRETE/GRAVEL/COBBLESTONE (road attribution)
10. **Vehicle.Road.Roughness** — IRI measurement

### Priority 3 — Lower urgency, scope discussion needed

11. **Weather hazard roll-up** — generalized exceptional condition flag (covers LOW_VISIBILITY, PRECIPITATION, WIND, ROAD_SURFACE as a single assessable hazard level). May be premature if PR #906 handles the most safety-critical cases (whiteout + icing).

---

## 5. Draft vspec Definitions

These are candidate vspec signal definitions for VSS contribution. Each follows the pattern established by existing merged signals (`RoadSurfaceCondition`, `Rollover`, `IsFire`).

**Placement note:** Signals 5.1–5.5 target `spec/Vehicle/Exterior.vspec`. Signals 5.6–5.7 require a new branch discussion (proposed `Vehicle.Road.*`). Signal 5.8 targets `spec/Vehicle/Exterior.vspec`.

---

### 5.1 VisibilityCondition (Exterior.vspec)

```vspec
VisibilityCondition:
  datatype: string
  type: sensor
  allowed: [
    'UNKNOWN',
    'CLEAR',
    'MIST',
    'LOW_FOG',
    'LOW_HEAVY_RAIN',
    'LOW_HEAVY_SNOW',
    'LOW_SMOKE',
    'LOW_SUN_GLARE'
  ]
  description: Assessed visibility condition outside the vehicle.
  comment: >
    Reports the dominant cause of reduced visibility. CLEAR indicates no
    significant visibility reduction. LOW_* values indicate conditions that
    materially reduce driver or sensor visibility range.
    UNKNOWN shall be used when visibility condition cannot be assessed
    (e.g., camera unavailable or confidence below threshold).
    Determination method is implementation specific. May be derived from
    camera-based classification, Vehicle.Body.Raindetection.Intensity,
    Vehicle.Exterior.AirTemperature, and Vehicle.Body.Windshield.Wiping.Mode.
    Complements Vehicle.Exterior.VisibilityDistance for quantitative range.
    Related to SENSORIS v1.6 VisibilityCondition.TypeAndConfidence.
    Primary consumers: ADAS systems, navigation (dynamic re-routing), and
    emergency dispatch systems.
    Related to VSS issue #877 (Connected Safety signals).
```

---

### 5.2 VisibilityDistance (Exterior.vspec)

```vspec
VisibilityDistance:
  datatype: float
  type: sensor
  unit: m
  min: 0
  description: Estimated visible distance ahead of the vehicle in current conditions.
  comment: >
    Forward visibility range in meters as assessed by the vehicle's sensing
    systems. 0 indicates near-zero visibility. Value may be limited by sensor
    range rather than actual atmospheric visibility; see VisibilityCondition
    for the qualitative assessment.
    Determination method is implementation specific. May be derived from
    camera-based visibility estimation, lidar range reduction, or
    radar clutter analysis.
    Related to SENSORIS v1.6 VisibilityCondition.visible_distance_and_accuracy.
    Related to VSS issue #877 (Connected Safety signals).
```

---

### 5.3 PrecipitationType (Exterior.vspec)

```vspec
PrecipitationType:
  datatype: string
  type: sensor
  allowed: [
    'UNKNOWN',
    'NONE',
    'RAIN',
    'MIXED_RAIN_SNOW',
    'SNOW',
    'HAIL'
  ]
  description: Type of precipitation currently detected outside the vehicle.
  comment: >
    Discriminates precipitation type from Vehicle.Body.Raindetection.Intensity,
    which reports intensity for rain only. NONE indicates no precipitation
    detected. HAIL includes sleet and freezing rain as a precipitation
    type (distinct from black ice formation on the road surface, which is
    reported by Vehicle.Safety.RoadIcingState).
    UNKNOWN shall be used when precipitation type cannot be assessed.
    Determination method is implementation specific.
    Related to SENSORIS v1.6 Precipitation.TypeAndConfidence.
    Related to VSS issue #877 (Connected Safety signals).
```

---

### 5.4 PrecipitationIntensity (Exterior.vspec)

```vspec
PrecipitationIntensity:
  datatype: float
  type: sensor
  unit: mm/h
  min: 0
  description: Precipitation intensity in millimeters per hour.
  comment: >
    Provides an absolute intensity measurement complementing
    Vehicle.Body.Raindetection.Intensity (which is a relative 0–100 percent
    scale). Applies to all precipitation types reported by
    Vehicle.Exterior.PrecipitationType; value is 0 when PrecipitationType
    is NONE. Measurement method is sensor specific.
    Related to SENSORIS v1.6 Precipitation.absolute_intensity_and_accuracy.
    Related to VSS issue #877 (Connected Safety signals).
```

---

### 5.5 AirPressure (Exterior.vspec)

```vspec
AirPressure:
  datatype: float
  type: sensor
  unit: hPa
  description: Atmospheric air pressure outside the vehicle.
  comment: >
    Static ambient air pressure measured by the vehicle's barometric sensor.
    May be used for altitude estimation, weather trend detection, and HVAC
    pressurization management.
    Related to SENSORIS v1.6 AtmosphereCondition.static_air_pressure.
```

---

### 5.6 WindSpeed and WindDirection (Exterior.vspec)

```vspec
WindSpeed:
  datatype: float
  type: sensor
  unit: m/s
  min: 0
  description: Wind speed outside the vehicle.
  comment: >
    Measured or estimated wind speed in meters per second.
    May be derived from anemometer sensors, aerodynamic load estimation,
    or external weather service input.
    Related to SENSORIS v1.6 WindCondition.speed_and_accuracy.

WindDirection:
  datatype: float
  type: sensor
  unit: degrees
  min: 0
  max: 360
  description: Wind direction in degrees (meteorological convention, 0 = North, 90 = East).
  comment: >
    Wind direction from which wind is blowing, using meteorological convention
    (0° = from North, 90° = from East, 180° = from South, 270° = from West).
    Only meaningful when WindSpeed is above a minimum threshold; value when
    WindSpeed is near 0 is implementation specific.
    Related to SENSORIS v1.6 WindCondition.direction_and_accuracy.
```

---

### 5.7 RoadSurfaceContaminant (Exterior.vspec)

```vspec
RoadSurfaceContaminant:
  datatype: string
  type: sensor
  allowed: [
    'UNKNOWN',
    'NONE',
    'MUD',
    'CHIPPINGS',
    'OIL',
    'FUEL'
  ]
  description: Detected non-weather surface contaminant on the road beneath or ahead of the vehicle.
  comment: >
    Reports road surface contaminants that are distinct from weather-related
    surface state (covered by Vehicle.Exterior.RoadSurfaceCondition) and
    road obstruction objects (tree, rockfall, etc.).
    NONE indicates no surface contaminant detected.
    UNKNOWN shall be used when the system cannot assess surface contamination.
    OIL and FUEL indicate liquid hydrocarbon contamination (slip hazard and
    fire risk). CHIPPINGS indicates loose aggregate (tire damage risk,
    reduced road holding).
    Determination method is implementation specific.
    Compliant with SENSORIS v1.6 RoadSurfaceCondition.TypeAndConfidence
    and TPEG-TEC road surface condition taxonomy.
    Related to VSS issue #877 (Connected Safety signals).
```

---

### 5.8 RoadObstruction (Exterior.vspec, or new Vehicle.Road branch)

**Note:** Placement needs discussion. This could go under `Vehicle.Exterior` as a detected-ahead signal, or under a future `Vehicle.Road` branch. Proposed here as `Vehicle.Exterior.RoadObstruction` pending architectural decision.

```vspec
RoadObstruction:
  datatype: string
  type: sensor
  allowed: [
    'UNKNOWN',
    'NONE',
    'TREE',
    'AVALANCHE',
    'ROCKFALLS',
    'SHED_LOAD',
    'LAND_SLIP',
    'ANIMAL',
    'ANIMAL_LARGE',
    'ANIMAL_HERD',
    'FLOODING'
  ]
  description: Type of road obstruction detected ahead of the vehicle.
  comment: >
    Reports the category of road obstruction detected by the vehicle's
    perception systems. NONE indicates no obstruction detected.
    UNKNOWN shall be used when obstruction type cannot be classified.
    ANIMAL covers small animals (cat, dog); ANIMAL_LARGE covers large animals
    (deer, horse, livestock); ANIMAL_HERD covers groups of animals on road.
    FLOODING indicates standing water sufficient to obstruct passage (distinct
    from WET surface state in Vehicle.Exterior.RoadSurfaceCondition).
    SHED_LOAD covers cargo fallen from another vehicle.
    Determination method is implementation specific (camera, radar, lidar).
    Compliant with SENSORIS v1.6 RoadObstructionCondition.TypeAndConfidence
    and TPEG-TEC road obstruction taxonomy.
    Primary consumers: navigation systems (dynamic re-routing), ADAS safety
    systems, and emergency dispatch systems.
    Related to VSS issue #877 (Connected Safety signals).
```

---

### 5.9 Road Geometry signals (proposed Vehicle.Road.* — new branch)

**Note:** These require a new `Vehicle.Road` branch discussion. The Road.vspec scratch file in the commercial-vehicles repo provides the conceptual basis. These are distinct from vehicle attitude signals (`Vehicle.Orientation.Pitch`, `Vehicle.AngularVelocity`) — they describe road geometry, not vehicle state.

```vspec
# Proposed: Vehicle.Road.Geometry (new branch)
# Maps to: SENSORIS InclinationAndCurvature and Road.vspec scratch

Road.Geometry.LongitudinalSlope:
  datatype: float
  type: sensor
  unit: degrees
  description: Longitudinal slope (inclination) of the road beneath the vehicle.
  comment: >
    Longitudinal declination (slope) of the road surface in degrees.
    Positive values indicate uphill grade; negative values indicate downhill.
    Distinct from Vehicle.Orientation.Pitch, which reports vehicle body
    attitude and may differ from road geometry when the vehicle is not
    all wheels on-road or when vehicle suspension is active.
    Related to SENSORIS v1.6 InclinationAndCurvature.longitudinal_inclination.
    Related to Road.vspec scratch (commercial-vehicles repo).

Road.Geometry.LateralSlope:
  datatype: float
  type: sensor
  unit: degrees
  description: Lateral slope (cross-fall) of the road beneath the vehicle.
  comment: >
    Lateral declination of the road surface in degrees. Also referred to as
    cross-fall. Positive values indicate right-side-lower slope; negative
    indicates left-side-lower.
    Distinct from Vehicle.Orientation.Roll.
    Related to SENSORIS v1.6 InclinationAndCurvature.lateral_inclination.
    Related to Road.vspec scratch (commercial-vehicles repo).

Road.Geometry.HorizontalCurvature:
  datatype: float
  type: sensor
  unit: 1/km
  description: Horizontal curvature of the road. Positive = curve right; negative = curve left; 0 = straight.
  comment: >
    Reciprocal of the horizontal curve radius (curvature = 1/radius).
    High radius (gentle curve) yields low absolute value; tight curve yields
    high absolute value. Negative values represent curves to the left;
    positive values represent curves to the right.
    Related to SENSORIS v1.6 InclinationAndCurvature.horizontal_curvature.
    Related to Road.vspec scratch (commercial-vehicles repo).
```

---

### 5.10 Road Surface Material (proposed Vehicle.Road.* or Exterior)

```vspec
# Proposed: Vehicle.Exterior.RoadSurfaceMaterial
# Maps to: SENSORIS SurfaceMaterialAndConfidence (road_attribution.proto)

RoadSurfaceMaterial:
  datatype: string
  type: sensor
  allowed: [
    'UNKNOWN',
    'ASPHALT',
    'CONCRETE',
    'COMPOSITE_PAVEMENT',
    'GRAVEL',
    'COBBLESTONE',
    'RECYCLED_PAVEMENT',
    'UNPAVED'
  ]
  description: Detected material type of the road surface beneath or ahead of the vehicle.
  comment: >
    Road surface material classification. UNKNOWN shall be used when the
    surface material cannot be classified. UNPAVED covers off-road,
    dirt road, and similar unimproved surfaces not classified by other values.
    RECYCLED_PAVEMENT covers reclaimed aggregate and recycling-mix surfaces.
    Determination method is implementation specific (camera classification,
    acoustic tire-road noise analysis, vibration-based classification).
    Related to SENSORIS v1.6 SurfaceMaterialAndConfidence
    (road_attribution.proto).
    Related to Road.vspec scratch (commercial-vehicles repo).
```

---

### 5.11 Road Roughness (proposed Vehicle.Road.* or Exterior)

```vspec
# Proposed: Vehicle.Road.Roughness or Vehicle.Exterior.RoadRoughness

RoadRoughness:
  datatype: float
  type: sensor
  unit: mm/km
  min: 0
  description: Road roughness index (IRI) in millimeters per kilometer.
  comment: >
    International Roughness Index (IRI) measurement of road surface quality.
    Lower values indicate smoother pavement; higher values indicate rougher
    or deteriorated pavement. IRI values: <2 mm/km = very smooth (new
    highway); 2–4 = good; 4–8 = fair; >8 = poor/unpaved. Measurement
    method is sensor specific; may be derived from vehicle body accelerometers
    with GPS position correlation.
    Related to SENSORIS v1.6 SurfaceAttribution.road_roughness_and_accuracy.
```

---

## 6. PR Strategy

Based on architectural precedent in VSS (merging connected safety signals in small, focused PRs), the following PR grouping is recommended:

### PR Group A — Vehicle.Exterior weather sensing (self-contained, no new branch)
Targets: `spec/Vehicle/Exterior.vspec`
Signals: `VisibilityCondition`, `VisibilityDistance`, `PrecipitationType`, `PrecipitationIntensity`, `AirPressure`
- Extends established `Exterior` branch
- Directly addresses SENSORIS coverage gaps for navigation and ADAS use cases
- `VisibilityCondition` pairs naturally with `Vehicle.Safety.Whiteout` (PR #906) as the underlying observed signal vs. the derived safety assessment

### PR Group B — Vehicle.Exterior wind signals
Targets: `spec/Vehicle/Exterior.vspec`
Signals: `WindSpeed`, `WindDirection`
- Low controversy, clear SENSORIS precedent
- Useful for cross-wind alerts (commercial vehicles especially relevant)
- Can be combined with Group A or submitted separately

### PR Group C — Road surface contaminant and obstruction
Targets: `spec/Vehicle/Exterior.vspec` (pending architectural discussion)
Signals: `RoadSurfaceContaminant`, `RoadObstruction`
- Extends `RoadSurfaceCondition` (merged PR #892) without overlap
- `RoadObstruction` placement requires discussion (Exterior vs. a new Road branch)
- Should reference and coordinate with PR #906 reviewers (@vje013, @erikbosch)

### PR Group D — Road geometry and material (new Vehicle.Road branch)
Requires: New branch proposal for `Vehicle.Road` (or `Vehicle.Exterior.Road`)
Signals: `Road.Geometry.*`, `RoadSurfaceMaterial`, `RoadRoughness`
- Most architecturally significant; needs separate discussion in VSS issue #877 or new issue
- Road.vspec scratch file (commercial-vehicles repo) provides additional community context
- SENSORIS road_attribution.proto provides full precedent

---

## 7. Open Questions for VSS Community

1. **`Vehicle.Exterior` vs. `Vehicle.Road` branch**: Should road-characterization signals (material, geometry, roughness) live under `Vehicle.Exterior` as perceived-environment signals, or should a new `Vehicle.Road` branch be created? The `Road.vspec` scratch in the commercial-vehicles repo suggests appetite for the latter.

2. **`RoadObstruction` vs. Object Detection branch**: SENSORIS `RoadObstructionCondition` lives in `traffic_events.proto`; a VSS Object Detection branch may be more appropriate than `Exterior` for this signal.

3. **Confidence values**: SENSORIS encodes confidence as a separate field alongside each measurement (e.g., `type_and_confidence.confidence`). VSS has no standard pattern for confidence-tagged values. PR #906's comment patterns reference input signals instead. Should VSS introduce a confidence or quality attribute pattern?

4. **PR #906 coordination**: `Vehicle.Exterior.VisibilityCondition` (this doc, Group A) is the observational upstream signal for `Vehicle.Safety.Whiteout` (PR #906). Both PRs should reference each other. PR #906's comment already lists `Vehicle.Body.Raindetection.Intensity` as an input — `VisibilityCondition` would be a cleaner high-level input to reference.

5. **Unit for `mm/h` precipitation**: VSS `units.yaml` should be checked to confirm `mm/h` (millimeters per hour) is a registered unit; if not, it needs to be added alongside the signal.

---

*This document is a working analysis intended to support COVESA VSS contribution discussions. Draft vspec definitions should be reviewed by VSS maintainers before submission.*
