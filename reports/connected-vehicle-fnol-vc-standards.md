# Streamlining Connected Vehicle Incident Reporting to Insurers
## A Proof-of-Insurance Credential with an FNOL Endpoint: Scope, Workflow, and Standards Landscape

*Revised September 2026 (first draft May 2026)*

---
## Disclaimer: Work in progress. Contributions from GenAI may be inaccurate representations. This revision incorporates reviewer feedback and a fact-check pass; see the Revision Notes at the end for what changed.

## Executive Summary

First Notice of Loss (FNOL) from connected vehicles to insurers remains largely manual and, where automated, proprietary: every insurer–telematics pairing is a bespoke integration, and nothing at the scene of an incident says, in machine-readable and verifiable form, who insures the vehicle or where an electronic notice should be sent.

COVESA's [Vehicle Credentials Vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/) (VVC, `https://w3id.org/vvc`) now defines a `ProofOfInsuranceCredential`. This report proposes a small, bounded extension: an `fnolEndpoint` property and consent terms on that credential, plus a profile for how the vehicle packages and delivers an FNOL submission to it. The FNOL carries an accident report shaped by the crash data sets vehicles already produce for emergency services (APCO/NENA VEDS in North America, eCall MSD in Europe), together with a snapshot of COVESA VSS signals as evidence.

Three design principles follow from reviewer feedback and are stated up front:

1. **COVESA's role is narrow.** COVESA defines vehicle-side vocabulary and packaging. It does not define insurer claims formats (ACORD, CSIO, national standards), emergency data sets, wallet or transport protocols, or consent law. It reuses those and publishes mappings to them.
2. **Manual by default, automatic only for severe crashes.** Crash detection produces false positives. The default is therefore a consented, occupant-initiated submission. Automatic submission is limited to a severity gate (airbag deployment together with high peak g-force / rapid deceleration, and rollover or fire flags where available) under prior consent, for the case where the occupant may be incapacitated.
3. **Reuse existing conventions.** The accident report is not a new crash record; it is the VEDS/MSD field set the vehicle already computes. The insurer-side landing points are the existing ACORD Property & Casualty XML and NGDS claims-notification messages (not ACORD 810, which is a Life & Annuity message), the CSIO FNOL service, and national EU formats.

The remainder of this document sets out COVESA's scope (Section 1), the problem (Section 2), the proposed architecture and workflow including consent (Section 3), the existing standards by region (Section 4), the organisations to engage (Section 5), gaps (Section 6), and an engagement strategy (Section 7). A companion Google Slides explainer with workflow diagrams accompanies this report.

---

## 1. COVESA's Scope and Role

| COVESA defines | COVESA reuses (does not define) | COVESA maps between |
|---|---|---|
| `ProofOfInsuranceCredential` and related terms in the Vehicle Credentials Vocabulary (already in VVC v1.0) | Insurer claims messages: ACORD 2 and ACORD P&C XML / NGDS (US), CSIO FNOL (Canada), BiPRO 503 / GDV, EDICourtage, SIVI and other national formats (EU) | VSS signals → accident-report fields (VEDS / MSD) |
| `fnolEndpoint` — the insurer's FNOL intake address carried in the credential (proposed) | Emergency crash data sets: APCO/NENA VEDS (ANS 2.102.1-2022), eCall MSD (EN 15722) | Accident report → ACORD / CSIO / national claim-notification aggregates |
| Consent terms carried with the credential: prior consent scope and in-vehicle consent expression (proposed) | Credential and wallet stack: W3C VC 2.0, DIDs, OpenID4VCI / OpenID4VP, ISO/IEC 18013-5 / TS 18013-7, EUDI Wallet ARF | POI credential → existing proof-of-insurance conventions (US e-ID card, CA eSlip, EU certificate / Green Card) |
| FNOL submission profile: envelope, minimal-notice vs full-report payloads, acknowledgment, status (proposed) | Consent law and guidance: GDPR / EDPB, EU Data Act, US state privacy law | Consent expression → legal requirements per jurisdiction |
| VSS signal set for incident evidence; alignment with the S2DM incident model | Vehicle platform: AOSP / Android Automotive OS, driver-distraction rules | — |

Two consequences: no insurer is asked to change its intake format, and no change is proposed to eCall, AACN, or any emergency-services channel. The vehicle sends the insurer notice *in addition to*, and only *after*, the regulated emergency notification.

---

## 2. The Problem

- **Latency.** Human-reported FNOL typically arrives days after the incident. Automated eFNOL narrows this to minutes but requires insurer-specific integrations.
- **Fragmentation.** Every OEM and telematics eFNOL programme surveyed (GM/OnStar, Toyota–State Farm crash-data release, Ford/Honda/Hyundai via Verisk Data Exchange, LexisNexis Telematics Exchange, CCC, CMT, Agero, Stellantis Mobilisights + OCTO, Toyota–Aioi Nissay Dowa in Japan) uses a proprietary API. None references ACORD, VEDS, or a verifiable credential. This is the standardisation gap.
- **No machine-readable routing.** At the scene, the identity of the insurer and the address for an electronic notice are not verifiable or actionable. An insurance card, paper or app-displayed, cannot be acted on programmatically.
- **Emergency data goes only to emergency services.** eCall MSD and AACN/VEDS already carry the crash data an insurer needs, but by design terminate at the PSAP.
- **False positives.** Crash-detection triggers fire on pothole strikes, hard braking, minor contact and dropped devices. An automatic FNOL on every trigger would flood insurer intake and leave unwanted claim records against policyholders. Any design must therefore treat the occupant's confirmation as the normal path and reserve automatic submission for cases where the trigger evidence is strong and the occupant may be unable to respond.
- **Carrier-to-carrier, not vehicle-to-carrier.** RiskStream RAPID X (production since February 2026) addresses inter-carrier FNOL sharing after an insurer receives the notice; it does not address vehicle-originated submission.
- **Theft.** Theft reporting relies on manual owner notification. Connected vehicles that detect unauthorised movement could initiate a standardised notice, but no protocol exists.

---

## 3. Proposed Architecture and Workflow

### 3.1 Credential chain

```
VehicleRegistrationCredential   (VVC — registration authority; VIN, plate, make/model, owner)
        ▲  registrationCredential (reference)
ProofOfInsuranceCredential      (VVC — insurer; policy, coverage limits, jurisdiction validity,
                                 + fnolEndpoint, + consent terms   ← proposed)
        ▲  reference to POI credential id
FNOL Submission                 (signed by vehicle / holder; accident report, VSS snapshot,
                                 consent evidence)                 ← proposed profile
```

Static vehicle identity lives only in the registration credential; the POI and the FNOL reference it rather than restating VIN and plate.

**Already in VVC v1.0:** `ProofOfInsuranceCredential`, `VehicleInsuranceCredential`, `VehicleInsuranceInformation`, `CoverageLimit`, `coverageType`, `coverageLimitPerPerson` / `coverageLimitPerAccident`, `jurisdictionValidity`, `insurerCode`, `issuingBureau`, `naicNumber`, `minimumLegalCoverageConfirmed`, `policyNumber`, `policyStartDate` / `policyEndDate`, `insuranceProvider`, `policyHolder`, `namedInsured`, `insuredAddress`. The vocabulary states that `ProofOfInsuranceCredential` is equivalent to the US insurance ID card, Canadian pink slip, EU national certificate and the Green Card.

**Proposed additions (the COVESA work item):**

- `fnolEndpoint` (IRI) on `VehicleInsuranceInformation` / `ProofOfInsuranceCredential`: the insurer's FNOL intake for this policy.
- Consent terms, either as a `termsOfUse` profile on the credential or as a separate holder-issued consent credential referencing it, expressing (a) whether prior consent to automatic severe-crash notice has been given, (b) its scope (data elements, severity gate), and (c) the consent record per ISO/IEC TS 27560.
- `FirstNoticeOfLoss` submission type with references to the POI credential, an accident report, a VSS snapshot, and consent evidence.

Illustrative POI credential subject (context prefixes omitted):

```json
{
  "type": ["VerifiableCredential", "ProofOfInsuranceCredential"],
  "issuer": "did:web:insurer.example",
  "validFrom": "2026-01-01T00:00:00Z",
  "validUntil": "2027-01-01T00:00:00Z",
  "credentialStatus": { "type": "BitstringStatusListEntry", "...": "..." },
  "credentialSubject": {
    "type": "VehicleInsuranceInformation",
    "policyNumber": "POL-987654",
    "registrationCredential": "urn:uuid:…",
    "coverageLimit": [ { "coverageType": "BI", "coverageLimitPerPerson": "…" } ],
    "jurisdictionValidity": ["US-CA"],
    "insurerCode": "…", "naicNumber": "…",
    "fnolEndpoint": "https://claims.insurer.example/fnol",
    "fnolConsent": {
      "automaticNotice": "severeCrashOnly",
      "consentRecord": "urn:uuid:…  (ISO/IEC TS 27560 record)"
    }
  }
}
```

`credentialStatus` (W3C Bitstring Status List, Recommendation May 2025) handles mid-term cancellation. Endpoint discovery via the insurer's DID Document `service` entry remains a valid alternative to the embedded URI; both can coexist, with the embedded URI as the cached default.

### 3.2 Accident report: based on existing conventions

The FNOL's accident report reuses the field set the vehicle already produces for emergency services rather than defining a new crash record:

- **North America:** APCO/NENA ANS 2.102.1-2022, *Advanced Automatic Crash Notification (AACN) Vehicle Emergency Data Set (VEDS)*, schema 3.1 — XML/NIEM, roughly 80 elements (crash severity, delta-V, principal direction of force, rollover, airbag deployment, occupant count, location). Carried in NG9-1-1 as Additional Data; IETF RFC 8148 requires VEDS for next-generation vehicle-initiated emergency calls.
- **Europe:** eCall Minimum Set of Data, EN 15722:2020 — vehicle identification, position, direction, timestamp, propulsion type, passenger count, optional additional data. Next Generation eCall (CEN/TS 17184) is mandatory for new EU type approvals from 1 January 2026 and all new registrations from 1 January 2027.
- **Common core:** COVESA VSS signals as the evidence layer — for example `Vehicle.Cabin.Seat.Row1.DriverSide.Airbag.IsDeployed`, `Vehicle.Speed`, `Vehicle.Acceleration.Longitudinal`, `Vehicle.CurrentLocation.*`, `Vehicle.Chassis.Brake.IsDriverEmergencyBrakingDetected`; and, once released, the in-development `Vehicle.Safety` branch (`IsFire`, `IsSubmersed`, `Rollover`, added to VSS master in May 2026 for crash detection and emergency response). Note that VSS has no `Vehicle.Accident` branch; the May 2026 draft of this report was wrong on that point.

Context vocabularies for later enrichment (police report, circumstances): MMUCC 6th edition (NHTSA, 2024, with NEMSIS linkage keys) in the US, CADaS v3.8.1 in the EU, STATS19 in the UK, and the European Accident Statement (constat amiable / CEA), which is the de facto pan-European two-party accident data set but has no standardised machine-readable schema.

### 3.3 Consent and the false-positive problem

**Default: manual, consented submission.** Crash-detection false positives are common enough that automatic FNOL on every trigger is unacceptable to insurers (triage load) and to policyholders (unwanted claim records, potential premium effects). When an incident is detected and the occupant is responsive, the head unit or phone presents a one-tap choice — *Send notice now · Not now · Call insurer* — showing what will be sent and to whom (insurer name from the POI credential). The FNOL is a notice of a possible claim; it does not open or admit a claim.

**Exception: severe crash with prior consent.** The combination of airbag deployment, high peak g-force / rapid deceleration, and where available rollover or fire flags is the same trigger set AACN and eCall use to place an automatic emergency call, and has a correspondingly low false-positive rate. In that case the occupant may be incapacitated. If, and only if, the policyholder gave prior consent at policy onboarding, the vehicle sends a *minimal notice* (policy reference, time, location, severity indicators) automatically; the full report follows on later confirmation. Where no prior consent exists, the vehicle holds the report locally and notifies the owner's phone or fleet manager.

**Fleet variant.** For commercial fleets the policyholder is the operator, who gives the prior consent and typically receives the notice through the fleet management platform, which may act as submission agent.

**Consent evidence.** Consent travels with the FNOL as a record structured per ISO/IEC TS 27560:2023 (consent record information structure, derived from the Kantara Consent Receipt; a W3C DPV mapping exists), satisfying GDPR Article 7 demonstrability and the "separate affirmative consent" standard set by the 2025 FTC and California Privacy Protection Agency orders against GM/OnStar.

### 3.4 In-vehicle interaction: the AOSP head unit

Two holder configurations:

- **Head unit as holder (target).** A wallet on the Android Automotive OS head unit holds the POI credential (issued via OpenID4VCI at policy inception/renewal), with keys in the TEE / StrongBox. The FNOL agent builds the report from VSS signals, signs it, delivers it to `fnolEndpoint`, and stores the acknowledgment and consent receipt.
- **Phone as holder (baseline).** The occupant's phone wallet holds the POI credential; the head unit acts as verifier/relay using the Android Digital Credentials API (Credential Manager). This is the safe baseline because Google documents Credential Manager and the Digital Credentials API for phones, XR and Wear OS; availability on Android Automotive OS is not documented.

Constraints on the consent prompt: Android Automotive `CarUxRestrictions` and the Driver Distraction Guidelines prohibit text entry and limit interaction while driving, so the prompt is shown only when the vehicle is stopped or post-crash, uses large single-tap controls with a voice alternative, and times out to the prior-consent rule. AOSP has no automotive-specific eCall or crash-notification framework; emergency calling is generic Radio HAL. COVESA's AOSP App Framework group lists consent management for third-party data access in scope, and a separate COVESA In-Car Wallet (payments) project exists, but neither has an identity/VC-wallet or consent-receipt deliverable — a gap this work would fill. Open-source wallet candidates are assessed in the companion report *aosp-vc-wallet-use-cases-standards.md* (OWF Multipaz, EUDI reference wallet, Procivis One, Bifold, SpruceKit).

### 3.5 End-to-end workflow

1. **Crash detected** — VSS signals (airbag deployment, delta-V, rollover).
2. **Emergency notification** — eCall MSD (EU) or AACN/VEDS (NA) to the PSAP. Unchanged; always first.
3. **Head unit reads the POI credential** — `fnolEndpoint`, consent terms.
4. **Consent** — prompt if the occupant is responsive; otherwise apply the severity gate and prior-consent rule (Section 3.3).
5. **Build the FNOL** — accident report (same data set as step 2) + VSS snapshot + consent evidence, signed by the vehicle or holder key.
6. **Deliver** — HTTPS POST to `fnolEndpoint`, or an OpenID4VP presentation where the insurer runs a verifier.
7. **Verify** (insurer) — POI signature and status, vehicle/holder signature, consent evidence.
8. **Map and open** (insurer) — into ACORD P&C XML / NGDS, CSIO FNOL, or a national claim-notification message; acknowledgment with claim reference returned to the wallet.

Steps 3–6 are the COVESA-defined vehicle-side behaviour. Steps 7–8 use existing insurer-side standards.

### 3.6 Role of the telematics data collector

Fleet management providers, aftermarket device providers and OEM telematics back-ends may act as data aggregator, report constructor, co-signer attesting to device calibration and data integrity, and submission agent where the vehicle lacks connectivity. The collector does not hold the POI credential; it acts under authorisation from the holder.

### 3.7 Theft

Theft follows the same pattern with a `theft` incident type: detection of unauthorised movement or geofence breach, a signed notice to `fnolEndpoint` (and optionally a law-enforcement endpoint), with location updates as subsequent submissions. It aligns with COVESA's S2DM `VehicleTheftIncident` model. Theft is always owner- or fleet-confirmed; the severity-gate automatic path does not apply.

---

## 4. Existing Standards and Conventions, by Region

### 4.1 Insurance FNOL and proof-of-insurance conventions

**United States**

- **ACORD 2 — Automobile Loss Notice.** The standard US auto FNOL form (current edition 2016/10), personal and commercial auto.
- **ACORD Property & Casualty XML.** The electronic auto claims-notification messages are `ClaimsSvcRq` / `ClaimsSvcRs` wrapping `ClaimsNotificationAddRq` / `ClaimsNotificationAddRs`, with aggregates `ClaimsOccurrence`, `AutoLossInfo`, `ClaimsParty`, `ClaimsDriverInfo`, `ClaimsInjuredInfo`. Related: `ClaimsFNOLDownloadRq/Rs`, `ClaimStatusInqRq/Rs`, `ClaimsSubsequentRptSubmitRq/Rs`. AL3 is the older batch download format.
- **ACORD Next-Generation Digital Standards (NGDS).** JSON/YAML RESTful API standards covering Policy, Claims, Party, Product and Reinsurance; the object model was launched 28 August 2025 and is positioned for mobile, IoT, cloud and AI-driven transactions. NGDS Claims is the API-layer landing point for a vehicle-originated notice.
- **Correction.** *ACORD 810 "First Notice of Loss Submission" is a Life & Annuity claims transaction* (its factsheet describes DTCC use as a death notification). It does not apply to auto and has been removed from this report's recommendations.
- **RiskStream RAPID X** (The Institutes). Production launch 12 February 2026; accelerates carrier-to-carrier FNOL by an average of seven days; RiskStream estimates $62–173 million industry-wide savings with broad adoption (the earlier "$53M" figure could not be sourced). A "Ready for Guidewire" ClaimCenter accelerator dates from 2022. Scope is inter-carrier; RAPID X is the natural downstream recipient of vehicle-originated FNOL.
- **Proof of insurance.** Electronic insurance ID cards are accepted in all states. The IICMVA *Model User Guide for Implementing Online Insurance Verification* (v7.0) defines the DMV-to-insurer web-service verification pattern used by state programmes; a VC-based POI would complement or replace it.

**Canada**

- **CSIO** (Centre for Study of Insurance Operations). FNOL reusable service (XML, licensed from ACORD) and **CSIO JSON API Standards for FNOL** (published 2023; first carrier certified April 2025). **My Proof of Insurance / eSlip** (since 2018) delivers the pink slip to phone wallets and is accepted as legal proof in most provinces — but as a PDF, not a cryptographically verifiable credential.

**European Union and United Kingdom**

- **Motor Insurance Directive 2009/103/EC** as amended by Directive (EU) 2021/2118; Commission Implementing Regulation (EU) 2024/1855 standardises the claims-history statement, to be provided electronically — a second insurer-issued attestation that could be a VC.
- **Green Card** (Council of Bureaux): black-and-white printable since 2021; authorities must accept electronic (PDF) Green Cards from 1 January 2025.
- **Germany:** BiPRO Norm **503** (Schadenservice: claims notification and inquiry web services; not "500-series", which is master data) and the GDV Schadennetz record format for claims data exchange; eVB electronic confirmation of insurance at registration.
- **France:** EDICourtage 2.0 broker–insurer messages including claims; DARVA operates the inter-insurer exchange and **e-constat auto**, the official digital European Accident Statement (two vehicles, no injuries, France only).
- **Netherlands:** SIVI All Finance Standard with an explicit `claimStructure` and the AFD loss-classification code list — directly reusable as a target schema.
- **Italy:** ANIA SITA database; insurance disc dematerialised since October 2015, police verify by plate.
- **UK:** electronic certificates permitted since 2010; **MIB Navigate** replaced the Motor Insurance Database in 2025, askMID for post-accident insurer lookup; Polaris maintains UK code lists and personal-lines EDI (claims coverage limited).
- **Insurance Europe** supports driver-controlled sharing of vehicle data and cites faster claims handling; the Commission's Data Act vehicle-data Guidance (C/2025/5026, 12 September 2025) names insurers as eligible third-party recipients.
- **EUDI Wallet.** No insurance attestation was piloted in the first Large Scale Pilots; the second-wave APTITUDE pilot includes mobile vehicle registration certificates. The Attestation Rulebook catalogue is open, so a Proof-of-Insurance rulebook could be registered.

**Other regions**

- **Japan:** no industry FNOL data standard; proprietary programmes (Toyota–Aioi Nissay Dowa telematics damage service); D-Call Net is the AACN analogue; compulsory-insurance certificate storable as PDF on a phone since November 2024.
- **Australia:** CTP is registration-linked (no separate proof document); no motor FNOL API standard.
- **India:** insurance status in VAHAN / mParivahan / DigiLocker via IRDAI's Insurance Information Bureau.
- **Mexico:** AMIS "Pólizas Vigentes" portal used by states for digital verification.
- **Brazil:** Open Insurance (SUSEP) consented data-sharing APIs — not FNOL-specific but the closest consented insurer-API analogue.

### 4.2 Emergency crash data sets

- **APCO/NENA ANS 2.102.1-2022 AACN VEDS** (schema 3.1): see Section 3.2. PSAP-only by design; no insurer-notification clause.
- **eCall:** UN Regulation No. 144 (AECS) in force 19 July 2018; Regulation (EU) 2015/758 mandatory for new M1/N1 types since 31 March 2018; MSD EN 15722:2020; NG eCall (CEN/TS 17184, Delegated Regulation (EU) 2024/1180) for new types from 1 January 2026 and all new registrations from 1 January 2027, driven by 2G/3G switch-off. Data protection and insurer notification are out of scope of Regulation 144. The insurer notice proposed here is a parallel, consented channel and does not modify eCall.

### 4.3 Vehicle data standards (COVESA)

- **VSS**: signal taxonomy and the evidence layer of the FNOL (Section 3.2 for the correct airbag and safety signal paths).
- **S2DM**: GraphQL-based data model; the incident model (`VehicleTheftIncident` complete; `AccidentReport`, `UnsafeDriving` stubs) is the schema home for the accident report's structured content.
- **Vehicle Credentials Vocabulary (VVC) v1.0**: `ProofOfInsuranceCredential` and insurance terms (Section 3.1); no FNOL term yet.
- **Commercial & Fleet Vehicle Expert Group** and the data collection campaigns: the natural home for this work item.
- **AOSP App Framework Standardization** and **In-Car Wallet (payments)** projects: adjacent; no VC-wallet or consent deliverable yet.

### 4.4 Verifiable credentials and identity

- **W3C Verifiable Credentials 2.0 family** — Recommendations 15 May 2025: Data Model 2.0, Data Integrity 1.0, EdDSA/ECDSA cryptosuites, VC-JOSE-COSE, Controlled Identifiers, **Bitstring Status List 1.0** (revocation / mid-term cancellation).
- **W3C DIDs 1.0** — insurer DID with `service` entry as an alternative endpoint-discovery path.
- **OpenID4VP 1.0** (final 9 July 2025) and **OpenID4VCI 1.0** (final 16 September 2025) — issuance of the POI credential and presentation of the FNOL.
- **ISO/IEC 18013-5** (mDL, mdoc) and **ISO/IEC TS 18013-7:2025** (second edition, May 2025; adds Digital Credentials API retrieval). Note: 18013-7 is a Technical Specification; the 2024 first edition is withdrawn.
- **ISO/IEC 23220** series — generic mdoc building blocks enabling a non-mDL mdoc such as a proof-of-insurance doctype.
- **IETF SD-JWT** (RFC 9901) and SD-JWT VC (draft) — selective disclosure; **Token Status List** (draft).
- **W3C Digital Credentials API** — shipped in Chrome 141 and Safari 26 (September 2025); phone-side holder path for Section 3.4.
- **EUDI Wallet ARF** (v2.x) and the QEAA/EAA implementing regulations (July 2025).
- **OpenWallet Foundation Multipaz** — mdoc + SD-JWT VC SDK with OpenID4VP/VCI; 1.0 expected around end 2026.
- **DIF** Presentation Exchange; **Trust over IP** Trust Registry Query Protocol v2.0 (now a ToIP Approved Deliverable, not an Implementers Draft).
- **MOBI** VID vehicle-identity standards and Citopia — adjacent vehicle-DID work; no active insurance working group confirmed.
- **Vehicle key management:** ISO/SAE 21434, SAE J3201, IEEE 1609.2 — foundations for a vehicle signing key; no vehicle-identity *credential* standard exists.

### 4.5 Consent and privacy frameworks

- **GDPR** Articles 6/7; **EDPB Guidelines 01/2020 v2.0** (connected vehicles; insurers are addressees; ePrivacy Article 5(3) consent for terminal access).
- **EU Data Act** (Regulation (EU) 2023/2854), applicable from 12 September 2025; Articles 4–5 user rights to access and share connected-product data; vehicle-data Guidance C/2025/5026.
- **eIDAS 2.0** (Regulation (EU) 2024/1183, in force 20 May 2024): Member States to offer an EUDI Wallet by about December 2026; private relying parties subject to strong-authentication obligations "including in the areas of transport, energy, banking and financial services…" must accept the wallet about 36 months after the implementing acts (~December 2027). *Insurance is not named explicitly*; insurers are covered insofar as they are financial-services relying parties. The May 2026 draft overstated this.
- **US:** state privacy law (CCPA/CPRA); the CPPA connected-vehicle enforcement sweep and the January 2025 FTC order against GM/OnStar (separate affirmative consent for sharing geolocation and driving data) are the operative precedents.
- **ISO/IEC TS 27560:2023** consent record structure; **W3C DPV** vocabulary and its 27560 guide; IEEE 7012-2025 machine-readable privacy terms.
- **Android Automotive**: `CarUxRestrictions`, Driver Distraction Guidelines; NHTSA visual-manual distraction guidelines (voluntary). "Privacy Sandbox" is unrelated to in-vehicle consent and is not cited.
- **UNECE WP.29/GRVA**: data protection and vehicle data access are agenda items; no deliverable yet.

---

## 5. Organisations to Engage

| Organisation | Relevance | Engagement |
|---|---|---|
| **ACORD** | US P&C XML and NGDS claims messages | Mapping from the COVESA accident report to `ClaimsNotificationAddRq` / NGDS Claims; vehicle-originated notice profile |
| **CSIO** | Canadian FNOL XML/JSON, eSlip | Mapping to CSIO FNOL JSON; VC-based eSlip successor |
| **RiskStream Collaborative** | RAPID X inter-carrier FNOL | Vehicle-originated FNOL as upstream input |
| **BiPRO / GDV-DL, DARVA, SIVI** | German, French, Dutch claims exchanges | National mapping tables; e-constat interoperability |
| **Insurance Europe / Council of Bureaux** | EU motor insurance policy; Green Card | POI credential alignment with MID certificates and electronic Green Card |
| **APCO / NENA** | VEDS | Reuse of VEDS 3.1 as the NA accident-report shape |
| **CEN TC 278 (eCall)** | MSD, NG eCall | Reuse of MSD as the EU accident-report shape |
| **COVESA VVC editors; CV Expert Group; AOSP App Framework group** | Vocabulary, incident model, head-unit consent | Host the proposal, S2DM alignment, reference consent UX |
| **W3C VC WG / CCG** | VC 2.0, status lists | Extension vocabulary review |
| **OpenID Foundation DCP WG** | OpenID4VCI / VP | Issuance and presentation profile |
| **EUDI Wallet consortium / Commission** | ARF, attestation rulebooks | Register a Proof-of-Insurance rulebook |
| **OpenWallet Foundation** | Multipaz, wallet infrastructure | Head-unit wallet reference implementation |
| **IICMVA** | US online insurance verification | Coexistence of VC-based POI with DMV verification |
| **MOBI** | Vehicle identity (VID) | Vehicle DID alignment |
| **Trust over IP** | Governance, trust registries | Insurer issuer trust registry |
| **UNECE WP.29 / GRVA** | eCall regulation, data access | Inform; no change to Regulation 144 requested |

---

## 6. Standards Gaps

| Gap | Current state | What is needed | Owner |
|---|---|---|---|
| FNOL endpoint in the POI credential | VVC v1.0 has `ProofOfInsuranceCredential` but no endpoint term | `fnolEndpoint` property | COVESA VVC |
| Consent terms with the credential | No standard expression of prior consent to automatic notice | `termsOfUse` profile or consent credential referencing ISO/IEC TS 27560 | COVESA VVC + DPV CG |
| FNOL submission profile | None | Envelope, minimal-notice vs full-report payloads, acknowledgment, status | COVESA CV Expert Group |
| Accident report profile | VEDS and MSD exist for PSAPs; no insurer-facing reuse profile; no machine-readable CEA schema | VSS → VEDS/MSD field mapping; S2DM `AccidentReport` completion | COVESA + APCO/NENA + CEN |
| Insurer mapping tables | Each eFNOL programme proprietary | Informative mappings to ACORD P&C XML / NGDS, CSIO JSON, BiPRO 503, SIVI | COVESA with ACORD/CSIO liaison |
| Severity gate definition | Triggers defined per OEM/TSP | Reference gate on VSS signals (airbag, delta-V, rollover, fire) aligned with AACN/eCall trigger practice | COVESA VSS |
| Head-unit wallet and consent UX | Digital Credentials API not documented for AAOS; COVESA AOSP group has no wallet deliverable | Reference design and AAOS gap analysis | COVESA AOSP group |
| Vehicle signing identity | No vehicle-identity credential standard | Vehicle DID method or key-attestation profile | COVESA / MOBI / SAE |
| EUDI attestation | No insurance rulebook | Proof-of-Insurance attestation rulebook | Insurers + COVESA |
| Theft update stream | No standard for repeated post-theft submissions | Subsequent-report submission profile | COVESA |

---

## 7. Engagement Strategy

**Immediate (COVESA)**

1. Open the VVC proposal: `fnolEndpoint`, consent terms, `FirstNoticeOfLoss` submission type.
2. Draft the FNOL submission profile and the severity-gate reference on VSS signals; complete the S2DM `AccidentReport` specialisation aligned to VEDS 3.1 and EN 15722 fields.
3. Prototype on the COVESA AOSP track: head-unit (or phone) wallet holding a POI credential, crash trigger, consent prompt, signed FNOL to a mock endpoint.

**Standards bodies (6–18 months)**

4. ACORD: mapping to P&C XML `ClaimsNotificationAddRq` aggregates and NGDS Claims; discuss a vehicle-originated notice profile.
5. CSIO: mapping to the FNOL JSON API; VC-based eSlip successor.
6. BiPRO, DARVA, SIVI: national EU mappings; e-constat interoperability.
7. APCO/NENA and CEN TC 278: confirm reuse of VEDS and MSD field sets outside the PSAP channel is acceptable and correctly attributed.
8. OpenID Foundation and W3C CCG: review the issuance/presentation profile and the vocabulary extension.
9. EUDI Wallet: register a Proof-of-Insurance attestation rulebook; engage insurers for a second-wave pilot.

**Regulatory alignment**

10. Monitor eIDAS 2.0 implementing acts and the Data Act vehicle-data Guidance; ensure the consent record structure meets EDPB and FTC/CPPA expectations.
11. UNECE WP.29: inform GRVA of the parallel consented channel; request no change to Regulation 144.

---

## 8. Summary of Key Standards

| Standard / organisation | Layer | Relevance |
|---|---|---|
| [COVESA Vehicle Credentials Vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/) | Vocabulary | `ProofOfInsuranceCredential`; home of the proposed `fnolEndpoint` |
| [COVESA VSS](https://covesa.global/vehicle-signal-specification/) | Vehicle data | Evidence signals; severity gate |
| [W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/), [Bitstring Status List](https://www.w3.org/TR/vc-bitstring-status-list/) | Credential | POI and FNOL envelope; cancellation status |
| [W3C DID 1.0](https://www.w3.org/TR/did-1.0/) | Identity | Insurer and vehicle identifiers; alternative endpoint discovery |
| [OpenID4VCI 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html), [OpenID4VP 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) | Protocol | Issuance and presentation |
| [ISO/IEC TS 18013-7:2025](https://www.iso.org/standard/91154.html), ISO/IEC 23220 | Credential format | mdoc path; EU wallet alignment |
| [ACORD P&C XML](https://www.acord.org/standards-architecture/acord-data-standards/Property_Casualty_Data_Standards), [ACORD NGDS](https://www.acord.org/standards-architecture/acord-data-standards/next-generation-digital-standards) | Insurer intake (US) | `ClaimsNotificationAddRq`; NGDS Claims |
| [CSIO FNOL](https://csio.com/solutions-tools/data-standards/reusable-services-library) | Insurer intake (CA) | FNOL XML and JSON API |
| BiPRO 503, GDV, EDICourtage, SIVI | Insurer intake (EU) | National claim notices |
| [APCO/NENA ANS 2.102.1-2022 VEDS](https://www.apcointl.org/standards/2-102-1-2022-advanced-automatic-collision-notification-aacn-vehicle-emergency-data-set-veds/) | Crash data (NA) | Accident-report shape |
| EN 15722 eCall MSD; [UN Regulation 144](https://unece.org/transport/press/new-un-regulation-automatic-emergency-call-system-road-traffic-accidents-will) | Crash data (EU) | Accident-report shape; unchanged emergency channel |
| [RiskStream RAPID X](https://www.riskstream.org/rapidx) | Inter-carrier | Downstream recipient |
| [eIDAS 2.0 / EUDI Wallet](https://eur-lex.europa.eu/eli/reg/2024/1183/oj/eng) | Regulation / wallet | Attestation rulebook; acceptance timeline |
| [EU Data Act](https://digital-strategy.ec.europa.eu/en/policies/data-act) | Regulation | User-directed sharing of vehicle data |
| [ISO/IEC TS 27560:2023](https://www.iso.org/standard/80392.html), [W3C DPV](https://w3id.org/dpv/2.1) | Consent | Consent record carried with the FNOL |
| [Android Automotive driver distraction](https://source.android.com/docs/automotive/driver_distraction/guidelines), [Digital Credentials API](https://developer.chrome.com/blog/digital-credentials-api-shipped) | In-vehicle | Consent UX constraints; phone-as-holder path |

---

## References

**Insurance industry**
- [ACORD Data Standards](https://www.acord.org/standards-architecture/acord-data-standards) · [ACORD P&C Data Standards](https://www.acord.org/standards-architecture/acord-data-standards/Property_Casualty_Data_Standards) · [ACORD NGDS](https://www.acord.org/standards-architecture/acord-data-standards/next-generation-digital-standards) · [ACORD NGDS object model launch, 28 Aug 2025](https://www.acord.org/ACORD-about/acord-news/2025/08/28/acord-launches-new-asset-for-streamlining-digital-data-exchange-across-the-insurance-ecosystem)
- [ACORD 810 factsheet (Life & Annuity — cited to document the correction)](https://www.acord.org/docs/default-source/standards-la-factsheets/acord_la_claims810firstnotice_factsheet_v01.pdf)
- [ACORD P&C XML schema reference (ClaimsSvcRq, ClaimsNotificationAddRq)](https://schemas.liquid-technologies.com/accord/pcs/1.16.0/http___www_acord_org_standards_pc_surety_acord1_xml_.html)
- [RiskStream RAPID X](https://www.riskstream.org/rapidx) · [RAPID X launch, 12 Feb 2026](https://www.businesswire.com/news/home/20260212862888/en/The-Institutes-RiskStream-Collaborative-Launches-RAPID-X-With-Leading-Auto-Insurers)
- [CSIO Reusable Services Library](https://csio.com/solutions-tools/data-standards/reusable-services-library) · [CSIO FNOL JSON API certification, Apr 2025](https://csio.com/news/northbridge-insurance-achieves-csios-json-api-standards-certification-first-notice-loss) · [CSIO My Proof of Insurance](https://csio.com/solutions-tools/my-proof-of-insurance)
- [IICMVA publications](https://iicmva.com/publications/)
- [BiPRO norms brochure](https://bipro.net/wp-content/uploads/2021/06/Broschu%CC%88re_Normen-WebServices_A4_online_202106.pdf) · [GDV-DL Schaden-Service](https://www.gdv-dl.de/kompetenzen/services-fuer-alle-versicherungssparten/schaden-service)
- [EDICourtage](https://www.edicourtage.fr/) · [e-constat auto (France Assureurs)](https://www.franceassureurs.fr/lassurance-protege-finance-et-emploie/lassurance-protege/les-demarches-en-cas-de-sinistre/e-constat-auto-application-mobile-constat-amiable-assureurs/)
- [SIVI AFS claim structure](https://www.manula.com/manuals/sivi/sivi-all-finance-standard/1/en/topic/claim-structure)
- [Polaris standards](https://www.polaris.co.uk/products/standards/) · [MIB Navigate](https://navigate.mib.org.uk/) · [UK Electronic Communication of Certificates of Insurance Order 2010](https://www.legislation.gov.uk/uksi/2010/1117/made)
- [Insurance Europe — motor insurance](https://www.insuranceeurope.eu/priorities/20/motor-insurance)
- [Directive (EU) 2021/2118](https://eur-lex.europa.eu/eli/dir/2021/2118/oj/eng) · [Implementing Regulation (EU) 2024/1855 (claims-history statement)](https://eur-lex.europa.eu/eli/reg_impl/2024/1855/oj/eng)
- [Green Card goes electronic (IETL)](https://www.ietl.net/news-details/the-green-card-turns-white.html)
- [Toyota / State Farm crash-data sharing](https://insurify.com/car-insurance/news/state-farm-instant-crash-data-sharing/) · [Ford and Verisk](https://www.verisk.com/company/newsroom/ford-and-verisk-collaborate-to-offer-telematics-data-to-insurers/) · [Mobilisights and OCTO](https://www.media.stellantis.com/em-en/mobilisights/press/mobilisights-and-octo-join-forces-to-turn-stellantis-connected-vehicle-data-into-actionable-insights)

**Emergency and crash data**
- [APCO/NENA ANS 2.102.1-2022 AACN VEDS](https://www.apcointl.org/standards/2-102-1-2022-advanced-automatic-collision-notification-aacn-vehicle-emergency-data-set-veds/) · [RFC 8148 — NG vehicle-initiated emergency calls](https://www.rfc-editor.org/rfc/rfc8148.html)
- [UN Regulation No. 144 (AECS)](https://treaties.un.org/doc/Publication/MTDSG/Volume%20I/Chapter%20XI/XI-B-16-144.en.pdf) · [EU eCall move to NG eCall (Delegated Regulation 2024/1180)](https://www.interregs.com/articles/news/293/eu-ecall-regulations-updated-to-require-4g-5g-compliant-systems)
- [NHTSA MMUCC](https://www.nhtsa.gov/traffic-records/model-minimum-uniform-crash-criteria) · [CADaS glossary v3.8.1](https://road-safety.transport.ec.europa.eu/system/files/2023-09/CADaS%20Glossary_v%203_8_1.pdf) · [UK STATS19 review](https://www.gov.uk/government/publications/road-safety-statistics-stats19-review-update-and-future-development-roadmap/road-safety-data-and-statistics-stats19-review-update-and-future-plans)

**COVESA**
- [Vehicle Credentials Vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/) · [VVC repository](https://github.com/COVESA/vehicle-credentials-vocabulary)
- [VSS repository](https://github.com/COVESA/vehicle_signal_specification) · [VSS Safety branch (master)](https://github.com/COVESA/vehicle_signal_specification/tree/master/spec/Safety) · [VSS Seat.vspec (Airbag.IsDeployed)](https://github.com/COVESA/vehicle_signal_specification/blob/master/spec/Cabin/Seat.vspec)
- [COVESA AOSP App Framework](https://covesa.global/aosp-framework/) · [COVESA In-Car Wallet project](https://covesa.global/project/in-car-wallet-payments-orchestration/)
- Companion reports in this repository: `aosp-vc-wallet-use-cases-standards.md`, `aosp-open-source-wallets-comparison.md`

**Credentials and identity**
- [W3C VC 2.0 family Recommendations, 15 May 2025](https://www.w3.org/news/2025/the-verifiable-credentials-2-0-family-of-specifications-is-now-a-w3c-recommendation/) · [VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) · [Bitstring Status List 1.0](https://www.w3.org/TR/2025/REC-vc-bitstring-status-list-20250515/) · [DID 1.0](https://www.w3.org/TR/did-1.0/)
- [OpenID4VCI 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) · [OpenID4VP 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)
- [ISO/IEC TS 18013-7:2025](https://www.iso.org/standard/91154.html) · [ISO/IEC 23220-1](https://www.iso.org/standard/74910.html)
- [W3C Digital Credentials API](https://www.w3.org/TR/digital-credentials/) · [Chrome ships DC API](https://developer.chrome.com/blog/digital-credentials-api-shipped) · [Android Digital Credentials announcement](https://android-developers.googleblog.com/2025/04/announcing-android-support-of-digital-credentials.html)
- [EUDI Wallet ARF](https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/) · [Attestation rulebook catalogue](https://github.com/eu-digital-identity-wallet/eudi-doc-attestation-rulebooks-catalog) · [EUDI implementing regulations, Jul 2025](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/909706465/New+round+of+EU+Digital+Identity+Wallet+implementing+regulations+adopted)
- [OpenWallet Foundation Multipaz](https://github.com/openwallet-foundation/multipaz) · [DIF Presentation Exchange](https://identity.foundation/presentation-exchange/) · [ToIP Trust Registry Protocol (approved)](https://trustoverip.github.io/tswg-trust-registry-protocol/approved/) · [MOBI standards](https://dlt.mobi/standards/)

**Regulation, consent and privacy**
- [Regulation (EU) 2024/1183 (eIDAS 2.0)](https://eur-lex.europa.eu/eli/reg/2024/1183/oj/eng) · [EU Data Act](https://digital-strategy.ec.europa.eu/en/policies/data-act) · [Commission Guidance on vehicle data, C/2025/5026](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AC_202505026)
- [EDPB Guidelines 01/2020 on connected vehicles](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-012020-processing-personal-data-context_en)
- [ISO/IEC TS 27560:2023](https://www.iso.org/standard/80392.html) · [DPV consent record guide](https://w3c-cg.github.io/dpv/guides/consent-27560) · [W3C DPV 2.1](https://w3id.org/dpv/2.1)
- [CPPA connected-vehicle review](https://cppa.ca.gov/announcements/2023/20230731.html)
- [Android Automotive driver distraction guidelines](https://source.android.com/docs/automotive/driver_distraction/guidelines) · [CarUxRestrictions](https://developer.android.com/reference/android/car/drivingstate/CarUxRestrictions) · [AOSP emergency call](https://source.android.com/docs/core/connect/emergency-call)
- [UNECE GRVA agenda 2025](https://unece.org/sites/default/files/2024-11/ECE-TRANS-WP.29-GRVA-2025-01e_0.pdf)

---

## Revision Notes (September 2026)

Changes from the May 2026 draft, following reviewer feedback and a fact-check pass:

- **COVESA scope** stated in the executive summary and as Section 1; architecture moved ahead of the standards survey.
- **ACORD:** replaced ACORD 810 (Life & Annuity) with ACORD 2 and the P&C XML `ClaimsSvcRq` / `ClaimsNotificationAddRq` messages; added NGDS. Removed the unverified "IoT devices as virtual parties" claim.
- **Credential model** aligned with VVC v1.0 (`ProofOfInsuranceCredential`), `fnolEndpoint` terminology adopted throughout; static identity moved to the registration credential.
- **Accident report** now explicitly based on VEDS 3.1 (APCO/NENA ANS 2.102.1-2022) and eCall MSD (EN 15722) rather than an ad hoc schema; NG eCall dates added.
- **Consent** section added: manual-by-default because of false positives; severity-gated automatic notice under prior consent; ISO/IEC TS 27560 consent record; AOSP head-unit interaction and driver-distraction constraints; phone-as-holder baseline because Digital Credentials API support on Android Automotive OS is undocumented.
- **VSS:** removed the non-existent `Vehicle.Accident.AirbagDeployed`; cited `Vehicle.Cabin.Seat.Row{n}.{Side}.Airbag.IsDeployed` and the in-development `Vehicle.Safety` branch.
- **RAPID X:** launch date confirmed (12 Feb 2026); "$53M/year" replaced with RiskStream's $62–173M range; Guidewire accelerator dated 2022.
- **eIDAS 2.0:** insurance is not named explicitly; acceptance obligation applies via "financial services" ~36 months after implementing acts.
- **ISO 18013-7:** corrected to ISO/IEC TS 18013-7:2025. **OpenID4VCI/VP 1.0** final dates added. **ToIP TRQP** status updated to Approved Deliverable.
- **Regional coverage** added: Canada (CSIO JSON API, eSlip), EU (MID amendments, Green Card electronic acceptance, BiPRO 503, GDV, EDICourtage/DARVA, SIVI, ANIA, eVB), UK (MIB Navigate, Polaris), Japan, Australia, India, Mexico, Brazil; market eFNOL programmes surveyed and found proprietary.
- **Removed** the "Privacy Sandbox" and AAOS eCall HAL references (inaccurate); removed the EU Digital Product Passport section as out of scope.
