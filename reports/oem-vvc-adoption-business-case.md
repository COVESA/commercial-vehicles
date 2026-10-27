# Why Vehicle Manufacturers Should Adopt Verifiable Vehicle Credentials and the Digital Driver's License: The Business Case

**Date:** October 2026
**Author:** COVESA Commercial and Fleet Vehicle Expert Group
**Audience:** OEM product, connected-services, software platform, compliance and standards leads; Tier-1 suppliers of head units, telematics units and secure hardware

> **Disclaimer.** The verifiable credential (VC) work described here, including the COVESA Verifiable Vehicle Credentials (VVC) vocabulary and the use cases in this report, builds on a vocabulary and use cases contributed by the California DMV and on ideas from COVESA members, insurers, vendors and standards participants. It does **not** indicate intent, commitment or endorsement by the California DMV or any other motor vehicle agency. Use cases are presented as possibilities for any jurisdiction and any manufacturer, not as any party's plans. Companion reports: the [motor vehicle agency business case](dmv-vvc-adoption-business-case.md), the [automotive insurance business case](vc-automotive-insurance-business-case.md) and the [plain-language explainer](vehicle-verifiable-credentials-explainer.md).

---

## Executive Summary

The vehicle is the one party present at every event in its own life: sale, registration, insurance, inspection, crash, repair, resale. Today it is the only party with no way to prove anything about itself. Ownership, coverage, inspection status and the identity of the driver are established around the vehicle, on paper and in agency databases, and the manufacturer's connected-vehicle platform is a bystander.

**W3C Verifiable Credentials** change that. A credential is a digitally signed statement that anyone can verify in under a second, offline if needed, and that the issuer can revoke instantly. The **[COVESA Verifiable Vehicle Credentials (VVC) vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/)** gives vehicle title, registration and proof of insurance a shared, open, royalty-free meaning. Mobile driver's licences give the driver the same. **COVESA VSS** gives the vehicle's own data a standard form. Put together, the vehicle can **hold** credentials about itself, **verify** credentials presented to it, and **sign** its own data as evidence.

For a manufacturer that is:

1. **A new feature surface on hardware already in the vehicle.** Title and registration in the car and shareable to a buyer at a private sale, insurance-lapse warnings on the dash, a crash report that reaches the right insurer in minutes, inspections pre-populated by the vehicle, a signed condition record to support resale value. All of it on the head unit and secure element already fitted.
2. **One integration instead of dozens.** Every insurer, agency, inspection body, fleet platform and wallet that accepts the open vocabulary is reached through one open protocol stack, replacing bespoke, per-partner interfaces for proof of insurance, eFNOL, registration and compliance data.
3. **Regulatory readiness.** Electronic roadworthiness certificates, battery passports, the EU Data Act, EU Digital Identity Wallet acceptance obligations, Plug & Charge, and consent rules for driving data in North America all call for signed, portable, consent-bearing vehicle data. Credentials are the common answer.
4. **Fleet and commercial sales differentiation.** Fleets buy on compliance cost. Automated registration, verifiable pre-trip inspections, driver licence and endorsement checks, and driverless daily self-checks are purchase criteria the vehicle can meet out of the box.
5. **Lower liability and privacy exposure.** The vehicle presents a proof, not personal data. Consent travels with the credential. Nothing is scanned, copied or stored by the verifier.
6. **No lock-in and a seat at the table.** VVC is MPL-2.0, the same licence as VSS, hosted at COVESA and developed in the open. The inspection, incident, wallet and driver-credential profiles are still being designed. Manufacturers that engage now shape what they will later build to.

---

## 1. Why Now

- **The credentials exist and are in use at scale.** VVC publishes title, registration and Proof of Insurance credential types (release candidate v1rc5, October 2026). The California DMV issues mobile driver's licences and vehicle title credentials into its own wallet, with more than 3.5 million mDL applications by mid-2026, and publishes an [open-source verifier](https://github.com/stateofca/opencred). More than twenty US states issue mDLs; the EU Digital Identity Wallet requires wallets to support both the ISO mdoc and SD-JWT VC formats.
- **Acceptance obligations are arriving.** From December 2027 EU law requires banks, insurers and other regulated private services to accept the EU Digital Identity Wallet on request. In September 2026 FinCEN and the US bank regulators [confirmed](https://www.fincen.gov/system/files/2026-09/MDL-VDC-FAQs.pdf) that banks and credit unions, including vehicle lenders, may accept mDLs and other government-issued verifiable digital credentials for customer identification. Vehicle finance, insurance and rental will be verifying digital credentials; the vehicle should be able to present and verify them too.
- **Vehicle data regulation points the same way.** The EU Data Act applies to connected vehicles from September 2025. The EU Battery Regulation requires a battery passport for EV batteries placed on the market from February 2027. The 2025 EU Roadworthiness Package proposes mandatory electronic inspection certificates ([COM(2025) 180](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2025%3A180%3AFIN)). ISO 15118-20, the protocol behind Plug & Charge, becomes mandatory for EU charging points installed or renovated from January 2027 ([Delegated Regulation (EU) 2025/656](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202500656)). Each requires signed, portable vehicle data with clear provenance.
- **Consent is now the price of using driving data.** US federal and state enforcement actions in 2026 against a connected-vehicle data programme established that separate, affirmative consent is required before driving data is shared. A credential carries its own consent record and discloses only what is asked. A data feed does not.
- **The paper model failed publicly.** In 2026 more than 150 million driver's licence scans held by one identity-verification vendor were offered for sale. Every party that relies on photographing a licence or a card is now asking how to verify without collecting.

---

## 2. What the Vehicle Can Do With Credentials

| Role | What it means | Examples |
|---|---|---|
| **Holder** | The vehicle's wallet stores credentials about the vehicle and presents them on request, with the owner's consent | Registration and title presented to a buyer, a border post, a parking facility, a service centre; Proof of Insurance available when the phone is absent or damaged |
| **Verifier** | The vehicle checks credentials presented to it | Driver's licence at ignition or for car-sharing and rental hand-over; fleet driver assignment; technician or roadside-assistance credentials before granting access |
| **Signer** | The vehicle signs a snapshot of its own VSS signals as evidence inside a credential | Accident report to the insurer, inspection self-report, odometer at sale, battery state of health for resale or passport |
| **Issuer (optional, later)** | The manufacturer issues credentials it is authoritative for | Build and software configuration, recall completion, battery passport data, service history |

The holder and signer roles are what no phone can do. Registration is vehicle-bound, an FNOL is triggered by sensors, a driverless vehicle has no occupant with a phone, and a VSS snapshot must be signed by the vehicle for anyone to trust it. The Expert Group's [AOSP wallet report](aosp-vc-wallet-use-cases-standards.md) recommends starting with the verifier role, which is the simplest, then holding the small set of credentials that genuinely belong on the vehicle.

---

## 3. Business Cases

### 3.1 Owner-Facing Features: Sale, Registration, Insurance

**Problem.** The owner's relationship with the vehicle's paperwork runs through the glovebox and the agency website. The manufacturer's app and head unit play no part.

**With credentials:**

- **Private sale from the car.** The seller presents the title credential from the vehicle or phone; the buyer verifies ownership, liens, brands and a signed odometer reading on the spot. NHTSA estimates more than 450,000 US vehicles a year are sold with false odometer readings ([NHTSA](https://www.nhtsa.gov/vehicle-safety/odometer-fraud)).
- **Registration in the vehicle.** Renewal updates the credential; expiry or suspension shows on the dash. Where an agency accepts vehicle evidence, renewal can carry a signed odometer or inspection snapshot.
- **Insurance lapse warning.** The vehicle holds the Proof of Insurance credential and checks its revocation status, so a cancelled policy produces a warning before enforcement does.
- **Fewer support calls.** Ownership transfer, registration status and coverage questions are answered by the credential, not by the manufacturer's contact centre.

### 3.2 Crash Response and First Notice of Loss

**Problem.** Automated crash notification to insurers exists only as one-off integrations between one manufacturer or telematics provider and one insurer. Each is proprietary and reaches a fraction of the fleet.

**With credentials:** the vehicle detects a crash in VSS signals, reads its own Proof of Insurance credential, finds the insurer's proposed `fnolEndpoint`, and sends a signed accident report with a VSS snapshot. The report reuses the crash record the vehicle already builds for emergency services (eCall MSD in Europe, VEDS where automatic crash notification is offered in North America), lands in insurers' existing claims formats, and is manual by default with automatic submission only above a severity threshold under prior consent. **One implementation reaches every participating insurer.** The manufacturer's connected service becomes the channel for a claim that begins in minutes rather than days. See the [FNOL report](connected-vehicle-fnol-vc-standards.md).

### 3.3 Inspection, Emissions and Roadworthiness

**Problem.** Periodic inspection is a station visit the vehicle takes no part in, and several jurisdictions are abandoning it as costly and unproven, while the EU is making the certificate electronic.

**With credentials:** a `VehicleInspectionCredential` records the result and references the registration credential. The vehicle contributes a signed VSS snapshot (lights, brakes, tires, diagnostic codes, readiness monitors, battery health), paired with what the inspector measures. Over time, items a regulator chooses to accept from vehicle evidence move online, pre-populated by the vehicle. For the manufacturer that is a maintenance-engagement channel, a reason for owners to keep the vehicle connected, and a head start on electronic certificates. See the [inspection credential report](vehicle-inspection-credential-data-requirements.md) and the proposed [VSS inspection overlay](../tmp/inspection-vss-extension/inspection.vspec).

### 3.4 Fleet and Commercial Vehicle Sales

**Problem.** Fleets spend heavily on compliance administration: registration across jurisdictions, driver qualification files, pre-trip inspections, insurance evidence, hours-of-service. Each is a document process a vehicle could support but does not.

**With credentials:**

- **Bulk and automated registration** from machine-readable registration and title credentials, including apportioned credentials for carriers.
- **Pre-trip inspection as a credential** (49 CFR 396.11 and 396.13; NSC Standard 13) with the vehicle's self-report attached; for **driverless vehicles**, the daily walk-around no one is present to perform becomes a signed self-check a regulator or fleet can verify.
- **Driver licence and endorsement verification** at assignment and per trip, including commercial classes and hazardous-materials endorsements, by selective disclosure.
- **Fleet FNOL and incident credentials** that reach the fleet platform and insurer together.

These become line items in fleet procurement. A vehicle that produces them natively lowers the fleet's cost of ownership and the manufacturer wins the comparison.

### 3.5 Resale, Certified Pre-Owned and Remarketing

**Problem.** Condition grades are subjective and self-declared. Buyers discount for uncertainty, which lowers residual values and lease economics.

**With credentials:** title, liens and brands verify instantly; measured tread depth, brake wear, battery state of health, diagnostic history and service visits travel with the vehicle as signed inspection credentials; the odometer is a signed reading at each event. Battery condition mapped to VSS feeds the EU battery passport and EV resale ([Battery Passport VSS mapping](BatteryPassport_VSS_Mapping.md)). Higher, verifiable residuals benefit the captive finance arm, certified pre-owned programmes and the customer.

### 3.6 Driver Identity in the Vehicle

**Problem.** The vehicle does not know who is driving, so personalisation, access control, car-sharing, rental hand-over and fleet assignment rely on key fobs, PINs and app accounts.

**With a digital driver's licence verified by the vehicle:** licence class, validity and age can be confirmed at ignition or hand-over without the vehicle storing personal data; a rental or car-share can bind the trip to a verified driver; a fleet can enforce that only drivers with the right class and endorsements operate a given vehicle. The W3C [Verifiable Driver's License vocabulary](https://w3c-ccg.github.io/vdl-vocab/) gives the licence a VC form that works alongside VVC. See the [global status report](vc-driver-license-global-status-2025.md).

### 3.7 In-Vehicle Payments and Charging

Toll, parking, fuel and charging payments need the vehicle's identity bound to the transaction for fleet accounts, disputes and tax. ISO 15118-20 Plug & Charge is a vehicle-to-charger exchange with no phone involved. A vehicle identity credential under the payment layer gives COVESA's In-Vehicle Payments work a verifiable identity it currently lacks. See the [AOSP wallet report](aosp-vc-wallet-use-cases-standards.md).

### 3.8 Privacy, Consent and Liability

Every use above presents a proof rather than data. The verifier learns "insured", "licensed for this class", "tires above threshold", not the policy document, the licence image or the trip history. Consent scope is carried with the credential and can be revoked. For the manufacturer that is lower breach exposure, a defensible consent record under US and EU privacy enforcement, and a connected-services story customers can accept.

---

## 4. What It Takes

| Component | What is needed | Status |
|---|---|---|
| **VSS data path** | Signals available to applications on the head unit or telematics unit (for example through a Kuksa or VISS broker) | Available in current SDV architectures |
| **Keys and identity** | A vehicle key pair in the secure element or trusted execution environment; a decentralized identifier for the vehicle | Common in current head units |
| **Wallet library** | Credential storage, presentation and verification without dependence on a proprietary services stack | Proposed as an open-source layer in the COVESA AOSP SDK; candidate open-source wallets compared in the [wallet comparison](aosp-open-source-wallets-comparison.md) |
| **Protocols** | OpenID for Verifiable Credential Issuance and Presentation, W3C Digital Credentials API, ISO/IEC 18013-5 for proximity | Published and in production elsewhere |
| **Vocabulary** | VVC for vehicle credentials, W3C CCG vocabulary for the licence, VSS for evidence | Published; inspection, FNOL and incident profiles proposed |
| **Partners** | An issuing agency or insurer, an inspection body, a fleet | Pilots sought |

Everything in the table is open, royalty-free and available. No new hardware is required for the verifier and holder roles.

---

## 5. A Phased Path

1. **Verify.** Add a verifier library to the head unit: driver's licence at ignition or hand-over, technician and roadside credentials. Simplest step, immediate use, no issuance needed.
2. **Hold.** Store the vehicle-bound credentials: registration, title, Proof of Insurance. Surface status and lapse warnings. Present to a buyer, a parking facility, a border post.
3. **Sign.** Assemble and sign VSS snapshots as evidence: FNOL to the insurer's endpoint, inspection self-report, odometer at sale, battery state of health.
4. **Issue.** Where the manufacturer is authoritative, issue credentials of its own: software and build configuration, recall completion, battery passport, service history.

Each step stands on its own and is intended to justify the next.

---

## 6. Common Objections

- **"Our phone app already does this."** A phone cannot sign the vehicle's data, is absent or damaged in the events that matter most, and does not exist for a driverless vehicle. The phone remains the right holder for personal identity; the vehicle is the right holder for its own credentials and evidence.
- **"Agencies and insurers are not asking for it."** Agencies are issuing credentials now, insurers face acceptance obligations from 2027, and both will integrate with whoever shows up with a working, open implementation. The business cases for [agencies](dmv-vvc-adoption-business-case.md) and [insurers](vc-automotive-insurance-business-case.md) are in this repository.
- **"It is another proprietary programme."** VVC is MPL-2.0 at COVESA, the same licence as VSS. W3C, OpenID Foundation and ISO protocols are open. Any conforming wallet or verifier works.
- **"The standards are not finished."** Title, registration and Proof of Insurance are published. The inspection, FNOL and incident profiles are where a manufacturer's input is needed, and early participants shape them.

---

## 7. Status and What We Ask of Manufacturers

| Item | Status (October 2026) |
|---|---|
| VVC vocabulary: title, registration, Proof of Insurance | Published at [covesa.github.io/vehicle-credentials-vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/), release candidate v1rc5, MPL-2.0 |
| Inspection credential and VSS overlay | Requirements documented; overlay validated against VSS 6.1; not yet in VVC |
| FNOL endpoint and consent terms | Proposed; builds on a first-responder crash report demonstrated by industry partners; in-vehicle prototype planned on the COVESA AOSP track |
| Incident credentials | Theft model complete in S2DM; crash and unsafe-driving in progress |
| In-vehicle wallet layer | Proposal before the COVESA AOSP App Framework group |
| Driver's licence | mDL live at scale; W3C VC form available |

We ask manufacturers to:

1. **Join the Commercial and Fleet Vehicle Expert Group** and the AOSP App Framework discussion on the wallet layer, and bring requirements for inspection, FNOL and in-vehicle credential handling.
2. **Prototype the verifier and holder roles** on an existing head unit with registration and Proof of Insurance credentials, and a signed VSS snapshot.
3. **Pick one pilot** with a partner: an insurer for FNOL, an inspection body or agency for a vehicle-assisted inspection, or a fleet for pre-trip and driver verification.
4. **Reference VVC and VSS** in supplier requirements for head units, telematics units and secure hardware so that credential handling is designed in rather than retrofitted.

---

## Links

- COVESA Verifiable Vehicle Credentials (VVC) vocabulary: <https://covesa.github.io/vehicle-credentials-vocabulary/> · [repository](https://github.com/COVESA/vehicle-credentials-vocabulary)
- COVESA VSS: <https://covesa.global/vehicle-signal-specification/> · [GitHub](https://github.com/COVESA/vehicle_signal_specification)
- This repository: [explainer](vehicle-verifiable-credentials-explainer.md) · [motor vehicle agency business case](dmv-vvc-adoption-business-case.md) · [insurance business case](vc-automotive-insurance-business-case.md) · [FNOL report](connected-vehicle-fnol-vc-standards.md) · [inspection credential report](vehicle-inspection-credential-data-requirements.md) · [AOSP wallet use cases](aosp-vc-wallet-use-cases-standards.md) · [open-source wallets comparison](aosp-open-source-wallets-comparison.md) · [driver's licence global status](vc-driver-license-global-status-2025.md) · [Battery Passport VSS mapping](BatteryPassport_VSS_Mapping.md)
- W3C Verifiable Credentials Data Model 2.0: <https://www.w3.org/TR/vc-data-model-2.0/> · [Bitstring Status List](https://www.w3.org/TR/vc-bitstring-status-list/) · W3C CCG [Verifiable Driver's License vocabulary](https://w3c-ccg.github.io/vdl-vocab/)
- CA DMV Wallet: [vehicle credentials](https://www.dmv.ca.gov/portal/ca-dmv-wallet/vehicles/) · [mDL for business and OpenCred](https://www.dmv.ca.gov/portal/ca-dmv-wallet/mdl-for-business/)
- EU Roadworthiness Package: [COM(2025) 180](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2025%3A180%3AFIN) · AFIR: [Delegated Regulation (EU) 2025/656](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202500656) · [FinCEN FAQ on verifiable digital credentials](https://www.fincen.gov/system/files/2026-09/MDL-VDC-FAQs.pdf) · [NHTSA odometer fraud](https://www.nhtsa.gov/vehicle-safety/odometer-fraud)
