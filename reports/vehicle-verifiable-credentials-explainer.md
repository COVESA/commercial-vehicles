# Vehicle Verifiable Credentials, the Digital Driver's License and VSS: An Explainer

**COVESA Commercial and Fleet Vehicle Expert Group**
**Date:** October 2026
**Audience:** anyone new to this work: OEMs, suppliers, fleets, insurers, motor vehicle agencies, wallet and software developers

> **Please read first.** The work described here is being done in COVESA, an open industry alliance. It builds on a vocabulary and a set of use cases contributed by the **California Department of Motor Vehicles (CA DMV)**, to whom COVESA owes a great deal: the DMV has deployed W3C Verifiable Credentials in production at scale, open-sourced its work, and brought real agency requirements to the table. However, **nothing in this document should be read as a statement of CA DMV policy, plans or intent**. COVESA has extended the vocabulary and is exploring use cases of its own. What any agency, including CA DMV, chooses to issue, accept or require is for that agency alone to say. The same applies to every other jurisdiction mentioned.

---

## 1. The problem in one paragraph

A vehicle's data is only as useful as the trust around it. Who owns this vehicle, who insures it, when it was last inspected, and who is licensed to drive it are all answered today by paper, plastic cards, stickers, PDFs and one-off database lookups. Each party that relies on those documents checks them by eye or re-keys them, keeps a copy, and cannot tell a forgery from the real thing. Title washing, odometer fraud, uninsured driving and identity theft all live in that gap. So does a great deal of cost and delay for fleets, insurers, dealers, repairers and agencies.

## 2. What a Verifiable Credential is

A [W3C Verifiable Credential](https://www.w3.org/TR/vc-data-model-2.0/) (VC) is a set of claims about a subject, digitally signed by the party that makes them (the **issuer**), held by the party they are about (the **holder**), and checked by whoever needs them (the **verifier**). The W3C VC Data Model 2.0 became a full W3C Recommendation in May 2025.

What that buys in practice:

- **Instant verification.** The verifier checks the signature itself. No call to the issuer, no bespoke integration, and verification can work offline.
- **Tamper evidence.** Any change to the content breaks the signature.
- **Revocation.** The issuer can mark a credential invalid the moment its status changes, for example when a title transfers or a policy lapses, using the [Bitstring Status List](https://www.w3.org/TR/vc-bitstring-status-list/).
- **Selective disclosure.** The holder can prove one fact, such as "licensed for this vehicle class" or "insured today", without handing over everything else on the document.
- **Linked data.** Credentials use JSON-LD, so every term has a published, machine-readable meaning. Software and AI systems can process them without guessing.

A **digital wallet** holds credentials and presents them. It can be an app on a phone, or software in the vehicle itself. The exchange protocols are open: OpenID for Verifiable Credential Issuance and Presentation (OpenID4VCI / OpenID4VP), the W3C Digital Credentials API, and, for in-person use, ISO/IEC 18013-5.

## 3. Verifiable Vehicle Credentials (VVC)

The **[Verifiable Vehicle Credentials vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/)** (VVC, namespace `https://w3id.org/vvc`) defines the shared meaning of credentials about a vehicle. It was created by the State of California and contributed to COVESA in June 2026. It is licensed MPL-2.0 and developed in the open at [github.com/COVESA/vehicle-credentials-vocabulary](https://github.com/COVESA/vehicle-credentials-vocabulary). Anyone can use it, extend it and propose changes.

The vocabulary currently defines:

| Credential | Issued by | What it states |
|---|---|---|
| **Vehicle Title Credential** | Titling agency | Owner, lienholder and lien release, title brands, odometer reading at titling, VIN, make, model, body and fuel type, weight, axles, jurisdiction and title number |
| **Vehicle Registration Credential** | Registering agency | Licence plate, registering organisation, issue, start and expiration dates, fee class |
| **Proof of Insurance Credential** (extends Vehicle Insurance Credential) | Insurer | Policy, insurer and insurer codes, named insured, per-type coverage limits, jurisdiction validity, confirmation that minimum legal coverage is met |

The Proof of Insurance credential was added at COVESA with input from insurers and standards participants. Release candidates are published as versioned JSON-LD contexts (v1rc5 as of October 2026), with a changelog in the repository.

**Credentials should link to each other.** In the Expert Group's proposed design, Registration references Title, Proof of Insurance references Registration, and inspection results and incident reports reference the credentials above them. The VIN would live in one place, the Registration credential, rather than being copied into every document as the published vocabulary allows today. A verifier follows only the links it needs, and sees only what it needs.

### Proposed, not yet in the vocabulary

The Expert Group has documented requirements for, and is proposing, the following. None of them is adopted yet:

- **Vehicle Inspection Credential**, covering periodic regulatory inspection, routine self-inspection, service visits and the commercial pre-trip inspection ([data requirements report](vehicle-inspection-credential-data-requirements.md)).
- **First Notice of Loss (FNOL)**: an `fnolEndpoint` and consent terms on the Proof of Insurance credential, so a vehicle can send a signed incident report straight to the right insurer ([FNOL report](connected-vehicle-fnol-vc-standards.md)).
- **Incident credentials** (theft, crash, unsafe-driving reports) modelled in COVESA's S2DM data model.
- **Accessibility placards, permits and business licences** as further candidates.

## 4. The digital driver's license

The driver side is further along than the vehicle side. **Mobile driver's licences (mDLs)** based on ISO/IEC 18013-5 are issued in more than twenty US states, and California reported more than 3.5 million applications by mid-2026. The EU Digital Identity Wallet requires wallets to support both ISO mdoc and IETF SD-JWT VC formats, with W3C VC optional. The W3C Credentials Community Group's [Verifiable Driver's License vocabulary](https://w3c-ccg.github.io/vdl-vocab/) expresses the same licence attributes as a W3C VC, so a driver credential can sit alongside vehicle credentials in the same wallet and be verified in the same flow. The Expert Group tracks this in its [global status report](vc-driver-license-global-status-2025.md).

Why that matters for vehicles and fleets:

- **Driver plus vehicle, together.** A fleet, an insurer or an investigator can establish who was authorised to drive which vehicle, with which licence class and endorsements, at the time of an event.
- **Commercial driver's licences.** Class, endorsements (including hazardous materials), restrictions and medical status can be verified by a fleet continuously rather than at hiring, and checked per trip. The Expert Group's view is that **inbound verification** of a digital CDL by fleets and telematics systems comes first; issuance belongs to licensing agencies.
- **Transactions.** A digital licence presented together with a digital title at the point of sale closes the identity-theft and title-washing path.
- **Data is an asset and a liability.** Every licence a business scans and keeps is useful to that business and, from that moment, a liability it has to protect. In 2026 scans of more than 150 million driver's licences held by a single identity-verification vendor were offered for sale on the dark web. W3C's [press release on the breach](https://www.w3.org/press-releases/2026/data-breaches-identity-theft-and-revocation-a-real-world-case-study-on-why-w3c-is-developing-verifiable-credential-barcodes/) uses it as a case study for signed, revocable credentials. Selective disclosure mitigates much of that risk: a fleet or rental desk usually needs to know only that a person holds a valid licence for a given vehicle class, not their name, address, date of birth or licence number. The verifier receives a proof of the one fact it needs and keeps no personally identifiable information, so there is nothing to breach. The asset is still used; the liability largely goes away.

## 5. Adding VSS: where it becomes powerful

Credentials establish **who and what**: the owner, the insurer, the inspector, the driver. COVESA's **[Vehicle Signal Specification](https://covesa.global/vehicle-signal-specification/)** (VSS) establishes **how the vehicle is right now**: a standard catalogue of signals such as odometer, tire pressure, brake pad wear, lamp defects, diagnostic trouble codes, traction battery state of health, airbag deployment and crash pulse, each with a defined name, type and unit.

Put the two together and the vehicle can produce **signed evidence** that any party can trust and any software can read:

- The vehicle (or its telematics unit) assembles a **VSS snapshot**, a set of signal values with timestamps, and signs it.
- The snapshot becomes the evidence block inside a credential: an inspection result, an incident report, a resale condition record.
- Each value carries its **provenance**: reported by the vehicle, measured by an inspector, or estimated by a model.
- Because the signal names are standard, an insurer, agency or buyer evaluates the evidence the same way whatever the make of vehicle.

### Example: inspection, from periodic to ongoing

1. **Today's inspection, digital certificate.** The station performs the inspection as it does now and issues a Vehicle Inspection Credential referencing the Registration credential. The EU's 2025 Roadworthiness Package already proposes mandatory electronic certificates ([COM(2025) 180](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2025%3A180%3AFIN)).
2. **Vehicle-assisted inspection.** As the inspector cycles lights, horn, wipers and brakes, an application reads the matching VSS signals and pairs them with what the inspector measures. Inspections get faster and every one produces a paired record of vehicle self-report against ground truth.
3. **Continuous evidence.** Between inspections the vehicle maintains a rolling readiness view: tread depth estimates, brake wear trend, lamp faults, diagnostic codes, battery health. The next inspection is pre-populated.
4. **Online routine inspection.** For items a regulator chooses to accept from vehicle evidence, inspection becomes a signed submission linked to registration renewal, with physical inspection reserved for what remains uninstrumented and for audits.

The same credential serves the **commercial pre-trip inspection** (49 CFR 396.11 and 396.13 in the US, NSC Standard 13 in Canada).

**Automated vehicles.** Regulators are attaching inspection and monitoring duties to automated driving systems that no conventional inspection regime covers: approval of the driving software and its operating domain, periodic checks of sensors, calibration and software version, cybersecurity and software-update status, in-service monitoring and incident reporting by the operator, and a daily pre-trip check that no driver is present to perform. The Expert Group is documenting what the UN, the EU, the US, the UK and Asian regulators require of automated vehicles in operation, and how a signed inspection credential with vehicle-reported VSS evidence could carry those obligations, in a new section of the [inspection credential report](vehicle-inspection-credential-data-requirements.md#14-automated-vehicles-regulator-required-inspection-and-in-service-monitoring). This work is in progress. The Expert Group has drafted a [VSS overlay](../tmp/inspection-vss-extension/inspection.vspec) proposing the missing signals, starting with tire tread depth and the malfunction indicator lamp, validated against VSS 6.1.

### Example: first notice of loss

A crash is detected in VSS signals. The vehicle reads its own Proof of Insurance credential, finds the insurer's `fnolEndpoint`, and sends a signed accident report with a VSS snapshot. The report reuses the crash record the vehicle already builds for emergency services (eCall MSD, VEDS) and lands in the insurer's existing claims formats. Submission is manual by default and automatic only above a severity threshold with prior consent, so false positives never reach the insurer. See the [FNOL report](connected-vehicle-fnol-vc-standards.md).

### Example: resale beyond "excellent condition"

Condition grades today are subjective and self-declared. With credentials, a buyer, dealer or lender verifies the Title (ownership, liens, brands) instantly, and reads measured tread depth, brake wear, battery state of health and diagnostic history from signed inspection credentials that travel with the vehicle. The odometer is a signed reading at each inspection, not a number written on a form.

## 6. The range of use cases

| Use case | Credentials involved | Where VSS adds evidence |
|---|---|---|
| Title transfer, private sale, lien release | Title, Registration, driver's licence | Odometer at sale |
| Continuous proof of insurance, uninsured-vehicle gap | Proof of Insurance, Registration | Lapse warning in vehicle |
| Roadside stop: plate lookup from the patrol vehicle, verified before approach | Registration, Insurance, Title status, Inspection | None required |
| Periodic, pre-trip and ongoing inspection; driverless daily checks | Inspection, Registration | Lights, brakes, tires, diagnostics, battery |
| Emergency response and FNOL | Proof of Insurance, incident report | Crash signals, occupancy, airbag status |
| Theft, total loss and salvage branding | Incident, Title | Location and status signals under consent |
| Fleet onboarding, driver assignment, CDL and endorsement checks | Driver's licence, Registration | Hours-of-service and trip context |
| Bulk and automated fleet registration renewal | Registration, Title, Insurance | Odometer, inspection evidence |
| Resale and remarketing condition records | Title, Inspection | Measured wear and battery health |
| Maintenance-based insurance discount, by consent | Inspection, Insurance | "Tires above threshold, no active faults" and nothing else |
| EV battery passport and charging | Registration, battery credential | Battery state of health, [Battery Passport VSS mapping](BatteryPassport_VSS_Mapping.md) |

## 7. The vehicle as holder and signer

Most of these flows work with a phone wallet. Several work better, or only, when the **vehicle itself** holds and presents credentials: registration is vehicle-bound, insurance must be reachable when the phone is absent or damaged, an FNOL is triggered by sensors, and a driverless vehicle has no occupant with a phone. The Expert Group has proposed an open-source wallet layer for the COVESA Android Open Source Project SDK, with keys in the vehicle's secure hardware, and compared candidate open-source wallets. See the [AOSP wallet use cases](aosp-vc-wallet-use-cases-standards.md) and [wallet comparison](aosp-open-source-wallets-comparison.md).

## 8. What COVESA defines, and what it does not

COVESA defines the **vehicle-side vocabulary and evidence packaging**: VVC terms, the VSS signal sets for inspection and incident evidence, and how a snapshot is embedded in a credential. COVESA does **not** define insurer claims formats, emergency data sets, wallet protocols, consent law or any agency's business rules. It reuses those and publishes mappings to them. The aim is that no insurer, agency or wallet has to change its intake format to accept a COVESA credential.

## 9. Where this stands (October 2026)

| Item | Status |
|---|---|
| VVC vocabulary: Title, Registration, Proof of Insurance | Published, release candidate v1rc5, MPL-2.0 |
| Inspection credential | Requirements documented across US, Canada, EU and Asia; VSS overlay drafted; not yet in VVC |
| FNOL endpoint and consent terms | Proposed; builds on a first-responder crash report demonstrated by industry partners; in-vehicle prototype planned on the COVESA AOSP track |
| Incident credentials | Theft model complete in S2DM; crash and unsafe-driving in progress |
| In-vehicle wallet | Proposal before the COVESA AOSP App Framework group |
| Digital driver's licence | Live at scale as mDL; W3C VC form available; fleet inbound verification under discussion |
| Agency adoption | CA DMV issues mDLs and vehicle title credentials into its own wallet and publishes an open-source verifier ([OpenCred](https://www.dmv.ca.gov/portal/ca-dmv-wallet/mdl-for-business/)); outreach to other North American and international jurisdictions is under way. No agency has announced adoption of the COVESA extensions. |

## 10. How to take part

- Review and propose changes to the vocabulary at [github.com/COVESA/vehicle-credentials-vocabulary](https://github.com/COVESA/vehicle-credentials-vocabulary).
- Read the detailed reports in this repository: [motor vehicle agency business case](dmv-vvc-adoption-business-case.md), [automotive insurance business case](vc-automotive-insurance-business-case.md), [inspection credential requirements](vehicle-inspection-credential-data-requirements.md), [FNOL](connected-vehicle-fnol-vc-standards.md), [AOSP wallet](aosp-vc-wallet-use-cases-standards.md), [driver's licence global status](vc-driver-license-global-status-2025.md).
- Join the COVESA Commercial and Fleet Vehicle Expert Group, or bring a pilot: an insurer, a motor vehicle agency, an inspection body, a fleet or a head-unit wallet prototype.

## Acknowledgements

This work would not exist without the California DMV's digital transformation team, who built and open-sourced the original Vehicle Credentials Vocabulary, deployed verifiable credentials to millions of residents, and shared the agency use cases that shaped COVESA's thinking. Thanks also to the W3C Verifiable Credentials Working Group and Credentials Community Group, Digital Bazaar, and the COVESA members, insurers and standards participants who have contributed to the vocabulary, the reports and the prototypes. Responsibility for the content, and for any errors, rests with the COVESA Commercial and Fleet Vehicle Expert Group.

## Links

- VVC vocabulary: <https://covesa.github.io/vehicle-credentials-vocabulary/> · [repository](https://github.com/COVESA/vehicle-credentials-vocabulary)
- COVESA VSS: <https://covesa.global/vehicle-signal-specification/> · [GitHub](https://github.com/COVESA/vehicle_signal_specification)
- W3C VC Data Model 2.0: <https://www.w3.org/TR/vc-data-model-2.0/> · [Bitstring Status List](https://www.w3.org/TR/vc-bitstring-status-list/)
- W3C CCG Verifiable Driver's License vocabulary: <https://w3c-ccg.github.io/vdl-vocab/>
- CA DMV Wallet: [vehicle credentials](https://www.dmv.ca.gov/portal/ca-dmv-wallet/vehicles/) · [mDL for business and OpenCred](https://www.dmv.ca.gov/portal/ca-dmv-wallet/mdl-for-business/) · [verify DMV-issued credentials](https://www.dmv.ca.gov/portal/ca-dmv-wallet/verify-dmv-issued-credentials/)
- EU Roadworthiness Package: [COM(2025) 180](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2025%3A180%3AFIN)
