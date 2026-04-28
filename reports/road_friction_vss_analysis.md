# Road Friction Estimation with COVESA VSS

*Generated: 2026-04-28*

## The Core Physics

Tire-road friction is characterized by the **friction coefficient μ** (mu):

```
F_friction = μ × N
```

Where `N` is the normal (vertical) force on the tire and `F_friction` is the maximum tangential force at the contact patch. In practice, there are two components:

- **μ_x** — longitudinal (acceleration/braking direction)
- **μ_y** — lateral (cornering direction)
- **μ_combined** — from friction circle/ellipse: `μ = √(μ_x² + μ_y²)` ≤ μ_peak

The **Pacejka Magic Formula** describes how μ varies with **slip ratio** λ:

```
λ = (ω_wheel × r_eff - v_vehicle) / v_vehicle   [driving]
λ = (v_vehicle - ω_wheel × r_eff) / v_vehicle   [braking]
```

μ rises steeply with slip up to ~15-20% slip (peak grip), then falls — that falling region is where ABS/TCS operate.

---

## VSS Signals — Complete Signal Map

### 1. Direct Road Friction Output (ESC calculates this internally)

| VSS Path | Unit | Notes |
|----------|------|-------|
| `Vehicle.ADAS.ESC.RoadFriction.MostProbable` | % (0=no grip, 100=max) | ESC system's own μ estimate |
| `Vehicle.ADAS.ESC.RoadFriction.LowerBound` | % | 5th percentile confidence bound |
| `Vehicle.ADAS.ESC.RoadFriction.UpperBound` | % | 95th percentile confidence bound |

This is the **most directly useful signal** if available — modern ESC ECUs (Bosch iBooster, Continental MK C2) compute μ internally from yaw deviation + wheel slip. Not all OEMs expose it on CAN.

### 2. Safety System Engagement (Primary Slip Indicators)

| VSS Path | Type | Interpretation |
|----------|------|---------------|
| `Vehicle.ADAS.ABS.IsEngaged` | boolean | Wheel(s) approaching lock — λ > threshold during braking |
| `Vehicle.ADAS.TCS.IsEngaged` | boolean | Driven wheel spinning — excess slip during acceleration |
| `Vehicle.ADAS.ESC.IsEngaged` | boolean | Yaw rate diverging from steering command — lateral slip |
| `Vehicle.ADAS.EBD.IsEngaged` | boolean | Brake force redistribution active — asymmetric slip |
| `Vehicle.ADAS.EBA.IsEngaged` | boolean | Emergency braking assist — very high deceleration demand |

**OEM engagement thresholds (typical):**
- **ABS**: wheel deceleration > ~10 m/s² OR slip ratio λ > 0.15–0.20
- **TCS**: driven wheel speed > reference × 1.10–1.15 (>10–15% slip)
- **ESC**: |yaw_rate_actual - yaw_rate_desired| > ~2–5°/s sustained

### 3. Wheel Speed — Foundation of Slip Ratio Calculation

| VSS Path | Unit | Notes |
|----------|------|-------|
| `Vehicle.Chassis.Axle.Row1.Wheel.Left.Speed` | km/h | Linear wheel speed |
| `Vehicle.Chassis.Axle.Row1.Wheel.Right.Speed` | km/h | Linear wheel speed |
| `Vehicle.Chassis.Axle.Row2.Wheel.Left.Speed` | km/h | Linear wheel speed |
| `Vehicle.Chassis.Axle.Row2.Wheel.Right.Speed` | km/h | Linear wheel speed |
| `Vehicle.Chassis.Axle.*.Wheel.*.AngularSpeed` | deg/s | Rotational speed |
| `Vehicle.Speed` | km/h | Vehicle reference speed |

**Slip ratio calculation from VSS signals:**

```python
# Per-wheel longitudinal slip (braking example)
v_vehicle = Vehicle.Speed / 3.6  # convert to m/s
omega_wheel = Vehicle.Chassis.Axle.Row1.Wheel.Left.AngularSpeed  # rad/s (convert from deg/s)
r_eff = Vehicle.Chassis.Axle.TireDiameter * 0.0127  # inches to meters, /2 for radius

v_wheel = omega_wheel * r_eff
slip_ratio = (v_vehicle - v_wheel) / max(v_vehicle, 0.001)  # avoid div/0
```

### 4. Torque / Force Signals (Computing μ from dynamics)

| VSS Path | Unit | Notes |
|----------|------|-------|
| `Vehicle.MotionManagement.Brake.Axle.Wheel.Torque` | Nm | Estimated friction brake torque per wheel |
| `Vehicle.MotionManagement.Brake.VehicleForceMaximum` | N | Max longitudinal brake force |
| `Vehicle.Powertrain.CombustionEngine.Torque` | Nm | ICE output (for driving μ_x) |
| `Vehicle.Powertrain.ElectricMotor.Torque` | Nm | EV motor output |
| `Vehicle.MotionManagement.ElectricAxle.Torque` | Nm | eAxle torque |

**Longitudinal μ estimation from brake torque:**

```python
# Force at contact patch = Torque / effective_radius
F_x = Vehicle.MotionManagement.Brake.Axle.Wheel.Torque / r_eff  # N

# Normal force (simplified equal distribution)
N_per_wheel = (Vehicle.CurrentOverallWeight * 9.81) / 4  # N

mu_x = abs(F_x) / N_per_wheel
```

This is an approximation — real implementations use load transfer models.

### 5. Accelerometer Signals (Independent μ Estimate)

| VSS Path | Unit | Notes |
|----------|------|-------|
| `Vehicle.Acceleration.Longitudinal` | m/s² | Braking/acceleration force |
| `Vehicle.Acceleration.Lateral` | m/s² | Cornering force |
| `Vehicle.Acceleration.Vertical` | m/s² | Road roughness, load variation |
| `Vehicle.AngularVelocity.Yaw` | deg/s | Actual vs. expected yaw (ESC input) |
| `Vehicle.AngularVelocity.Roll` | deg/s | Load transfer indicator |
| `Vehicle.AngularVelocity.Pitch` | deg/s | Nose-dive/squat indicator |

**μ from accelerometer (fastest / most robust method):**

```python
# Combined acceleration = total friction demand on tires
g = 9.81
a_long = Vehicle.Acceleration.Longitudinal  # m/s²
a_lat  = Vehicle.Acceleration.Lateral       # m/s²

a_combined = sqrt(a_long**2 + a_lat**2)

# This IS the minimum μ the road is currently supplying
mu_current_minimum = a_combined / g

# Peak μ requires knowing slip ratio at same moment
# If ABS.IsEngaged == True: mu_current ≈ mu_peak (operating near limit)
```

The **key insight**: `a_combined / g` gives you a **guaranteed lower bound on μ** — if the car is accelerating laterally at 0.5g without sliding, μ is at least 0.5.

### 6. Tire Condition Signals

| VSS Path | Unit | Notes |
|----------|------|-------|
| `Vehicle.Chassis.Axle.*.Wheel.*.Tire.Pressure` | kPa | Low pressure → larger contact patch but less responsive |
| `Vehicle.Chassis.Axle.*.Wheel.*.Tire.RubberTemperature` | °C | Cold rubber < 40°C → significantly reduced grip |
| `Vehicle.Chassis.Axle.*.Wheel.*.Tire.AirTemperature` | °C | Internal air temp proxy for rubber temp |
| `Vehicle.Chassis.Axle.*.Wheel.*.Brake.PadWear` | % | Brake effectiveness proxy |

**New proposed signals (not yet in VSS 7.0):**

| Proposed VSS Path | Unit | Rationale |
|-------------------|------|-----------|
| `Vehicle.Chassis.Axle.*.Wheel.*.Tire.VibrationLevel` | dB or m/s² | Microphone/accelerometer on inner liner |
| `Vehicle.Chassis.Axle.*.Wheel.*.Tire.VibrationSpectrum` | array | FFT bands, 20–2500 Hz for road classification |
| `Vehicle.Chassis.Axle.*.Wheel.*.Tire.TreadDepth` | mm | Wear state → baseline μ degradation |

Research shows that on **snow/ice**, vibration energy concentrates in **20–600 Hz**; on **dry asphalt**, energy dominates at **600–2500 Hz**. This is discriminable with CNN on the raw signal.

### 7. Environmental / Road State Signals

| VSS Path | Unit | Notes |
|----------|------|-------|
| `Vehicle.Exterior.AirTemperature` | °C | Below 3°C → ice risk window |
| `Vehicle.Exterior.Humidity` | % | Combined with temp → frost prediction |
| `Vehicle.Body.Windshield.Wiping.System.IsWiping` | bool | Proxy for rain → wet road |
| `Vehicle.Body.Windshield.Wiping.System.Frequency` | cpm | Wiper speed → rain intensity proxy |

### 8. Suspension Load (for Normal Force Estimation)

| VSS Path | Unit | Notes |
|----------|------|-------|
| `Vehicle.CurrentOverallWeight` | kg | Total mass (needed for N) |
| `Vehicle.MotionManagement.Suspension.Axle.Wheel.DampingForce` | N | Per-corner vertical force |
| `Vehicle.MotionManagement.Suspension.RollTorque` | Nm | Load transfer during cornering |
| `Vehicle.MotionManagement.Steering.SteeringWheel.Angle` | deg | Understeer/oversteer detection |

---

## Baseline vs. Degraded μ

**Typical peak μ values:**

| Condition | μ_peak | Key Signal Indicators |
|-----------|--------|----------------------|
| Dry asphalt, new tires | 0.8–1.0 | Baseline reference |
| Dry asphalt, worn tires | 0.6–0.8 | `BrakePadWear > 70%`, `TireTreadDepth < 3mm` |
| Wet road | 0.5–0.7 | `IsWiping == true`, `Humidity > 80%` |
| Aquaplaning risk | 0.1–0.3 | `IsWiping + Speed > 80 km/h + Pressure low` |
| Compacted snow | 0.2–0.4 | `AirTemp < 0°C + VibrationSpectrum[20-600Hz] elevated` |
| Black ice | 0.05–0.15 | `AirTemp 0–3°C + Humidity near 100% + ABS.IsEngaged at low slip` |

**Baseline μ degradation model:**

```python
def estimate_mu_baseline(signals):
    mu_base = 0.9  # dry asphalt, new tires

    # Tire temperature effect (cold rubber reduces grip)
    T_rubber = signals['tire_rubber_temperature']  # °C
    if T_rubber < 40:
        mu_base *= 0.7 + 0.3 * (T_rubber / 40)

    # Tire pressure effect (under-inflated changes contact mechanics)
    P_kpa = signals['tire_pressure']
    P_nominal = 220  # kPa typical
    if P_kpa < P_nominal * 0.85:
        mu_base *= 0.90  # moderate reduction

    # Tread wear (if available)
    tread_mm = signals.get('tread_depth', 6.5)  # legal min 1.6mm
    if tread_mm < 3.0:
        mu_base *= 0.75 + 0.25 * (tread_mm / 6.5)

    # Environmental degradation
    T_ambient = signals['air_temperature']
    if T_ambient < 0:
        mu_base *= 0.25  # likely ice/snow regime
    elif T_ambient < 3 and signals['humidity'] > 90:
        mu_base *= 0.35  # black ice risk

    if signals['is_wiping']:
        wiper_speed = signals['wiper_frequency']
        wet_factor = 0.55 + 0.15 * (1 - wiper_speed / 60)  # faster wiper = wetter
        mu_base *= wet_factor

    return mu_base
```

---

## All Friction Indicators (Ranked by Reliability)

| Priority | Signal / Derived Metric | What it Tells You |
|----------|------------------------|-------------------|
| 1 | `ESC.RoadFriction.MostProbable` | Direct OEM μ estimate (most accurate when available) |
| 2 | `Acceleration.Lateral / g` | Guaranteed lower bound on current μ |
| 3 | `Acceleration.Longitudinal / g` | Longitudinal μ demand currently being met |
| 4 | `ABS.IsEngaged` | Operating at or near μ_peak limit (braking) |
| 5 | `TCS.IsEngaged` | Driven wheel exceeded μ limit (accelerating) |
| 6 | `ESC.IsEngaged` | Lateral μ exceeded — yaw instability |
| 7 | Wheel slip ratio λ (computed) | Position on μ-slip curve |
| 8 | `Brake.Axle.Wheel.Torque / (r × N)` | Estimated instantaneous μ_x |
| 9 | `Tire.RubberTemperature` | Grip state of rubber compound |
| 10 | `AirTemperature < 3°C` | Ice/snow regime entry condition |
| 11 | `Windshield.IsWiping` | Wet road proxy |
| 12 | Tire vibration spectrum (new) | Road surface texture classification |
| 13 | `AngularVelocity.Yaw` vs. steering angle | Understeer/oversteer detection |
| 14 | `Tire.Pressure` | Contact patch geometry |

---

## Proposed New VSS Signals

These would close the gaps identified above and are technically feasible with current sensor hardware:

```yaml
# Proposed additions to Vehicle.Chassis.Axle.*.Wheel.*.Tire.*
Tire.TreadDepth:
  datatype: float
  unit: mm
  description: Estimated remaining tread depth

Tire.VibrationAcceleration:
  datatype: float
  unit: m/s^2
  description: RMS vibration magnitude from inner-liner accelerometer

Tire.VibrationSpectrum:
  datatype: float[]
  unit: dB
  description: Frequency-band vibration energy (e.g. 20-600Hz, 600-2500Hz bands)
  comment: Enables road surface classification (dry/wet/snow/ice)

Tire.SlipRatio:
  datatype: float
  unit: percent
  description: Longitudinal tire slip ratio, derived from wheel vs vehicle speed

# Proposed addition to Vehicle.ADAS.ESC.*
ESC.RoadFriction.SurfaceClass:
  datatype: string
  enum: [Dry, Wet, SlushySnow, PackedSnow, Ice, Unknown]
  description: Classified road surface type from ESC friction estimator
```

---

## Research Resources

### Foundational / Review

- [Road Friction Virtual Sensing: A Review of Estimation Techniques with Emphasis on Low Excitation Approaches](https://www.mdpi.com/2076-3417/7/12/1230) — MDPI 2017, best overview of the whole problem space
- [Estimation of Tire-Road Friction for Road Vehicles](https://arxiv.org/pdf/1908.00452) — arXiv survey, Kalman/EKF approaches

### Dynamics-Based Estimation

- [Tire-road friction estimation and traction control strategy for motorized electric vehicle](https://pmc.ncbi.nlm.nih.gov/articles/PMC5491023/) — PLOS ONE / PMC, EV-specific, open access
- [Estimation of Road Friction Coefficient in Different Road Conditions Based on Vehicle Braking Dynamics](https://link.springer.com/article/10.1007/s10033-017-0143-z) — Springer, braking-specific
- [Estimation of tire–road friction coefficient and its application in chassis control systems](https://www.tandfonline.com/doi/full/10.1080/21642583.2014.985804) — Taylor & Francis, ESC integration

### Intelligent Tire / Sensor Fusion

- [A novel estimation method for tire-road friction coefficient using intelligent tire and tire dynamics](https://www.sciencedirect.com/science/article/abs/pii/S0888327025005734) — ScienceDirect 2025, accelerometer + NN
- [Tire Force Estimation in Intelligent Tires Using Machine Learning](https://arxiv.org/pdf/2010.06299) — arXiv, ML on accelerometer data
- [Tire-road friction coefficient estimation method design using PVDF piezoelectric film sensors](https://www.sciencedirect.com/science/article/abs/pii/S0924424722006422) — ScienceDirect, piezo sensors

### Acoustic / Vibration Classification

- [Classification of Road Surfaces Based on CNN Architecture and Tire Acoustical Signals](https://www.mdpi.com/2076-3442/12/19/9521) — MDPI, CNN on tire sound
- [Intelligent Tire Sensor-Based Real-Time Road Surface Classification Using ANN](https://pmc.ncbi.nlm.nih.gov/articles/PMC8125707/) — PMC, real-time road type → μ
- [Identification of Road-Surface Type Using Deep Neural Networks for Friction Coefficient Estimation](https://pmc.ncbi.nlm.nih.gov/articles/PMC7037890/) — PMC, DNN road type classifier

### Environmental & Weather

- [Study on the Influence of Environmental Conditions on Road Friction Characteristics](https://www.mdpi.com/2075-4442/11/7/277) — Temperature, humidity, rain effects on μ
- [A Fusion Estimation Method for Tire-Road Friction Coefficient Based on Weather and Road Images](https://www.mdpi.com/2075-4442/13/10/459) — Fusion of camera + weather signals

### ABS / TCS Algorithms

- [An ABS algorithm using real-time wheel reference slip estimation](https://journals.sagepub.com/doi/abs/10.1177/09544070211024083) — Sage Journals, reference slip tracking
- [Clemson CVEL: Traction Control System](https://cecas.clemson.edu/cvel/auto/AuE835_Projects_2011/Tiwari_project.html) — Reference on threshold detection architecture
