# Standardized Vehicle Data for Public Safety and the Insurance of Autonomous Vehicles: The Role of Open Standards in Regulatory Alignment

# Status: Draft #
**A COVESA Position Paper**

**March 2026**

**Contributors:** COVESA Commercial and Fleet Vehicles Expert Group, MOTER Project

---

## Executive Summary

The deployment of Automated Driving Systems (ADS) holds the promise of fundamentally improving road safety — reducing the human errors that account for the vast majority of traffic fatalities and serious injuries worldwide. Realizing this promise, however, depends on more than the technology itself. It requires a robust ecosystem of accountability, transparency, and verifiable safety performance built on standardized, interoperable vehicle data.

Public safety demands that the behaviour of autonomous vehicles be observable, measurable, and independently verifiable. Governments need data to enforce safety standards. Emergency responders need data to understand incidents. Researchers need data to identify systemic risks. And independent third parties — particularly the insurance industry — play an essential role in this ecosystem, providing an ongoing, market-driven mechanism for evaluating vehicle safety performance, pricing risk accurately, and ensuring that victims of incidents involving ADS-equipped vehicles receive fair and timely compensation.

The proposed United Nations Global Technical Regulation on Automated Driving Systems (ECE/TRANS/WP.29/GRVA/2026/2) recognizes the need for data recording through its Data Storage System for Automated Driving (DSSAD) requirements. However, the current regulatory text focuses primarily on post-incident investigation and type-approval compliance. It does not fully address the broader public safety ecosystem — the independent third parties such as insurers, fleet safety managers, and road safety researchers — who require ongoing, standardized access to ADS operational data to fulfil their societal functions.

COVESA (Connected Vehicle Systems Alliance) and its member organizations are actively defining the open data standards needed to support this broader ecosystem. Through the Vehicle Signal Specification (VSS) and the MOTER (Mobility, Observation, Telematics, Evaluation and Risk) project, COVESA is building the data vocabulary that can serve regulatory compliance, public safety evaluation, and independent third-party needs — while preserving automotive manufacturers' intellectual property in their ADS implementations.

This paper presents the public safety case for why standardized, open vehicle data definitions are essential for the safe deployment and independent oversight of autonomous vehicles, identifies which data points are already defined within COVESA standards and which require further development, and proposes an approach that balances transparency with IP protection through the use of higher-level abstracted data elements.

---

## 1. Public Safety and the Need for Independent Oversight of Autonomous Vehicles

### 1.1 The Public Safety Imperative

Road traffic injuries remain one of the leading causes of death and disability worldwide. The United Nations has recognized road safety as a critical public health challenge, and the UN General Assembly's Global Plan for the Decade of Action for Road Safety 2021–2030 calls for a reduction in road traffic deaths and injuries of at least 50 per cent by 2030.

Automated Driving Systems have the potential to contribute significantly to this goal by reducing or eliminating the human errors — distraction, impairment, fatigue, poor judgement — that underlie the majority of crashes. However, this potential can only be realized if ADS-equipped vehicles are held to rigorous, transparent, and independently verifiable safety standards throughout their operational life — not merely at the point of type approval.

Public safety requires that autonomous vehicles operate within a framework of continuous accountability. This framework must include:

- **Regulatory oversight** — governments must be able to verify that deployed ADS perform safely and within their approved operational parameters
- **Incident investigation** — when crashes or safety-critical events occur, investigators must be able to reconstruct what happened, who or what was in control, and how the vehicle responded
- **Systemic risk identification** — researchers and safety authorities must be able to identify patterns, failure modes, and emerging risks across the ADS fleet
- **Independent third-party evaluation** — entities outside the manufacturer, such as insurers and fleet safety organizations, must be able to independently assess vehicle safety performance based on objective, standardized data

### 1.2 The Essential Role of Independent Third Parties

Independent third parties — particularly the insurance industry — serve a vital function in the public safety ecosystem that goes beyond their commercial role. Insurers act as a continuous, market-driven mechanism for:

- **Ongoing safety assessment** — unlike type approval, which evaluates a system at a point in time, insurance risk assessment is continuous, responding to real-world performance data across the fleet
- **Financial accountability** — insurance ensures that victims of incidents involving ADS-equipped vehicles are compensated, maintaining public trust in autonomous mobility
- **Safety incentivization** — through risk-based pricing, insurers create direct financial incentives for manufacturers and fleet operators to maintain and improve ADS safety performance
- **Data-driven transparency** — actuarial analysis of ADS operational data produces independent, objective safety assessments that complement manufacturer self-reporting and regulatory audits

For insurers to fulfil this public safety function, they require access to standardized vehicle data that can reliably answer fundamental questions: Was the ADS operating? Did a human take over? Was remote guidance provided? What triggered a transition or emergency manoeuvre? Without this data, the insurance industry cannot accurately price ADS risk, and the market-driven safety incentive mechanism breaks down.

### 1.3 The Regulatory Landscape

The proposed UN GTR on ADS (ECE/TRANS/WP.29/GRVA/2026/2) establishes a comprehensive framework for ADS safety requirements. Its provisions are performance-based and technology-neutral, recognizing that ADS technology is evolving rapidly and that regulations must not restrict future innovation.

Of particular relevance is Annex 6 of the proposed GTR, which defines the Data Storage System for Automated Driving (DSSAD). The DSSAD requirements mandate the recording of time-stamped events including:

- Activation and deactivation of ADS features (by system or user)
- ODD exit events
- Start of ADS fallback to user or to a Minimal Risk Condition
- User input to driving controls while ADS is active
- Prevention of user takeover (with reasons)
- Start and end of emergency manoeuvres
- Detected collisions and failure situations
- Remote intervention in tactical functions

The DSSAD also mandates time-series data recording during triggering events, including detected object distances and velocities, ADS-requested acceleration, braking, and steering demands, vehicle acceleration data, and ADS-determined vehicle speed.

These requirements represent a significant step forward for post-incident investigation and regulatory compliance. However, they do not fully address the needs of the broader public safety ecosystem — the independent third parties who require standardized, ongoing access to ADS operational data. Furthermore, the regulation does not specify the data semantics, taxonomies, or interoperability standards that would enable practical use of this data across stakeholders and jurisdictions.

### 1.4 The Gap Between Regulatory Compliance and Public Safety Ecosystem Needs

A comprehensive public safety framework requires more than a mandated recording obligation. It requires:

1. **Standardized data definitions** — common semantics for what each data element means, how it is measured, and how it should be interpreted, enabling consistent analysis across manufacturers and jurisdictions
2. **Interoperable data formats** — consistent, machine-readable representations that work across vehicle manufacturers, fleet management systems, insurance platforms, and research institutions
3. **Appropriate sampling and reporting logic** — specifications for when and how frequently data should be captured, balancing completeness with data volume management
4. **Layered data access** — the ability for independent third parties to access higher-level operational summaries without requiring access to proprietary, lower-level ADS implementation details

COVESA's work directly addresses each of these needs.

---

## 2. COVESA's Role: Building the Open Data Vocabulary

### 2.1 The Vehicle Signal Specification (VSS)

The COVESA Vehicle Signal Specification is an open, community-developed taxonomy for vehicle data. VSS defines a tree-structured hierarchy of vehicle signals — from basic vehicle attributes to advanced driver assistance systems (ADAS) and increasingly autonomous driving functions. It provides standardized names, data types, units, and descriptions for each signal, enabling interoperability across the automotive ecosystem.

VSS is already referenced and adopted by major automotive platforms, including the Android Automotive Vehicle Hardware Abstraction Layer (VHAL), which maps platform-level vehicle properties to corresponding VSS paths. This alignment between platform-level APIs and open standards creates a practical pathway for data access.

### 2.2 The MOTER Project

COVESA's MOTER (Mobility, Observation, Telematics, Evaluation and Risk) project is a cross-industry initiative that brings together insurers, fleet operators, telematics providers, and automotive manufacturers to define the specific vehicle data points needed for safety assessment, insurance, and fleet management applications. MOTER has developed a comprehensive mapping of safety use cases to required data points, with each data point linked to:

- Its existing or proposed VSS path
- Corresponding VHAL (Android Automotive) property where available
- Equivalent SAE J1939 PGN/SPN codes for heavy-duty vehicles
- Sensoris definitions where applicable
- Recommended sampling rates and data reporting logic
- Priority and importance ratings
- Applicable SAE automation levels

### 2.3 Cross-Industry Collaboration

COVESA's work on ADS-related data standards involves active collaboration across the automotive, insurance, telematics, and fleet management industries. Major insurers participate in COVESA's Commercial and Fleet Vehicles working group, contributing insurance domain expertise to the data standardization process. Discussions are also underway with national insurance industry associations regarding the harmonization of digital proof of insurance — a domain where standardized vehicle identity and status data is fundamental.

The COVESA All Members Meeting (AMM) programme includes dedicated sessions on fleet safety and insurance data topics, bringing together MOTER contributors, automotive OEMs, telematics providers, fleet operators, and insurers to advance standardized vehicle data for public safety and commercial applications.

---

## 3. Essential Data Points for Public Safety and Insurance of Autonomous Vehicles

The MOTER project has identified a comprehensive set of data points essential for public safety evaluation and the insurance of ADS-equipped vehicles. These data points fall into several categories, reflecting the distinct questions that regulators, investigators, insurers, and safety researchers must be able to answer.

### 3.1 ADS Operational Status

The most fundamental question for both public safety and insurance is: **who or what was controlling the vehicle at any given moment?**

| Data Point | Public Safety / Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| ADS activation/deactivation status | Determine whether the ADS was performing the DDT | DSSAD 5.2.1: Activation/Deactivation of the feature |
| ADS operating mode (SAE level) | Establish applicable liability and regulatory framework | Implicit in ADS feature identification |
| ODD boundary status | Determine if ADS was operating within its designed parameters | DSSAD 5.2.1: ODD exit |
| Autonomous driving status | Continuous confirmation that ADS is in control | Referenced in MOTER SAFETY04 use cases |

### 3.2 Transitions of Control

When the ADS ceases to perform the Dynamic Driving Task and a human must assume control, the circumstances and execution of this transition are critical to both incident investigation and liability determination.

| Data Point | Public Safety / Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| Transition demand to driver (with reason) | Understand why the ADS requested human intervention | DSSAD 5.2.1: Start of ADS fallback to user |
| Manual interaction/override by driver, safety driver, or remote operator | Determine who took control, when, and through what means | DSSAD 5.2.1: User input to driving controls |
| Deactivation of ADS function | Track system shutdown events and their initiators | DSSAD 5.2.1: Deactivation by system or user |
| Prevention of user takeover (with reason) | Assess whether the ADS appropriately prevented an unsafe handover | DSSAD 5.2.1: Prevention of user takeover |
| Detection that fallback user is not available | Evaluate driver readiness and engagement | DSSAD 5.2.1: Detection that fallback-user is not available |

### 3.3 Emergency Situations and Safety Responses

How the vehicle responds in critical and emergency situations directly affects public safety outcomes, incident investigation, and claims adjudication.

| Data Point | Public Safety / Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| Start/end of emergency manoeuvre | Bracket the critical event window for reconstruction and analysis | DSSAD 5.2.1: Start/End of Emergency Manoeuvre |
| Application of Minimal Risk Condition (safety stop, turtle mode) | Assess the ADS response to situations exceeding its capabilities | DSSAD 5.2.1: Start of ADS fallback to an MRC / MRC achieved |
| Emergency braking event | Determine if and when automatic emergency braking was applied | DSSAD 5.3.2: ADS-requested service braking demand |
| Detected collision | Confirm whether a collision occurred and trigger data preservation | DSSAD 5.2.1: Detected collision; DSSAD 5.3.1 trigger |
| Detected failure situation (ADS, sensor, other vehicle systems) | Evaluate whether a system failure contributed to an incident | DSSAD 5.2.1: Detected failure situation |

### 3.4 Remote Operations

As remote guidance and teleoperation become integral to ADS deployment, particularly for commercial fleets, regulators and insurers must understand the role of remote operators in the safety chain.

| Data Point | Public Safety / Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| Remote intervention in tactical function | Determine if and when a remote operator influenced the vehicle's behaviour | DSSAD 5.2.1: Remote intervention in a tactical function |
| Remote termination | Assess whether the ADS was remotely shut down and under what circumstances | GTR 4.1.4.4: Remote termination capability |

### 3.5 Supporting Contextual Data

In addition to ADS-specific data, public safety evaluation and insurance require contextual data that frames the driving environment and vehicle state at the time of any event.

| Data Point | Existing VSS Path | Standard Status |
|---|---|---|
| Vehicle speed | Vehicle.Speed | Defined in VSS |
| Longitudinal acceleration | Vehicle.Acceleration.Longitudinal | Defined in VSS |
| Lateral acceleration | Vehicle.Acceleration.Lateral | Defined in VSS |
| Vertical acceleration | Vehicle.Acceleration.Vertical | Defined in VSS |
| Yaw rate | Vehicle.AngularVelocity.Yaw | Defined in VSS |
| GPS position | Vehicle.CurrentLocation | Defined in VSS |
| Lane departure detection status | Vehicle.ADAS.LaneDepartureDetection.IsEnabled | Defined in VSS |
| Electronic stability control | Vehicle.ADAS.ESC.IsEnabled / IsEngaged | Defined in VSS |
| Blind spot detection | Vehicle.ADAS.BSD (proposed) | Under development |
| Forward collision warning | Vehicle.ADAS.FCW (proposed) | Under development |
| Brake pedal status | Vehicle.Chassis.Brake | Defined in VSS |
| Headlight status | Vehicle.Body.Lights | Defined in VSS |
| Seatbelt status | Vehicle.Cabin.Seat.*.IsBelted | Defined in VSS |
| Windshield wiper status | Vehicle.Body.Windshield.Front.Wiping | Defined in VSS |

---

## 4. Current State of Standardization

### 4.1 What Is Already Defined in COVESA VSS

A significant number of the data points required for public safety evaluation and the insurance of autonomous vehicles are already defined within the COVESA Vehicle Signal Specification. These include the foundational vehicle dynamics signals (acceleration, speed, position), ADAS feature status signals (lane departure, ESC, collision mitigation), driver state indicators (seatbelt status), and environmental context signals (headlights, wipers).

For conventional driver-assistance systems (SAE Levels 0–2), the existing VSS tree provides substantial coverage of the data points identified in the MOTER project's safety use cases. Many of these signals also have corresponding VHAL properties in Android Automotive and PGN/SPN codes in the SAE J1939 standard for heavy-duty vehicles, providing multiple pathways for data access.

### 4.2 What Requires Further Development

The data points most critical to public safety oversight of vehicles operating at SAE Levels 3 and above — the ADS operational status, transition of control, and emergency response signals — require additional standardization work. COVESA intends to develop these definitions through its ongoing projects:

**Signals under active development or planned:**

- **ADS operational status** — a clear, standardized signal indicating whether an ADS feature is actively performing the DDT, and at what level of automation
- **Transition demand events** — structured data capturing when the ADS requests human intervention, including the reason for the request and the driver's response
- **Emergency manoeuvre bracketing** — start and end timestamps for emergency manoeuvres, enabling precise event reconstruction
- **Minimal Risk Condition application** — standardized indication that the ADS has initiated a fallback to a safe state, including the type of MRC applied
- **Remote operator intervention** — data elements capturing when and how remote guidance or teleoperation is provided
- **Manual override classification** — distinguishing between driver-initiated takeover, safety driver intervention, and remote operator override

### 4.3 Alignment with UNECE GTR DSSAD Requirements

The MOTER project's data point definitions show strong alignment with the DSSAD requirements in Annex 6 of the proposed UN GTR. This alignment is not coincidental — COVESA members have been tracking the development of the GTR and ensuring that the industry's open data standards can support regulatory compliance.

However, there are important areas where the COVESA work extends beyond the current DSSAD scope to serve the broader public safety ecosystem:

1. **Ongoing operational data access** — The DSSAD is designed primarily for event-triggered recording and post-incident data retrieval. Public safety evaluation and insurance risk assessment also require periodic or continuous reporting of ADS operational summaries to identify systemic risks and trends before they result in incidents.

2. **Cross-manufacturer interoperability** — The DSSAD requires data to be provided in "an open standard format (e.g. JSON, CSV, XML)" but does not specify the semantic content of the data fields. VSS provides the standardized vocabulary that makes data from different manufacturers comparable and interoperable — essential for fleet-wide and population-wide safety analysis.

3. **Sampling and reporting specifications** — The MOTER project defines recommended sampling rates and data reporting logic for each data point (e.g., "Event Based: Every time status changes" or "20–50 Hz" for acceleration data during events), providing practical implementation guidance beyond the DSSAD's structural requirements.

---

## 5. Protecting Intellectual Property Through Layered Abstraction

### 5.1 The Challenge

Automotive manufacturers invest heavily in the development of their ADS technologies. The algorithms, sensor fusion strategies, decision-making logic, and control systems that constitute an ADS implementation represent significant intellectual property. Understandably, manufacturers are reluctant to expose the inner workings of these systems through standardized data interfaces.

At the same time, the public safety ecosystem — regulators, insurers, researchers, and other independent third parties — has legitimate needs for data that characterizes ADS behaviour and performance. Resolving this tension is essential for the broad, safe deployment of autonomous vehicles.

### 5.2 The Approach: Higher-Level Abstracted Data Elements

COVESA proposes an approach based on layered data abstraction. Rather than requiring manufacturers to expose the raw sensor data, algorithmic outputs, or internal decision states of their ADS implementations, the standard would define higher-level data elements that characterize outcomes and events without revealing proprietary methods.

**Example: Emergency Manoeuvre**

The UNECE GTR DSSAD requires recording of "Start of Emergency Manoeuvre" and "End of Emergency Manoeuvre." The MOTER project aligns with this by defining "start/end of emergency manoeuvre" as a data point under the SAFETY04 use case family.

This is a higher-level abstraction. It tells the investigator or insurer that the ADS entered an emergency state, when it started, and when it ended — without requiring the manufacturer to disclose:

- Which specific sensors detected the threat
- What algorithmic pipeline classified the situation as an emergency
- What candidate manoeuvres were evaluated and rejected
- How the control system executed the chosen manoeuvre at a sub-second level

The manufacturer's proprietary decision-making process remains protected. What is standardized is the *outcome classification* — the fact that an emergency manoeuvre occurred, its temporal boundaries, and its context (through supporting data points).

**Example: Transition Demand**

Similarly, when an ADS issues a transition demand to a human driver, the standardized data would capture:

- That a transition demand was issued
- The timestamp
- A categorical reason (e.g., ODD boundary, system fault, environmental conditions)
- Whether the human responded, and when
- The outcome (successful handover, ADS fallback to MRC, etc.)

The standard would not require disclosure of the specific sensor readings, confidence levels, or planning-horizon calculations that led the ADS to determine a transition was necessary.

### 5.3 Benefits of This Approach

This layered abstraction provides multiple benefits:

- **For public safety:** Independent third parties gain access to meaningful, standardized data for safety evaluation and risk assessment without the delays or limitations of accessing proprietary system internals. Systemic risks can be identified earlier, and safety performance can be compared across manufacturers.

- **For manufacturers:** Core ADS intellectual property is protected. Competitive differentiation in ADS technology is preserved. Compliance burden is reduced because the required data elements are high-level event classifications rather than raw system internals.

- **For insurers:** The data needed for risk assessment and claims adjudication is available in a standardized, interoperable format. Actuarial models can be built on consistent data across manufacturers, enabling accurate pricing that reflects actual ADS safety performance.

- **For regulators:** Safety performance can be evaluated through standardized outcome data. Compliance can be verified without requiring access to proprietary implementations.

- **For fleet operators:** Consistent data semantics enable fleet safety management across mixed-manufacturer fleets. Safety coaching and operational optimization can be based on standardized metrics.

### 5.4 Alignment with GTR Principles

This approach directly aligns with the principles stated in the proposed UN GTR, which specifies that technical provisions should be "performance based, technology neutral, and based on state-of-the-art technology, while avoiding restricting future innovation." By standardizing outcomes rather than implementations, the data standard allows manufacturers to innovate freely in their ADS architectures while still providing the transparency that the public safety ecosystem requires.

The DSSAD provisions themselves reflect this philosophy. Section 3.2 of Annex 6 states that "information required to interpret the output to correlate it with respect to the data elements... shall be provided by the manufacturer to an authorized entity on request and subject to applicable national law(s)." This establishes the principle that the manufacturer retains control over interpretation guidance while providing standardized data elements — precisely the layered approach that COVESA advocates.

---

## 6. Recommendations

### 6.1 For Regulatory Bodies

1. **Reference open data standards in ADS regulations.** As the DSSAD requirements are finalized, we recommend that the regulation reference or encourage alignment with existing open vehicle data standards, particularly the COVESA Vehicle Signal Specification, for semantic interoperability. The DSSAD appropriately mandates open data formats (JSON, CSV, XML) — extending this to include standardized data semantics would significantly enhance the practical utility of the recorded data for the entire public safety ecosystem.

2. **Design data requirements to serve the full public safety ecosystem.** The current DSSAD is oriented toward safety evaluation and post-incident investigation. We recommend that regulatory bodies consider the needs of independent third parties — insurers, fleet safety managers, and road safety researchers — who require ongoing access to standardized ADS operational data to fulfil their complementary public safety functions.

3. **Adopt the principle of layered data abstraction.** Regulations should explicitly support the concept of standardized, higher-level data elements that characterize ADS outcomes and events without requiring disclosure of proprietary implementation details. This approach balances the competing interests of public transparency and intellectual property protection.

4. **Harmonize data requirements internationally.** Given the global nature of both the automotive and insurance industries, data standards should be harmonized across jurisdictions. The COVESA VSS provides a vendor-neutral, internationally applicable foundation for this harmonization, supporting the UN's broader goals of regulatory coherence.

### 6.2 For the Insurance Industry and Independent Third Parties

1. **Engage with open standards development.** Insurers and other independent safety evaluators should participate in COVESA and similar open standards organizations to ensure that the data definitions being developed meet their safety assessment, actuarial, and claims processing needs.

2. **Develop ADS-aware safety and risk models.** The availability of standardized ADS operational data enables the development of new assessment models that properly account for the distinct safety profiles and risk characteristics of human-driven, ADS-assisted, and fully autonomous vehicle operation.

3. **Support the harmonization of digital proof of insurance.** As digital vehicle identity and insurance documentation evolve, alignment with standardized vehicle data taxonomies will reduce friction and support more responsive, data-driven safety oversight.

### 6.3 For Automotive Manufacturers

1. **Adopt open data standards for ADS status reporting.** Implementing standardized data elements for ADS operational status, transitions of control, and emergency events provides a defensible, industry-accepted framework for data sharing that protects core IP while meeting regulatory requirements and enabling independent safety evaluation.

2. **Participate in the definition of higher-level data abstractions.** Manufacturers have the domain expertise to ensure that standardized data elements accurately and fairly characterize ADS performance without exposing proprietary methods. Active participation in the standards process is the most effective way to shape these definitions and ensure they are technically sound.

3. **Support interoperable data access interfaces.** The DSSAD requirement for data accessibility through "an electronic communication interface that complies with a publicly available interface standard" aligns with COVESA's work on the Vehicle Information Service Specification (VISS). Implementing these interfaces facilitates regulatory compliance while enabling the broader public safety ecosystem.

---

## 7. Conclusion

The safe deployment of autonomous vehicles is not solely a technical challenge — it is an ecosystem challenge. Public safety depends on a framework of continuous accountability that extends beyond the manufacturer and the regulator to include independent third parties who provide ongoing, objective safety assessment. Insurers are essential to this framework: they provide the financial accountability mechanism, the continuous risk evaluation, and the market-driven safety incentives that complement regulatory oversight.

For this ecosystem to function, all participants need access to standardized, interoperable vehicle data. Without it, regulators cannot consistently enforce safety requirements across manufacturers. Investigators cannot reliably reconstruct incidents. Insurers cannot accurately assess risk. And the public cannot have confidence that autonomous vehicles are being held to rigorous, transparent safety standards.

COVESA's open data standards — the Vehicle Signal Specification and the MOTER project's safety and insurance data point definitions — provide the common vocabulary that enables all stakeholders to function effectively. Many of the foundational data points are already defined. The ADS-specific data elements are under active development, informed by the requirements of the UNECE GTR DSSAD and the practical needs of the full public safety ecosystem.

We call upon the regulatory community to engage with these open standards efforts, to reference them where appropriate in ADS regulations, and to adopt the principle of layered data abstraction that balances transparency with intellectual property protection. The path to safe, accountable, commercially viable autonomous vehicles runs through standardized data — and the standards community is ready to build it.

---

## References

1. United Nations Economic Commission for Europe, "Proposal for a new United Nations Global Technical Regulation on Automated Driving Systems (ADS)," ECE/TRANS/WP.29/GRVA/2026/2, November 2025.

2. COVESA, "Vehicle Signal Specification (VSS)," https://covesa.global/vss

3. COVESA MOTER Project, "MOTER VSS Data additions v3," Working document, 2025–2026.

4. SAE International, "Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles," SAE J3016, 2021.

5. SAE International, "Digital Data Communications for Use by Heavy-Duty Vehicles," SAE J1939, ongoing.

6. ECE/TRANS/WP.29/2019/34/Rev.2, "Framework Document on Automated/Autonomous Vehicles."

7. ECE/TRANS/WP.29/2024/39, "Integrated FRAV/VMAD Guidelines."

8. United Nations General Assembly, "Global Plan for the Decade of Action for Road Safety 2021–2030."

---

*This paper is published by COVESA (Connected Vehicle Systems Alliance) as an input to the regulatory development process for Automated Driving Systems. COVESA is a global alliance of automotive manufacturers, technology companies, insurers, fleet operators, and other stakeholders committed to developing open standards for connected vehicle data. For more information, visit www.covesa.global.*

*COVESA's Commercial and Fleet Vehicles working group meets regularly to advance these standards. Participation is open to all COVESA members. Contact information is available through the COVESA website.*
