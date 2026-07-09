# CA DMV Vehicle Credentials Collaboration: Benefits to COVESA Stakeholders

**Date:** July 2026  
**Author:** Ted Guild, Geotab / COVESA Commercial and Fleet Expert Group  
**Status:** Draft for discussion  
---

## Executive Summary

The California Department of Motor Vehicles (CA DMV) — the leading state agency deploying Verifiable Credentials (VCs) at scale in production — has initiated a collaboration with COVESA to transfer and evolve a Vehicle Credential vocabulary for broad industry adoption. The collaboration is structured as a phased contribution: CA DMV transfers the `vehicle-credentials-vocabulary` repository (now licensed MPLv2 and hosted at [github.com/covesa/vehicle-credentials-vocabulary](https://github.com/covesa/vehicle-credentials-vocabulary)) to COVESA's GitHub organization, COVESA shapes the work to address industry use cases, and CA DMV participates in setting vehicle standards through COVESA's technical bodies.

This work directly addresses high-impact, high-cost challenges in California — and by extension across the US and internationally — covering vehicle sales fraud, insurance verification, traffic stop safety, emergency response, emissions compliance, commercial licensing, and fleet registration. The total addressable problem set exceeds **$9 billion per year** in California alone for their state agencies. The commercial revenue potential combined with vehicle data normalized in [COVESA Vehicle Signal Specification](https://covesa.global/vehicle-signal-specification/) (VSS) is yet unquantified but should be substantial.

This report summarizes how the collaboration benefits COVESA's three primary stakeholder groups: **OEMs and Tier-1 Suppliers**, **Data Consumers (fleet operators, insurers, and other verticals)**, and **COVESA as a standards body**.

---

## Background: What CA DMV Is Building

The CA DMV is deploying a suite of digitally-verifiable vehicle and driver credentials, anchored in W3C Verifiable Credentials (VC) standards, issued into a California DMV Wallet. The credential data model covers six core areas:

- **Driver's License** — digital mDL/VC usable in vehicle-to-officer and vehicle-to-buyer flows
- **Vehicle Title** — cryptographically verifiable ownership and lien status
- **Vehicle Registration** — linked to insurance compliance enforcement
- **Vehicle Insurance** — proof of coverage tied to registration, with vehicle-enforced compliance
- **Vehicle Inspection** — smog and safety certificates issued as VCs
- **Emergency Response** — automatic VC-based crash notification to E911 and insurers

These credentials are designed to be stored **in the vehicle itself**, not only in a phone wallet, enabling vehicle-to-vehicle, vehicle-to-infrastructure, and vehicle-to-cloud credential exchanges.

COVESA is the logical industry home for this vocabulary because it creates connected vehicle standards adopted by the world's largest OEMs (BMW, Ford, GM, Honda, Hyundai, Volvo, Nissan) and Tier-1 suppliers (Bosch, NXP, ARM, Renesas, Michelin). If CA DMV wants their digital credentials integrated into automobiles and industry verticals such as insurance, E911, fleet management, and vehicle maintenance, **COVESA is the place to establish those standards**.

COVESA will seek to collaborate with organizations like the [American Association of Motor Vehicle Administrators](https://aamva.org/) to promote wider adoption of these verifiable credentials. We understand other North American states/provinces are already considering adoption.

---

## Benefits to OEMs and Tier-1 Suppliers

### 1. A Pre-Validated Credential Vocabulary with Government Authority

CA DMV is not a research project — it is a production deployment in the largest US state, representing ~28 million registered vehicles. OEMs that implement the COVESA-hosted vehicle credential vocabulary gain:

- An **authoritative, government-issued schema** to build on, reducing design risk versus proprietary alternatives
- A vocabulary already negotiated for **MPLv2 open-source licensing**, ensuring patent grants from contributors and that improvements remain open (critical for consortium adoption)
- A direct liaison with CA DMV's Digital Transformation team (Chief Digital Transformation Officer, IT Specialists, Product Managers) who can provide implementation guidance and real-world test datasets

### 2. In-Vehicle Credential Storage as a Platform Differentiator

The use cases envision credentials stored in the vehicle's onboard system, not just the driver's phone. This creates a new vehicle feature surface:

- **Vehicle Title and Registration upload** into the vehicle's system, shareable directly to a buyer's device during a private sale
- **Insurance compliance monitoring**, with the vehicle itself warning the driver of coverage lapses and — per the CA DMV model — limiting speed to 25 mph if coverage is confirmed lapsed
- **Automatic crash notification** transmitting a Verifiable Presentation (vehicle model, crash telemetry, occupant data, insurance) to E911 and insurers upon impact

For OEMs, particularly those already active in COVESA's connected vehicle work (BMW is an early participant in this collaboration through Daniel Alvarez-Coello), these features represent genuine safety and convenience differentiation built on open, interoperable standards rather than proprietary systems.

### 3. Reduced Regulatory Compliance Cost

Several use cases have direct regulatory implications for vehicles sold in California:

- **Emissions compliance**: digital vehicle inspection certificates linked to registration renewal reduce manual smog check paper flows. OEMs building vehicles with embedded registration VC support could streamline the compliance lifecycle.
- **Commercial Driver's Licenses**: digital CDL credentials enable automated verification of driver qualifications, with implications for OEM telematics systems in commercial vehicles.

COVESA provides the standardization layer that prevents each OEM from implementing incompatible proprietary flows, which historically has been a significant cost driver for in-vehicle compliance features.

### 4. Early-Mover Access to California's Deployment Network

CA DMV has positioned this collaboration as multi-year ("next several months to years"). COVESA members who engage early gain:

- Influence over the vocabulary design before it hardens into deployment
- Access to CA DMV's broader agency network — CA Bureau of Automotive Repair, other state agencies, and potentially port authorities (Los Angeles handles large volumes of imported vehicles)
- A credible proof point for advocacy with other states and internationally (EU battery passport and vehicle data regulations are developing in parallel)

### 5. Alignment with SDV Architecture

For OEMs building Software Defined Vehicle (SDV) architectures, embedding credential issuance and verification into the vehicle's software stack is a natural extension of connectivity platforms. COVESA's VSS (Vehicle Signal Specification) and S2DM data models already define the signal layer; the vehicle credential vocabulary adds a trust and identity layer. Coordinating these through COVESA avoids fragmentation between the data model and the credential model.

---

## Benefits to Data Consumers: Fleet Operators, Insurers, and Others

### Fleet Operators

Fleet operators manage vehicles across multiple registration jurisdictions, insurance providers, and driver qualification requirements. The vehicle credential model addresses several high-friction operational areas:

**Streamlined Fleet Registration**  
Digitizing registration credentials and linking them directly to fleet management systems can reduce administrative overhead in multi-vehicle registration renewals. The CA DMV model envisions registration as a machine-readable VC, enabling automated compliance checking rather than manual document management.

**Commercial Driver's License Verification**  
Fleet operators must verify CDL status, endorsements, and restrictions continuously. A digital CDL as a VC, issued by the DMV and verifiable in real time, reduces the risk of employing drivers with lapsed or suspended licenses — a significant liability for fleet operators.

**Long-Haul Trucker Safety**  
The presentation includes long-haul trucker safety as an explicit use case. Digital HOS (Hours of Service) logs, CDL credentials, and vehicle inspection records as VCs create an integrated compliance and safety picture that fleet telematics providers (including Geotab) can consume through a common vocabulary.

**Smarter Accident Response for Fleets**  
Upon impact, a commercial vehicle automatically transmitting a Verifiable Presentation to E911 and the fleet operator — containing vehicle ID, cargo manifest, occupant data, and insurance — dramatically improves First Notice of Loss (FNOL) speed and accuracy. Fleet insurance premiums are significantly influenced by FNOL quality; this use case directly benefits fleet operators through faster claims resolution and lower premiums.

**Emissions Compliance Automation**  
California's emissions requirements (Smog Check, CARB regulations) are increasingly stringent for commercial fleets. Digital inspection certificates as VCs enable automated compliance monitoring and documentation, reducing audit burden.

### Insurance Companies

The vehicle credential model presents the insurance industry with its most significant structural opportunity:

**Real-Time Insurance Verification at Scale**  
California has one of the highest rates of uninsured motorists in the US — approximately **20% of drivers**, costing law-abiding residents more than **$1.1B/year in higher premiums** and costing Californians more than **$5.57B/year** in losses from uninsured accident costs. Digital vehicle registration coupled with a digital Proof of Insurance (POI) credential enables:

- Continuous coverage verification rather than point-in-time checks
- Automated detection of lapsed coverage with compelled compliance (suspended registration, suspended license)
- Significant reduction in the uninsured driver pool, benefiting the entire insured population through lower premiums

**First Notice of Loss Integration**  
The accident response use case directly integrates insurers into the emergency response data flow. Upon a crash, the vehicle transmits insurance credentials along with crash telemetry to E911. Insurers receive structured, verifiable FNOL data — vehicle identification, crash severity indicators, occupant data — enabling faster claims handling and reduced fraud. The presentation specifically notes that working with the insurance industry on what data to include in the POI credential is a collaborative design opportunity.

**Anti-Fraud for Vehicle Transactions**  
Vehicle sales fraud costs California residents roughly **$3.4B/year** (US total ~$30B/year), with 1 in 44 vehicle titles in circulation believed to be fraudulent. Dealer-related fraud losses exceeded **$200M in 2024**. A digital vehicle title with cryptographic verification of ownership and lien status — shareable directly from the vehicle to a buyer's device — eliminates the "title washing" and identity theft vectors that plague the current paper-based system. Insurers benefit through reduced fraudulent title-linked insurance claims.

### Other Data Consumers

**Law Enforcement**  
Safer traffic stops via vehicle-to-cruiser credential exchange reduce the physical danger of roadside document checks — currently responsible for **1 in 6 police officer deaths** and more than **$561M in costs over the past decade in California**. Digital badge credentials from officer to driver, combined with consent-based license and registration sharing, eliminate the need to approach an unknown vehicle before establishing identity and safety status.

**Municipalities and Parking Authorities**  
Disabled person parking placard fraud costs California an estimated **$210M annually** in lost meter revenue, with cities like San Francisco losing **$22M/year** from fraudulent placard use. Digital disabled parking placards as VCs, transmitted to smart parking sensors, enable automated verification without physical placard display — protecting municipal revenue and ensuring accessible parking availability for genuinely disabled residents.

**Port Authorities and Vehicle Import/Export**  
Early discussions with CA DMV flagged Los Angeles port vehicle shipments as a use case — digital title and registration credentials could streamline vehicle import compliance and reduce the fraud that occurs in the primary, secondary, and tertiary vehicle sales markets.

---

## Benefits to COVESA as a Standards Organization

### 1. Government Partnership Elevates Standards Credibility

A formal collaboration with a state government agency — one already in production deployment at scale — provides COVESA with:

- A real-world validation partner for the vehicle credential vocabulary
- A reference implementation with actual user adoption, rather than a purely theoretical standard
- Credibility when engaging other state DMVs, the AAMVA (American Association of Motor Vehicle Administrators), and equivalent bodies in Europe (ACEA members are already COVESA members)

The AAMVA question was explicitly raised in collaboration discussions: CA DMV engaged Ajay Gupta (Chief Digital Transformation Officer) who asked "why COVESA instead of AAMVA?" COVESA's answer is speed-to-execution, engaged technologists, and established OEM/supplier relationships. A CA DMV-validated credential vocabulary strengthens that answer considerably.

### 2. New Technical Working Group Focus

The vehicle credential vocabulary complements and extends existing COVESA work:

- **VSS / S2DM**: the signal and data model layer beneath credentials — crash telemetry, occupant data, and vehicle state signals are already within VSS scope
- **Commercial and Fleet Vehicle Expert Group**: fleet registration, CDL, and commercial vehicle use cases align directly with ongoing work
- **ACEA FMS / Heavy Duty**: the Commercial Driver's License and Long-Haul Trucker Safety use cases extend naturally into COVESA's heavy-duty vehicle work

Hosting the vehicle credential vocabulary at COVESA creates a natural home for a new expert group focused on verifiable vehicle and driver credentials, potentially attracting new COVESA members from the insurance and legal identity sectors.

### 3. Open Source Governance Leadership

The MPLv2 licensing negotiation — secured by CA DMV after engagement with California Department of Technology — establishes an important precedent: government-developed vehicle data standards can be open-sourced under terms that include patent grants and copyleft protections suitable for an industry consortium. COVESA's experience governing open-source projects (VSS is Apache 2.0, for example) makes it a natural steward.

### 4. W3C Liaison

The credential vocabulary is grounded in W3C Verifiable Credentials and related standards. COVESA already has engagement with W3C through members including Ted Guild. There is an informal liaison between COVESA's vehicle credential work and W3C's Verifiable Credentials Working Group would be a natural next step, potentially making COVESA the automotive sector's voice in that standards body.

**EV and Battery Passport Angles**  
Early email discussions specifically flagged EV-related credentials as a collaborative angle with CA DMV. Battery state-of-health and charging history as verifiable credentials are relevant both to insurers (for underwriting EVs) and to COVESA's existing battery passport work.

COVESA is collaborating with W3C, UNECE, EU Webuild and others on Digital Product Passports initially for EU Battery Passport but also other potential vehicle originated regulated data exchanges. 

[More on why Digital Product Passport collaboration may be important to COVESA.](https://docs.google.com/document/d/1Du_4R6TYQ0z-cgB3GomLOjIDMq4uROhg9Hnotor1WdQ/edit?tab=t.0#heading=h.iw5wf7uodttv)

The Digital Product Passport work will be able to bridge the [different driver's license](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-driver-license-global-status-2025.md) and other Decentralized Identifier (DID) platforms that are not W3C Verifiable Credentials based. 

### 5. California as a Global Regulatory Bellwether

California regulations routinely become de facto US national standards (emissions being the most famous example). A COVESA vehicle credential vocabulary validated by CA DMV positions COVESA to influence:

- How other US states implement digital vehicle credentials
- How the EU approaches vehicle identity in the context of the European Digital Identity (EUDI) wallet framework
- How ISO and SAE develop vehicle data credential standards

The collaboration with Carolynn Bernier (CEA, France) — who expressed strong interest in the CA DMV collaboration in early discussions — indicates European SDOs are already watching this work closely.

---

## Collaboration Structure and Next Steps

The collaboration proceeds in order of increasing effort:

1. **CA DMV contributes** the Vehicle Credential vocabulary to COVESA's GitHub organization (MPLv2 license confirmed; Paul Boyes confirmed the clone in May 2026)
2. **CA DMV engages** with COVESA to shape current and future work around digital credentials
3. **CA DMV participates** in setting vehicle standards that address their use cases through COVESA

Immediate actions to advance the collaboration:
- Finalize onboarding of the repository into COVESA's GitHub organization
- Establish a COVESA expert group or task force for vehicle and driver credentials
- Develop COVESA member briefing materials for the vehicle credential use cases (the "2026 COVESA Proposal for Verifiable Vehicle Credentials Project" document circulated by Paul Boyes is a starting point)
- Explore liaison formalization with W3C Verifiable Credentials WG and coordination with AAMVA

---

## Summary of Quantified Impact (California)

| Use Case | Annual Cost / Problem Scale |
|---|---|
| Vehicle Sales Fraud | $3.4B/year lost by CA residents |
| Uninsured Vehicle Costs | $5.57B/year (lost wages, medical, property) |
| Higher Premiums from Uninsured Drivers | $1.1B/year paid by insured residents |
| Traffic Stop Injuries/Deaths | $561M over past decade |
| Disabled Parking Placard Fraud | $210M/year statewide |
| San Francisco Parking Fraud Alone | $22M/year |

Total well-documented addressable problem scope in California alone exceeds **$9 billion annually**, with US-wide vehicle fraud estimated at ~$30B/year.

---

## Key Contacts

| Name | Role | Organization |
|---|---|---|
| Manu Sporny / Manushantha Sporny | Digital Credentials Lead | CA DMV / Digital Bazaar |
| Ajay Gupta | Chief Digital Transformation Officer | CA DMV |
| Navneet Grewal | IT Specialist III / Product Manager, Digital Transformation | CA DMV |
| Wesley Smith | DMV Digital Programs | CA DMV |
| Paul Boyes | Executive Director | COVESA |
| Daniel Alvarez-Coello | Vehicle Credentials Project Lead | BMW Group / COVESA |
| Chaitanya Podalakuru | Standards/Digital Programs | Ford Motor Company |
| Ted Guild | Commercial Vehicle Expert Group / W3C  | Geotab / COVESA |

---

*This report is based on the COVESA Vehicle Credentials Use Cases for California (2026) presentation and correspondence from the COVESA–CA DMV collaboration thread (December 2025 – July 2026). The GitHub repository for the Vehicle Credentials Vocabulary is: [https://github.com/covesa/vehicle-credentials-vocabulary](https://github.com/covesa/vehicle-credentials-vocabulary)*
