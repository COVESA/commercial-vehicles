# Why Motor Vehicle Agencies Should Adopt COVESA Verifiable Vehicle Credentials: The Business Case

**Date:** September 2026
**Author:** Ted Guild, Geotab / COVESA Commercial and Fleet Vehicle Group
**Audience:** Departments of Motor Vehicles, ministries of transportation (e.g. Ontario MTO), registration and roadworthiness authorities, and their associations (AAMVA, CCMTA)

> **Disclaimer.** The verifiable credential (VC) work described here, including the COVESA Verifiable Vehicle Credentials (VVC) vocabulary and the use cases in this report, includes ideas contributed by several parties: COVESA members, vendors, insurers and standards participants. It does **not** indicate intent, commitment or endorsement by the California DMV, or by any other state, provincial or regional motor vehicle agency or ministry with which this work is being discussed. Use cases are presented as possibilities for any jurisdiction, not as any agency's plans.

---

## Executive Summary

Motor vehicle agencies issue the documents that the rest of the road economy depends on: vehicle titles, registrations, driver's licences, permits, placards, and dealer and inspection-station licences. Almost all of them are still paper, plastic or PDF. Every party that relies on them has to check them by eye, by phone or through a bespoke database lookup: insurers, lenders, dealers, buyers, police, parking operators, rental companies, repair shops. That is slow and costly, and it makes forgery, title washing and identity fraud easy.

**W3C Verifiable Credentials** turn those documents into digitally signed statements. Anyone can verify one instantly, even offline, without calling the agency. The agency can revoke it the moment its status changes. The **COVESA [Verifiable Vehicle Credentials (VVC) vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/)** defines the shared, open meaning of the vehicle credentials: title, registration and proof of insurance today, with inspection and incident credentials proposed. Using the same vocabulary, any agency, insurer, OEM, fleet or wallet can issue and read them.

The VVC work is a **collaboration between the California DMV and COVESA**. The vocabulary was contributed to COVESA, is licensed MPL-2.0, and is developed openly at [github.com/COVESA/vehicle-credentials-vocabulary](https://github.com/COVESA/vehicle-credentials-vocabulary). Because it is open, any jurisdiction can adopt it, extend it and help shape it.

Adopting VVC lets an agency:

1. **Cut fraud** in title, lien, odometer and registration records. A signed credential cannot be altered, and a revoked one fails verification instantly.
2. **Lower its operating cost.** Third parties verify credentials themselves instead of calling the agency, querying its systems or visiting a counter. Paper, printing, mailing and manual lookups fall.
3. **Close the uninsured-vehicle gap** by linking a Proof of Insurance credential to registration, so coverage can be checked continuously rather than once a year.
4. **Make roadside stops safer and faster** with consented, instantly verifiable exchange of licence, registration and insurance, including between the vehicle and a patrol car.
5. **Protect residents' privacy and reduce breach risk.** Verifiers receive a proof, not a scan, so there is no database of copied documents to steal.
6. **Interoperate with neighbours and industry** through one open vocabulary shared with other jurisdictions, insurers, OEMs and fleets, instead of a proprietary format per vendor.

This report is one of a set of COVESA vehicle credentials reports that remain current and should be read together:

- [Business case: Verifiable Credentials for Automotive Insurance](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-automotive-insurance-business-case.md) covers Proof of Insurance, claims, and privacy and breach risk.
- [Vehicle Inspection Credential: data requirements](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vehicle-inspection-credential-data-requirements.md) covers the proposed inspection credential across US, Canadian, EU and Asian regimes.
- [Streamlining Connected Vehicle Incident Reporting to Insurers (FNOL)](https://github.com/COVESA/commercial-vehicles/blob/main/reports/connected-vehicle-fnol-vc-standards.md) covers the POI-to-FNOL credential chain and crash reporting.
- [AOSP VC wallet use cases and standards](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-vc-wallet-use-cases-standards.md) and the [AOSP open-source wallets comparison](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-open-source-wallets-comparison.md) cover holding and presenting credentials from the vehicle itself.

---

## 1. What VVC Is

| Property | What it means for the agency |
|---|---|
| **Built on W3C VC 2.0** | International standard for signed, machine-verifiable statements. Works with OpenID4VCI/VP issuance and presentation, selective disclosure and Bitstring Status List revocation. Complements ISO 18013-5 mobile driver's licences and the W3C CCG [Verifiable Driver's License vocabulary](https://w3c-ccg.github.io/vdl-vocab/). |
| **Vehicle credentials defined** | `VehicleTitleCredential` (owner, lienholder, lien release, odometer reading, VIN, make, model, body and fuel type, weight, axles), `VehicleRegistrationCredential` (plate, registering organisation, validity) and `ProofOfInsuranceCredential` / `VehicleInsuranceCredential` (insurer, policy, coverage, validity). See the [published vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/). |
| **Open and royalty-free** | MPL-2.0 licence, public repository, public review. The agency can reference it in rules and procurement without licensing a proprietary schema. |
| **Vendor-neutral, industry-backed** | Hosted by COVESA, whose members include vehicle manufacturers, suppliers, telematics, insurance-adjacent and cloud companies. They are the parties that will build wallets, vehicles and verifiers around these credentials. |
| **Designed to live in the vehicle too** | Credentials can be held in a phone wallet **or in the vehicle's own wallet** (e.g. an Android Automotive head unit), so the vehicle can present its own registration and insurance. See the [AOSP vehicle wallet report](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-vc-wallet-use-cases-standards.md). |
| **Linked credentials** | Registration references title; POI references registration; FNOL and incident reports reference POI. Each party verifies only the link it needs. The VIN lives in the registration credential, not everywhere. |
| **Linked data, ready for software and AI** | Based on RDF / JSON-LD, so every term has a precise, published meaning that agency systems, analytics and AI tools can process directly. |

---

## 2. Business Cases

### 2.1 Vehicle Title, Liens and Ownership Transfer

**Problem.** Paper titles are forged, altered and "washed". A salvage or flood brand disappears when a vehicle is re-titled in another jurisdiction. Hidden liens and forged lien releases cost buyers and lenders. Odometer disclosures rely on what the seller writes down; NHTSA estimates that more than 450,000 vehicles are sold each year in the US with false odometer readings, costing buyers more than US$1 billion a year ([NHTSA](https://www.nhtsa.gov/vehicle-safety/odometer-fraud)).

**With VVC:**

- A `VehicleTitleCredential` signed by the agency proves ownership, brand and lien status. Any alteration breaks the signature, and a superseded title is revoked.
- **Lien release** is a signed update from the lender, not a mailed letter, extending electronic lien and title (ELT) programmes to the buyer and the next jurisdiction.
- **Private sales** become safe: the seller presents the title (from a phone or directly from the vehicle), and the buyer verifies ownership, liens and the recorded odometer reading on the spot before paying.
- **Dealers, lenders, auctions and ports** verify title status instantly, for new sales, trade-ins, financing, salvage auctions and imports and exports.
- **Cross-jurisdiction transfer:** a receiving agency verifies the brand and lien status signed by the sending agency, instead of relying on a paper title and a database query.

### 2.2 Registration

**Problem.** Registration status is checked through stickers, paper cards and per-agency database queries, and fleets renew hundreds or thousands of vehicles through manual processes.

**With VVC:**

- A `VehicleRegistrationCredential` is always current: renewal updates it, and suspension or expiry is reflected immediately through revocation status.
- **Law enforcement, parking and toll operators, insurers and rental companies** verify it without a bespoke interface to the agency.
- **Fleets** receive registration credentials in machine-readable form for automated compliance tracking. For commercial carriers, apportioned (IRP) cab cards and permits follow the same pattern.
- **The vehicle holds its own registration**, and can present it at a roadside stop, a border, a parking facility or a service centre.

### 2.3 Proof of Insurance and the Uninsured-Vehicle Gap

**Problem.** Uninsured vehicles impose large costs on insured drivers and crash victims. Agencies enforce insurance through periodic reporting, database matching and paper cards that may already be out of date.

**With VVC:**

- The insurer issues a `ProofOfInsuranceCredential` that references the vehicle's registration credential. The agency, police and other drivers can verify coverage **at any moment**, and a cancelled policy is revoked immediately.
- **Continuous verification** replaces point-in-time checks at renewal. A lapse can prompt a notice to the owner, even a warning in the vehicle, before enforcement follows under the jurisdiction's own rules.
- It complements existing online insurance-verification models (IICMVA) and uses the same credential insurers need for claims.
- **Status:** POI is being discussed with one or more states or provinces, but there is no public confirmation of adoption at this point. See the [insurance business case](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-automotive-insurance-business-case.md).

### 2.4 Driver's Licences and Commercial Licensing

**Problem.** Physical licences are scanned and photocopied by every business that checks them, and commercial driver qualifications (class, endorsements, restrictions, medical status) must be re-verified continuously by employers and enforcement.

**With VVC alongside mobile driver's licences:**

- The agency's mDL or VC driver's licence (21 US states plus Puerto Rico now issue mDLs; see [global status](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-driver-license-global-status-2025.md)) works in the same wallets and flows as the vehicle credentials. One trust framework serves both.
- **Selective disclosure** proves "licensed for this class", "over 25" or "valid" without handing over address, date of birth or licence number.
- **Commercial driver's licence** status and endorsements can be verified by fleets in real time, reducing the risk of drivers with lapsed or suspended licences.
- Adding medical-alert information to the driver's licence credential, for first responders, has been raised but is only in early discussion.

### 2.5 Inspection and Emissions

**Problem.** Inspection results are recorded on paper certificates and stickers, or in station databases that other parties cannot easily verify. The EU is moving to mandatory digital roadworthiness certificates that record odometer readings at every test ([COM(2025) 180](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2025%3A180%3AFIN)).

**With VVC:**

- A proposed `VehicleInspectionCredential`, issued by a licensed station and referencing the registration credential, gives agencies, buyers and insurers a verifiable, revocable inspection result in place of a sticker or paper certificate.
- A buyer or insurer checks the inspection result alongside the title and registration, in the same wallet and the same verification step.
- The same credential covers commercial pre-trip and periodic inspections (49 CFR 396.11/396.13; NSC Standard 13).
- Over time, the credential can optionally include readings taken from the vehicle itself, such as diagnostic codes or emissions readiness, described in COVESA's Vehicle Signal Specification (VSS). That opens a path from digital certificates today to vehicle-assisted inspections later.

See the [Vehicle Inspection Credential report](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vehicle-inspection-credential-data-requirements.md).

### 2.6 Safer Roadside Stops

**Problem.** Traffic stops and roadside checks are dangerous for officers and drivers, partly because identity and vehicle status can only be established by walking up to the vehicle. Commercial enforcement involves checking many separate documents.

**With VVC:**

- **Vehicle-to-officer exchange:** with the driver's consent, the vehicle or phone presents licence, registration and proof of insurance to the patrol vehicle before anyone approaches. An officer credential can prove the officer's identity to the driver. See the [AOSP vehicle wallet report](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-vc-wallet-use-cases-standards.md) for the in-vehicle presentation flows.
- **Commercial compliance bundle:** registration, apportioned credentials, insurance, CDL and the latest inspection are verified in one exchange, at the roadside or at a weigh station.
- **Fewer disputes:** every credential is signed and time-stamped, so there is less argument about what was shown and when.

### 2.7 Crash Reports and Incident Credentials

**Problem.** Police crash reports are compiled by hand at the scene and reach agency records and insurers days or weeks later. Theft reports, tow records and salvage decisions are separate documents that each party re-keys.

**With VVC:**

- **Police crash and theft reports as credentials:** signed by the reporting agency, bound to the registration credential, and shareable with the owner, the insurer and the titling agency. A theft report can flag the title and registration instantly; recovery clears the flag.
- **FNOL (first notice of loss):** an incident notice from the vehicle, phone or fleet platform presents the POI and registration credentials, so the insurer (and, with consent, the police or agency) knows immediately which vehicle, owner and policy are involved. It can also attach crash data from the vehicle, which may be described in VSS. See the [FNOL report](https://github.com/COVESA/commercial-vehicles/blob/main/reports/connected-vehicle-fnol-vc-standards.md).
- **Total loss and salvage:** the insurer's total-loss decision, as a credential, feeds directly into title branding, so salvage status cannot be washed.

### 2.8 Permits, Placards and Business Licences

The same pattern extends to other documents agencies issue:

- **Accessibility parking placards:** verifiable by parking sensors and enforcement, and revocable when no longer valid, which reduces misuse.
- **Special plates, oversize and overweight permits, temporary operating permits.**
- **Dealer, salvage-dealer, inspection-station and driving-school licences:** buyers and other parties can verify they are dealing with a licensed business, and every credential that business issues (a sale document, an inspection result) can be traced back to its licence.

### 2.9 Privacy and Breach Risk

Today every party that relies on a licence or vehicle document copies it, and those copies accumulate into targets. In September 2026 more than 153 million driver's licence scans taken from IDScan.net, an identity-verification vendor, were put up for sale on the dark web. With VCs the verifier receives a **cryptographic proof, not an image**, and only the attributes it needs. Residents are better protected, and so are the agency and the businesses that rely on its documents. See §2.8 of the [insurance business case](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-automotive-insurance-business-case.md).

---

## 3. Cross-Cutting Benefits

**Lower operating cost.** Every verification a third party does itself is one the agency does not handle: no phone call, counter visit, mailed document or custom data-sharing agreement per partner. Issuance and revocation replace re-printing and re-mailing.

**Streamlined workflows with adjacent industries.** Insurers, lenders, dealers, rental, repair, towing and salvage businesses, OEMs, fleets and law enforcement all accept the same credentials. One agency integration serves every partner.

**Interoperability and reciprocity.** An open, shared vocabulary means a title, registration or inspection credential issued in one jurisdiction can be verified in another. That simplifies transfers, imports and reciprocal enforcement, and fits the multi-jurisdiction role of AAMVA and CCMTA, as well as the EU's move to digital registration and roadworthiness documents.

**No lock-in.** Any conforming wallet, verifier or issuance platform works. The agency is not tied to one vendor's format.

**A seat at the table.** VVC is young. Inspection, incident and permit credentials are still being designed. Agencies that take part shape the credentials they will issue and rely on.

---

## 4. Status

| Item | Status (September 2026) |
|---|---|
| VVC vocabulary: title, registration | Published at [covesa.github.io/vehicle-credentials-vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/), MPL-2.0 |
| Proof of Insurance credential | Defined in VVC; being discussed with one or more jurisdictions; no public adoption announced |
| Inspection credential | Proposed; data requirements across US, Canada, EU, Japan, Korea, China and India documented; not yet in VVC |
| FNOL and incident credentials | FNOL profile proposed (`fnolEndpoint` on POI); S2DM theft model complete, accident and unsafe-driving models in progress |
| Mobile driver's licences | 21 US states plus Puerto Rico issue mDLs; W3C CCG VDL vocabulary available |
| Permits, placards, business licences | Candidate credentials; not yet defined in VVC |

---

## 5. What We Ask of Agencies

1. **Join the conversation.** Take part in COVESA's vehicle credentials work, directly or through AAMVA or CCMTA, and share your requirements and extensions.
2. **Pick one pilot.** Good starting points: a title credential with lien release for dealer or private sales, a registration credential for fleets, or accepting a Proof of Insurance credential linked to registration.
3. **Reference VVC in procurement.** When modernising title, registration or permit systems, require that credentials be issued in the open VVC vocabulary, so any wallet and any verifier can use them.
4. **Coordinate across borders** with neighbouring states and provinces, and with the EU digital registration and roadworthiness data sets, so one credential works everywhere.

---

## Links

- COVESA Verifiable Vehicle Credentials (VVC) vocabulary: <https://covesa.github.io/vehicle-credentials-vocabulary/> · [Proof of Insurance](https://covesa.github.io/vehicle-credentials-vocabulary/#ProofOfInsuranceCredential) · [repository](https://github.com/COVESA/vehicle-credentials-vocabulary)
- [Business case: Verifiable Credentials for Automotive Insurance](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-automotive-insurance-business-case.md)
- [FNOL report: Streamlining Connected Vehicle Incident Reporting to Insurers](https://github.com/COVESA/commercial-vehicles/blob/main/reports/connected-vehicle-fnol-vc-standards.md)
- [Vehicle Inspection Credential: data requirements](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vehicle-inspection-credential-data-requirements.md)
- [AOSP VC wallet use cases and standards](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-vc-wallet-use-cases-standards.md) · [AOSP open-source wallets comparison](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-open-source-wallets-comparison.md)
- [VC driver's licences: global status](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-driver-license-global-status-2025.md) · [W3C CCG Verifiable Driver's License vocabulary](https://w3c-ccg.github.io/vdl-vocab/)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) · [W3C Bitstring Status List](https://www.w3.org/TR/vc-bitstring-status-list/)
- [NHTSA: odometer fraud](https://www.nhtsa.gov/vehicle-safety/odometer-fraud) · [EU roadworthiness package, COM(2025) 180](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2025%3A180%3AFIN)
- [AAMVA](https://www.aamva.org/) · [CCMTA](https://www.ccmta.ca/) · [IICMVA](https://www.iicmva.com/)
