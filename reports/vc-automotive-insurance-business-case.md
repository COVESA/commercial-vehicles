# Verifiable Credentials for Automotive Insurance: The Business Case

*September 2026 · Ted Guild (Geotab, COVESA Commercial & Fleet Vehicles Expert Group)*

---
**Disclaimer:** Work in progress, and deliberately high level. Contributions from GenAI may be inaccurate. The detailed technical and standards analysis is in the linked companion reports.

## Executive Summary

US private passenger auto insurance is a [US$371 billion](https://collisionweek.com/2026/04/02/progressive-closes-gap-state-farm-top-u-s-auto-insurers-reshape-market-2025/) line that still runs on documents that are easy to forge and hard to check: paper or PDF insurance cards, photographed driver's licences, self-reported mileage, and claims filed by phone days after the event. One in seven US drivers is uninsured and [one in three is uninsured or underinsured](https://insurance-research.org/news/one-three-drivers-are-either-uninsured-or-underinsured-us-exposing-themselves-and-other). Fraud touches about [10% of property-casualty losses](https://insurancefraud.org/fraud-stats/). And every party that checks a document today keeps a copy, which is how a single vendor came to hold, and lose, [more than 153 million licence scans](https://krebsonsecurity.com/2026/09/fbi-probes-service-selling-153m-drivers-licenses/) this month.

W3C Verifiable Credentials (VCs) replace those documents with digitally signed statements that anyone can check in under a second, offline if necessary, without calling the issuer. COVESA's [Verifiable Vehicle Credentials (VVC) vocabulary](https://covesa.github.io/vehicle-credentials-vocabulary/) already defines vehicle title, vehicle registration and [Proof of Insurance](https://covesa.github.io/vehicle-credentials-vocabulary/#ProofOfInsuranceCredential) credentials. Combined with the mobile driver's licences (mDL) that 21 US states now issue, and with vehicle data described in [COVESA VSS](https://covesa.global/vehicle-signal-specification/), they give insurers six things:

1. **Instant, verifiable proof of insurance** at the roadside, the DMV, the rental counter and the crash scene.
2. **First Notice of Loss (FNOL) in minutes, not days,** routed to the right insurer automatically, followed by theft, police, repair and other claim reports that are also signed credentials.
3. **Less fraud:** claims bound to a genuine registration credential and a genuine driver's licence, carrying signed vehicle data as evidence.
4. **Privacy-preserving usage-based insurance (UBI):** policyholders prove how they drive without handing over raw location and trip data.
5. **Lower operating cost:** claims, underwriting and servicing run on structured, signed data that software and AI consume directly, with no re-keying and no phone calls to check a document. The same credentials streamline work with DMVs, law enforcement, lenders, dealers, rental, repair, towing, OEMs and fleets.
6. **Lower breach exposure:** verifiers receive a cryptographic proof instead of keeping a scan. Data an insurer or its vendor never holds cannot be stolen (§3.8).

Fraud reduction matters, but the larger gain is **streamlining the business**. Every credential is structured, signed data with defined meaning, built on the W3C linked-data model, so the same data works for people, conventional software and AI.

No public production use of W3C VCs in auto insurance exists yet. The same pattern is live or piloted next door: EU health insurance cards in the EU Digital Identity Wallet, US health-plan cards, and insurer-issued motor policies in India's DigiLocker. US insurers have run blockchain proof-of-insurance trials. §6 has the examples. The building blocks, the regulatory pull and a fresh reminder of the cost of the status quo are all in place; the first insurers to move will set the pattern the rest adopt.

## 1. Why Now

Four things changed in the past two years that make this practical rather than aspirational:

- **The credentials exist.** VVC v1.0 publishes registration, title and Proof of Insurance credential types. The California DMV is issuing registration credentials. 21 US states plus Puerto Rico issue TSA-accepted mDLs, and Canadian provinces and the EU are following.
- **Regulators are opening the door.** In September 2026 FinCEN and the US bank regulators [confirmed](https://www.fincen.gov/system/files/2026-09/MDL-VDC-FAQs.pdf) that banks and credit unions, including auto lenders, may accept mDLs and other government-issued verifiable digital credentials for customer identification. From 24 December 2027, EU law requires banks, insurers and other regulated private services to accept the EU Digital Identity Wallet on request.
- **Consent rules for vehicle data are now explicit.** The FTC's January 2026 order against a North American automaker's connected-vehicle service, and California's record CCPA settlement with the same automaker in May 2026, make separate, affirmative consent the price of using driving data. A credential that carries its own consent record fits that rule; a data-broker feed does not.
- **The paper model just failed at scale.** The IDScan.net breach (§3.8) showed what happens when the way to trust a licence is to photograph it. Insurers, rental companies and lenders are now asking how to verify without collecting.

## 2. The Credential Family

Each credential comes from the party that is authoritative for it. Credentials refer to each other rather than restating data, so the VIN lives only in the registration credential and the insurer never re-keys it.

| Credential | Issuer | What it proves | Status |
|---|---|---|---|
| Vehicle Registration | DMV / registration authority | This vehicle (VIN, plate) is registered, and to whom | In VVC v1.0; CA DMV programme |
| Vehicle Title | DMV | Ownership, liens, brand (e.g. salvage) | In VVC v1.0 |
| **Proof of Insurance (POI)** | Insurer | This vehicle is covered by this policy, these limits, these dates, in these jurisdictions | In VVC v1.0 (`ProofOfInsuranceCredential`) |
| Driver's licence (mDL / VC) | DMV | Identity and driving privileges of the person | ISO/IEC 18013-5 in production; W3C CCG [Verifiable Driver's License vocabulary](https://w3c-ccg.github.io/vdl-vocab/) |
| FNOL submission | Vehicle / policyholder | An incident occurred, with signed vehicle evidence | Proposed (`fnolEndpoint` on the POI, FNOL submission profile) |
| Other incident and claim reports (theft, police, repair, towing, total loss, etc.) | Vehicle, owner, police, repairer, other claim parties | The specific facts each party is authoritative for | Proposed; theft data model complete in COVESA S2DM |
| Vehicle inspection | Inspector, service shop, or the vehicle itself | Roadworthiness and maintenance state | Proposed |
| UBI policy and driving summary | Insurer / telematics provider | Consent scope; aggregate mileage or risk band | Proposed |

```
VehicleRegistrationCredential  (DMV)  ◄──── references ────┐
        ▲                                                  │
ProofOfInsuranceCredential     (insurer, + fnolEndpoint)   │
        ▲                                                  │
FNOL submission                (signed by vehicle / holder, evidence from VSS)
        │
        └── presented alongside the driver's licence credential (DMV)
```

## 3. Business Cases

### 3.1 Proof of Insurance

Today's insurance ID card, whether paper, PDF or app screenshot, can be edited in minutes, and checking it means a phone call or a state online-verification query. A POI credential is signed by the insurer, verifies in under a second, and carries revocation status, so a policy cancelled mid-term stops verifying.

The problem it addresses is large and growing. The Insurance Research Council found [15.4% of US motorists uninsured in 2023](https://insurance-research.org/news/one-three-drivers-are-either-uninsured-or-underinsured-us-exposing-themselves-and-other) and 33.4% uninsured or underinsured, up 10 points since 2017. Every insured driver pays for that through uninsured-motorist coverage.

- **Law enforcement and DMVs:** instant check at a traffic stop or registration renewal; complements the IICMVA online-verification model rather than replacing state systems.
- **Uninsured motorists:** a lapsed or fake card no longer passes a glance; states can enforce financial-responsibility laws at the roadside.
- **Third parties:** rental agencies, car-sharing, dealers, repair shops, parking and toll operators confirm coverage without integrating with each insurer.
- **Cross-border:** one credential carries jurisdiction validity (US state, Canadian province, EU Green Card equivalence) instead of separate paper documents.
- **At the crash scene:** the other driver verifies the policy and insurer on the spot, and the credential says where to send the claim.

**Adoption status.** POI credentials are under discussion with one or more states or provinces. No jurisdiction has publicly confirmed adoption yet.

### 3.2 First Notice of Loss

Human-reported FNOL typically arrives days after the incident. The automated eFNOL programmes that exist work, but each is a proprietary, one-off integration between one OEM or telematics provider and one insurer. A large US carrier's 2025 crash-detection service, for example, covers [1.5 million policyholders](https://www.autobodynews.com/news/progressives-real-time-crash-detection-could-accelerate-shop-intake-cycles) through one telematics partner; no other carrier, and no other data source, can plug into it.

The proposed `fnolEndpoint` property on the POI credential tells the vehicle, phone or fleet platform exactly where to send a signed notice for this policy, so one integration works with every participating insurer.

- **Shorter cycle time:** telematics-driven FNOL is already reported to cut the claim life cycle by [up to 60% for low-speed collisions and soft-tissue injuries](https://ims.tech/knowledge-hub/digital-transformation-claims-processing/) and reduce claim touchpoints by 30%. Earlier notice means earlier triage, towing, rental and repair scheduling, which lowers loss-adjustment expense and rental days.
- **Better first data:** the notice carries the crash data set the vehicle already computes for emergency services (APCO/NENA VEDS in North America, eCall MSD in Europe) plus signed VSS signals, instead of a recollection over the phone.
- **Controlled by the policyholder:** manual confirmation by default, because crash detection produces false positives. Automatic minimal notice applies only to severe crashes (airbag plus high deceleration, rollover or fire) and only with prior consent.
- **Fits existing insurer systems:** the notice maps to ACORD P&C XML / NGDS, CSIO FNOL and national EU formats. No insurer changes its intake.

Details: [Streamlining Connected Vehicle Incident Reporting to Insurers (FNOL report)](https://github.com/COVESA/commercial-vehicles/blob/main/reports/connected-vehicle-fnol-vc-standards.md).

### 3.3 Other Claims and Incident Reports as Credentials

The crash FNOL is only the first document in a claim. Every later report comes from a party that is authoritative for its own facts, and each can be issued as a VC that references the POI and registration credentials. The claim file becomes a chain of signed, independently verifiable documents rather than a folder of PDFs, photos and faxes.

| Report | Issued by | Insurer benefit |
|---|---|---|
| **Theft report** | Vehicle (unauthorised movement, geofence breach) confirmed by owner or fleet; later location updates as follow-on credentials | Earlier notice, verifiable location trail, faster recovery, and a record that the theft preceded any claimed damage |
| Police / law-enforcement report | Police agency | Report number, fault findings and citations verified at source, not re-keyed |
| Vandalism, glass, hail and weather damage | Vehicle (intrusion, glass-break, parked-impact signals) and owner; weather data provider | Signed time and place of loss; weather claims checked against event data |
| Towing and roadside assistance | Tow / roadside provider | Confirmed pickup time, location and destination; fewer disputed tow bills |
| Repair estimate and completed-repair record | Repair shop, appraiser | Tamper-evident estimate; completed-repair proof supports supplements and resale |
| Total loss and salvage | Insurer, then DMV title brand | Salvage status follows the vehicle and resists title washing |
| Rental / replacement vehicle | Rental company | Verified rental days and charges |
| Injury and medical bills | Medical provider | Provider-verified treatment; fewer inflated or fabricated bills |
| Unsafe-driving or near-miss event | Vehicle / fleet platform (with consent) | Fleet risk management and coaching evidence, kept separate from claims |

Because every document is signed and references the same policy and vehicle, inconsistencies surface automatically: a repair estimate for a vehicle reported stolen, or a claimed loss location that contradicts the vehicle's signed evidence. That supports both straight-through processing of clean claims and the fraud controls in §3.4.

Theft is the most mature case. COVESA's S2DM incident model defines a complete `VehicleTheftIncident`; the accident and unsafe-driving models are still stubs. Theft notices are always owner- or fleet-confirmed and never sent automatically on the severity gate (FNOL report §3.7). The head-unit wallet design treats theft as a vehicle-issued credential because no occupant may be present ([AOSP wallet report, UC-7](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-vc-wallet-use-cases-standards.md)).

### 3.4 Reducing Insurance Fraud

The Coalition Against Insurance Fraud estimates fraud costs US consumers [at least $308.6 billion a year](https://insurancefraud.org/fraud-stats/), of which about $45 billion is property-casualty and $7.4 billion is auto theft, and that fraud is present in about 10% of property-casualty losses. Much of auto fraud depends on unverifiable identity and unverifiable facts. A claim **signed with, or bound to, the registration credential and the driver's licence credential** closes several of those gaps:

| Fraud pattern | How signed credentials help |
|---|---|
| Fake or altered insurance card; claim against a lapsed policy | POI signature and revocation status checked at FNOL |
| Policy bought *after* the loss ("post-dating") | Credential validity dates plus a signed, time-stamped vehicle event show the event predates the policy |
| Ghost or phantom vehicles; VIN cloning | Claim must reference a DMV-signed registration credential; the VIN comes from the DMV, not the claimant |
| Claimant identity fraud; undisclosed or excluded drivers | Driver's licence credential bound to the submission shows who was driving and whether they were licensed |
| Staged crashes; exaggerated severity | Vehicle-signed VSS evidence (speed, deceleration, airbag state, location) contradicts implausible narratives |
| False theft claims ("owner give-ups") | Signed vehicle theft credential and location trail; normal key use at the claimed time of theft is visible |
| Salvage, title washing and odometer fraud | Title brand and odometer history carried in DMV and inspection credentials |
| Mileage misrepresentation at quote or renewal | Signed odometer / UBI summary replaces self-reported mileage |

Signing the claim with the holder's credentials also creates a **non-repudiable record**: the claimant cannot later deny what was submitted, and the insurer's SIU, subrogation counterparties, reinsurers and inter-carrier networks such as RiskStream RAPID X can verify the same artefact independently.

**Limits:** a credential proves who issued a statement and that it has not been altered. It does not prove the underlying event is true. Collusion between drivers, compromised device keys and manipulated sensors remain risks. Vehicle key protection (TEE/StrongBox, ISO/SAE 21434) and telematics co-signatures reduce them, and insurers' existing analytics still apply.

### 3.5 Streamlining the Business and Lowering Operating Cost

Most of the cost of insurance operations goes into collecting, re-keying, reconciling and checking documents. Signed, structured credentials remove that work:

- **Straight-through processing:** a claim whose policy, vehicle, driver and evidence all verify cryptographically can be triaged, reserved and routed without manual review. Adjusters' time goes to the claims that need judgement.
- **No re-keying:** VIN, plate, policy number, coverage limits and licence details arrive as signed data from their authoritative source. No transcription errors, no call-backs.
- **Verification without integration:** checking a credential needs the issuer's public key, not a bespoke API with each DMV, insurer, repairer or rental company. That removes most point-to-point integration cost.
- **Faster quote-to-bind:** verified licence, registration, title, prior-insurance and driving-summary credentials replace document uploads and third-party lookups.
- **Servicing:** mid-term changes, cancellations (status list), renewals and proof-of-insurance requests from DMVs, lenders and lessors become a credential update, not a mailing.
- **Subrogation and inter-carrier exchange:** both carriers verify the same signed artefacts, so there is less dispute over facts and faster settlement.
- **Audit and regulatory reporting:** every decision can point to the signed inputs it used, which simplifies market-conduct exams, rate filings and internal audit.

The scale of the opportunity is visible in the one comparable deployment that has been measured: when the EU put the European Health Insurance Card in a digital wallet, verifying a patient's entitlement went [from about 30 minutes to 13 seconds](https://www.3cl.org/beyond-dc4eu/) (§6).

#### Streamlining workflows with adjacent industries

Insurance touches many other industries around the same vehicle and driver, and today each link is a phone call, a fax, a PDF or a bilateral integration. Because anyone who trusts the issuer can verify a credential, the credentials an insurer issues or receives also streamline the partner's workflow, and vice versa:

| Adjacent industry | Shared credentials | Workflow streamlined |
|---|---|---|
| DMVs and registration authorities | Registration, title, POI | Insurance verification at registration and renewal; salvage branding after total loss; fewer uninsured-vehicle suspensions |
| Law enforcement and emergency services | POI, registration, driver's licence, police report | Roadside checks; crash-scene exchange of information; report numbers flow straight into the claim |
| Auto lenders and lessors | Title (lien), POI | Proof of required coverage and loss-payee status without chasing the borrower; payoff and lien release after total loss |
| Dealers and used-vehicle marketplaces | Title, registration, inspection, repair and salvage history | Faster sale and title transfer; verified vehicle history; insurance bound at point of sale |
| Rental, car-sharing and ride-hail platforms | POI, driver's licence, rental record | Instant coverage and driver checks at pickup; verified rental days on replacement-vehicle claims |
| Repair shops, parts suppliers and appraisers | FNOL, repair estimate, completed repair | Estimate-to-approval without re-keying; verified repair completion for supplements, warranty and resale |
| Towing, roadside and salvage auctions | Tow record, total-loss and salvage credentials | Fewer disputed tow bills; salvage vehicles move to auction with a verifiable status |
| OEMs and telematics / fleet platforms | Vehicle evidence (VSS), inspection, UBI summary | One consented, standard output for every insurer instead of a bespoke feed per carrier |
| Fleet operators and commercial transport | POI, registration, inspection, driver assignment | Compliance bundles for roadside and weigh-station checks double as underwriting and claims evidence |
| Healthcare providers and EMS | Injury and treatment records | Verified medical billing on injury claims (medical alert data on the licence remains early discussion; see §4) |
| Reinsurers and inter-carrier networks | Any signed claim artefact | Portfolio and subrogation data verified at source rather than re-reported |

The benefit compounds: each industry that issues or accepts credentials makes the network more valuable for all the others, as email and card payments did. Building on open vocabularies (VVC, VSS) rather than proprietary formats is what makes that network possible.

#### Built for software and AI consumption

VCs use the W3C VC Data Model 2.0, which is based on **RDF expressed as JSON-LD**. Every property (`policyNumber`, `coverageLimitPerAccident`, the VSS signal paths) is a globally unique IRI with a published definition in the VVC vocabulary or VSS. For automation this means:

- **Unambiguous meaning:** software and AI models do not guess what a field means or reconcile inconsistent labels across carriers, DMVs and OEMs.
- **Knowledge-graph ready:** credentials from different issuers merge into a linked-data graph (policy ↔ vehicle ↔ driver ↔ incident ↔ repair) that standard tools query (SPARQL, graph databases) and validate (SHACL).
- **Trusted inputs for AI:** each fact carries its issuer and signature, so an AI claims assistant can check provenance before acting and explain its output by citing the credentials it relied on. That is a stronger basis than extracting facts from PDFs and photos.
- **Better models:** consistent, verified, well-described data across insurers is a better basis for pricing, reserving and fraud detection than proprietary, differently coded feeds.
- **Mapping to existing standards:** because the semantics are explicit, mappings to ACORD, CSIO and national formats are published once and reused.

Credentials can also be secured as JOSE/COSE or SD-JWT, and mDL uses ISO mdoc (CBOR), which is not RDF. The VVC vocabulary still gives these formats a common semantic reference.

### 3.6 Usage-Based Insurance

The US already has some 30 million UBI policyholders, about half the world's total, yet adoption is held back by privacy concerns and by the cost of proprietary dongles and apps. US regulators have made clear that sharing driving data requires separate, affirmative consent (the FTC's order against a North American automaker's connected-vehicle service, finalised January 2026, and California's record CCPA settlement with the same automaker, May 2026). VCs address both:

- **Consent in the credential:** the UBI policy credential records which signals, at what granularity and for how long, as an auditable consent record (ISO/IEC TS 27560), rather than a clause buried in terms of service.
- **Data minimisation:** at renewal the policyholder presents a *selectively disclosed* summary (total miles, risk band, count of harsh events) without exposing raw trips or locations.
- **Portability:** a verifiable driving-history credential moves with the driver between insurers, which lowers acquisition cost for carriers and rewards safe drivers when they switch.
- **No hardware lock-in:** the evidence comes from the vehicle's own signals, described in VSS, whether the vehicle is read by an OEM cloud, an aftermarket device or a fleet platform.
- **Rate-filing transparency:** scoring inputs expressed in published vocabularies (VVC, VSS) rather than proprietary scores are easier to explain to state insurance departments.
- **Fleets:** the operator is the policyholder, gives consent once and shares verified driver and vehicle risk data with its carrier.

A related opportunity is a **"well-maintained vehicle" discount**: an opt-in periodic inspection credential (tire tread, brakes, lamps, warning lights) generated by the vehicle and sent to an insurer endpoint published in the POI. It works as loss prevention, and the same credential serves as evidence of roadworthiness at claim time. See the [Vehicle Inspection Credential report, §13.5](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vehicle-inspection-credential-data-requirements.md).

### 3.7 Automated and Autonomous Vehicles

As liability shifts from the driver to the vehicle, manufacturer and software, insurers need trustworthy records of which system was in control and what it sensed. Signed vehicle evidence bound to registration and POI credentials is the natural basis for that. See the COVESA whitepaper [Insuring Autonomous Vehicles: Data Requirements](https://github.com/COVESA/commercial-vehicles/blob/main/reports/COVESA_Whitepaper_Insuring_Autonomous_Vehicles_Data_Requirements.md).

### 3.8 Protecting Customer Privacy and Company Reputation from Data Breaches

Today's model of checking a document by copying it creates the data that attackers steal. Every party that needs to trust a licence or insurance card (insurer, agent, rental counter, repair shop, dealer, lender) photographs or scans it and keeps the copy. Thousands of copies of the same document build up, each a liability for the company holding it.

**The IDScan.net breach shows the cost.** In early September 2026 a dark-web marketplace called "Nexus" began selling more than **153 million driver's licence scans** (front, back and UV/IR images), plus about 10 million ID cards, 3 million travel documents and 579,000 medical cards. The data came from the cloud platform of IDScan.net, an identity-verification vendor used by major rental, retail, logistics and financial-services companies. IDScan.net confirmed unauthorised access, and the FBI opened an investigation. The seller claimed to have been drawing from the platform for more than a year ([Krebs on Security](https://krebsonsecurity.com/2026/09/fbi-probes-service-selling-153m-drivers-licenses/), [Help Net Security](https://www.helpnetsecurity.com/2026/09/11/idscan-net-data-breach-153-million-drivers-licenses/), [Malwarebytes](https://www.malwarebytes.com/blog/news/2026/09/dark-web-site-puts-153-million-drivers-licenses-and-millions-more-ids-up-for-sale)). The breach was a structural consequence of the paper model, not bad luck: centralised copies become centralised targets. Stolen licence images are also raw material for insurance fraud: synthetic identities, fraudulent policies and staged-claim rings (§3.4).

**Verifiable credentials change the model from "copy and keep" to "verify and discard":**

- **The verifier gets a proof, not an image.** An insurer, agent or rental counter confirms cryptographically that a licence is valid and DMV-issued, that the driver meets an age threshold, and that they are licensed for the vehicle class. It never stores a scan. No scan database, nothing to breach.
- **Selective disclosure limits what is shared.** A POI check reveals "covered, this vehicle, valid until…", not the policy file. A licence check can reveal "over 25" instead of date of birth, home address and licence number. Selective disclosure is available today with ISO 18013-5 mDL and SD-JWT VC. UBI summaries likewise replace raw trip logs (§3.6).
- **The holder authorises each presentation.** The customer approves every disclosure in their wallet, which produces an auditable consent record and fits where US regulators have moved on connected-car data.
- **Revocation replaces re-collection.** A cancelled policy or suspended licence is flagged through a status list, so verifiers do not keep and re-check copies.
- **The same approach protects paper.** Where a physical card remains, a signed credential printed in its barcode lets a scanner verify the card rather than photograph it.

**Why it matters to insurers as companies, not only to their customers:**

- **Smaller breach exposure.** Data you do not hold cannot be stolen, disclosed or held for ransom. Every licence image, insurance card and claim attachment an insurer or its vendors *doesn't* keep reduces its liability under the NAIC Insurance Data Security Model Law and state breach-notification, GLBA, CCPA and GDPR obligations. The [IBM Cost of a Data Breach 2026](https://www.ibm.com/reports/data-breach) report puts the average breach at a record US$4.99 million worldwide and US$11.5 million in the United States.
- **Less third-party and vendor risk.** The IDScan.net case was a *vendor* breach that exposed the vendor's customers. Verifying credentials in software, without a vendor keeping images, removes a layer of supply-chain risk and the reputational harm that comes with it.
- **Brand and trust.** For regulated, trust-based businesses, being named in a breach headline is expensive in churn, regulatory attention and litigation. "We never collect your licence image" is a strong, simple promise.
- **Better cyber underwriting.** Insurers that write cyber cover can treat credential-based verification and data minimisation as risk-reducing controls when pricing commercial clients such as rental companies, dealers and fleets.

**Limits to be honest about:** VCs minimise data but do not make it disappear. The verifier still receives whatever attributes are disclosed and must protect them. Issuers (DMVs, insurers) and holders' wallets become the security-critical points, although issuers already hold this data today. Standard signatures can let colluding verifiers link presentations. Truly unlinkable, zero-knowledge presentations (for example BBS signatures) are specified at W3C but still depend on IETF work that has not been finalised. Until then, the practical privacy gain comes from selective disclosure and not retaining data, rather than from full anonymity.

## 4. Driver's Licence Credentials and Medical Alert Information

Mobile driver's licences are in production: 21 US states plus Puerto Rico are TSA-accepted, and Canadian provinces and the EUDI Wallet are following (see [VC Driver's Licence Global Status](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-driver-license-global-status-2025.md)). For insurers they provide verified identity at quote, bind, claim and roadside.

Adding **medical alert information** (allergies, conditions, emergency contacts) to the driver's licence credential, so that first responders could reach it after a crash, has been raised. It is **only in early discussion**. There is no specification or deployment, and important questions remain open: access for an incapacitated holder ("break-glass"), health-data privacy, and who may read it.

## 5. Where the Credentials Live: The Vehicle Wallet

The phone wallet covers person-bound credentials (driver's licence) today. Vehicle-bound credentials (registration, POI) and sensor-triggered submissions (FNOL, theft) need to be available when the phone is absent or damaged, which argues for a wallet or verifier on the head unit. The COVESA AOSP work assesses this and the open-source options:

- [Digital Wallet for the COVESA AOSP Platform: Use Cases and Open-Source Foundations](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-vc-wallet-use-cases-standards.md). Insurance use cases UC-5 to UC-9 (POI, eFNOL, theft, eCall bridge, UBI).
- [Open Source Wallet Solutions for AOSP: Comparison](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-open-source-wallets-comparison.md). Multipaz, Bifold, walt.id and others.

## 6. Current Use in the Insurance Industry

**Short answer:** no public, production deployment of W3C Verifiable Credentials exists in personal or commercial auto insurance, for proof of insurance, FNOL, claims or UBI (searched September 2026). The pattern is in production or pilot in neighbouring insurance lines, and in auto insurance using earlier technology. That is the precedent for the business cases above.

| Example | Line / region | What it does | Technology | Status |
|---|---|---|---|---|
| [DC4EU European Health Insurance Card (EHIC)](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/930453001/EHIC) | Public health insurance, EU | The citizen holds the EHIC as an attestation in an EU Digital Identity Wallet; a provider abroad verifies it on the spot | IETF SD-JWT VC, OpenID4VCI, data model based on W3C VC | Large-scale pilot (101 partners, 25 countries). Verification of healthcare rights fell [from about 30 minutes to 13 seconds](https://www.3cl.org/beyond-dc4eu/). Proposed follow-on: European Social Security Pass (ESSPASS) |
| [CARIN Digital Insurance Card](https://hl7.org/fhir/us/insurance-card/Use_Case.html) / [SMART Health Insurance Card](https://www.thecommonsproject.org/digital-insurance-card-project) | Private health insurance, US | The health plan issues a signed insurance card that the member keeps in a wallet and shows by QR code at check-in; the provider verifies it cryptographically | HL7 FHIR plus SMART Health Cards (a FHIR-based verifiable-credential framework) | Published HL7 standard for trial use (STU 1.1); payer and provider pilots |
| [India DigiLocker motor insurance](https://www.universalsompo.com/blogs/general-insurance/digilocker-insurance/) | Motor insurance, India | Insurers registered as DigiLocker issuers push motor, health and travel policies into the citizen's government wallet. Under a MoRTH advisory, police and RTOs accept these documents in place of originals | Government-signed digital documents (PKI), not W3C VC | **In production at national scale.** The closest live analogue to a proof-of-insurance credential |
| [RiskStream contactless proof of insurance](https://www.ledgerinsights.com/riskstream-tests-blockchain-proof-of-insurance/) | Personal auto, US | A driver shares proof of insurance by QR code or access key; carriers verify it with each other | Permissioned blockchain (Corda, the "Canopy" network) | Member-to-member test completed with COUNTRY Financial (2020). A related [certificate-of-insurance verification POC](https://www.trustlayer.io/resources/trustlayer-riskstream-collaborative-liberty-mutual-nationwide-realtime-proof-certificate-of-insurance-solution) involved Liberty Mutual, Nationwide and TrustLayer. No public production roll-out |
| [RiskStream / LIMRA licensing and appointments](https://www.limra.com/en/newsroom/news-releases/2019/limra-and-the-institutes-riskstream-collaborative-announce-plans-to-develop-blockchain-solution-for-life-insurance-licensing-and-appointments/) | Life and annuity distribution, US | Carriers validate agents' licences to sell specific products in each state automatically, instead of through repeated paperwork | Permissioned blockchain | Announced 2019 |
| US mobile driver's licences (ISO 18013-5 mDL) | Identity, US | 21 states plus Puerto Rico issue mDLs ([status report](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-driver-license-global-status-2025.md)). In September 2026, FinCEN and the federal bank regulators [confirmed](https://www.fincen.gov/system/files/2026-09/MDL-VDC-FAQs.pdf) that banks and credit unions, including auto lenders, may accept mDLs and other government-issued verifiable digital credentials for customer identification | ISO mdoc | In production. No public announcement found of an auto insurer accepting mDLs at quote or claim |

**What this shows:**

- **Insurers already issue signed, wallet-held coverage documents** in health insurance (EHIC, CARIN) and in Indian motor insurance (DigiLocker). Proof of auto insurance is the same pattern, applied to a line that is compulsory in almost every jurisdiction.
- **The verification savings are measurable.** DC4EU's 30-minutes-to-13-seconds figure for EHIC is the kind of result §3.5 expects for proof of insurance, FNOL and inter-carrier exchange.
- **The US auto industry has already tried the idea on shared ledgers.** Open W3C and ISO credential formats remove the need for every party to join one consortium network. A DMV, a police officer or a repair shop can verify a credential without being a ledger member.
- **The regulatory pull is growing:** the US bank-regulator FAQ on mDLs and the EU requirement for regulated private services to accept EUDI Wallets from December 2027. Auto insurance is next to both, through lenders and through identity checks at quote and claim.

## 7. Common Objections

| Objection | Response |
|---|---|
| "We already get eFNOL from our telematics partner." | You get it from *one* partner, for the vehicles that partner covers, in that partner's format. A published `fnolEndpoint` lets every OEM, aftermarket device and fleet platform reach you the same way, and the notice arrives signed. |
| "States already have online insurance verification (IICMVA)." | Those systems answer "is this VIN insured today?" for state agencies. A POI credential answers the same question for anyone the policyholder chooses to show it to, offline, without the verifier integrating with the state or the insurer. The two complement each other. |
| "No auto insurer has done this." | Correct, which is why the first movers set the profile everyone else adopts. The components (VVC, mDL, SD-JWT, status lists, OpenID4VC) are all published and in production elsewhere; what is missing is an insurer to issue the first POI credential and stand up the first signed-FNOL endpoint. |
| "This is a big IT project." | Issuing a credential is signing a JSON document and publishing a public key and a status list. Verifying one is a library call. The ACORD and CSIO mappings mean intake systems do not change. A pilot is measured in weeks, not years (§8). |
| "Blockchain proof of insurance didn't take off." | It required every verifier to join a consortium network. W3C and ISO credentials need only the issuer's public key, so a repair shop or police officer can verify without membership. The lesson was about the distribution model, not the idea. |
| "Customers won't adopt wallets." | 21 states already issue mDLs, the EU requires every member state to offer a wallet by the end of 2026, and every major phone platform ships one. Insurers do not have to build or distribute a wallet; they issue into the ones customers already have. |

## 8. Status and What Is Still Needed

| Item | Status |
|---|---|
| `ProofOfInsuranceCredential` in VVC | Published in the vocabulary (v1.0, which is marked experimental and subject to change) |
| POI adoption by a state or province | Under discussion; **no public confirmation of adoption** |
| `fnolEndpoint`, FNOL submission profile, consent terms | Proposed (COVESA work item) |
| Theft and other incident / claim report credentials | Theft data model complete in S2DM; accident and unsafe-driving models are stubs; other report types not yet started |
| Mappings to ACORD, CSIO, EU national claim formats | Proposed; need insurer-body liaison |
| UBI and inspection credentials | Concept; need insurer pilots |
| Medical alert data on the driver's licence | Early discussion only |
| Head-unit wallet | Proposed COVESA AOSP workstream |

**What a first pilot looks like.** One insurer, one state, one fleet or telematics partner:

1. Issue `ProofOfInsuranceCredential` for a pilot book of policies, with a status list for cancellations and an `fnolEndpoint`.
2. Accept the state's mDL and registration credential at quote and at FNOL, and stop storing licence images for those customers.
3. Have the fleet or telematics partner submit signed FNOL notices to the endpoint, mapped into the existing ACORD or CSIO intake.
4. Measure: time to FNOL, time to first payment, re-keying errors, verification calls avoided, and licence images not collected.

**Where insurers, regulators and industry bodies can help:**

- Insurers: pilot POI issuance and a signed-FNOL intake endpoint; define what evidence would earn UBI and maintenance discounts.
- Regulators (NAIC, state insurance departments, IICMVA, provincial regulators): guidance on accepting VC-based proof of insurance, and on consent and rate-filing treatment of credential-based UBI.
- Standards bodies (ACORD, CSIO, AAIS, BiPRO/GDV, SIVI): mapping from the COVESA FNOL profile into existing claim messages.
- Adjacent industries (DMVs and AAMVA, lenders, dealers, rental, repair and towing networks, OEMs, fleet platforms): accept and issue the same credentials, so that one integration serves every partner instead of one per insurer.

## Links

- COVESA Verifiable Vehicle Credentials (VVC) specification: <https://covesa.github.io/vehicle-credentials-vocabulary/> · [Proof of Insurance](https://covesa.github.io/vehicle-credentials-vocabulary/#ProofOfInsuranceCredential) · [repository](https://github.com/COVESA/vehicle-credentials-vocabulary)
- [FNOL report: Streamlining Connected Vehicle Incident Reporting to Insurers](https://github.com/COVESA/commercial-vehicles/blob/main/reports/connected-vehicle-fnol-vc-standards.md)
- [AOSP VC wallet use cases and standards](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-vc-wallet-use-cases-standards.md) · [AOSP open-source wallets comparison](https://github.com/COVESA/commercial-vehicles/blob/main/reports/aosp-open-source-wallets-comparison.md)
- [Vehicle Inspection Credential: data requirements](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vehicle-inspection-credential-data-requirements.md)
- [VC driver's licences: global status](https://github.com/COVESA/commercial-vehicles/blob/main/reports/vc-driver-license-global-status-2025.md)
- [COVESA whitepaper: Insuring Autonomous Vehicles](https://github.com/COVESA/commercial-vehicles/blob/main/reports/COVESA_Whitepaper_Insuring_Autonomous_Vehicles_Data_Requirements.md)
- [COVESA Vehicle Signal Specification (VSS)](https://covesa.global/vehicle-signal-specification/)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) · [W3C JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) · [W3C RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) · [W3C Bitstring Status List](https://www.w3.org/TR/vc-bitstring-status-list/) · [W3C CCG Verifiable Driver's License vocabulary](https://w3c-ccg.github.io/vdl-vocab/)
- [Insurance Research Council: Uninsured and Underinsured Motorists 2017–2023](https://insurance-research.org/news/one-three-drivers-are-either-uninsured-or-underinsured-us-exposing-themselves-and-other) · [NAIC 2025 private passenger auto market share](https://collisionweek.com/2026/04/02/progressive-closes-gap-state-farm-top-u-s-auto-insurers-reshape-market-2025/)
- [Coalition Against Insurance Fraud: fraud statistics](https://insurancefraud.org/fraud-stats/)
- IDScan.net / Nexus breach: [Krebs on Security](https://krebsonsecurity.com/2026/09/fbi-probes-service-selling-153m-drivers-licenses/) · [Help Net Security](https://www.helpnetsecurity.com/2026/09/11/idscan-net-data-breach-153-million-drivers-licenses/) · [Malwarebytes](https://www.malwarebytes.com/blog/news/2026/09/dark-web-site-puts-153-million-drivers-licenses-and-millions-more-ids-up-for-sale)
- [IBM Cost of a Data Breach Report](https://www.ibm.com/reports/data-breach) · [NAIC Insurance Data Security Model Law (#668)](https://content.naic.org/sites/default/files/model-law-668.pdf)
