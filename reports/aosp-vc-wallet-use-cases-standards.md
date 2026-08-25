# Digital Wallet for the COVESA AOSP Platform: Use Cases and Open-Source Foundations

**Date:** 2026-08-12  
**Author:** Ted Guild (COVESA)  
**Intended audience:** COVESA AOSP App Framework Standardization Group  
**Related work:** COVESA Vehicle Credentials Vocabulary (VCV), COVESA In-Car Wallet project, W3C VC v2.0, ISO 18013-5

---

## Purpose

DRAFT - contains known flaws wrt regulations and workflows

This document is a proposal input for the COVESA AOSP App Framework Standardization Group to consider whether to establish a **digital wallet workstream** within the COVESA AOSP SDK.

It makes the case that: (1) a significant and growing class of automotive use cases requires verifiable credential (VC) management on the head unit and cannot be served by the Google Automotive Services (GAS) stack alone; (2) several viable open-source wallet foundations exist that could be integrated into the COVESA SDK as a shared library; and (3) adjacent COVESA projects (In-Car Wallet, Vehicle Credentials Vocabulary) are already active and need a credential management layer to complete their work.

The document enumerates concrete use cases, analyzes open-source wallet candidates, and identifies the specific gap in the current AOSP App Framework scope that a new workstream would address.

---

## AOSP in the Automotive Context

### COVESA AOSP App Framework vs. AAOS

Two distinct automotive Android ecosystems are relevant here:

**Android Automotive OS (AAOS)** is Google's commercial automotive Android product. Vehicles shipping with Google Automotive Services (GAS) get the full Google stack — Google Maps, Google Play, Google Pay, and the Android Digital Credentials API via Google Play Services. GAS is a licensing agreement; the wallet and identity credential functionality it provides is not open source and not available without Google's involvement.

**COVESA AOSP App Framework Standardization Group** works on the complementary open-source layer: AOSP *without* GAS. Chaired by representatives from FORVIA, BMW, and GM, this group standardizes shared libraries (the COVESA SDK) that enable automotive apps to work across any AOSP-based head unit, regardless of manufacturer or GAS licensing status. Current workstreams include UnifiedPush Notifications, Entertainment Stream, Emulator, and Vehicle Data. Digital wallet is not yet a COVESA AOSP workstream — it is a gap.

**COVESA In-Car Wallet – Payments & Orchestration** is a separate COVESA project (also called "Vehicle as a Wallet") focused on the payment and transaction layer. Active participants include GM, Infineon, Verra Mobility, Pair Point, Sheeva.AI, FIDO Alliance, Starfish, and Mavi. Its primary focus is in-vehicle payments (toll, parking, EV charging, fuel), with some overlap into authentication via the FIDO Alliance connection. A white paper is in progress and Plug & Charge (ISO 15118) demonstrations have taken place.

**The gap:** Neither the COVESA AOSP group nor the In-Car Wallet project currently addresses W3C VC / ISO 18013-5 credential management as a distinct software layer on AOSP head units without GAS. That gap is where the use cases below live, and where an open-source wallet solution is needed.

### Why the GAS Dependency Matters

On a GAS device, Android Credential Manager API handles VC presentation natively and routes requests to installed wallet apps. On a non-GAS AOSP head unit, that API is absent. A VC wallet must therefore either:

1. **Embed a complete wallet library** (credential storage, key management, presentation protocol) directly in a COVESA AOSP library or OEM app, or
2. **Leverage an open-source wallet** (see §Open-Source Wallet Options) that can run without Play Services.

Option 1 aligns with the COVESA AOSP SDK model. Option 2 requires selecting a wallet project with an appropriate architecture and license.

---

## Priority Use Cases for Initial Scope

Before the full enumeration below, this section identifies the three use cases that are most mature, have active standards support, and most clearly require head-unit credential holding. These are the recommended starting point for any COVESA AOSP wallet workstream MVP.

> **Strategic note (per Manu Sporny / Digital Bazaar, Aug 2026):** The fastest path to demonstrated viability is not to build a full head-unit wallet across all 20 use cases, but to (1) implement the **verifier** side on the head unit first — much simpler than full issuance — and (2) target the narrow set of credentials that genuinely cannot be held on the driver's phone. The driver's phone wallet (Apple Wallet, Google Wallet, or a W3C VC-compatible wallet) handles the majority of personal credential use cases today. The AOSP group work item should be scoped accordingly.

| Priority | Use Case | Why Head-Unit Holds (Not Phone) | Standards Ready |
|---|---|---|---|
| 1 | UC-1: mDL / vehicle registration presentation | Registration is vehicle-bound; phone is an acceptable relay but not the primary holder | ISO 18013-5, COVESA VCV — production |
| 2 | UC-5 / UC-6: Proof of Insurance + eFNOL | POI must be accessible when phone is absent/damaged; eFNOL is autonomously triggered by sensors | COVESA VCV fnolEndpoint, OpenID4VCI — active |
| 3 | UC-10: Plug & Charge / EV fleet billing | ISO 15118-20 vehicle-to-charger authentication requires no phone; fleet billing binds to vehicle identity | ISO 15118-20 — EU AFIR-mandated by Jan 2027 |

Everything else in this document is **extended scope** — real use cases, but better addressed once the MVP verifier and core holder capabilities are proven.

---

## Standards Readiness

| Standard | Status (2026) |
|---|---|
| W3C VC Data Model v2.0 | W3C Recommendation (May 2025) |
| W3C Data Integrity (EdDSA, ECDSA) | W3C Recommendation (May 2025) |
| W3C Bitstring Status List v1.0 | W3C Recommendation (May 2025) |
| W3C VC API | W3C CCG Community Report (active); HTTP API for wallet-to-issuer and wallet-to-verifier interactions; used in CA DMV deployment |
| SD-JWT VC | IETF RFC (2025) |
| ISO 18013-5 (mDL) | Published; TSA-accepted in 21+ US states |
| ISO 18013-7 | Published (2025); Digital Credentials API binding |
| OpenID4VP 1.0 | Final specification |
| OpenID4VCI 1.0 | Final specification |
| Android Digital Credentials API | GA (April 2025); GAS devices only |
| eIDAS 2.0 / EUDIW | Member state rollout deadline: late 2026 |
| ISO 15118-20 | EU AFIR mandate: all new public chargers by Jan 2027 |
| COVESA Vehicle Credentials Vocabulary | Active; CA DMV production deployment underway |
| IEEE 1609.2 / 1609.2.1 | Published; SCMS pseudonym certificate management for V2X |
| 3GPP NR-V2X (Release 16/17) | Published; PC5 sidelink unicast/groupcast/broadcast |
| ETSI ITS / EN 302 636 series | Published; European C-ITS message and security standards |
| SAE J2735 | Published; Basic Safety Message and V2X data dictionary |
| 5GAA SCMS Certificate Policy (TR) | Active (2025); North American V2X credential policy |

---

## Head Unit vs. Phone: Holder, Verifier, and Fast-Path Roles

Not every credential should live on the vehicle, and not every head-unit capability requires holding credentials at all. The right architecture depends on three roles — **Holder** (stores the credential and controls presentation), **Issuer** (signs and delivers), and **Verifier** (validates a presented credential) — and on three questions: (a) is the credential vehicle-bound or person-bound? (b) must it be available autonomously without the driver's phone? (c) is it triggered by vehicle sensor events rather than driver action?

### Fast Path: Phone-Holds / Head-Unit-Verifies

The fastest path to demonstrating VC viability in automotive is to implement the **verifier** role on the head unit first. This requires no new wallet infrastructure — only a credential verification library and a trust registry. The driver's phone wallet (Apple Wallet, Google Wallet, or any W3C VC / ISO 18013-5 compatible wallet) holds and presents credentials over BLE/NFC. The head unit verifies. This already works for mDL today.

Implementing the head unit as a verifier first covers: driver authentication at ignition (mDL from phone), access control (fleet driver assignment from phone), and law enforcement stop (officer's phone or MDT presents, vehicle head unit or officer verifier checks). No new OEM wallet software is required on the vehicle side beyond a verification library.

### When Head-Unit Holding Is Genuinely Required

Head-unit holding is justified only when:
- The credential is **vehicle-subject** (the vehicle, not the driver, is the named subject), or
- Presentation must happen **autonomously** (no human present or phone available), or
- The credential is **sensor-triggered** at a moment when human action is not possible

| Credential Type | Role on Head Unit | Phone Alternative? | Rationale |
|---|---|---|---|
| Vehicle registration / title | **Holder** | No | Vehicle-bound; must persist without driver's phone; needed if vehicle is unoccupied |
| Proof of Insurance (POI) | **Holder** | Fallback only | Required at accident scene when phone is damaged or absent; used by autonomous eFNOL |
| Incident / FNOL VC | **Issuer + Holder** | No | Generated by vehicle sensors at moment of impact; phone may be damaged |
| Theft alert VC | **Issuer + Holder** | No | Submitted autonomously when no occupant is present |
| Fleet / vehicle assignment | **Holder** | BLE relay acceptable | Controls vehicle access; must persist across driver changes |
| Fleet compliance bundle | **Holder** | No | USDOT, IFTA, inspection credentials are vehicle-specific |
| ELD / HOS driver identity | **Holder** | Workaround | Must bind to the vehicle's electronic log |
| Weigh station pre-clearance | **Holder** | No | Geofence-triggered, automated |
| UBI / telematics consent | **Holder** | No | Consent scope is tied to vehicle signals; must persist across driver changes |
| Cross-border cargo bundle | **Holder** | No | Cargo + vehicle credentials travel with the truck |
| ISO 15118 Plug & Charge (EV) | **Holder** | No | Vehicle-to-charger authentication; ISO 15118 protocol has no phone path |
| Mobile Driver's License (mDL) | **Verifier only** | Phone holds | Person-bound identity; head unit relays or verifies via CCC Digital Key BLE |
| Payment credentials (consumer) | **Verifier / relay** | Phone holds | Card network tokenization is phone-resident |
| EV charging — fleet billing | **Holder** | Workaround | Fleet cost allocation requires vehicle identity credential at the head unit |
| Toll payment — fleet | **Holder** | Workaround | Fleet account binding requires vehicle identity |

**Summary principle:** The AOSP group's fastest contribution is a **verifier library** that works without GAS — this covers mDL at ignition, access control, and law enforcement stops immediately with no new wallet infrastructure. Head-unit *holding* is justified for vehicle-subject, autonomously-triggered, and sensor-generated credentials: registration, POI, FNOL, fleet compliance, Plug & Charge. Personal identity (mDL) and consumer payment credentials are and should remain phone-resident; the head unit verifies or relays them.

---

## Open-Source Wallet Options for AOSP Head Units

Five open-source wallet projects are viable candidates for automotive deployment. None was designed for head units; all require adaptation. The table summarizes, with detailed assessments below.

| Project | License | Language | Credential Formats | Protocols | GAS-Free? | Maturity | Automotive Fit |
|---|---|---|---|---|---|---|---|
| OWF Multipaz | Apache 2.0 | Kotlin Multiplatform | mdoc, SD-JWT VC, W3C VC | OpenID4VP, 18013-5/7, Digital Credentials API | Yes | Pre-1.0 (~late 2026) | **Best fit** |
| EUDI Reference Wallet | Apache 2.0 | Kotlin (Android) | mdoc, SD-JWT VC, W3C VC | OpenID4VP, OpenID4VCI, 18013-5 | Partial | Production (EU pilot) | Good for EU scope |
| Procivis One | Apache 2.0 | Rust core + React Native | mdoc, SD-JWT VC, W3C VC | OID4VC, 18013-5 | Yes (core) | Production | Moderate fit |
| OWF Bifold | Apache 2.0 | React Native | W3C VC, AnonCreds | DIDComm, OID4VC | Yes | Production | Low fit (phone-first) |
| SpruceID Credible / SpruceKit | Apache 2.0 / MIT | Flutter + Rust | W3C VC, DID, 18013-5 | OpenID4VP, DIDComm | Yes | Production | Moderate fit |

---

### 1. OWF Multipaz (OpenWallet Foundation)

**Repository:** `openwallet-foundation-labs/identity-credential` (renamed Multipaz)  
**Origin:** Originally Google's Android Identity Credential library; donated to OWF

**What it is:** Kotlin Multiplatform libraries providing core building blocks for ISO mdoc, SD-JWT VC, and W3C VC credential management. Includes proximity presentment (BLE/NFC per ISO 18013-5) and remote presentment via OpenID4VP / ISO 18013-7. Targets Android, iOS, and server-side environments from a shared codebase.

**Strengths for AOSP head units:**
- Written in Kotlin — the native language for AOSP app development; minimal porting overhead
- Android-specific library (`identity-android`) uses Android Keystore for hardware-backed key storage, and Android BLE/NFC APIs directly — no GAS dependency
- Supports ISO 18013-5 proximity presentment natively, which is the protocol for roadside/weigh-station presentation scenarios
- Covers ISO 18013-7:2025 (Digital Credentials API binding) for when GAS is present
- Zero-knowledge proof support (Google Longfellow-ZK integration) for privacy-preserving selective disclosure
- OWF governance means no single-vendor lock-in; royalty-free

**Weaknesses:**
- Pre-1.0 (API and storage formats subject to change); production-readiness expected late 2026 or early 2027
- No head-unit–specific adaptations yet; proximity presentment assumes a handheld form factor (screen, NFC reader at user height)
- No UX layer — purely a library; the COVESA AOSP group would need to build the wallet application on top
- Kotlin Multiplatform maturity on iOS/embedded is still evolving; Android path is solid

**Verdict:** The strongest technical foundation for a COVESA AOSP wallet library. The COVESA AOSP SDK model (adding libraries to a shared collection) maps directly onto Multipaz's architecture. The pre-1.0 status is a risk but the timeline aligns with a realistic COVESA development horizon.

---

### 2. EU Digital Identity Wallet (EUDI) Reference Implementation

**Repository:** `eu-digital-identity-wallet/eudi-app-android-wallet-ui` and associated libraries  
**Governance:** European Commission; open source under Apache 2.0

**What it is:** The official Android reference implementation for eIDAS 2.0 compliance. Comprises a wallet UI app and a set of modular Android libraries (`eudi-lib-android-wallet-core`, `eudi-lib-android-iso18013-data-transfer`, `eudi-lib-android-verifier-core`). Production-deployed in EU member state pilots.

**Strengths for AOSP head units:**
- Production-quality Android code with active EU government backing; libraries are more mature than Multipaz for immediate deployment
- Strongest eIDAS 2.0 / EUDIW alignment — if EU fleet vehicles must present EUDIW-compatible credentials, this is the reference implementation to build from
- Modular: the core library layer can be extracted from the phone UI and embedded in a head unit app
- OpenID4VCI + OpenID4VP implemented and tested in real deployments

**Weaknesses:**
- Architecturally phone-centric; the UI shell assumes a touchscreen smartphone, not a vehicle display or ambient/voice interaction
- Regulatory focus is EU identity documents (PID, mDL); fleet and commercial vehicle credential types (USDOT, IFTA, VCV) are out of scope without extension
- GAS-independence not a design goal — tested primarily on standard Android devices with Play Services; adaptation for GAS-free AOSP requires validation
- EC governance moves at regulatory pace; adding COVESA VCV credential types would require either forking or upstream contribution with EU Commission alignment

**Verdict:** Well-suited as the eIDAS 2.0 compliance layer for EU-deployed vehicles. Less suited as a general-purpose fleet credential wallet without significant extension. Best used as a library dependency for the EU jurisdiction slice, not as the primary wallet architecture.

---

### 3. Procivis One

**Repository:** `procivis/one-wallet` and `procivis/one-core`  
**Governance:** Procivis AG (Swiss); Apache 2.0

**What it is:** A full-stack open-source digital identity platform: Rust-based core (one-core) providing credential issuance, holding, and verification, with a React Native SDK and wallet app on top. eIDAS 2.0 compliant. Apache 2.0 licensed.

**Strengths for AOSP head units:**
- Rust core is portable to constrained environments; could be compiled for embedded Android without the full React Native layer
- Broad credential format support (ISO 18013-5, SD-JWT VC, W3C VC, AnonCreds) out of the box
- eIDAS 2.0 compliance already validated in production (Swiss public sector deployments)
- Apache 2.0 license with no CLA requirement

**Weaknesses:**
- React Native UI layer is not appropriate for automotive head units; OEMs would need to replace it entirely with an AOSP-native UI
- Rust-on-Android build chain adds complexity for COVESA AOSP integration compared to a Kotlin-native library
- No Android Keystore / hardware security integration in the open-source layer (handled in the proprietary backend); GAS-free key management needs custom work
- Swiss-government–centric development priorities; automotive credential types not represented in the roadmap

**Verdict:** The Rust core is technically sound and could underpin an embedded wallet. But the architectural split between Rust core and React Native UX means more integration work than Multipaz for AOSP head units. Best suited if a cross-platform (Android + non-Android IVI OS) wallet is required.

---

### 4. OWF Bifold Wallet

**Repository:** `openwallet-foundation/bifold-wallet`  
**Governance:** OpenWallet Foundation; Apache 2.0  
**Origin:** Hyperledger Aries Bifold

**What it is:** A React Native mobile agent built on OWF Credo-ts (TypeScript), targeting Hyperledger Aries / AnonCreds and W3C VC ecosystems. Designed for person-held identity wallets in government and enterprise contexts.

**Strengths for AOSP head units:**
- OWF governance; active community; production deployments (several Canadian province government ID programs)
- Strong DIDComm v2 + AnonCreds support, which is relevant if the issuer ecosystem uses Hyperledger-stack issuers
- React Native allows a single codebase across Android and iOS if dual-platform support is needed

**Weaknesses:**
- React Native is a poor fit for automotive head unit deployment: heavy JavaScript runtime, assumes phone UX paradigms (touch, notifications, biometric auth), not designed for ambient or voice interaction
- AnonCreds / Aries DIDComm lineage is diverging from ISO 18013-5 and OpenID4VP mainstream; ISO mDL and mdoc formats are not natively supported
- No hardware key storage integration in the base library; relies on React Native Keychain which does not use Android Keystore directly
- No automotive credential types; community focus is government ID and enterprise HR credentials
- GAS-free AOSP not tested; React Native on AOSP without Play Services has known limitations

**Verdict:** Not recommended as the primary wallet for an AOSP head unit. The Aries/AnonCreds lineage is misaligned with ISO 18013-5 and COVESA VCV. React Native on non-GAS AOSP is a significant engineering risk. Consider only if interoperability with an existing Hyperledger Aries issuer ecosystem is a hard requirement.

---

### 5. SpruceID / SpruceKit

**Repositories:** `spruceid/wallet` (Credible, Flutter), `spruceid/openid4vp`, various Rust libraries  
**Governance:** Spruce Systems, Inc.; Apache 2.0 / MIT  

**What it is:** A family of open-source libraries and a reference wallet (Credible, built in Flutter) covering W3C VC, DIDs, ISO 18013-5 mDL, and OpenID4VP. SpruceKit provides native Kotlin, Swift, and Rust library bindings alongside the Flutter app. Spruce has been a significant contributor to mDL interoperability work with AAMVA, NIST, Google, Panasonic, Samsung, and CA DMV.

**Strengths for AOSP head units:**
- Rust libraries (`ssi`, `didkit`) compile to native Android via JNI — no React Native or Flutter runtime required in a pure library deployment
- Strong track record in mDL / ISO 18013-5 interoperability; CA DMV mDL deployment used SpruceID technology
- OpenID4VP implementation is well-tested; used in production government identity programs
- Apache 2.0 / MIT licensing; no CLA
- Actively engaged with AAMVA and state DMV programs — relevant given CA DMV's COVESA VCV involvement

**Weaknesses:**
- Credible (Flutter wallet app) is a phone-first application; the Flutter runtime adds overhead inappropriate for embedded head units
- The Rust library layer is the valuable part for automotive; extracting it from the Flutter application and writing AOSP-native UX is significant work
- DID method support is broad but opinionated (heavy `did:key`, `did:web`); some COVESA VCV use cases may require additional DID method registration
- Company-controlled project (Spruce Systems) rather than foundation-governed; roadmap depends on commercial priorities
- Less direct community overlap with COVESA than OWF projects

**Verdict:** The Rust library core (especially the ISO 18013-5 and OpenID4VP layers) is production-grade and has the strongest government mDL deployment track record of any open-source option. For a COVESA AOSP wallet where CA DMV interoperability is a near-term requirement, SpruceID's Rust libraries are worth integrating as a dependency even if Multipaz is the primary framework.

---

### Recommended Architecture

Given the constraints of GAS-free AOSP, COVESA governance, and the credential types required:

**Primary foundation:** OWF Multipaz (Kotlin Multiplatform) as the COVESA AOSP SDK wallet library — Android-native, OWF-governed, ISO 18013-5/7 + OpenID4VP, hardware keystore integration.

**EU compliance layer:** EUDI library set (`eudi-lib-android-wallet-core`) as a dependency for eIDAS 2.0 attestation types; keeps EU jurisdiction credentials conformant without rebuilding that work.

**mDL / government credential interoperability:** SpruceID Rust libraries (via JNI) where CA DMV or AAMVA interoperability is the immediate requirement and Multipaz's pre-1.0 state is a risk.

**COVESA In-Car Wallet alignment:** The payment and orchestration layer (toll, parking, EV) developed by the In-Car Wallet project should be integrated as the transaction layer sitting above the VC wallet layer — the VC wallet provides identity and credential management; In-Car Wallet provides payment orchestration and UX.

---

## VC Exchange Models

Three distinct exchange models apply across the use cases below. Many use cases support more than one; the right choice depends on connectivity, latency, privacy requirements, and the nature of the verifier.

---

### Model A: Direct (Device-to-Device)

The vehicle head unit wallet and a reader or peer device exchange credentials directly over a local radio channel — no internet connectivity required at exchange time. This is the same architectural pattern regardless of radio technology; the two sub-modes differ in operational parameters (range, speed, hardware), not in fundamental structure.

#### Sub-mode A1: Short-range (BLE / NFC / QR)

The reader — an officer's handheld scanner, a weigh station fixed terminal, a charging station controller, a parking gate — engages the head unit via NFC tap, QR code scan, or BLE using ISO 18013-5 device engagement protocols. Range is ~4 cm (NFC) to ~10 m (BLE); the vehicle must be stationary or near-stop.

*Standards:* ISO 18013-5 engagement + BLE data transfer; OpenID4VP 1.0; Bitstring Status List (cached revocation).

#### Sub-mode A2: Extended-range / high-speed (C-V2X PC5 Sidelink)

The head unit and a Roadside Unit (RSU), police vehicle terminal, or port gantry exchange credentials over the 5.9 GHz NR-V2X PC5 sidelink. Range is 50–300 m; operates at vehicle speeds up to 250 km/h with latency below 20 ms. No cellular network is involved — it is a direct radio link, making it the same class of exchange as A1 but freed from the proximity and low-speed constraints of BLE/NFC.

Under 3GPP NR-V2X (Release 16/17), the PC5 sidelink supports three transmission modes — broadcast (unsuitable for VC due to privacy exposure), groupcast (useful for port clusters and convoys), and unicast (a bidirectional, authenticated session between two UEs, the mode relevant to VC exchange). Over a unicast PC5 session the vehicle can transmit: (1) a **VC URI** pointing to its credential endpoint for out-of-band retrieval; (2) a **compact VC or VP directly** (SD-JWT VC or ISO mdoc, within NR-V2X payload limits — compact formats preferred); or (3) respond to a **VP request from the RSU** mirroring the QR-initiated flow in ISO 18013-7 but using the sidelink radio as transport.

**V2X security layer vs. VC application layer:** IEEE 1609.2 / ETSI C-ITS SCMS pseudonym certificates authenticate V2X messages at the radio layer but carry no identity claims. The two layers are complementary:

| Layer | Technology | Provides | Lacks |
|---|---|---|---|
| V2X transport auth | IEEE 1609.2 SCMS pseudonym cert | Message authenticity; sender anonymized | Identity claims (registration, insurance, cargo); no holder binding to a specific vehicle |
| Application VC | W3C VC / SD-JWT / ISO mdoc | Structured identity and authorization claims | Transport security; does not replace SCMS |

The pseudonym certificate tells the RSU "this message came from a legitimate V2X device." The VC tells the RSU "this specific vehicle has a valid registration, is insured by X, and is authorized to carry hazmat cargo." Both are needed.

*Standards (current):* 3GPP NR-V2X Release 16/17; IEEE 1609.2 / 1609.2.1; ETSI EN 302 636-x; SAE J2735; 5GAA SCMS Certificate Policy.
*Standards (gaps):* No current standard defines VC payload types for SAE J2735 / ETSI ITS messages; no OpenID4VP profile exists for PC5 unicast transport; no trust federation mechanism links SCMS trust anchors to VC issuer trust anchors. These three gaps must be resolved before interoperable deployment is possible — COVESA, 5GAA, and 3GPP SA6 are the natural homes for the work.

**Operational differences between A1 and A2:**

| | A1 (BLE/NFC/QR) | A2 (C-V2X PC5) |
|---|---|---|
| Range | ~4 cm – 10 m | 50 – 300 m |
| Vehicle speed | Stationary / near-stop | Up to 250 km/h |
| VC protocol | ISO 18013-5 (specified) | Not yet standardized |
| Reader hardware | NFC reader / QR scanner | NR-V2X RSU or V2X-equipped vehicle |
| Transport auth | None / TLS binding | IEEE 1609.2 SCMS pseudonym cert |
| Deployed infrastructure | Widely available | Limited NR-V2X RSU deployments (2026) |

**Shared strengths (both sub-modes):**
- Works without internet — critical in remote corridors, tunnels, and congested enforcement zones
- No third-party cloud observes the exchange; strong privacy
- Cached revocation data (Bitstring Status List) enables offline verification with acceptable staleness window
- Verifier-initiated engagement; the vehicle does not silently expose credentials

**Additional strengths of A2 (C-V2X):**
- Enables credential exchange without stopping — border lanes, weigh station approaches, toll gantries, moving roadside stops (V2V)
- RSU infrastructure is dual-purpose: same hardware serves traffic safety messages (SPaT, MAP) and VC verification
- SCMS trust anchor can vouch for VC issuers, creating a coherent chain from radio layer to application layer

**Shared weaknesses:**
- Real-time revocation requires a network fetch; cached data introduces a staleness window
- Holder-binding to a vehicle (rather than a person) requires adaptation of ISO 18013-5 engagement assumptions (antenna placement, QR display location, pairing model)

**Additional weaknesses of A2 (C-V2X):**
- NR-V2X unicast session establishment takes 50–200 ms; not suitable for sub-100 ms pass-through
- LTE-V2X (Release 14, widely deployed) supports only broadcast sidelink, not unicast — unicast requires NR-V2X (Release 16+) RSUs, which are not yet widely deployed as of 2026
- Head units require a dedicated C-V2X modem (e.g., Qualcomm 9150 C-V2X) in addition to the cellular modem; not all non-GAS AOSP vehicles will have this
- Privacy risk: a unique VC (VIN-linked claims) over V2X radio is linkable across RSUs even with SCMS pseudonym rotation; selective disclosure and short-lived tokens are important mitigations

**A2 venue-specific scenarios:**

*Law enforcement V2V (moving roadside stop):* A police vehicle initiates a unicast PC5 session with a target vehicle's head unit while both are in motion, exchanging a signed VP at highway speed while pacing. The officer's terminal forwards the VP to the MDT for NCIC/CJIS lookup (combining A2 with Model B).

*Border crossing approach lane:* RSUs 200–500 m before the booth initiate a PC5 unicast request. The vehicle assembles and signs a selective disclosure VP (vehicle identity, cargo manifest, customs bond). The officer's terminal receives the pre-verified VP before the vehicle reaches the booth.

*Port of entry hub (Long Beach, Rotterdam):* RSUs at gate lanes authenticate truck credentials (USDOT, cargo, hazmat endorsement) via PC5 unicast or groupcast as the vehicle approaches at low speed. The gate system pre-stages a lane assignment before the barrier.

*Weigh station bypass (PrePass evolution):* Rather than a transponder binary signal, the vehicle transmits a compact signed VC in the approach corridor via PC5 unicast. The enforcement system verifies compliance and sends the bypass/pull-in decision to the vehicle before the loop decision point.

**Best suited for:** UC-1 (A1 stationary, A2 moving V2V), UC-2 (A2 border lane), UC-10 (A1 over ISO 15118 PLC), UC-11 (A1 DSRC, A2 NR-V2X gantry), UC-12 (A1), UC-14 (A1), UC-17 (A1 gate NFC, A2 port approach), UC-19 (A1 stop, A2 weigh station approach), UC-20 (A1 booth, A2 lane pre-check).

---

### Model B: Cloud-to-Client

A cloud service initiates or responds to a credential exchange with the vehicle head unit as the client endpoint. Two sub-patterns:

**Issuance (push):** A cloud issuer — insurer, fleet manager, DMV — delivers a new or updated VC to the head unit wallet via OpenID4VCI or the **W3C VC API** over HTTPS. The head unit is the holder. This is how the POI credential gets into the wallet in the first place, and how fleet assignment credentials are provisioned at scale. The W3C VC API (W3C CCG Community Report) defines a standardized HTTP interface for credential issuance and presentation that is used in CA DMV production deployments; OpenID4VCI is the OpenID Foundation's parallel issuance protocol. Both are viable — implementors should choose based on ecosystem alignment (W3C VC API for COVESA VCV / CA DMV integration; OpenID4VCI for broader OpenID4VP ecosystem interop).

**Presentation request (pull):** A cloud-connected verifier sends an OpenID4VP presentation request to the vehicle over a network channel; the head unit wallet responds with a signed verifiable presentation. The canonical example in this document is the police Mobile Data Terminal (MDT): the officer's MDT is a ruggedized computer connected to law enforcement cloud systems — CJIS, NCIC, and the state DMV — via secure cellular. Rather than carrying a proximity NFC reader, the officer sends a presentation request from the MDT to the vehicle's registered network endpoint. The vehicle's head unit wallet processes the request, applies the requested selective disclosure, and responds with a signed VP. The MDT receives the VP, verifies the signature locally, and can simultaneously forward it to NCIC or a state DMV lookup for cross-reference against outstanding warrants or suspended licenses. This approach reaches vehicles before an officer has left their cruiser, and works even if the officer's reader hardware is unavailable.

**Strengths:**
- No specialized reader hardware required — any networked device can act as a verifier
- Enables proactive issuance: insurers can push an updated POI VC to all fleet vehicles automatically at renewal, without each driver initiating a request
- Presentation requests can be initiated from any networked location, before physical proximity — supports pre-clearance, pre-dispatch, and remote compliance checks
- Audit trail is created at the cloud level, useful for compliance reporting and dispute resolution
- Works for use cases where physical proximity is impractical (vehicle is still en route to a checkpoint)

**Weaknesses:**
- Requires reliable network connectivity at the vehicle — cellular dead zones, tunnels, and remote routes break the flow; not a fallback for offline scenarios
- Introduces a network-exposed endpoint on the vehicle — an attack surface that direct exchange does not have; the vehicle's DID service endpoint must be secured and authenticated
- Network latency adds 1–10 seconds compared to proximity exchange; at highway speed, this matters for toll
- Requires the vehicle to have a stable, resolvable identifier — a DID with a publicly reachable service endpoint, or a registered fleet telematics address — neither of which is yet standardized for AOSP head units
- Privacy implications: the verifier's cloud system learns which vehicle is being queried, from where, and when; this is more exposure than a proximity-only exchange where no third party observes the transaction
- Legal and procedural questions in law enforcement contexts: some jurisdictions require that the driver be present and aware when credentials are presented; an invisible remote request may raise Fourth Amendment (US) or GDPR (EU) issues depending on jurisdiction

**Best suited for:** UC-4 (fleet assignment issuance), UC-5 (POI issuance), UC-9 (UBI issuance and renewal submission), UC-1 (MDT scenario as an alternative to proximity), UC-16 (cross-fleet driver credential issuance), UC-18 (EUDIW issuance from member state provider).

---

### Model C: Cloud-to-Cloud (Machine-to-Machine)

Backend systems exchange VCs or verifiable presentations without direct vehicle or driver involvement at exchange time. The vehicle's credentials have been delivered to a cloud intermediary — a fleet telematics platform, an insurer portal, a DMV registry — and the exchange happens between those backends. The vehicle's signed VC acts as a portable trust artifact that backends can verify independently.

This model is particularly well-suited to the eFNOL flow: the head unit generates and signs the incident VC at the moment of collision, then transmits it to the insurer's `fnolEndpoint`. From that point on, the insurer's backend can exchange the VC with a reinsurer, a body shop network, a law firm, or a government road safety authority — all cloud-to-cloud, with the vehicle's cryptographic signature providing provenance at every step. Similarly, border pre-clearance is cloud-to-cloud: the fleet telematics platform submits a compliance credential bundle to CBP's Automated Commercial Environment (ACE) hours before the truck reaches the crossing; the truck arrives to a pre-cleared signal rather than a manual inspection.

**Strengths:**
- No vehicle connectivity required at exchange time — the credential was delivered earlier and the exchange happens on the backend
- High throughput: a fleet operator can simultaneously pre-clear hundreds of vehicles against a shipper's compliance system, a customs authority, or an insurance underwriter
- Natural fit for batch regulatory reporting: FMCSA HOS submission, IFTA tax filing, emissions compliance — none of which need real-time vehicle involvement
- Reduces point-of-service latency: pre-clearance before arrival eliminates wait at weigh station or border booth
- Enables long-running multi-party workflows: title transfer, cargo contracts, insurance claims — none of which need the vehicle to be active after initial signing

**Weaknesses:**
- The vehicle is not a party to the exchange at the time it occurs — it cannot apply selective disclosure in real time, request consent, or observe what is shared; consent and disclosure scope must be encoded in the credential at issuance time
- The VC held in a cloud system is a copy; if the original is revoked and the cloud copy is stale, the verifier may act on an invalid credential — requires robust, near-real-time revocation propagation to all intermediaries
- The vehicle's signed credential must have been registered or published in advance, which requires an ecosystem of VC registries or fleet identity directories that is still nascent
- The cloud intermediary becomes a trust point: if it is compromised, forged verifiable presentations could be submitted in the vehicle's name; the cryptographic binding of the credential to the vehicle's TEE-backed key provides some protection, but the intermediary's custody of the VC is a risk
- Regulatory frameworks for machine-to-machine VC exchange in fleet contexts are undeveloped; it is unclear whether a cloud-submitted VC satisfies the same legal evidentiary standard as a directly-presented one in all jurisdictions

**Best suited for:** UC-6 (eFNOL submission to insurer), UC-7 (theft alert to insurer/law enforcement), UC-8 (eCall insurance channel), UC-15 (HOS log submission to FMCSA), UC-19 (pre-dispatch compliance submission to shipper), UC-20 (advance customs declaration), UC-3 (title transfer between DMV and buyer's wallet).

---

### Information Flow Diagrams

The following ASCII diagrams show the credential exchange flow for each model. In all cases the vehicle's VC wallet holds credentials in TEE-backed storage on the AOSP head unit.

---

#### Model A1: Direct — Short-range (BLE/NFC/QR)

```
  Vehicle Head Unit
  ┌────────────────────────┐
  │  VC Wallet (TEE)       │
  │  registration VC       │  ← 1. Officer presents QR / NFC tap
  │  POI VC                │  → 2. Head unit engages BLE
  │  mDL (relayed from     │  ← 3. VP request (selective fields)
  │        phone via BLE)  │  → 4. Head unit signs and returns VP
  └────────────────────────┘  ← 5. Verify sig locally; display result

  Reader: officer handheld / weigh station terminal / parking gate
  Range: ~4 cm (NFC) to ~10 m (BLE)   Vehicle speed: stationary

  No internet required. Revocation: cached Bitstring Status List.
```

*Standards:* ISO 18013-5 engagement + BLE data transfer; OpenID4VP 1.0.

---

#### Model A2: Direct — Extended-range (C-V2X PC5 Sidelink)

```
  Infrastructure RSU scenario (border lane / weigh station / port gate)

  Vehicle approaching at speed
  ┌────────────────────────────────────┐
  │  C-V2X modem (PC5) + VC Wallet    │
  │                                    │  5.9 GHz PC5 unicast (~200 m range)
  │  ← VP request from RSU            │  IEEE 1609.2 SCMS pseudonym cert
  │  → signed selective VP            │  + SD-JWT VC payload
  └────────────────────────────────────┘

       ┌──────────────────────────────────────────────────┐
       │  RSU at border / port / weigh station            │
       │  1. Broadcast VP request (OID4VP-over-V2X)       │
       │  2. Receive signed VP over sidelink              │
       │  3. Verify IEEE 1609.2 transport sig             │
       │  4. Verify VC issuer sig (cached public key)     │
       │  5. Check revocation (cached status list)        │
       │  6. Send result → officer terminal / gate ctrl   │
       └──────────────────────────────────────────────────┘
  Vehicle reaches booth already pre-verified.

  V2V scenario (police vehicle pacing target at highway speed)

  ┌───────────────────────┐  PC5 unicast   ┌───────────────────────┐
  │  Police Vehicle       │ ─────────────► │  Target Vehicle       │
  │  V2X terminal + MDT   │  VP request    │  Head Unit VC Wallet  │
  │                       │ ◄───────────── │  signs selective VP   │
  │  verify VP; fwd NCIC  │  SD-JWT VP     │  (TEE-signed)         │
  └───────────────────────┘                └───────────────────────┘

  Layer stack (both scenarios):
  ┌─────────────────────────────────────────────┐
  │  Application: W3C VP / SD-JWT VC / VC URI   │  ← COVESA VCV types
  ├─────────────────────────────────────────────┤
  │  Session: OpenID4VP (V2X profile — gap)     │  ← needs standardization
  ├─────────────────────────────────────────────┤
  │  Transport auth: IEEE 1609.2 SCMS cert      │  ← existing V2X PKI
  ├─────────────────────────────────────────────┤
  │  Radio: 3GPP NR-V2X PC5 (5.9 GHz)          │  ← existing 3GPP/5GAA
  └─────────────────────────────────────────────┘
```

*Standards:* 3GPP NR-V2X Release 16/17; IEEE 1609.2/1609.2.1; ETSI EN 302 636-x; SAE J2735; 5GAA SCMS Certificate Policy; OpenID4VP 1.0 (profile adaptation needed); W3C VC v2.0 / SD-JWT VC.

---

#### Model B: Cloud-to-Client (Issuance push / MDT pull)

```
  ISSUANCE (push)
  ┌──────────────┐   OpenID4VCI    ┌──────────────────────┐
  │  DMV /       │ ──────────────► │  Head Unit VC Wallet │
  │  Insurer     │  (HTTPS/TLS)    │  (TEE storage)       │
  │  Backend     │                 └──────────────────────┘
  └──────────────┘

  PRESENTATION (pull — police MDT scenario)
  ┌──────────────┐  OID4VP request  ┌──────────────────────┐
  │  Officer MDT │ ───────────────► │  Head Unit VC Wallet │
  │  (CJIS net)  │  (vehicle DID    │                      │
  │              │   service EP)    │  signs selective VP  │
  │              │ ◄─────────────── │                      │
  │  verify VP   │   signed VP      └──────────────────────┘
  │  fwd to NCIC │
  └──────┬───────┘
         │ NCIC / state DMV
         ▼  lookup (C2C)
  ┌──────────────┐
  │  Law Enf.    │
  │  Cloud (CJIS)│
  └──────────────┘
```

*Standards:* OpenID4VCI 1.0 (issuance); OpenID4VP 1.0 (presentation); W3C DID service endpoints; CJIS Security Policy (law enforcement network).

---

#### Model C: Cloud-to-Cloud (Machine-to-Machine)

```
  eFNOL example

  ┌──────────────────────────────┐
  │  Vehicle (collision event)   │
  │  ┌────────────────────────┐  │
  │  │  VSS sensors →         │  │  autonomous POST
  │  │  signed incident VC    │──┼──────────────────────────────►
  │  │  (TEE-signed, VIN DID) │  │                    ┌──────────────────┐
  │  └────────────────────────┘  │                    │  Insurer backend │
  └──────────────────────────────┘                    │  (fnolEndpoint)  │
                                                      └────────┬─────────┘
                                                               │ forward VC
                                         ┌─────────────────────┤
                                         ▼                     ▼
                                  ┌────────────┐     ┌──────────────────┐
                                  │ Reinsurer  │     │  Repair Network  │
                                  │  backend   │     │  / Road Safety   │
                                  └────────────┘     │  Authority       │
                                                     └──────────────────┘

  Border pre-clearance example

  ┌────────────────────┐  credential bundle VP   ┌─────────────────────┐
  │  Fleet Telematics  │ ───────────────────────► │  CBP ACE / EU       │
  │  Platform          │  (hours before arrival)  │  Customs EDI        │
  └────────────────────┘                          └──────────┬──────────┘
                                                             │ pre-clear decision
                                                             ▼
                                                  ┌──────────────────────┐
                                                  │  Border booth:       │
                                                  │  confirm/spot-check  │
                                                  │  (proximity or V2X)  │
                                                  └──────────────────────┘
```

*Standards:* W3C VC v2.0; OpenID4VP 1.0; COVESA VCV fnolEndpoint; WCO data model; CBP ACE APIs.

---

### Summary: Exchange Model by Use Case

| UC | Name | Direct A1 (BLE/NFC) | Direct A2 (C-V2X) | Cloud-to-Client (B) | Cloud-to-Cloud (C) | Primary |
|---|---|---|---|---|---|---|
| UC-1 | Roadside Credential Presentation | ✓ (stationary) | ✓ (V2V moving) | ✓ (MDT) | — | A1 or A2 or B |
| UC-2 | Cross-Jurisdiction Presentation | ✓ | ✓ (border lane) | — | ✓ (pre-declaration) | C + A2 |
| UC-3 | Digital Vehicle Title Transfer | — | — | ✓ (issuance) | ✓ (DMV registry) | C |
| UC-4 | Vehicle Assignment Credential | — | — | ✓ (issuance) | — | B |
| UC-5 | Proof of Insurance Credential | — | — | ✓ (issuance) | ✓ (DMV renewal) | B |
| UC-6 | Automated eFNOL | — | — | — | ✓ | C |
| UC-7 | Theft Alert VC | — | — | — | ✓ | C |
| UC-8 | eCall Bridge | — | — | — | ✓ | C |
| UC-9 | UBI Credential | — | — | ✓ (issuance + renewal) | ✓ (telematics) | B + C |
| UC-10 | ISO 15118 Plug & Charge | ✓ (PLC) | — | ✓ (provisioning) | — | A1 |
| UC-11 | Toll Payment | ✓ (DSRC) | ✓ (gantry) | ✓ (cellular) | ✓ (fleet) | A1 or A2 |
| UC-12 | Parking | ✓ | — | ✓ (permit) | — | A1 |
| UC-13 | Fuel and Proximity Retail | ✓ | — | ✓ | — | A1 + B |
| UC-14 | mDL Driver Authentication | ✓ | — | ✓ (revocation) | — | A1 |
| UC-15 | ELD / HOS Driver Identity | — | — | — | ✓ (FMCSA) | C |
| UC-16 | Cross-Fleet Driver Credential | ✓ | — | ✓ (issuance) | — | A1 + B |
| UC-17 | Cargo Endorsement Verification | ✓ (gate NFC) | ✓ (port approach) | ✓ (logistics API) | — | A1 or A2 |
| UC-18 | eIDAS 2.0 / EUDIW Compliance | ✓ | — | ✓ (issuance) | ✓ (regulatory) | A1 + B + C |
| UC-19 | Fleet Compliance Bundle | ✓ (stationary) | ✓ (weigh station) | — | ✓ (pre-dispatch) | C + A2 |
| UC-20 | Commercial Vehicle Border Pre-Clearance | ✓ (booth) | ✓ (lane approach) | — | ✓ (advance) | C + A2 |

---

## VSS Data in Verifiable Credentials

COVESA's Vehicle Signal Specification (VSS) defines a standardized, hierarchical tree of named signals describing vehicle state — speed, acceleration, GPS position, odometer, fuel level, tire pressure, airbag deployment status, engine diagnostics, driver behavior metrics, and more. VSS signals are identified by dot-notation paths (e.g., `Vehicle.Speed`, `Vehicle.ADAS.ABS.IsActive`, `Vehicle.CurrentLocation.Latitude`) and carry typed values with defined units.

When vehicle data needs to accompany a VC — either as proof of what the vehicle was doing at a moment in time, or as the subject of a consent or insurance claim — there are two distinct integration patterns. Both are appropriate in different circumstances and are not mutually exclusive.

---

### Pattern 1: VSS Claims Embedded Inside a VC

VSS signal values are encoded directly as claims within the VC's credential subject. The VC issuer (typically the head unit's on-board wallet software, acting as a self-sovereign issuer on behalf of the vehicle DID) signs the entire payload, making the VSS data cryptographically bound to the vehicle identity and tamper-evident.

**Structure:** Each VSS signal becomes a claim key–value pair in the credential subject, using the VSS path as the claim name or mapped to a COVESA VCV vocabulary term:

```json
{
  "@context": ["https://www.w3.org/ns/credentials/v2", "https://covesa.org/vss/v1"],
  "type": ["VerifiableCredential", "VehicleIncidentCredential"],
  "issuer": "did:example:vehicle:VIN1234567890",
  "issuanceDate": "2026-08-12T14:32:01Z",
  "credentialSubject": {
    "id": "did:example:vehicle:VIN1234567890",
    "incidentTimestamp": "2026-08-12T14:31:58Z",
    "Vehicle.Speed": 72.4,
    "Vehicle.Acceleration.Longitudinal": -8.3,
    "Vehicle.CurrentLocation.Latitude": 37.4419,
    "Vehicle.CurrentLocation.Longitude": -122.1430,
    "Vehicle.Chassis.Axle.Row1.Airbag.IsDeployed": true,
    "Vehicle.OBD.RelativeThrottlePosition": 0.0
  }
}
```

**When this is the right pattern:**

- **Incident VCs (eFNOL, UC-6):** The collision event is a single moment in time. A small set of VSS signals at the instant of impact — speed, acceleration, GPS, airbag status — are the legally relevant facts. Embedding them directly in the signed VC makes them inseparable from the vehicle's identity assertion; the insurer receives a single artifact that is self-describing, cryptographically signed, and immediately verifiable without a separate data channel.

- **Theft alert VCs (UC-7):** Location trajectory (a time-series of `Vehicle.CurrentLocation.*` samples) embedded as a claim array captures the vehicle's path from the moment unauthorized movement was detected. Small enough for a VC payload; legally significant as a signed, timestamped trail.

- **UBI consent and attestation VCs (UC-9):** Aggregate VSS-derived statistics — total miles (`Vehicle.TraveledDistance`), hard-braking event count, night-driving fraction — are enrolled as claims in the UBI attestation VC that the driver presents at renewal. Selective disclosure (SD-JWT) allows the driver to reveal only the summary statistics the insurer is contractually entitled to, not the raw trip data.

- **EV charging session VCs (UC-10, fleet billing):** `Vehicle.Powertrain.TractionBattery.StateOfCharge.Current`, session start/end timestamps, and energy delivered can be embedded in the charging session VC, creating a verifiable receipt bound to the vehicle identity — useful for fleet cost allocation and tax credit documentation.

- **eCall bridge VC (UC-8):** The same signal snapshot as the FNOL case, delivered on the parallel insurer channel alongside the eCall PSAP notification.

**Design constraints for embedded VSS claims:**

- **Payload size:** VC payloads transmitted over BLE (ISO 18013-5) or C-V2X sidelink (Model A2) are constrained. A single-moment snapshot (8–15 VSS signals) is feasible; a multi-minute time series is not. For the proximity and V2X exchange models, compact formats (SD-JWT VC, CBOR-encoded mdoc) are preferable over JSON-LD for VSS claim payloads.
- **Claim namespace:** VSS paths should be declared in a `@context` extension (`https://covesa.org/vss/v1` or equivalent) so verifiers can resolve the semantics without ambiguity. COVESA VCV is the natural home for registering these claim types.
- **Attestation chain:** The head unit wallet is the self-sovereign issuer of the VSS-containing VC, using the vehicle's TEE-backed DID key. An attached telematics device (e.g., a GO device) can co-sign as a second endorser, attesting that the sensor values were calibrated and unmodified at the time of capture — important for legal evidentiary weight.
- **Selective disclosure:** VSS claims in an SD-JWT VC can be individually blinded, allowing a driver to prove "my speed was below the limit" without revealing the exact value, or to prove an airbag deployed without exposing GPS coordinates.

---

### Pattern 2: VC + Separate VSS Payload (Dual-Channel)

The VC and the VSS data travel as distinct artifacts. The VC is a lightweight authorization or consent token — it identifies the vehicle, asserts what data may be shared, defines the scope of consent, and carries a reference (hash or URI) to the VSS data. The VSS data itself is delivered via a separate channel appropriate to its volume and timing: a COVESA VISS WebSocket stream, a W3C SSEP feed, a telematics platform API, or a compressed archive.

**Why a separate channel:**

Some VSS use cases involve data volumes or streaming patterns that do not fit inside a VC payload:

- A 30-minute trip log at 10 Hz sampling across 20 signals is hundreds of thousands of data points — far beyond any VC transport budget.
- Real-time streaming (e.g., a live feed to an insurer's risk model during a test drive) is a continuous channel, not a point-in-time credential.
- Regulatory submissions (HOS logs, emissions data) may require structured VSS-format files in specific schemas that are too large to embed.

In these cases the VC acts as a **capability token and provenance anchor**: it asserts that the vehicle (identified by its DID) consents to sharing a defined set of VSS signals over a defined period, and it carries a cryptographic commitment (content hash or Merkle root) to the VSS data so that a verifier can confirm the data was not altered after the VC was issued.

**Structure:**

```
┌────────────────────────────────────────┐     ┌─────────────────────────────┐
│  VC (signed by vehicle DID)            │     │  VSS Data Payload           │
│  - vehicle identity claims             │     │  (VISS stream / file)       │
│  - consent scope (signal list,         │     │  - Vehicle.Speed[]          │
│    time window)                        │     │  - Vehicle.CurrentLocation[]│
│  - data hash / Merkle root  ──────────►│────►│  - Vehicle.Powertrain.*[]  │
│  - vssEndpoint URI                     │     │  - ...                      │
└────────────────────────────────────────┘     └─────────────────────────────┘
         VC delivered once                       Data streamed or batched
         (OpenID4VCI or VC issuance)             (COVESA VISS / HTTP / MQTT)
```

**When this is the right pattern:**

- **UBI telematics data collection (UC-9):** The insurer needs weeks of trip data. The UBI VC encodes the driver's consent (which signals, what time window, which aggregation policy) and a VISS endpoint URI. The telematics platform pulls the VSS stream from the vehicle using the VC as the authorization token. At renewal, a separate attestation VC encodes the aggregate summary statistics derived from that stream.

- **Fleet compliance reporting — HOS / IFTA (UC-15, UC-19):** The VC is the driver identity and consent assertion; the underlying ELD log (VSS-formatted trip segments, driver activity states keyed to `Vehicle.Driver.*` signals) is submitted as a structured file to FMCSA. The VC's hash commitment lets FMCSA verify the log file matches what the vehicle signed.

- **Emissions compliance (UC-19, fleet):** `Vehicle.OBD.*` and `Vehicle.Powertrain.*` signals over a reporting period are submitted as a VSS data file. The VC asserts vehicle identity and calibration attestation; the emissions authority verifies the data file against the VC's hash.

- **Port and border pre-clearance (UC-20):** The cargo manifest VC references a VSS-encoded cargo sensor payload (load cell readings, refrigeration temperature via `Vehicle.Cargo.*` signals if defined in the VSS extension) as a separate attachment. Customs can verify both the manifest credential and the sensor data independently.

- **Live ADAS or safety data sharing (future):** A research institution or road safety authority requests live ADAS signal data from a fleet. The VC encodes consent and data access scope; the institution receives a VISS WebSocket stream authenticated by the VC. This pattern aligns with W3C VISS v2 / SSEP capability negotiation.

**Design constraints for dual-channel pattern:**

- **Hash commitment:** The VC must carry a cryptographic commitment to the VSS data (SHA-256 content hash of the data file, or Merkle root of a time-series batch) at issuance time. This requires the data to be finalized before the VC is signed — workable for historical data (trip logs, incident snapshots post-processing) but not for live streams; for streaming use cases, the VC scopes the consent and the stream is authenticated by the vehicle's DID separately.
- **VSS endpoint reference:** A `vssEndpoint` URI in the VC credentialSubject (analogous to the existing `fnolEndpoint` pattern in COVESA VCV) points to the VISS server or data API where the VSS data can be retrieved. The verifier authenticates to this endpoint using the VC as the bearer credential.
- **COVESA VISS alignment:** W3C Vehicle Information Service Specification (VISS) v2 defines the REST/WebSocket API for accessing VSS signals from a vehicle server. The dual-channel pattern maps naturally onto VISS: the VC is the authorization artifact; VISS is the data delivery channel. A `vssEndpoint` claim pointing to a VISS server URI, combined with OpenID4VP for VC presentation as the auth step, would constitute a complete, standards-based vehicle data sharing protocol.

---

### VSS Integration Summary by Use Case

| UC | VSS Role | Pattern | Key VSS Signals |
|---|---|---|---|
| UC-6 (eFNOL) | Incident evidence — speed, location, airbag at moment of impact | Embedded in VC | `Vehicle.Speed`, `Vehicle.Acceleration.*`, `Vehicle.CurrentLocation.*`, `Vehicle.Chassis.Axle.Row1.Airbag.IsDeployed` |
| UC-7 (Theft alert) | Location trajectory from detection to recovery | Embedded in VC (array of timestamped samples) | `Vehicle.CurrentLocation.*`, `Vehicle.Speed` |
| UC-8 (eCall bridge) | Same incident snapshot as UC-6, parallel insurer channel | Embedded in VC | Same as UC-6 |
| UC-9 (UBI) | Consent scope and aggregate stats in VC; raw trip data via separate feed | Dual-channel | `Vehicle.TraveledDistance`, `Vehicle.Speed` (aggregated), `Vehicle.Driver.AttentiveProbability` (if available) |
| UC-10 (Plug & Charge) | Charging session receipt — energy delivered, SoC delta | Embedded in VC | `Vehicle.Powertrain.TractionBattery.StateOfCharge.Current`, session timestamps |
| UC-15 (ELD / HOS) | Driver activity log submitted as VSS file; VC provides identity + hash commitment | Dual-channel | `Vehicle.Driver.*`, trip waypoints, duty-status state transitions |
| UC-19 (Fleet compliance) | Emissions and diagnostic data filed as VSS batch; VC is identity + calibration attestation | Dual-channel | `Vehicle.OBD.*`, `Vehicle.Powertrain.*` |
| UC-20 (Border pre-clearance) | Cargo sensor attestation attached to cargo manifest VC | Dual-channel | `Vehicle.Cargo.*` (VSS extension), refrigeration temp, load sensor readings |

---

### Gap: VSS Claim Vocabulary in COVESA VCV

Currently, COVESA VCV defines credential types for vehicle registration, proof of insurance, and incident reporting, but does not yet formally register VSS signal paths as named claim types within the VCV vocabulary. Doing so would:

1. Allow verifiers to resolve the semantics of VSS claims in a VC without a custom context extension per deployment
2. Enable selective disclosure policies to be expressed in terms of named VSS claim groups (e.g., "location claims", "powertrain claims") rather than individual signal paths
3. Provide a shared namespace for the `vssEndpoint` URI scheme and the dual-channel data reference pattern

This is a concrete work item for COVESA VCV in coordination with the Commercial Vehicles WG and the AOSP wallet workstream.

---

## Use Cases

### Category 1: Government Identity & Vehicle Credentials

**UC-1: Roadside Credential Presentation**

A law enforcement officer or roadside inspector presents a QR code or NFC tap; the head unit wallet presents the vehicle registration credential and the driver's mDL via ISO 18013-5 / OpenID4VP. Selective disclosure limits the presentation to legally required fields.

*Standards:* ISO 18013-5, OpenID4VP 1.0, COVESA VCV (registration), W3C VC selective disclosure.  
*Wallet layer:* Proximity presentment (BLE/NFC from head unit); Multipaz `identity-android` proximity APIs.

*Exchange model:* **Direct A1 (stationary), Direct A2 (C-V2X V2V moving), and Cloud-to-Client MDT (B).**

The proximity flow — officer holds a BLE/NFC reader to the vehicle — is the baseline. It requires no network, provides strong privacy, and is driver-visible. The MDT (Mobile Data Terminal) alternative is increasingly relevant: the officer's ruggedized in-cruiser computer, connected to CJIS/NCIC and the state DMV over secure cellular, sends an OpenID4VP presentation request to the vehicle's registered network endpoint. The vehicle responds with a signed VP; the MDT verifies it locally and can forward to NCIC for outstanding warrant or suspended-license checks simultaneously. The MDT model eliminates the need for the officer to carry a proximity reader, and allows credential verification before the officer exits the cruiser. The tradeoff is that it requires network connectivity and a registered vehicle endpoint — and raises procedural questions in jurisdictions where credential presentation must be driver-visible and consensual.

A third path is emerging via **C-V2X sidelink (Model A2, V2V)**: a police vehicle equipped with an NR-V2X PC5 terminal initiates a unicast sidelink session with the target vehicle's C-V2X modem while both are in motion. The VC wallet on the target vehicle's head unit responds with a signed selective-disclosure VP (registration, insurance, license status) transmitted over the 5.9 GHz sidelink. This enables credential exchange without either vehicle stopping — while pacing alongside at highway speed, within the ~200 m sidelink range. The VP is then forwarded from the officer's V2X terminal to the MDT for NCIC/CJIS cross-reference. This approach depends on the target vehicle having an NR-V2X-capable modem in addition to the AOSP head unit, and on a profile of OpenID4VP adapted for PC5 unicast transport rather than HTTP — neither of which is standardized yet.

---

**UC-2: Cross-Jurisdiction Credential Presentation**

A vehicle traveling across state or national borders presents jurisdiction-specific credentials from the head unit wallet to the appropriate verifier. The wallet resolves which credential format the verifier requires (mdoc vs. W3C VC) and presents accordingly.

*Standards:* ISO 18013-5, W3C VC v2.0, OpenID4VP 1.0, COVESA VCV.

*Exchange model:* **Direct A1 (at fixed readers), Cloud-to-Cloud (C, advance declaration), and Direct A2 (C-V2X, lane approach).**

At fixed border or weigh station readers, proximity exchange via ISO 18013-5 BLE/NFC is the natural mode — the vehicle stops, the reader is fixed infrastructure. Cloud-to-cloud advance declaration is a complementary mode: a fleet telematics platform submits a credential bundle to the relevant customs authority (CBP ACE in the US, customs EDI systems in the EU) hours before the vehicle arrives, enabling pre-clearance decisions without any at-the-booth exchange. C-V2X sidelink adds a third path: RSUs deployed at the approach lane initiate a PC5 unicast session with the vehicle 200–500 m before the booth, exchange the credential bundle at approach speed, and deliver a pre-verification result to the officer's terminal before the vehicle arrives. This is the use case where V2X delivers the clearest operational value over BLE/NFC: the vehicle need not stop for the credential exchange, and the approach-lane RSU investment serves both credential verification and traffic safety messaging (SPaT, work zone warnings) on shared infrastructure.

---

**UC-3: Digital Vehicle Title Transfer**

When a vehicle is sold, the title VC is cryptographically revoked by the issuing DMV and a new credential issued to the new owner via the Bitstring Status List revocation mechanism. Eliminates paper title delays.

*Standards:* W3C VC v2.0, Bitstring Status List v1.0, COVESA VCV (title), W3C DIDs.

*Exchange model:* **Cloud-to-Client (issuance) and Cloud-to-Cloud (registry).**

The seller's title VC revocation and the buyer's new credential issuance are both cloud-initiated events. The new owner's head unit receives the title VC via OpenID4VCI from the DMV issuer backend. Registry cross-checks between DMV, lienholder, and insurance systems are cloud-to-cloud. There is no meaningful proximity component — title transfer is a background administrative event, not a real-time presentation.

---

**UC-4: Vehicle Assignment Credential**

A fleet operator issues a time-scoped vehicle assignment credential to an authorized driver. The head unit wallet verifies the credential at ignition. Revocation propagates in near-real-time when the assignment expires.

*Standards:* W3C VC v2.0, DID-based issuance, Bitstring Status List, OpenID4VP 1.0.

*Exchange model:* **Cloud-to-Client (issuance).**

The fleet management system delivers the assignment credential to the head unit via OpenID4VCI. Verification at ignition is local — the head unit checks the credential's signature and revocation status without a network round-trip, which is important for vehicles in areas with poor connectivity. This is a pure cloud-to-client issuance use case; the presentation (at ignition) is device-local, not a network exchange.

---

### Category 2: Insurance — First Notice of Loss (FNOL)

**UC-5: Proof of Insurance (POI) Credential**

The insurer issues a POI VC to the vehicle's head unit wallet containing: policy number, coverage type, validity period, insurer DID, and a `fnolEndpoint` URI. The driver presents the POI VC on demand via selective disclosure.

*Standards:* W3C VC v2.0, COVESA VCV (proof of insurance), OpenID4VP 1.0, W3C DIDs.  
*Gap:* `fnolEndpoint` URI scheme to be standardized in VCV.

*Exchange model:* **Cloud-to-Client (issuance) and Cloud-to-Cloud (DMV verification at registration renewal).**

The insurer pushes the POI VC to the head unit at policy inception and renewal via OpenID4VCI — a cloud-to-client issuance. At a traffic stop the driver presents it via proximity. The DMV can verify insurance status at registration renewal by querying the insurer's backend directly (cloud-to-cloud), cross-referencing the VC credential ID against the issuer's registry without requiring the driver to present the credential at a DMV office. Both the issuance and the DMV-side verification benefit significantly from the cloud model; the proximity presentation at roadside is the fallback.

---

**UC-6: Automated eFNOL Submission**

On a triggering event (collision detection via airbag deployment, G-force threshold, or geofence breach), the head unit wallet generates and signs an incident VC (GPS coordinates, speed/heading, VSS-encoded sensor readings, timestamp, vehicle DID) and delivers it to the `fnolEndpoint` in the POI credential. A co-signature from an attached telematics device attests sensor calibration and data integrity. FNOL lag reduced from days to minutes.

*Standards:* W3C VC v2.0, COVESA VSS, COVESA VCV (incident), W3C DIDs, OpenID4VP 1.0.  
*Reference:* [COVESA FNOL VC Standards Report](https://github.com/COVESA/commercial-vehicles/blob/main/reports/connected-vehicle-fnol-vc-standards.md)  
*VSS:* **Embedded (Pattern 1).** `Vehicle.Speed`, `Vehicle.Acceleration.Longitudinal`, `Vehicle.CurrentLocation.*`, `Vehicle.Chassis.Axle.Row1.Airbag.IsDeployed`, `Vehicle.OBD.RelativeThrottlePosition` — signed as VC claims at the moment of impact.

*Exchange model:* **Cloud-to-Cloud (primary).**

The head unit autonomously submits the signed incident VC to the insurer's `fnolEndpoint` over HTTPS. There is no human or proximity reader involved — the vehicle is acting as an autonomous agent. Once in the insurer's system, the VC becomes a cloud artifact that can be exchanged with reinsurers, repair networks, road safety authorities, and legal systems entirely in the cloud. This is the use case most clearly served by cloud-to-cloud: the vehicle generates the credential, but everything that follows is machine-to-machine. Proximity exchange is not applicable — there is no verifier physically present at the moment of collision.

---

**UC-7: Theft Alert VC**

On detection of unauthorized vehicle movement, the head unit wallet generates a signed theft VC with location trajectory. The wallet routes a verifiable presentation to the insurer endpoint and optionally to a law enforcement endpoint. Vehicle DID provides a cryptographic chain of custody persistent even if the head unit is later tampered with (key material in TEE/StrongBox).

*Standards:* W3C VC v2.0, OpenID4VP 1.0, W3C DIDs, COVESA VCV (theft incident).  
*VSS:* **Embedded (Pattern 1).** Time-series array of `Vehicle.CurrentLocation.*` and `Vehicle.Speed` samples from detection event onward; small enough to embed directly as a VC claim array.

*Exchange model:* **Cloud-to-Cloud (primary).**

The vehicle submits the theft VC to the insurer and law enforcement endpoints autonomously, with no occupant present. From those cloud endpoints, the credential can be forwarded to law enforcement dispatch systems, recovery networks, and insurance investigators — all cloud-to-cloud. The TEE-backed vehicle DID ensures the credential's provenance is verifiable even if the physical device is later recovered tampered.

---

**UC-8: eCall Bridge**

EU eCall notifies emergency services; a parallel VC-signed channel notifies the insurer simultaneously. The head unit wallet holds both the emergency contact credential and the POI VC and fires both channels on the same trigger event.

*Standards:* EU eCall (112), W3C VC v2.0, COVESA VCV (POI + incident).  
*VSS:* **Embedded (Pattern 1).** Same snapshot as UC-6 — the parallel insurer VC carries the same VSS signal claims as the FNOL credential, signed by the vehicle DID at the moment the eCall trigger fires.

*Exchange model:* **Cloud-to-Cloud (primary).**

eCall's existing D2D (device-to-PSAP) channel handles the emergency services notification via the standardized eCall protocol. The parallel VC submission to the insurer is a separate cloud push from the vehicle. Both are autonomous vehicle-initiated actions with no driver interaction. Once received by the insurer, further exchanges with reinsurers or road safety bodies are cloud-to-cloud.

---

**UC-9: Usage-Based Insurance (UBI) Credential**

The insurer issues a UBI policy credential held in the head unit wallet with embedded telematics consent terms. At renewal, the driver presents a selective disclosure proof (aggregate miles, risk band) without exposing raw trip data. Consent and data minimization are enforced at the VC layer.

*Standards:* W3C VC v2.0, SD-JWT VC, COVESA VSS (odometer, driving behavior), OpenID4VP 1.0.  
*VSS:* **Dual-channel (Pattern 2).** The UBI policy VC encodes consent scope (which signals, which time window) and a `vssEndpoint` URI. Raw trip data — `Vehicle.TraveledDistance`, `Vehicle.Speed` samples, hard-braking events — streams via COVESA VISS to the telematics platform. At renewal, a separate SD-JWT attestation VC embeds aggregate statistics (`Vehicle.TraveledDistance` total, risk-band score) as selectively-disclosable claims so the driver can prove aggregate behavior without exposing raw trip data.

*Exchange model:* **Cloud-to-Client (issuance and renewal), Cloud-to-Cloud (telematics aggregation).**

Issuance is cloud-to-client: the insurer delivers the UBI credential to the head unit wallet via OpenID4VCI. Telematics data aggregation — the underlying data that informs the risk score — is cloud-to-cloud between the telematics platform and the insurer. At renewal, the driver can present a selective disclosure VP either by proximity (e.g., on an insurer's web portal via OpenID4VP browser flow), or the insurer's backend can request the VP from the vehicle's registered endpoint (cloud-to-client pull). The cloud model for renewal is preferable because it does not require the driver to visit an office or interact with a kiosk; the insurer queries the vehicle directly.

---

### Category 3: In-Vehicle Payments

**UC-10: ISO 15118 Plug & Charge with VC Identity Binding**

The head unit wallet holds an EV contract credential. The vehicle authenticates to the charging station via ISO 15118-20, with the contract credential linking payment authorization to a verifiable vehicle identity (DMV-issued). Fleet billing splits charging costs to the correct cost center automatically. ISO 15118 is a vehicle-to-charger protocol — head unit is the only viable holder.

*Standards:* ISO 15118-20 (EU AFIR mandate Jan 2027), W3C VC v2.0, COVESA VCV (vehicle identity, EV contract).  
*Alignment:* COVESA In-Car Wallet project (Plug & Charge demonstrations underway).  
*VSS:* **Embedded (Pattern 1) for fleet billing.** `Vehicle.Powertrain.TractionBattery.StateOfCharge.Current` (start and end), energy delivered, and session timestamps embedded in the charging session VC — creating a verifiable receipt bound to the vehicle DID for fleet cost allocation and tax credit documentation.

*Exchange model:* **Direct A1 (at the charger, primary) and Cloud-to-Client (contract provisioning).**

The ISO 15118-20 protocol is inherently proximity-based: the vehicle connects to the charger physically, and the certificate and contract credentials are exchanged over the power line communication (PLC) channel or vehicle-to-grid (V2G) network — no cellular required at exchange time. This makes Plug & Charge one of the few use cases where proximity is mandated by the underlying protocol rather than chosen for convenience. Cloud-to-client applies to the upstream provisioning: the e-mobility service provider (eMSP) delivers the contract certificate to the vehicle's head unit via OpenID4VCI before the charging session begins.

---

**UC-11: Toll Payment with Vehicle Identity Binding**

The head unit wallet presents a payment credential bound to a vehicle identity credential for toll processing. Identity binding enables fleet accounts, dispute resolution, and tax documentation. Verification at highway speed.

*Standards:* W3C VC v2.0, ISO 18013-5, OpenID4VP 1.0, COVESA VCV (vehicle identity).  
*Industry precedent:* Mastercard/Volvo/NC Turnpike pilot (2025).

*Exchange model:* **Direct A1 (DSRC), Direct A2 (C-V2X gantry), Cloud-to-Client (B, cellular-assisted), and Cloud-to-Cloud (C, fleet reconciliation).**

Toll is a four-layer use case. The at-speed transaction itself is proximity-like (DSRC at 5.9 GHz, which does not use ISO 18013-5 but is structurally a device-to-reader exchange at the gantry). Cellular-assisted tolling — where the vehicle's head unit presents a VP to the toll authority's backend via a cellular connection — is cloud-to-client and trades sub-100ms latency for the ability to handle complex credential logic (fleet accounts, tax exemptions) that DSRC's narrow window cannot support. Fleet account reconciliation — the toll authority submitting a signed trip VC to the fleet operator's billing system — is cloud-to-cloud. NR-V2X sidelink at 5.9 GHz is the natural evolution path for gantry tolling: rather than DSRC (WAVE, IEEE 802.11p), a C-V2X RSU at the gantry can initiate a PC5 unicast session with the approaching vehicle and receive a signed, fleet-identity-bound VC directly — providing richer payment authorization data than a transponder beep, at comparable sub-100ms latency, within the existing 5.9 GHz band allocation.

---

**UC-12: Parking with Verified Vehicle Identity**

The head unit wallet presents a fleet payment credential plus vehicle identity credential at a connected parking facility. Enables permit validation, automated expense allocation, and ticketless exit.

*Standards:* W3C VC v2.0, OpenID4VP 1.0, COVESA VCV (vehicle identity).

*Exchange model:* **Direct A1 (gate reader) and Cloud-to-Client (permit validation).**

At the entry gate, proximity exchange via QR or NFC is the natural mode — fast, reliable, works in underground garages with poor cellular. Permit validation (confirming the vehicle is on an approved corporate list) can be a cloud-to-client call from the parking management system to the fleet's credential registry, without requiring the driver to present anything explicitly.

---

**UC-13: Fuel and Proximity Retail**

Geolocation triggers payment credential presentation at a fueling station. Fleet fuel credentials as VCs enforce spend controls at the credential level, enabling richer policy without per-merchant backend integrations.

*Standards:* W3C VC v2.0, OpenID4VP 1.0, COVESA VCV (fleet credential).

*Exchange model:* **Direct A1 (at the pump) and Cloud-to-Client (merchant POS verification).**

The fuel station's point-of-sale system can act as either a proximity reader (NFC/QR at the pump) or a cloud-to-client verifier that requests a VP from the vehicle's registered endpoint when the vehicle's presence is detected geofencing-style. The cloud-to-client model enables richer fleet policy enforcement — the merchant's backend can query the fleet's fuel credit limit in real time — but requires connectivity. The proximity model is simpler and faster for most retail scenarios.

---

### Category 4: Driver Identity & Access

**UC-14: mDL-Based Driver Authentication**

Driver's mDL (stored in head unit wallet, or relayed from phone via BLE/NFC per CCC Digital Key 3.0) authenticates at ignition. Cryptographic verification replaces PIN entry; the head unit logs a verifiable driver identity record.

*Standards:* ISO 18013-5, CCC Digital Key 3.0, W3C DIDs, OpenID4VP 1.0.

*Exchange model:* **Direct A1 (primary), with Cloud-to-Client for revocation.**

Driver authentication at ignition is a local proximity exchange: the mDL credential (from phone via BLE, or from head unit wallet) is presented to the head unit's verifier component, which checks the signature locally. Revocation checking — confirming the driver's license has not been suspended since the credential was issued — requires a network fetch of the Bitstring Status List from the DMV's endpoint. In connectivity-constrained environments, cached revocation data with a defined staleness window is acceptable. The cloud model is not appropriate for ignition authorization itself — introducing a network dependency on starting the vehicle creates an unacceptable failure mode.

---

**UC-15: ELD / HOS Driver Identity**

FMCSA ELD mandate requires verified driver identity for Hours of Service logs. A VC-based driver credential presented to the head unit replaces manual driver ID entry, binds the HOS log to a cryptographically verified identity.

*Standards:* ISO 18013-5, W3C VC v2.0, FMCSA ELD mandate (49 CFR Part 395).  
*VSS:* **Dual-channel (Pattern 2).** The driver identity VC carries the cryptographic identity binding; the HOS log itself — trip segments, duty-status state transitions keyed to `Vehicle.Driver.*` signals, odometer readings from `Vehicle.TraveledDistance` — is submitted as a structured VSS-formatted file with the VC providing a hash commitment and identity attestation.

*Exchange model:* **Cloud-to-Cloud (HOS submission to FMCSA).**

The driver identity binding at the ELD is local (proximity or device-local verification). The significant exchange is the submission of the HOS log — now carrying a VC-signed driver identity — from the fleet's telematics platform to FMCSA's systems. This is a cloud-to-cloud workflow: the fleet backend packages the signed HOS records as a verifiable presentation and submits them to FMCSA's Electronic Logging Device portal. The cryptographic driver identity binding in the VC replaces the current reliance on self-reported driver ID, which is a known audit weakness.

---

**UC-16: Cross-Fleet Driver Credential**

In rental, rideshare, or multi-operator fleet scenarios, a driver presents a universal credential (DID + mDL + operator endorsements) to the head unit wallet. Any compatible vehicle verifies the credential without carrier-specific application installation.

*Standards:* W3C VC v2.0, ISO 18013-5, W3C DIDs, OpenID4VP 1.0.

*Exchange model:* **Cloud-to-Client (issuance of operator endorsement VC) and Direct A1 (presentation to vehicle).**

The operator endorsement credential — authorizing the driver to operate a specific class or fleet of vehicles — is issued cloud-to-client by the fleet operator's management system. The driver carries it in their phone wallet or the head unit. Presentation at ignition is proximity: the driver's device presents the credential to the vehicle's head unit verifier locally. The cross-fleet model requires a shared credential schema (COVESA VCV driver endorsement type) so that Vehicle A and Vehicle B, operated by different fleet companies, can both verify the same credential without a common backend.

---

**UC-17: Cargo Endorsement Verification**

Transporting regulated cargo (alcohol, pharmaceuticals, hazardous materials) requires verified driver endorsements. The head unit wallet presents the relevant credential at cargo pickup, creating a verifiable chain of custody before the vehicle leaves the terminal.

*Standards:* ISO 18013-5, W3C VC v2.0, OpenID4VP 1.0, COVESA VCV (driver endorsement).

*Exchange model:* **Direct A1 (terminal gate reader), Cloud-to-Client (B, logistics platform API), and Direct A2 (C-V2X, port gate lane).**

At a physical terminal gate, proximity exchange via QR or NFC is the primary mode — the gate reader verifies the driver's endorsement credential before raising the barrier. The logistics platform can also verify endorsements via a cloud-to-client request to the driver's registered endpoint as part of electronic dispatch, before the driver physically arrives — confirming endorsement validity at load assignment rather than at gate, which prevents a wasted trip if a license has lapsed. At high-throughput port and intermodal terminal gates (Long Beach, Rotterdam), C-V2X RSUs mounted at the gate lane can authenticate both the vehicle credentials and the driver's cargo endorsements via PC5 sidelink groupcast as the truck approaches the weigh-in station at low speed — allowing the gate control system to pre-stage a lane assignment before the truck reaches the barrier, reducing dwell time in congested gate queues.

---

### Category 5: Regulatory & Compliance

**UC-18: eIDAS 2.0 / EUDIW In-Vehicle Compliance**

EU member states must offer EUDIW by late 2026; regulated sectors must accept them. An AOSP head unit wallet implementing the EUDIW attestation interface satisfies the in-vehicle presentation requirement for insurance cards, vehicle registration, and driver identity across EU jurisdictions.

*Standards:* eIDAS 2.0, EUDIW attestation format, W3C VC v2.0, ISO 18013-5.  
*Wallet layer:* EUDI Android library set.

*Exchange model:* **All three models apply (A1, B, and C).**

EUDIW credential issuance from member state providers is cloud-to-client (OpenID4VCI). In-vehicle presentation to law enforcement, border agents, or insurance verifiers is proximity. Regulatory reporting — the member state demonstrating wallet deployment and usage statistics to the European Commission — is cloud-to-cloud. This use case sits at the intersection of all three models and is the strongest argument for the COVESA AOSP wallet supporting all three exchange paths rather than optimizing for one.

---

**UC-19: Fleet Compliance Credential Bundle**

A single verifiable presentation from the head unit containing: USDOT number VC, vehicle inspection VC, emissions compliance VC, IFTA tax credential, driver qualification file VC. Revocation status checked at presentation time. Presented to shipper at dispatch or enforcement at roadside.

*Standards:* W3C VC v2.0, Bitstring Status List, OpenID4VP 1.0, COVESA VCV (compliance bundle), FMCSA/DOT data schemas.  
*VSS:* **Dual-channel (Pattern 2) for emissions and diagnostics.** The compliance bundle VC asserts vehicle identity, inspection status, and regulatory credentials. A separate VSS batch file of `Vehicle.OBD.*` and `Vehicle.Powertrain.*` readings over the reporting period is submitted alongside the VC for emissions compliance verification, with the VC carrying a hash commitment to the data file.

*Exchange model:* **Direct A1 (roadside weigh station, stationary), Cloud-to-Cloud (C, pre-dispatch shipper), and Direct A2 (C-V2X, weigh station approach).**

At a roadside weigh station, the enforcement officer's fixed reader requests the compliance bundle via proximity exchange (vehicle stops). Pre-dispatch, the fleet operator's backend submits the same bundle to the shipper's compliance system via cloud-to-cloud — confirming the truck is legal to load before the driver arrives at the terminal. The pre-dispatch cloud-to-cloud flow is arguably higher value: catching a lapsed IFTA credential or an overdue inspection before the truck is loaded prevents a wasted trip and potential enforcement action. C-V2X sidelink extends the roadside weigh station scenario: RSUs in the weigh-station approach corridor can initiate a PC5 unicast session with the truck at highway speed, receive the compliance bundle VC, and transmit a bypass/pull-in decision to the vehicle's head unit before the driver reaches the bypass loop — mirroring what PrePass transponders do today but with cryptographically verifiable credential content rather than a simple binary signal.

---

**UC-20: Commercial Vehicle Border Pre-Clearance**

A commercial vehicle approaching a border crossing presents a credential bundle (vehicle registration, cargo manifest VC, driver identity, customs bond, hazmat declaration) from the head unit wallet via ISO 18013-5 / OpenID4VP. Pre-clearance decisions are made before the vehicle reaches the booth.

*Standards:* ISO 18013-5, W3C VC v2.0, OpenID4VP 1.0, COVESA VCV (cargo manifest, vehicle, driver credentials), WCO data model alignment.  
*VSS:* **Dual-channel (Pattern 2) for cargo sensor data.** The cargo manifest VC references a VSS-encoded cargo sensor payload — refrigeration temperature, load cell readings, hazmat container seal status via `Vehicle.Cargo.*` signals (VSS extension required) — as a separate attachment. Customs can verify the manifest credential and the sensor data independently; the VC's hash commitment links the two.

*Exchange model:* **Cloud-to-Cloud (C, advance declaration, primary), Direct A2 (C-V2X, lane approach), and Direct A1 (at the booth, final check).**

The advance declaration — submitting the credential bundle to CBP's Automated Commercial Environment (ACE) or EU customs EDI systems hours before arrival — is cloud-to-cloud and is where the pre-clearance decision is actually made. For CTPAT-certified carriers, this alone may eliminate the at-booth stop entirely. C-V2X sidelink provides the final real-time verification layer: RSUs in the border approach lane initiate a PC5 unicast session with the truck at approach speed, re-verify the credential bundle against the pre-declared bundle (checking for revocations that occurred since the advance submission), and deliver a lane-assignment signal to the vehicle — green/bypass or red/pull aside — before the booth. This eliminates the risk that a credential revoked between the advance submission and physical arrival goes undetected. The at-booth proximity exchange is the fallback for non-pre-cleared vehicles or systems without V2X infrastructure.

---

## Recommendation to the COVESA AOSP App Framework Group

### The Gap in the Current Scope

The COVESA AOSP SDK currently standardizes: UnifiedPush Notifications, Entertainment Stream, Emulator, Vehicle Data, and the shared SDK library framework. It does not include a credential management or digital wallet layer.

The COVESA In-Car Wallet project addresses payment orchestration (toll, parking, EV charging, fuel) but not the underlying VC credential management infrastructure those payment flows depend on for identity binding, fleet account authorization, and regulatory compliance presentation.

The COVESA Vehicle Credentials Vocabulary defines credential schemas but has no reference implementation that runs on a GAS-free AOSP head unit.

This creates a concrete gap: OEMs and fleet operators building on non-GAS AOSP have no standardized, open-source path to implement W3C VC / ISO 18013-5 credential management on the head unit.

### Proposed: COVESA AOSP Digital Wallet Workstream

#### Phase 1 (Fast Path): Head-Unit Verifier Library

The fastest deliverable — and the one most likely to get immediate adoption — is a **GAS-free verifier library** for AOSP head units. This does not require building a wallet. It requires a credential verification component that:
- Validates W3C VC / SD-JWT / mdoc presentations received over BLE/NFC or HTTPS
- Checks revocation via W3C Bitstring Status List (cached for offline)
- Resolves DIDs from a trust registry (COVESA VCV, AAMVA, CA DMV)
- Operates without Google Play Services

This immediately enables: mDL-based driver authentication at ignition (phone holds, vehicle verifies), fleet driver access control, and law enforcement roadside verification — all using existing phone wallets. No new OEM wallet infrastructure is required.

#### Phase 2: Head-Unit Holder for Vehicle-Subject Credentials

Once the verifier layer is proven, add a holder library for the narrow set of use cases that genuinely require vehicle-side credential holding:

**Scope:** Design, specify, and contribute a wallet library module to the COVESA AOSP SDK that enables:
- Credential storage with hardware-backed key management (Android StrongBox / TEE, no GAS dependency)
- Credential issuance via OpenID4VCI and/or the W3C VC API (cloud-to-client)
- Credential presentation via OpenID4VP and ISO 18013-5 proximity presentment (BLE/NFC)
- Cloud-to-cloud VC submission via the `fnolEndpoint` and equivalent autonomous push patterns
- COVESA VCV credential type support (vehicle registration, POI, FNOL, fleet compliance)
- Revocation checking via W3C Bitstring Status List

**Recommended foundation:** OWF Multipaz (Kotlin Multiplatform, Apache 2.0, Android Keystore native, ISO 18013-5/7 + OpenID4VP). Contribute COVESA VCV credential type definitions upstream to OWF Multipaz.

**Coordination:**
- With COVESA In-Car Wallet: VC credential management is the identity/authorization layer; In-Car Wallet provides the payment orchestration layer above it
- With COVESA VCV: wallet implements the credential types VCV defines; AOSP group should have a seat in VCV discussions
- With OWF: formal collaboration on Multipaz to avoid divergent forks

### Specific Work Items

| Item | Action | Coordination |
|---|---|---|
| COVESA AOSP wallet workstream | Propose charter to AOSP App Framework chairs (FORVIA, BMW, GM) | COVESA AOSP group |
| COVESA SDK wallet library | Integrate OWF Multipaz as a COVESA library | OWF + COVESA joint contribution |
| GAS-free AOSP wallet architecture guidance | Document design constraints and tested configuration | COVESA AOSP group |
| COVESA VCV credential types in Multipaz | Contribute VCV credential type definitions to OWF Multipaz | COVESA VCV + OWF |
| In-Car Wallet integration spec | Define the interface between VC wallet layer and payment orchestration | COVESA In-Car Wallet project |
| EUDIW attestation mapping | Map VCV types to EUDIW attestation rules (late 2026 deadline) | COVESA / eIDAS alignment |
| Telematics device attestation VC | Define co-signer credential type in VCV for attached telematics hardware | COVESA VCV |
| Vehicle network endpoint spec | Define a standardized DID service endpoint for cloud-to-client VP requests | COVESA VCV + IETF |
| V2X VC application-layer profile | Define VC URI and compact VC payload types for NR-V2X application messages; profile OpenID4VP for PC5 unicast transport | COVESA + 5GAA + 3GPP SA6 |
| SCMS–VC trust federation spec | Define how V2X SCMS trust anchors vouch for VC issuer public keys so RSUs can verify both layers without separate trust configuration | 5GAA + COVESA VCV |

---

## Relationship to Other COVESA and External Work

| Group / Project | Relationship to a COVESA AOSP Wallet Workstream |
|---|---|
| **COVESA VCV** | Defines the credential schemas the wallet would implement. CA DMV production deployment (registration + POI) is the immediate driver. The wallet workstream should have representation in VCV discussions. |
| **COVESA In-Car Wallet** | Handles payment orchestration above the VC layer. A wallet workstream provides the identity and credential management infrastructure In-Car Wallet's payment use cases (ISO 15118, toll, parking) depend on. These are complementary, not competing. |
| **COVESA Commercial Vehicles WG** | Source of fleet-specific credential types (compliance bundle, cargo manifest, driver qualification) that the wallet workstream would need to support. |
| **COVESA FNOL Report** | Technical architecture for insurance/FNOL use cases (UC-5 through UC-9); a wallet workstream would produce the implementation layer for that work. |
| **OWF (OpenWallet Foundation)** | Home of Multipaz (recommended wallet library foundation). A formal COVESA–OWF collaboration would allow COVESA VCV credential types to be contributed upstream to Multipaz rather than maintained as a private fork. |
| **W3C VC WG** | VCDM v2.0 and associated recommendations are the normative foundation. These use cases may inform the next W3C VC charter cycle's automotive/IoT work items. |
| **W3C CCG / VC API** | The W3C VC API (CCG Community Report) is an HTTP-based wallet-to-issuer and wallet-to-verifier interface used in production by CA DMV. An AOSP wallet workstream should evaluate VC API alongside OpenID4VCI/4VP for COVESA VCV integration, given CA DMV's active deployment. |
| **OpenID Foundation** | OpenID4VP 1.0 is the presentation protocol; ISO 18013-7:2025 binds it to the Digital Credentials API. Wallet workstream should track OpenID4VP profile work for automotive. |
| **eIDAS 2.0 / EC** | EU member state rollout deadline is late 2026. COVESA AOSP wallet must support EUDIW attestation formats for EU-market vehicles; EUDI library set is the recommended dependency for this slice. |
| **5GAA / C-V2X ecosystem** | C-V2X sidelink (Model A2) extends the Direct exchange model to highway-speed and extended-range scenarios: law enforcement V2V stops, border/port approach lanes, weigh station bypass, and toll gantries. A COVESA AOSP wallet workstream should coordinate with 5GAA on: (a) a VC URI or compact VC payload definition for V2X application messages; (b) a profile of OpenID4VP for PC5 unicast transport; (c) SCMS–to–VC-issuer trust federation. The V2X credential exchange gap is currently unaddressed by any active standards body. |
| **3GPP SA6 / SA3** | 3GPP SA6 (application layer) and SA3 (security) cover NR-V2X application-layer security and ProSe (proximity services). A VC payload extension to the NR-V2X application layer would require SA6 engagement. |
| **ETSI TC ITS** | European ITS standardization body (EN 302 636 series, ETSI C-ITS security). EU-deployed RSUs follow ETSI security norms; any European V2X VC exchange profile must align with ETSI C-ITS certificate policy, not only IEEE 1609.2. |

---

## Sources

- [COVESA In-Car Wallet – Payments & Orchestration](https://covesa.global/project/in-car-wallet-payments-orchestration/)
- [COVESA AOSP App Framework Standardization Group](https://covesa.global/project/aosp-app-framework-standardization-group/)
- [COVESA IVP as a Wallet proposed project](https://covesa.atlassian.net/wiki/spaces/WIK4/pages/39067223/IVP+as+a+Wallet+Proposed+Project)
- [W3C VC API (CCG Community Report)](https://w3c-ccg.github.io/vc-api/)
- [OWF Multipaz (identity-credential)](https://github.com/openwallet-foundation-labs/identity-credential)
- [OWF Bifold Wallet](https://github.com/openwallet-foundation/bifold-wallet)
- [EUDI Android Wallet UI](https://github.com/eu-digital-identity-wallet/eudi-app-android-wallet-ui)
- [EUDI Android Wallet Core library](https://github.com/eu-digital-identity-wallet/eudi-lib-android-wallet-core)
- [Procivis One Wallet](https://github.com/procivis/one-wallet)
- [SpruceID Wallet (Credible)](https://github.com/spruceid/wallet)
- [SpruceID CA DMV highlight](https://spruceid.com/customer-highlight/california-highlight)
- [CA DMV Wallet](https://www.dmv.ca.gov/portal/ca-dmv-wallet/)
- [CA DMV Vehicle Credentials](https://www.dmv.ca.gov/portal/ca-dmv-wallet/vehicles/)
- [NIST: From DMV to Wallet](https://www.nist.gov/blogs/cybersecurity-insights/dmv-wallet-understanding-verifiable-digital-credential-issuance)
- [COVESA FNOL VC Standards Report](https://github.com/COVESA/commercial-vehicles/blob/main/reports/connected-vehicle-fnol-vc-standards.md)
- [COVESA CV Workshop: Connected Vehicle Safety & Mobility Data — Industry Workshop (July 2026)](https://docs.google.com/presentation/d/1kJWH5KOzKrgtTraz74tx2Yq6lFfSga2WKJnDryWur7M/edit) — public slide deck from the COVESA Commercial & Fleet Vehicles Expert Group workshop; includes CA DMV verifiable credentials presentation (Manu Sporny / CA DMV), agenda chaired by Paul Boyes; covers VSS crash signals, S2DM incident model, CA DMV credential vocabulary, and insurance/FNOL use cases
- [EU-California DMV, DPP and Business Wallet Use Case Sheet](https://docs.google.com/spreadsheets/d/1kKo0aDslEPJWpszQw9vQPbJNOeWc52T7NBXNEKJt2xs/edit) — ranked cross-jurisdiction use cases for CA DMV and EU/German VC interoperability including vehicle title, fleet compliance, EV charging, CARB Clean Truck Check, and customs/DPP credential flows
- [W3C VC v2.0 Recommendation (May 2025)](https://www.w3.org/TR/vc-data-model-2.0/)
- [Android Digital Credentials API (April 2025)](https://android-developers.googleblog.com/2025/04/announcing-android-support-of-digital-credentials.html)
- [OpenID4VP 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)
- [ISO 15118 – Plug & Charge](https://en.wikipedia.org/wiki/ISO_15118)
- [Self-Sovereign Identity for EV Charging (arXiv)](https://arxiv.org/html/2403.06632v1)
- [Mastercard in-car toll payment pilot (2025)](https://www.mastercard.com/us/en/news-and-trends/stories/2025/in-car-payments-toll-roads.html)
- [OpenWallet Foundation](https://openwallet.foundation/)
- [5GAA: C-V2X Explained](https://5gaa.org/c-v2x-explained/)
- [5GAA: Credential Management Supporting V2X Commercial Deployments](https://5gaa.org/credential-management-supporting-v2x-commercial-deployments/)
- [5GAA: Securing North American V2X Deployments (SCMS Certificate Policy)](https://5gaa.org/events/5gaa-online-session-securing-north-american-v2x-deployments-introducing-the-5gaa-scms-certificate-policy/)
- [5GAA C-V2X Use Cases and Service Level Requirements Vol. I v2.0 (Jan 2025)](https://5gaa.org/content/uploads/2025/01/5gaa-c-v2x-use-cases-and-service-level-requirements-vol-i-v2.0.pdf)
- [5GAA: V2N2X Security, Privacy, and Data Quality](https://5gaa.org/v2n2x-security-privacy-and-data-quality/)
- [5GAA NR-V2X Direct Communication Evaluation (2024)](https://5gaa.org/content/uploads/2024/07/5gaa-wi-nr-v2x-eval.pdf)
- [NR Sidelink Performance Evaluation for 5G-V2X Services (MDPI 2023)](https://www.mdpi.com/2624-8921/5/4/92)
- [US DOT / ITS: Vehicle-to-Everything (V2X) Technology Executive Briefing (2025)](https://www.itskrs.its.dot.gov/briefings/executive-briefing/vehicle-everything-v2x-technology)
- [IEEE 1609.2 / SCMS for V2X Security (overview)](https://www.emergentmind.com/topics/security-credential-management-system-scms)
- [NIST: Public Safety Applications in 5G NR Systems with Sidelink](https://www.nist.gov/publications/towards-system-level-simulations-public-safety-applications-5g-nr-systems-sidelink)
