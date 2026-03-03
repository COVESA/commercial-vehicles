# Status: Draft #
# Standardized Vehicle Data for Insuring Autonomous Vehicles: The Role of Open Standards in Regulatory Alignment

**A COVESA Position Paper**

**March 2026**

**Contributors:** COVESA Commercial and Fleet Vehicles Expert Group

---

## Executive Summary

The global deployment of Automated Driving Systems (ADS) is accelerating, bringing with it a fundamental transformation in how motor vehicles are insured. Traditional insurance models built on driver behaviour assessment are insufficient for vehicles where the driving task is performed — in whole or in part — by an automated system. Insurers, regulators, fleet operators, and automotive manufacturers all require access to standardized, interoperable data that can reliably answer a core set of questions: Was the ADS operating? Did a human take over? Was remote guidance provided? What triggered a transition or emergency manoeuvre?

The proposed United Nations Global Technical Regulation on Automated Driving Systems (ECE/TRANS/WP.29/GRVA/2026/2) recognizes this need through its Data Storage System for Automated Driving (DSSAD) requirements. However, the current regulatory text focuses primarily on safety compliance and post-incident investigation. It does not fully address the broader ecosystem of stakeholders — particularly insurers and fleet operators — who require ongoing, standardized access to ADS operational data for risk assessment, premium calculation, and claims adjudication.

COVESA (Connected Vehicle Systems Alliance) and its member organizations are actively defining the open data standards needed to bridge this gap. Through the Vehicle Signal Specification (VSS), the MOTER (Mobility, Observation, Telematics, Evaluation and Risk) project, and collaboration with industry partners including Allianz, Geotab, Cox Automotive, and others, COVESA is building the data vocabulary that can serve both regulatory compliance and commercial insurance needs — while preserving automotive manufacturers' intellectual property in their ADS implementations.

This paper presents the case for why standardized, open vehicle data definitions are essential for insuring autonomous vehicles, identifies which data points are already defined within COVESA standards and which require further development, and proposes an approach that balances transparency with IP protection through the use of higher-level abstracted data elements.

---

## 1. The Insurance Challenge of Automated Driving

### 1.1 A Paradigm Shift in Liability and Risk Assessment

The insurance industry has developed over a century of actuarial models based on human driver behaviour. Premiums are calculated on the basis of driver demographics, driving history, vehicle type, and increasingly on telematics data that captures driving patterns such as harsh braking, speeding, and cornering.

ADS-equipped vehicles fundamentally disrupt these models. When a vehicle operating at SAE Level 3 or higher is performing the Dynamic Driving Task (DDT), the traditional concept of "driver risk" no longer applies in the same way. Instead, liability and risk assessment must account for:

- **The operational state of the ADS** — whether the system was actively controlling the vehicle at any given moment
- **Transitions of control** — when and why the ADS requested human intervention, and whether the human responded appropriately
- **System limitations** — the boundaries of the Operational Design Domain (ODD) and whether the ADS was operating within them
- **Emergency responses** — how the ADS handled critical situations, including Minimal Risk Conditions (MRC) and emergency manoeuvres
- **Remote operations** — whether remote guidance or intervention was provided, and its effectiveness

Without standardized access to this data, insurers cannot accurately assess risk, calculate premiums, or adjudicate claims involving ADS-equipped vehicles. This creates a market impediment to ADS deployment: vehicles that cannot be properly insured cannot be widely adopted.

### 1.2 The Regulatory Landscape

The proposed UN GTR on ADS (ECE/TRANS/WP.29/GRVA/2026/2) establishes a comprehensive framework for ADS safety requirements. Its provisions are performance-based and technology-neutral, recognizing that ADS technology is evolving rapidly and that regulations must not restrict future innovation.

Of particular relevance to the insurance industry is Annex 6 of the proposed GTR, which defines the Data Storage System for Automated Driving (DSSAD). The DSSAD requirements mandate the recording of time-stamped events including:

- Activation and deactivation of ADS features (by system or user)
- ODD exit events
- Start of ADS fallback to user or to a Minimal Risk Condition
- User input to driving controls while ADS is active
- Prevention of user takeover (with reasons)
- Start and end of emergency manoeuvres
- Detected collisions and failure situations
- Remote intervention in tactical functions

The DSSAD also mandates time-series data recording during triggering events, including detected object distances and velocities, ADS-requested acceleration, braking, and steering demands, vehicle acceleration data, and ADS-determined vehicle speed.

These requirements represent a significant step forward. However, they are oriented primarily toward post-incident investigation and regulatory compliance rather than toward the ongoing, systematic data access that insurers require for risk modelling and portfolio management. Furthermore, the regulation appropriately notes that data accessibility requirements are "without prejudice to applicable laws governing access to data, availability, privacy and data protection" — but does not specify the data formats, interfaces, or taxonomies that would enable practical interoperability across the insurance ecosystem.

### 1.3 The Gap Between Regulation and Insurance Practice

The insurance industry needs more than a mandated recording obligation. It needs:

1. **Standardized data definitions** — common semantics for what each data element means, how it is measured, and how it should be interpreted
2. **Interoperable data formats** — consistent, machine-readable representations that work across vehicle manufacturers, fleet management systems, and insurance platforms
3. **Appropriate sampling and reporting logic** — specifications for when and how frequently data should be captured, balancing completeness with data volume management
4. **Layered data access** — the ability to access higher-level operational summaries without requiring access to proprietary, lower-level ADS implementation details

COVESA's work directly addresses each of these needs.

---

## 2. COVESA's Role: Building the Open Data Vocabulary

### 2.1 The Vehicle Signal Specification (VSS)

The COVESA Vehicle Signal Specification is an open, community-developed taxonomy for vehicle data. VSS defines a tree-structured hierarchy of vehicle signals — from basic vehicle attributes to advanced driver assistance systems (ADAS) and increasingly autonomous driving functions. It provides standardized names, data types, units, and descriptions for each signal, enabling interoperability across the automotive ecosystem.

VSS is already referenced and adopted by major automotive platforms, including the Android Automotive Vehicle Hardware Abstraction Layer (VHAL), which maps platform-level vehicle properties to corresponding VSS paths. This alignment between platform-level APIs and open standards creates a practical pathway for data access.

### 2.2 The MOTER Project

COVESA's MOTER (Mobility, Observation, Telematics, Evaluation and Risk) project is a cross-industry initiative that brings together insurers, fleet operators, telematics providers, and automotive manufacturers to define the specific vehicle data points needed for insurance and fleet safety applications. MOTER has developed a comprehensive mapping of use cases to required data points, with each data point linked to:

- Its existing or proposed VSS path
- Corresponding VHAL (Android Automotive) property where available
- Equivalent SAE J1939 PGN/SPN codes for heavy-duty vehicles
- Sensoris definitions where applicable
- Recommended sampling rates and data reporting logic
- Priority and importance ratings
- Applicable SAE automation levels

### 2.3 Industry Collaboration

COVESA's work on ADS-related data standards involves active collaboration with insurance industry stakeholders. Allianz Partners, through its Automotive Innovation and Connected Car division, participates in COVESA's Commercial and Fleet Vehicles working group, contributing insurance domain expertise to the data standardization process. Discussions are also underway with the German insurance industry association (GDV) regarding the harmonization of digital proof of insurance — a domain where standardized vehicle identity and status data is fundamental.

The COVESA All Members Meeting (AMM) programme includes dedicated sessions on fleet and insurance data topics, bringing together MOTER contributors, Endava, Cox Automotive, Geotab, and other industry participants to advance data-driven business value for fleets and insurers.

---

## 3. Essential Data Points for Insuring Autonomous Vehicles

The MOTER project has identified a comprehensive set of data points essential for insuring ADS-equipped vehicles. These data points fall into several categories, reflecting the distinct questions that insurers must be able to answer.

### 3.1 ADS Operational Status

The most fundamental question for insuring an autonomous vehicle is: **who or what was controlling the vehicle at the time of an incident?**

| Data Point | Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| ADS activation/deactivation status | Determine whether the ADS was performing the DDT | DSSAD 5.2.1: Activation/Deactivation of the feature |
| ADS operating mode (SAE level) | Assess applicable liability framework | Implicit in ADS feature identification |
| ODD boundary status | Determine if ADS was operating within its designed parameters | DSSAD 5.2.1: ODD exit |
| Autonomous driving status | Continuous confirmation that ADS is in control | Referenced in MOTER SAFETY04 use cases |

### 3.2 Transitions of Control

When the ADS ceases to perform the DDT and a human must assume control, the circumstances and execution of this transition are critical to liability determination.

| Data Point | Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| Transition demand to driver (with reason) | Understand why the ADS requested human intervention | DSSAD 5.2.1: Start of ADS fallback to user |
| Manual interaction/override by driver, safety driver, or remote operator | Determine who took control, when, and through what means | DSSAD 5.2.1: User input to driving controls |
| Deactivation of ADS function | Track system shutdown events and their initiators | DSSAD 5.2.1: Deactivation by system or user |
| Prevention of user takeover (with reason) | Assess whether the ADS appropriately prevented an unsafe handover | DSSAD 5.2.1: Prevention of user takeover |
| Detection that fallback user is not available | Evaluate driver readiness and engagement | DSSAD 5.2.1: Detection that fallback-user is not available |

### 3.3 Emergency Situations and Safety Responses

How the vehicle responds in critical and emergency situations directly impacts claims outcomes and safety performance evaluation.

| Data Point | Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| Start/end of emergency manoeuvre | Bracket the critical event window for reconstruction | DSSAD 5.2.1: Start/End of Emergency Manoeuvre |
| Application of Minimal Risk Condition (safety stop, turtle mode) | Assess the ADS response to situations exceeding its capabilities | DSSAD 5.2.1: Start of ADS fallback to an MRC / MRC achieved |
| Emergency braking event | Determine if and when automatic emergency braking was applied | DSSAD 5.3.2: ADS-requested service braking demand |
| Detected collision | Confirm whether a collision occurred and trigger data preservation | DSSAD 5.2.1: Detected collision; DSSAD 5.3.1 trigger |
| Detected failure situation (ADS, sensor, other vehicle systems) | Evaluate whether a system failure contributed to an incident | DSSAD 5.2.1: Detected failure situation |

### 3.4 Remote Operations

As remote guidance and teleoperation become integral to ADS deployment, particularly for commercial fleets, insurers must understand the role of remote operators.

| Data Point | Insurance Purpose | UNECE GTR Alignment |
|---|---|---|
| Remote intervention in tactical function | Determine if and when a remote operator influenced the vehicle's behaviour | DSSAD 5.2.1: Remote intervention in a tactical function |
| Remote termination | Assess whether the ADS was remotely shut down | GTR 4.1.4.4: Remote termination capability |

### 3.5 Supporting Contextual Data

In addition to ADS-specific data, insurers require contextual data that frames the driving environment and vehicle state at the time of any event.

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

A significant number of the data points required for insuring autonomous vehicles are already defined within the COVESA Vehicle Signal Specification. These include the foundational vehicle dynamics signals (acceleration, speed, position), ADAS feature status signals (lane departure, ESC, collision mitigation), driver state indicators (seatbelt status), and environmental context signals (headlights, wipers).

For conventional driver-assistance systems (SAE Levels 0-2), the existing VSS tree provides substantial coverage of the data points identified in the MOTER project's safety use cases. Many of these signals also have corresponding VHAL properties in Android Automotive and PGN/SPN codes in the SAE J1939 standard for heavy-duty vehicles, providing multiple pathways for data access.

### 4.2 What Requires Further Development

The data points most critical to insuring vehicles operating at SAE Levels 3 and above — the ADS operational status, transition of control, and emergency response signals — require additional standardization work. COVESA intends to develop these definitions through its ongoing projects:

**Signals under active development or planned:**

- **ADS operational status** — a clear, standardized signal indicating whether an ADS feature is actively performing the DDT, and at what level of automation
- **Transition demand events** — structured data capturing when the ADS requests human intervention, including the reason for the request and the driver's response
- **Emergency manoeuvre bracketing** — start and end timestamps for emergency manoeuvres, enabling precise event reconstruction
- **Minimal Risk Condition application** — standardized indication that the ADS has initiated a fallback to a safe state, including the type of MRC applied
- **Remote operator intervention** — data elements capturing when and how remote guidance or teleoperation is provided
- **Manual override classification** — distinguishing between driver-initiated takeover, safety driver intervention, and remote operator override

### 4.3 Alignment with UNECE GTR DSSAD Requirements

The MOTER project's data point definitions show strong alignment with the DSSAD requirements in Annex 6 of the proposed UN GTR. This alignment is not coincidental — COVESA members have been tracking the development of the GTR and ensuring that the industry's open data standards can support regulatory compliance.

However, there are important areas where the COVESA work extends beyond the current DSSAD scope:

1. **Ongoing operational data access** — The DSSAD is designed primarily for event-triggered recording and post-incident data retrieval. Insurance and fleet management applications also require periodic or continuous reporting of ADS operational summaries.

2. **Cross-manufacturer interoperability** — The DSSAD requires data to be provided in "an open standard format (e.g. JSON, CSV, XML)" but does not specify the semantic content of the data fields. VSS provides the standardized vocabulary that makes data from different manufacturers comparable and interoperable.

3. **Sampling and reporting specifications** — The MOTER project defines recommended sampling rates and data reporting logic for each data point (e.g., "Event Based: Every time status changes" or "20-50 Hz" for acceleration data during events), providing practical implementation guidance beyond the DSSAD's structural requirements.

---

## 5. Protecting Intellectual Property Through Layered Abstraction

### 5.1 The Challenge

Automotive manufacturers invest heavily in the development of their ADS technologies. The algorithms, sensor fusion strategies, decision-making logic, and control systems that constitute an ADS implementation represent significant intellectual property. Understandably, manufacturers are reluctant to expose the inner workings of these systems through standardized data interfaces.

At the same time, regulators, insurers, and other stakeholders have legitimate needs for data that characterizes ADS behaviour and performance. Resolving this tension is essential for the broad deployment of autonomous vehicles.

### 5.2 The Approach: Higher-Level Abstracted Data Elements

COVESA proposes an approach based on layered data abstraction. Rather than requiring manufacturers to expose the raw sensor data, algorithmic outputs, or internal decision states of their ADS implementations, the standard would define higher-level data elements that characterize outcomes and events without revealing proprietary methods.

**Example: Emergency Manoeuvre**

The UNECE GTR DSSAD requires recording of "Start of Emergency Manoeuvre" and "End of Emergency Manoeuvre." The MOTER project aligns with this by defining "start/end of emergency manoeuvre" as a data point under the SAFETY04 use case family.

This is a higher-level abstraction. It tells the insurer that the ADS entered an emergency state, when it started, and when it ended — without requiring the manufacturer to disclose:

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

- **For manufacturers:** Core ADS intellectual property is protected. Competitive differentiation in ADS technology is preserved. Compliance burden is reduced because the required data elements are high-level event classifications rather than raw system internals.

- **For insurers:** The data needed for risk assessment and claims adjudication is available in a standardized, interoperable format. Actuarial models can be built on consistent data across manufacturers.

- **For regulators:** Safety performance can be evaluated through standardized outcome data. Compliance can be verified without requiring access to proprietary implementations.

- **For fleet operators:** Consistent data semantics enable fleet management across mixed-manufacturer fleets. Safety coaching and operational optimization can be based on standardized metrics.

### 5.4 Alignment with GTR Principles

This approach directly aligns with the principles stated in the proposed UN GTR, which specifies that technical provisions should be "performance based, technology neutral, and based on state-of-the-art technology, while avoiding restricting future innovation." By standardizing outcomes rather than implementations, the data standard allows manufacturers to innovate freely in their ADS architectures while still providing the transparency that the broader ecosystem requires.

The DSSAD provisions themselves reflect this philosophy. Section 3.2 of Annex 6 states that "information required to interpret the output to correlate it with respect to the data elements... shall be provided by the manufacturer to an authorized entity on request and subject to applicable national law(s)." This establishes the principle that the manufacturer retains control over interpretation guidance while providing standardized data elements — precisely the layered approach that COVESA advocates.

---

## 6. Recommendations

### 6.1 For Regulatory Bodies

1. **Reference open data standards in ADS regulations.** As the DSSAD requirements are finalized, we recommend that the regulation reference or encourage alignment with existing open vehicle data standards, particularly the COVESA Vehicle Signal Specification, for semantic interoperability. The DSSAD appropriately mandates open data formats (JSON, CSV, XML) — extending this to include standardized data semantics would significantly enhance the practical utility of the recorded data.

2. **Consider insurance data needs alongside safety compliance.** The current DSSAD is oriented toward safety evaluation and post-incident investigation. We recommend that regulatory bodies engage with the insurance industry to ensure that data requirements also support the ongoing risk assessment, premium calculation, and claims adjudication processes that are essential for the commercial viability of ADS deployment.

3. **Adopt the principle of layered data abstraction.** Regulations should explicitly support the concept of standardized, higher-level data elements that characterize ADS outcomes and events without requiring disclosure of proprietary implementation details. This approach balances the competing interests of transparency and intellectual property protection.

4. **Harmonize data requirements internationally.** Given the global nature of both the automotive and insurance industries, data standards should be harmonized across jurisdictions. The COVESA VSS provides a vendor-neutral, internationally applicable foundation for this harmonization.

### 6.2 For the Insurance Industry

1. **Engage with open standards development.** Insurers should participate in COVESA and similar open standards organizations to ensure that the data definitions being developed meet their actuarial and claims processing needs.

2. **Develop ADS-aware risk models.** The availability of standardized ADS operational data enables the development of new actuarial models that properly account for the distinct risk profiles of human-driven, ADS-assisted, and fully autonomous vehicle operation.

3. **Support the harmonization of digital proof of insurance.** As digital vehicle identity and insurance documentation evolve, alignment with standardized vehicle data taxonomies will reduce friction and enable new service models.

### 6.3 For Automotive Manufacturers

1. **Adopt open data standards for ADS status reporting.** Implementing standardized data elements for ADS operational status, transitions of control, and emergency events provides a defensible, industry-accepted framework for data sharing that protects core IP while meeting regulatory and commercial requirements.

2. **Participate in the definition of higher-level data abstractions.** Manufacturers have the domain expertise to ensure that standardized data elements accurately and fairly characterize ADS performance without exposing proprietary methods. Active participation in the standards process is the most effective way to shape these definitions.

3. **Support interoperable data access interfaces.** The DSSAD requirement for data accessibility through "an electronic communication interface that complies with a publicly available interface standard" aligns with COVESA's work on the Vehicle Information Service Specification (VISS). Implementing these interfaces facilitates compliance while enabling broader ecosystem value.

---

## 7. Conclusion

The transition to autonomous vehicles is not solely a technical challenge — it is an ecosystem challenge. Vehicles that cannot be insured cannot be widely deployed. Insurers that lack standardized data cannot accurately assess risk. Manufacturers that are forced to expose proprietary implementations will resist data sharing. Regulators that lack interoperable data semantics will struggle to enforce performance requirements consistently.

COVESA's open data standards — the Vehicle Signal Specification, the MOTER project's insurance and fleet data point definitions, and the evolving ADS-specific signal taxonomy — provide the common vocabulary that enables all stakeholders to function effectively. Many of the foundational data points are already defined. The ADS-specific data elements are under active development, informed by the requirements of the UNECE GTR DSSAD and the practical needs of insurers and fleet operators.

We call upon the regulatory community to engage with these open standards efforts, to reference them where appropriate in ADS regulations, and to adopt the principle of layered data abstraction that balances transparency with intellectual property protection. The path to safe, insurable, commercially viable autonomous vehicles runs through standardized data — and the standards community is ready to build it.

---

## References

1. United Nations Economic Commission for Europe, "Proposal for a new United Nations Global Technical Regulation on Automated Driving Systems (ADS)," ECE/TRANS/WP.29/GRVA/2026/2, November 2025.

2. COVESA, "Vehicle Signal Specification (VSS)," https://covesa.global/vss

3. COVESA MOTER Project, "MOTER VSS Data additions v3," Working document, 2025-2026.

4. SAE International, "Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles," SAE J3016, 2021.

5. SAE International, "Digital Data Communications for Use by Heavy-Duty Vehicles," SAE J1939, ongoing.

6. ECE/TRANS/WP.29/2019/34/Rev.2, "Framework Document on Automated/Autonomous Vehicles."

7. ECE/TRANS/WP.29/2024/39, "Integrated FRAV/VMAD Guidelines."

---

*This paper is published by COVESA (Connected Vehicle Systems Alliance) as an input to the regulatory development process for Automated Driving Systems. COVESA is a global alliance of automotive manufacturers, technology companies, insurers, fleet operators, and other stakeholders committed to developing open standards for connected vehicle data. For more information, visit www.covesa.global.*

*COVESA's Commercial and Fleet Vehicles working group meets regularly to advance these standards. Participation is open to all COVESA members. Contact information is available through the COVESA website.*
