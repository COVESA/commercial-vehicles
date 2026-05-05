# Open Source Wallet Solutions for AOSP — Comparison

*Researched: 2026-05-05*

---

## Summary Table

| Project | Language / Stack | W3C VC Support | GitHub Stars | Community Activity | Production Evidence |
|---|---|---|---|---|---|
| [Multipaz](#1-multipaz-openwallet-foundation) | Kotlin Multiplatform | Full (VC-JOSE-COSE, SD-JWT VC) + mDL | ~268 | Very active (4–8 wk releases) | Google Wallet; mDL state pilots |
| [Bifold Wallet](#2-bifold-wallet-openwallet-foundation) | React Native | Full (W3C VC, AnonCreds) | ~750+ | Very active; large gov user base | BC Wallet (BC Gov), Brazil gov, several others in App Stores |
| [waltid-identity](#3-waltid-identity) | Kotlin (multiplatform) | Full (JWT-VC, SD-JWT, mdoc) | ~1.3K | Active; commercial entity behind it | 38K+ developers/orgs; enterprise customers |
| [TrustBloc wallet-sdk](#4-trustbloc-wallet-sdk) | Go / GoMobile | Full (W3C VC + DIDs, OID4VCI) | ~100 | Moderate; ongoing in 2025 | LF Decentralized Trust projects; reference wallet |
| [Sphereon mobile-wallet](#5-sphereon-mobile-wallet) | React Native (Expo) | Full (W3C VC, OID4VCI, OID4VP) | ~170 | Moderate; EU eIDAS focus | Available on Google Play; EU FUNKE pilot participant |
| [Learner Credential Wallet](#6-learner-credential-wallet-owf-labs) | React Native | W3C VC (education-focused) | ~200 | Low–moderate | MIT/DCC; deployed for academic institutions |

---

## 1. Multipaz (OpenWallet Foundation)

**Repos:** [openwallet-foundation/multipaz](https://github.com/openwallet-foundation/multipaz) (SDK) · [openwallet-foundation-labs/identity-credential](https://github.com/openwallet-foundation-labs/identity-credential) (predecessor lab)

### Overview
Kotlin Multiplatform library originally built by Google and donated to the OpenWallet Foundation in 2023. It targets Android, iOS, and server-side environments from a single codebase. The OWF TAC has it as an Impact-stage project. The library was renamed from `identity-credential` to `multipaz` during its promotion from the labs to the main OWF org.

### AOSP Relationship
This is the closest thing to a canonical AOSP wallet SDK. Google plans to publish source code to AOSP in Q2 and Q4 to align with the trunk-stable development model. Google Wallet itself is built on this library.

### Credential Formats
- ISO/IEC 18013-5:2021 mdoc / mDL (proximity via NFC and BLE)
- ISO/IEC 18013-7:2025 (online mDL presentation via W3C Digital Credentials API)
- IETF SD-JWT VC
- OpenID4VP 1.0 / OpenID4VCI

### W3C Verifiable Credentials
Supports W3C Digital Credentials API (browser/web presentation) and SD-JWT VC credential format. Less focused on the W3C VC-JOSE-COSE Data Model in isolation — the primary credential format is mdoc/mDL with SD-JWT VC as the secondary. Full verifier/holder/issuer path is implemented.

### Community Activity
- Releases published to Maven Central every 4–8 weeks
- ~268 stars, 128 forks (relatively low star count given institutional backing)
- Active issue tracker; Google engineers as primary contributors
- Developer documentation at developer.multipaz.org
- Production-quality wallet and reader example apps included; production app separation planned for 2026

### Production Evidence
- **Google Wallet** is built on this library — the most significant production deployment
- Several US states use it for mDL issuance (California, Arizona, Maryland, etc.)
- Referenced in Android Developer documentation as the recommended SDK for digital credentials

### Strengths
- Deepest AOSP integration; direct Google lineage
- Best ISO 18013-x coverage
- Kotlin Multiplatform enables shared code with iOS

### Weaknesses
- Lower W3C VC Data Model focus than DID-based projects
- Star count understates real adoption

---

## 2. Bifold Wallet (OpenWallet Foundation)

**Repos:** [openwallet-foundation/bifold-wallet](https://github.com/openwallet-foundation/bifold-wallet) · [bcgov/bc-wallet-mobile](https://github.com/bcgov/bc-wallet-mobile)

### Overview
Previously Hyperledger Aries Bifold, now an OWF Impact-stage project. A React Native wallet framework built on top of [Credo](https://github.com/openwallet-foundation/credo-ts) (formerly Aries Framework JavaScript) for the verifiable credential exchange layer. Designed to be forked and customized — BC Wallet is the flagship deployment.

### AOSP Relationship
React Native app that runs on standard Android (not AOSP-specific). No direct AOSP integration; relies on the Android system for secure storage.

### Credential Formats
- AnonCreds (Hyperledger Anoncreds; primary format for government VC use cases)
- W3C VC Data Model (via Credo)
- OID4VCI / OID4VP (in progress)
- DIF Presentation Exchange

### W3C Verifiable Credentials
Yes — Credo implements the full W3C VC Data Model. DSR Corporation completed W3C VC Data Model support for Hyperledger AnonCreds in BC Gov's Code With Us project. Both AnonCreds and W3C-format VCs are supported simultaneously.

### Community Activity
- ~750+ GitHub stars on bifold-wallet; much more active than star count suggests given downstream forks
- Maintained by a large community of government, academic, and commercial contributors
- Hyperledger Discord and mailing lists active
- BC Gov, IDIM, iDRAMP, DSR, Indicio, among active contributors
- Multiple releases per month

### Production Evidence
- **BC Wallet** (Government of British Columbia): citizens use it for permits, professional credentials, and court access — over 4 million credentials in OrgBook BC
- **Brazil government** deployments
- **Algorand Foundation** Rocca Wallet based on Bifold
- Multiple App Store deployments globally
- Law Society of British Columbia, BC Registries integrations

### Strengths
- Best-proven government/enterprise production track record
- Largest user-facing deployment evidence (App Store downloads)
- Highly extensible theming and plugin model

### Weaknesses
- React Native stack is heavier than native Kotlin
- AnonCreds-first lineage means mdoc/mDL support is less mature
- More complex setup than SDK-only options

---

## 3. waltid-identity

**Repo:** [walt-id/waltid-identity](https://github.com/walt-id/waltid-identity)

### Overview
Open-source Kotlin Multiplatform identity and wallet toolkit from walt.id (a Vienna-based company). Marketed as "The Community Stack." Provides Issuer API, Verifier API, Wallet API, and DID/Crypto libraries. The web wallet is the primary end-user surface; the Kotlin SDK enables embedding in Android apps.

### AOSP Relationship
No direct AOSP integration. Kotlin SDK works on Android. The project is more server/cloud-centric with Android as an embedding target rather than a native mobile wallet framework.

### Credential Formats
- W3C VC Data Model (JWT-VC, JSON-LD)
- SD-JWT VC
- ISO 18013-5 mDL / mdoc
- OID4VCI / OID4VP / SIOPv2

### W3C Verifiable Credentials
Strongest W3C VC focus of all entries here. Full Issuer/Holder/Verifier stack. Supports W3C VC 1.1 and 2.0. Both JWT and JSON-LD proof types. DID resolution for DIDs in VC subjects and issuers.

### Community Activity
- ~1.3K GitHub stars — highest among the projects surveyed
- 38,000+ developers and organizations self-reported on platform
- Commercial entity behind it (walt.id) ensures continuity
- Frequent releases; active issue tracker
- Used in EU eIDAS2 / EUDI Wallet ecosystem experiments

### Production Evidence
- Enterprise customers in financial services, government (Germany/Austria)
- EU ARF (Architecture Reference Framework) implementation reference
- Used in EUDI Wallet Large Scale Pilots (LSPs)
- 2025 revenue growth and distribution partner expansion reported

### Strengths
- Most comprehensive W3C VC coverage
- Largest stated developer community
- Enterprise support available
- Active EU regulatory alignment (eIDAS 2.0)

### Weaknesses
- Primary product is web/server; Android is secondary
- No native AOSP wallet app — SDK only
- Commercial company means open-source governance is less community-driven

---

## 4. TrustBloc wallet-sdk

**Repos:** [trustbloc/wallet-sdk](https://github.com/trustbloc/wallet-sdk) · [trustbloc/wallet](https://github.com/trustbloc/wallet)

### Overview
Go-based SDK with GoMobile bindings that generate Android (AAR) and iOS frameworks. Backed by TrustBloc, an LF Decentralized Trust project. Provides holder-side APIs: receive VCs via OID4VCI, present via OID4VP, manage DIDs.

### AOSP Relationship
No direct AOSP integration. The Android binding is a standard AAR that apps include. No native AOSP system service or HAL involvement.

### Credential Formats
- W3C VC (JWT-VC)
- OID4VCI / OID4VP
- DID-signed credentials

### W3C Verifiable Credentials
Full holder-side W3C VC support with DID-based proofs. Supports receiving and presenting VCs signed using W3C DIDs (did:web, did:key, did:orb). Verifiable Credential Service (VCS) in a companion repo provides issuer/verifier.

### Community Activity
- ~100 GitHub stars; smaller community
- Updates in early 2025 (gomobile Android crash fixes)
- Primarily driven by TrustBloc/LF Decentralized Trust organization members
- Moderate issue and PR activity

### Production Evidence
- Used in LF Decentralized Trust ecosystem projects
- Reference wallet application available
- Less evidence of large-scale public-facing deployments compared to Multipaz or Bifold

### Strengths
- Go SDK is portable and easy to audit
- GoMobile approach allows sharing logic across Android and iOS
- Good OID4VCI/OID4VP protocol coverage

### Weaknesses
- Small community
- No standalone end-user wallet app with broad deployment
- Go dependency adds complexity for Android teams

---

## 5. Sphereon mobile-wallet

**Repos:** [Sphereon-Opensource/mobile-wallet](https://github.com/Sphereon-Opensource/mobile-wallet)

### Overview
Open-source (GPLv3) React Native / Expo mobile wallet from Sphereon, a Dutch identity company. Available on the Google Play Store and Apple App Store. Participated in EU FUNKE (Prototype for German EUDI Wallet) pilot. Built on Sphereon's Apache 2.0-licensed SSI SDK.

### AOSP Relationship
No direct AOSP integration. Standard Android app distributed via Google Play.

### Credential Formats
- W3C VC (JWT-VC)
- SD-JWT VC
- OID4VCI / OID4VP
- SIOPv2

### W3C Verifiable Credentials
Full W3C VC support with OID4VCI issuance and OID4VP presentation. Participated in JFF/W3C-EDU plugfest interoperability testing. DID-based credential subjects.

### Community Activity
- ~170 GitHub stars
- Moderate activity; Expo SDK updates tracked
- Sphereon is an active contributor to the broader SSI ecosystem (multiple related repos)
- EU FUNKE branch (`funke`) shows recent EU-specific development

### Production Evidence
- **Available on Google Play** — real end-user deployment
- Participated in JFF Plugfest 2 interoperability testing
- EU FUNKE pilot (German EUDI wallet prototype)
- TNO SSI Lab (Netherlands) maintains a fork used in Dutch government pilots

### Strengths
- Real App Store deployment
- EU regulatory alignment (eIDAS 2.0 / FUNKE)
- Interoperability-tested via JFF Plugfests

### Weaknesses
- GPLv3 license may complicate commercial embedding
- Expo/React Native adds bundle overhead
- Smaller community than Bifold or walt.id

---

## 6. Learner Credential Wallet (OWF Labs)

**Repo:** [openwallet-foundation-labs/learner-credential-wallet](https://github.com/openwallet-foundation-labs/learner-credential-wallet)

### Overview
Cross-platform React Native wallet from MIT Digital Credentials Consortium (DCC), now under OWF Labs. Focused exclusively on education credentials (academic degrees, professional certifications). Originally part of the JFF/W3C VC Education effort.

### AOSP Relationship
No AOSP-specific integration. Standard React Native Android app.

### Credential Formats
- W3C VC Data Model (JSON-LD, primarily)
- Linked Data Proofs
- VC-HTTP-API / Chapi for exchange

### W3C Verifiable Credentials
Education-sector W3C VC focus. Implements the W3C VC Data Model with JSON-LD proofs. Compatible with Open Badges v3, CLR (Comprehensive Learner Record), and EDU-specific VC vocabularies.

### Community Activity
- ~200 GitHub stars
- Moderate; MIT/DCC-driven
- Activity peaks around plugfest and interoperability events
- Lower cadence than other projects

### Production Evidence
- Deployed for MIT, participating DCC-member universities
- Interoperability tested in JFF plugfests
- MIT Open Learning describes it as in active use for learner records

### Strengths
- Best fit for education / credentialing use cases
- Strong W3C VC JSON-LD proof coverage
- OWF Labs governance

### Weaknesses
- Domain-specific — poor fit outside education
- No mdoc/mDL or OpenID4VC support
- Smaller contributor base

---

## Cross-Cutting Observations

### W3C VC Support Depth

| Project | VC Data Model | SD-JWT VC | JSON-LD | OID4VCI | OID4VP | mdoc |
|---|---|---|---|---|---|---|
| Multipaz | Partial (SD-JWT VC) | Yes | No | Yes | Yes | Yes (primary) |
| Bifold | Yes | Partial | Yes | Yes | Yes | No |
| waltid-identity | Yes (deepest) | Yes | Yes | Yes | Yes | Yes |
| TrustBloc | Yes | No | No | Yes | Yes | No |
| Sphereon | Yes | Yes | No | Yes | Yes | No |
| Learner Credential | Yes | No | Yes (primary) | No | No | No |

### Best Choice by Use Case

| Use Case | Recommended Project |
|---|---|
| AOSP-native / mDL (driver's license) | **Multipaz** |
| Government SSI / citizen wallet | **Bifold** |
| Full W3C VC issuance/verification stack | **waltid-identity** |
| EU eIDAS 2.0 / EUDI Wallet alignment | **waltid-identity** or **Sphereon** |
| Education credentials | **Learner Credential Wallet** |
| Go-based cross-platform SDK | **TrustBloc wallet-sdk** |

---

## Sources

- [Android Developers Blog: Announcing Android support of digital credentials](https://android-developers.googleblog.com/2025/04/announcing-android-support-of-digital-credentials.html)
- [Identity Credential | Android Open Source Project](https://source.android.com/docs/security/features/identity-credentials)
- [openwallet-foundation/multipaz on GitHub](https://github.com/openwallet-foundation/multipaz)
- [openwallet-foundation-labs/identity-credential on GitHub](https://github.com/openwallet-foundation-labs/identity-credential)
- [openwallet-foundation/bifold-wallet on GitHub](https://github.com/openwallet-foundation/bifold-wallet)
- [bcgov/bc-wallet-mobile on GitHub](https://github.com/bcgov/bc-wallet-mobile)
- [About BC Wallet | Digital Credential Services](https://digital.gov.bc.ca/digital-trust/about/about-bc-wallet/)
- [BC Digital Trust: Leveraging Hyperledger Tools For Digital Trust](https://www.lfdecentralizedtrust.org/blog/bc-digital-trust-leveraging-hyperledger-tools-for-digital-trust)
- [walt-id/waltid-identity on GitHub](https://github.com/walt-id/waltid-identity)
- [The state of identity & walt.id 2025](https://walt.id/blog/the-state-of-identity-and-waltid-2025)
- [trustbloc/wallet-sdk on GitHub](https://github.com/trustbloc/wallet-sdk)
- [Sphereon-Opensource/mobile-wallet on GitHub](https://github.com/Sphereon-Opensource/mobile-wallet)
- [openwallet-foundation-labs/learner-credential-wallet on GitHub](https://github.com/openwallet-foundation-labs/learner-credential-wallet)
- [W3C Verifiable Credentials 2.0 press release](https://www.w3.org/press-releases/2025/verifiable-credentials-2-0/)
- [OpenID for Verifiable Credentials Libraries](https://openid.net/sg/openid4vc/libraries/)
- [OpenWallet Foundation Projects](https://openwallet.foundation/projects/)
- [Identity Credential — OWF TAC](https://tac.openwallet.foundation/projects/identity-credential/)
