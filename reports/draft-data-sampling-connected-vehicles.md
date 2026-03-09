# Sampling With Purpose: Why Connected Vehicle Data Must Serve the Needs of Those Who Use It

The connected vehicle generates thousands of data points per second. GPS coordinates, engine speed, battery voltage, acceleration, tire pressure, fuel levels, fault codes — the list runs to thousands of signals on a modern platform. Yet raw data volume is not useful data. Without sampling strategies shaped by specific use cases, vehicle telemetry either lacks the resolution to support the analysis a data consumer requires, or overwhelms them with noise that obscures it.

The question facing the industry is not "how much data can we collect?" It is: what data do insurers, fleet operators, maintenance providers, emergency responders, and regulators actually need — at what fidelity — to accomplish the analyses their roles demand? Get the sampling wrong, and the data cannot serve its purpose. The analyses simply cannot be done.

## The Problem: One Size Fits None

Consider a single vehicle traveling a delivery route. Its onboard systems can report any number of signals at any moment. But the consumers of that data need fundamentally different things:

- An insurer scoring driving behavior needs granular acceleration and braking events. Engine coolant temperature every five minutes is irrelevant.
- A fleet operator optimizing routes needs accurate GPS tracks and fuel consumption trends. Airbag deployment status adds nothing until an incident occurs.
- A maintenance provider predicting starter motor failure needs cranking voltage captured at high frequency during ignition — but only for several seconds the engine is cranking.
- An emergency responder needs crash detection within seconds — airbag deployment, impact severity, number of occupants, whether seatbelts were worn and precise location. Odometer readings and oil life percentages are useless in that moment.
- A regulator monitoring emissions compliance needs periodic fuel consumption and aftertreatment system data, at intervals measured in minutes, not milliseconds.

Sample every signal at the same fixed rate and transmit everything to everyone, and the result satisfies no one. High-frequency data where it is not needed wastes bandwidth and storage. Low-frequency data where high fidelity is required leaves gaps that make the analysis impossible.

## The Foundation: Curve Logging and the Ramer-Douglas-Peucker Algorithm

One solution that has proven itself draws from an insight in computational geometry. The Ramer-Douglas-Peucker (RDP) algorithm, first published in the 1970s for cartographic generalization, addresses a deceptively simple problem: given a curve composed of many points, represent it with fewer points while preserving its essential shape.

### How It Works

RDP takes an ordered set of points and a tolerance parameter, epsilon (ε):

1. Draw a straight line between the first and last point of the segment.
2. Find the intermediate point farthest from this line.
3. If that maximum distance exceeds ε, the point is significant — keep it, and recursively apply the same process to the sub-segments on either side.
4. If the maximum distance falls within ε, all intermediate points can be discarded. The simplified curve will not deviate from the original by more than ε.

The result: a curve that retains points where meaningful change occurs — sharp turns, sudden accelerations, significant deviations — and discards those that fall along predictable, interpolatable paths.

### From Cartography to Vehicles

The same principle that simplifies coastlines on a map compresses vehicle telemetry. A vehicle traveling at steady speed on a straight highway produces data points that, plotted over time, form a nearly straight line. Recording every one-second sample adds volume without adding information. But the moment the driver brakes hard, turns sharply, or accelerates, the signal deviates — and those are precisely the points that matter.

Geotab developed its curve logging algorithm as an adaptation of RDP for time-series vehicle data. Rather than perpendicular distance (which introduces scaling issues between time and signal magnitude), the implementation uses vertical distance — the deviation of the actual signal value from the interpolated value at that timestamp. This makes the epsilon parameter directly interpretable in the units of the signal being measured: 3.8 km/h for speed, 0.894 V for battery voltage, 4°C for coolant temperature.

Geotab open-sourced the algorithm — first in Python for prototyping, then in Rust for production and embedded systems — under the Mozilla Public License (MPL) at [github.com/Geotab/curve](https://github.com/Geotab/curve). The goal is not to generate revenue from licensing intellectual property. It is to improve the quality and pertinence of connected vehicle data across the industry by making the algorithm freely available for any OEM, telematics provider, or platform developer to implement.

### Independent Validation: The Eclipse SDV Benchmark

The effectiveness of curve logging has been independently validated. In early 2024, engineers at Bosch integrated Geotab's open-source Rust implementation into the Eclipse SDV Fleet Management Blueprint — an open-source reference architecture for vehicle fleet data platforms.

Using real trip data — GPS and vehicle speed recordings captured at approximately 1 Hz during a neighborhood delivery route — the engineering team applied the curve algorithm with the Fleet Management Data Guidelines error threshold of 3.8 km/h for vehicle speed.

The results: approximately 76% data reduction while retaining the critical changes and trend of the data. Before-and-after visualizations confirmed that the compressed curve preserved every significant speed change, every acceleration and deceleration event, while eliminating redundant points recorded during steady-state driving.

This is the key distinction. Curve logging is lossy compression, but the loss is bounded and configurable. The epsilon parameter guarantees that the reconstructed signal never deviates more than the specified threshold from the original. For a speed epsilon of 3.8 km/h, any consumer of the data can reconstruct the vehicle's speed profile with confidence that it is accurate within that margin at every point in time. The algorithm, the error thresholds, and the integration are all open source — available for scrutiny, adoption, and extension by anyone.

## Fleet Management Data: Standards Built on Purpose-Driven Sampling

The curve logging algorithm is a mechanism. The question of *what* to sample, *how often*, and with *what tolerance* is answered by a complementary effort: the COVESA Fleet Management Data (FMD) recommendations.

Developed through the COVESA Commercial and Fleet Vehicle Expert Group, FMD defines approximately 100 vehicle signals organized across five pillars — Productivity, Maintenance, Safety, Compliance, and Sustainability — each with specific sampling frequencies, curve error thresholds, and importance classifications tied to concrete use cases. Every signal entry answers the question: who needs this data, for what purpose, and at what fidelity?

### The Diversity of Sampling

The range of sampling strategies across FMD reveals how different data consumers require fundamentally different approaches:

| Signal | Sampling | Curve Error (ε) | Primary Use Cases |
|---|---|---|---|
| GPS position | 1 Hz (ideal: curve/smart logic) | 1.8 km distance | Fleet tracking, compliance, routing |
| GPS position (safety) | **5 Hz** | 1.8 km distance | Accident reconstruction |
| Road speed | Every 15 seconds | 3.8 km/h | Compliance, speed monitoring |
| Battery voltage | Every 30 seconds | 0.894 V | Predictive maintenance |
| Cranking voltage | **100 Hz burst** (5 seconds) | Tuned tolerance | Starter motor health |
| Engine coolant temp | Every 5 minutes | 4°C | Maintenance, overheating |
| Tire pressure | Every 5 minutes | 16 kPa | Safety, maintenance |
| EV state of charge | On change | 1% | Range management, battery health |
| Fuel level remaining | Every 2 minutes | 3.5% | Fuel management, sustainability |
| Airbag deployment | On change (event) | — | Crash detection, emergency response |
| Ignition status | On change (event) | — | Trip detection, compliance |
| Heartbeat | Every ~24 hours | — | Connectivity monitoring |

From a heartbeat signal sampled once per day to cranking voltage captured at 100 Hz in five-second bursts. From event-driven signals that transmit only when state changes to continuous signals compressed via curve logging. Each strategy exists because a specific data consumer needs that specific fidelity to accomplish a specific analysis. Without it, the analysis cannot be done.

## Industry Verticals: Different Consumers, Different Requirements

### Insurance

Usage-based insurance (UBI) and pay-how-you-drive programs depend on accurate characterization of driving behavior. Insurers need longitudinal acceleration at 1 Hz minimum to detect harsh braking events, lateral acceleration for cornering behavior, speed patterns relative to road context, trip segmentation via ignition events and GPS, and high-fidelity GPS (5 Hz) with acceleration data for crash reconstruction and claims validation.

If acceleration is sampled too infrequently, harsh braking events fall between samples and disappear from the record. The risk score becomes unreliable. Premiums become inaccurate. The entire UBI value proposition collapses — not because the data was unavailable on the vehicle, but because the sampling was not designed for the analysis the insurer needed to perform.

The COVESA Commercial and Fleet Vehicle Expert Group includes insurance participants for precisely this reason. A dedicated set of insurance data signals, aligned with VSS, defines sampling parameters for both basic and advanced (ADAS-equipped) vehicle scoring. The EU Usage-Based Insurance market is projected to reach €15+ billion by 2030. Standardized, properly sampled data is the foundation — current OEM-specific implementations have been described by insurers as cost-prohibitive, requiring multi-year integrations that standardized conventions could collapse to a single effort.

### Fleet Operations

Fleet operators — last-mile delivery, long-haul logistics, service vehicles — need data that drives operational decisions. Real-time GPS tracking with curve-logged compression balances position accuracy against data costs across thousands of vehicles. Fuel consumption trends identify inefficient driving. Engine hours and odometer enable service interval planning. Idle time feeds sustainability reporting. ELD compliance requires speed, GPS, ignition, odometer, and engine hours at prescribed intervals.

The scale problem is real. Testing 25 Hz sampling on 5,000 vehicles from a 100,000-unit fleet doubled total records to 200 million. Curve logging achieves comparable or better analytical fidelity with a fraction of the data volume, making fleet-scale analytics economically viable. An EU-funded project demonstrating heavy-duty battery electric vehicles across European logistics corridors has proposed using the COVESA FMD standard for its data collection framework — recognizing that standardized, purpose-driven sampling is essential for multi-fleet, cross-border operations.

### Predictive Maintenance

Predictive maintenance requires data that captures the leading indicators of component degradation — and those indicators are signal-specific:

- **Cranking voltage at 100 Hz**: The sawtooth voltage pattern during engine start reveals starter motor and battery health. Standard curve logging with default parameters smooths out these critical oscillations. A tuned variant with lower tolerance preserves the diagnostic features while still reducing data volume by over 70%.
- **Battery voltage** at 30-second intervals with 0.894 V epsilon: Gradual voltage decline over weeks indicates battery aging.
- **Engine coolant and oil temperature** at 5-minute intervals: Thermal anomalies precede mechanical failures.
- **Diagnostic trouble codes (DTCs)** on event: The specific fault information needed for proactive intervention.
- **Tire pressure** at 5-minute intervals with 16 kPa epsilon: Slow leaks detected days before roadside failure.

COVESA members working in fleet maintenance are actively mapping J-1939 heavy-duty fault codes to VSS and developing predictive maintenance models that depend on these specific sampling parameters. Without the right data fidelity, a predictive model cannot distinguish normal wear from abnormal degradation. The "predictive" in predictive maintenance becomes aspiration rather than capability.

### Road Safety and Emergency Responders

Road safety and emergency response are the most time-critical data use cases. Crash detection requires event-driven airbag deployment signals transmitted within seconds. Accident reconstruction demands 5 Hz GPS and sub-second acceleration data — at standard 1 Hz sampling, a vehicle traveling 100 km/h moves 28 meters between samples, far too coarse to reconstruct the dynamics of a collision.

First responder dispatch needs real-time location, impact severity, and vehicle identification. Systems integrated into 9-1-1 platforms can relay crash data including video to dispatchers within seconds of airbag deployment — but only if the vehicle's data architecture captures and transmits the right signals at the right frequency.

COVESA's Connected Safety group is working to normalize airbag deployment signals across all vehicle makes and models so that 9-1-1 Real Time Intelligence Centers receive standardized crash data regardless of manufacturer. NHTSA has been working to align VSS data points for emergency reporting. Without standardized sampling conventions, the promise of connected vehicle safety remains fragmented across proprietary implementations that cannot interoperate at the moment they are needed most.

Dangerous intersection identification operates at a different timescale but with the same dependency on sampling. Hard-braking events correlated with GPS position reveal hazardous intersections before fatalities force the analysis. Lateral acceleration at specific locations indicates road design problems. Road surface quality can be inferred from vertical acceleration patterns. These analyses require that individual vehicles collect acceleration and GPS at sufficient fidelity to capture discrete events — even though the road authority's analysis operates on aggregated data across thousands of vehicles over months or years.

### Vehicle Theft Recovery

Theft recovery inverts the typical data volume concern. Here, more data is better: high-frequency GPS to track a stolen vehicle in real time, ignition and motion events to detect unauthorized use, VIN and device identity for verification.

CAN injection — where thieves exploit the vehicle's own controller area network to bypass keyless entry — has become a significant threat, with over 745,000 vehicles stolen in the first three quarters of 2022 alone, a 24% increase over 2019. Connected vehicle data that includes ignition events, location tracking, and cybersecurity anomaly detection provides a layer of defense that mechanical measures alone cannot. COVESA's Commercial Vehicle group is modeling vehicle theft reporting as a VSS data collection use case, defining the signals and sampling conventions needed for both real-time recovery and forensic analysis.

## Regulator Interests: Standardized Data for Public Mandates

Regulators need standardized, auditable data across entire vehicle populations — often aggregated and anonymized, but collected with sufficient fidelity at the source to support their mandates.

### Road Safety: Intersections and Roadway Upkeep

Transportation authorities need aggregated fleet data to identify hazardous locations. Hard-braking events correlated with GPS position reveal dangerous intersections. Lateral acceleration events at specific locations indicate road design problems or obstacle hazards. Road surface quality can be inferred from vertical acceleration patterns — potholes, uneven pavement, and deteriorating conditions produce characteristic signatures in properly sampled accelerometer data.

The sampling requirements flow from the analysis: capture acceleration and GPS at sufficient fidelity to record discrete events in individual vehicles, then aggregate across the fleet to identify systemic patterns. The data exists on the vehicles. The question is whether it is sampled in a way that preserves the events of interest.

### Vehicle Safety Inspection

Traditional annual inspections represent a point-in-time snapshot. A vehicle can pass and immediately deteriorate. Connected vehicle data enables a different model: continuous compliance monitoring. Tire pressure, brake system status, lighting functionality, emissions system health — these can all be monitored via the signals already defined in FMD.

The implication is significant. A vehicle receiving timely repairs based on connected data arrives at inspection already compliant. Or the inspection itself becomes a continuous, data-driven process rather than an annual event. State regulators and COVESA are exploring this model, with verifiable vehicle credentials that include inspection status built on the same VSS data model and sampling conventions.

### EV Battery Health

As the global fleet electrifies, battery health monitoring becomes both an operational necessity and a regulatory requirement:

- State of charge (SOC) sampled on change with 1% epsilon tracks usage patterns
- Charging energy (AC and DC) at 2-minute intervals with 1 kWh epsilon enables efficiency analysis
- Battery temperature at 5-minute intervals with 5°C epsilon detects thermal events that accelerate degradation
- State of health derived from these signals over time reveals degradation curves

The EU Battery Passport mandates dynamic data reporting for EV batteries throughout their lifecycle. The dynamic data points of the Battery Passport can be addressed by collecting data in VSS — the same framework serving fleet operators and insurers also serves the regulatory requirement, provided sampling parameters are correctly defined for each use case.

### Emissions: From Periodic Testing to Continuous Monitoring

Emissions compliance is transitioning from periodic tailpipe testing to continuous monitoring via connected data. Fuel consumption and DEF/AdBlue levels track emissions-relevant consumables. Aftertreatment system status — DPF regeneration, SCR health — indicates whether emissions controls are functioning. Engine diagnostics including the malfunction indicator lamp and emissions-related DTCs provide ongoing compliance evidence.

Fragmentation is a real problem. Different states currently impose different requirements for vehicle class and emissions data. Standardized sampling conventions aligned with FMD and VSS could resolve this — so that emissions reporting follows the same signal definitions and sampling parameters regardless of jurisdiction.

COVESA's collaboration with state regulators has specifically identified verifiable emissions reporting as a future use case for vehicle data credentials, combining VSS-based data collection with verifiable credential technology to create tamper-evident compliance records.

## Sampling Determines Capability

The thread connecting all of these use cases is straightforward: the sampling strategy determines what analysis is possible.

- Sample GPS at 1 Hz with curve logging, and fleet vehicles can be tracked efficiently within ELD compliance requirements. Sample at 5 Hz, and accidents can be reconstructed. Sample at 24-hour intervals, and the only conclusion is that the vehicle is still connected.
- Sample cranking voltage at 100 Hz for 5 seconds, and starter motor failure can be predicted weeks in advance. Sample battery voltage every 30 seconds with standard curve logging, and the maintenance trend is visible but the cranking signature disappears entirely.
- Sample acceleration at 1 Hz, and driving behavior can be scored for insurance. Sample every 15 seconds, and harsh braking events — which last 1-2 seconds — vanish between data points.
- Capture airbag deployment as a change event, and emergency responders receive notification within seconds. Poll airbag status every 5 minutes, and the notification arrives after the golden hour has passed.

Data sampled without regard to its intended use cannot serve its purpose. It is either too sparse to capture the phenomena of interest, or too dense to be economically transmitted, stored, and processed at scale.

Curve logging addresses the density problem elegantly. By guaranteeing that every retained data point represents a meaningful signal change within a defined tolerance, it achieves 76% compression — independently validated — without sacrificing analytical utility. But the epsilon parameter, the sampling frequency, and the trigger conditions must all be set with the data consumer's needs in mind.

This is why the FMD framework matters. It does not prescribe a single sampling regime. It prescribes different regimes for different signals serving different use cases — through an open standard (COVESA VSS) with an open-source compression algorithm (curve logging under MPL), enabling any OEM, telematics provider, or platform developer to implement without proprietary lock-in.

## The Path Forward

The connected vehicle data ecosystem is at an inflection point. The global telematics market is projected to reach USD 149.9 billion by 2028. The EU Data Act mandates open access to vehicle-generated data. OEMs across multiple continents are evaluating standardized fleet data recommendations. Regulators are defining data requirements that align with open, standards-based approaches.

The organizations that will derive the most value from this data are those that recognize a fundamental reality: data sampling is not a technical afterthought. It is a design decision that determines whether the data can serve its intended purpose.

What is needed:

1. **Adoption of open, purpose-driven sampling standards** — defining what signals to collect, at what fidelity, for which use cases. The COVESA Fleet Management Data recommendations provide this framework.

2. **Implementation of intelligent compression** — algorithms like curve logging, open-sourced and independently validated, achieving 76% data reduction while preserving analytical fidelity. The code is available. The error thresholds for fleet management signals are published.

3. **Collaboration between data consumers and data producers** — insurers, fleet operators, maintenance providers, emergency responders, and regulators articulating their specific data needs, and OEMs and telematics providers implementing sampling strategies that serve them.

4. **Regulatory alignment** around standardized data conventions — so that emissions reporting uses the same signal definitions and sampling parameters regardless of jurisdiction, and crash data from any vehicle is equally actionable by any first responder system.

The alternative — proprietary, one-size-fits-all data collection that serves no consumer well — is not merely inefficient. It is an obstacle to the safety, sustainability, and operational intelligence that connected vehicle data promises.

Without sampling designed around the needs of those who use the data, the most important analyses cannot be accomplished.

---

*The curve logging algorithm is available as open source at [github.com/Geotab/curve](https://github.com/Geotab/curve) under the Mozilla Public License. The COVESA Fleet Management Data recommendations and Vehicle Signal Specification are developed collaboratively at [covesa.global](https://www.covesa.global). The Eclipse SDV Fleet Management Blueprint, incorporating the curve logging integration, is available at [github.com/eclipse-sdv-blueprints/fleet-management](https://github.com/eclipse-sdv-blueprints/fleet-management).*
