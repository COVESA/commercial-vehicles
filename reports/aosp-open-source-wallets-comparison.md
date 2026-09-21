# Open Source Wallet Solutions for AOSP — Comparison

*Researched: 2026-05-05 — fact-checked and updated 2026-09-21 (GitHub statistics, OWF project stages, licenses, and deployment claims re-verified; see Revision Notes at end)*

---

## Summary Table

| Project | Language / Stack | W3C VC Support | GitHub Stars | Community Activity | Production Evidence |
|---|---|---|---|---|---|
| [Multipaz](#1-multipaz-openwallet-foundation) | Kotlin Multiplatform | SD-JWT VC + W3C Digital Credentials API (no W3C VC Data Model) + mDL/mdoc | ~295 | Very active (4–8 wk releases) | Google Wallet and EUDI reference wallet build on it (Google, Sept 2026) |
| [Bifold Wallet](#2-bifold-wallet-openwallet-foundation) | React Native | Full (W3C VC 1.1/2.0, AnonCreds, SD-JWT, mdoc) | ~204 | Active on GitHub; removed from OWF active project roster June 2026 | BC Wallet (BC Gov), Algorand Rocca; BC Wallet being folded into BC Services Card app |
| [waltid-identity](#3-waltid-identity) | Kotlin (multiplatform) | Full (JWT-VC, SD-JWT, mdoc) | ~309 | Active; commercial entity behind it | 30K+ developers/orgs (self-reported); used across EU Large Scale Pilots |
| [TrustBloc wallet-sdk](#4-trustbloc-wallet-sdk) | Go / GoMobile | Full (W3C VC + DIDs, OID4VCI) | ~30 | Maintenance mode (dependency/CI fixes; last release Feb 2026) | Gen Digital (ex-SecureKey) open source; reference wallet archived |
| [Sphereon mobile-wallet](#5-sphereon-mobile-wallet) | React Native (Expo) | Full (W3C VC, OID4VCI, OID4VP) | ~110 | Moderate; EU eIDAS focus | Available on Google Play; SPRIND FUNKE EUDI wallet challenge participant |
| [Learner Credential Wallet](#6-learner-credential-wallet-owf-labs) | React Native | W3C VC (education-focused) | ~88 | Low; DCC@MIT stewardship ending (last MIT release 2.2.10, June 2026) | Deployed for DCC-member academic institutions |

---

## 1. Multipaz (OpenWallet Foundation)

**Repos:** [openwallet-foundation/multipaz](https://github.com/openwallet-foundation/multipaz) (SDK) · [openwallet-foundation/multipaz-wallet](https://github.com/openwallet-foundation/multipaz-wallet) and [multipaz-identity-reader](https://github.com/openwallet-foundation/multipaz-identity-reader) (standalone wallet and reader apps, 2026). The former `openwallet-foundation-labs/identity-credential` URL redirects to the same repository.

### Overview
Kotlin Multiplatform library originally built by Google (as the Android Identity Credential library) and accepted into OpenWallet Foundation Labs in October 2023. It targets Android, iOS, and server-side environments from a single codebase. It was renamed from `identity-credential` to `multipaz` in release 0.90 (March 2025; packages moved from `com.android.identity` to `org.multipaz`), and the OWF TAC promoted it from Labs to a **Growth**-stage project in June 2026.

### AOSP Relationship
This is the closest thing to a canonical wallet SDK for Android, though it is an OWF library, not part of AOSP itself. In September 2026 Google publicly stated that Multipaz "serves as a foundational component for Google Wallet and the European Digital Identity Wallet (EUDIW) reference implementation"; the repository README still notes it is not an official or supported Google product.

### Credential Formats
- ISO/IEC 18013-5:2021 mdoc / mDL (proximity via NFC and BLE)
- ISO/IEC 18013-7:2025 (online mDL presentation via W3C Digital Credentials API)
- IETF SD-JWT VC
- OpenID4VP 1.0 / OpenID4VCI

### W3C Verifiable Credentials
Supports the W3C Digital Credentials API (browser/web presentation) and the IETF SD-JWT VC credential format. It does **not** implement the W3C VC Data Model (JSON-LD / VC-JOSE-COSE) — the primary credential format is mdoc/mDL with SD-JWT VC as the secondary. Full verifier/holder/issuer path is implemented for those formats, including zero-knowledge presentations via the bundled Google Longfellow-ZK library (`multipaz-longfellow`).

### Community Activity
- Releases published to Maven Central every 4–8 weeks
- ~295 stars, 148 forks as of Sept 2026 (relatively low star count given institutional backing)
- Active issue tracker; Google engineers as primary contributors
- Developer documentation at developer.multipaz.org
- Standalone wallet and reader apps split out into `multipaz-wallet` and `multipaz-identity-reader` repositories in April 2026
- Latest release 0.101.0 (Sept 2026); README expects 1.0 "around late 2026 or early 2027"

### Production Evidence
- **Google Wallet** and the **EU Digital Identity Wallet reference implementation** build on this library (per Google, Sept 2026) — the most significant production lineage
- Google's Wallet verifier documentation recommends Multipaz for reader/verifier apps; Android's holder/issuer developer docs point to the AndroidX Credential Manager libraries rather than Multipaz
- No public evidence ties Multipaz to any specific US state's mDL issuance system

### Strengths
- Deepest AOSP integration; direct Google lineage
- Best ISO 18013-x coverage
- Kotlin Multiplatform enables shared code with iOS

### Weaknesses
- No W3C VC Data Model (JSON-LD) support; SD-JWT VC and mdoc only
- Still pre-1.0 (APIs and storage formats may change)
- Star count understates real adoption

---

## 2. Bifold Wallet (OpenWallet Foundation)

**Repos:** [openwallet-foundation/bifold-wallet](https://github.com/openwallet-foundation/bifold-wallet) · [bcgov/bc-wallet-mobile](https://github.com/bcgov/bc-wallet-mobile)

### Overview
Previously Hyperledger Aries Bifold; an OWF Growth-stage project from February 2024 until the TAC removed it from the active project roster in June 2026 (the GitHub repository remains active and unarchived). A React Native wallet framework built on top of [Credo](https://github.com/openwallet-foundation/credo-ts) (formerly Aries Framework JavaScript; itself an OWF Growth project) for the verifiable credential exchange layer. Designed to be forked and customized — BC Wallet is the flagship deployment.

### AOSP Relationship
React Native app that runs on standard Android (not AOSP-specific). No direct AOSP integration; relies on the Android system for secure storage.

### Credential Formats
- AnonCreds (Hyperledger AnonCreds; primary format for the BC Gov deployment)
- W3C VC Data Model 1.1 and 2.0 (via Credo)
- SD-JWT VC
- ISO 18013-5 mdoc and ISO 18013-7 Annex B (via Credo's mdoc module)
- OID4VCI / OID4VP 1.0
- DIF Presentation Exchange, DIDComm

### W3C Verifiable Credentials
Yes — Credo implements the full W3C VC Data Model. DSR Corporation completed W3C VC Data Model support for Hyperledger AnonCreds in BC Gov's Code With Us project. Both AnonCreds and W3C-format VCs are supported simultaneously.

### Community Activity
- ~204 GitHub stars, ~200 forks on bifold-wallet (Sept 2026); more active than star count suggests given downstream forks
- Maintained by a large community of government, academic, and commercial contributors
- Hyperledger Discord and mailing lists active
- BC Gov, IDIM, iDRAMP, DSR, Indicio, among active contributors
- Multiple releases per month

### Production Evidence
- **BC Wallet** (Government of British Columbia): used for pilot credentials including the Law Society of BC Lawyer Credential and Access to Court Materials. BC Gov describes it as "not yet an enterprise service" and, as of Sept 2026, is folding BC Wallet functionality into the BC Services Card app
- **Algorand Foundation** Rocca Wallet is a Bifold fork (basis for Pera Wallet 7.0)
- The project README cites use by "governmental bodies in Canada and teams in Brazil"; no named Brazilian deployment is public
- (OrgBook BC's 4M+ credentials are an ACA-Py/Aries VCR registry metric, not a Bifold wallet metric)

### Strengths
- Best-proven government/enterprise production track record
- Largest user-facing deployment evidence (App Store downloads)
- Highly extensible theming and plugin model

### Weaknesses
- React Native stack is heavier than native Kotlin
- AnonCreds-first lineage; mdoc/mDL support arrived later via Credo and is less battle-tested than Multipaz's
- Governance uncertainty after removal from the OWF active roster (June 2026)
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
- ~309 GitHub stars (Sept 2026); the archived predecessor `waltid-ssikit` is separate
- 30,000+ developers and organizations self-reported (walt.id, March 2026)
- Commercial entity behind it (walt.id) ensures continuity
- Frequent releases; active issue tracker
- Used in EU eIDAS2 / EUDI Wallet ecosystem experiments

### Production Evidence
- Enterprise customers in financial services and government
- Aligned with the EU ARF (Architecture Reference Framework)
- walt.id reports its open-source components were used across all of the first EUDI Wallet Large Scale Pilots (self-reported, March 2026)
- Revenue/ARR doubled in 2025 per walt.id

### Strengths
- Most comprehensive W3C VC coverage
- Large stated developer community
- Enterprise support available
- Active EU regulatory alignment (eIDAS 2.0)

### Weaknesses
- Primary product is web/server; Android is secondary
- No native AOSP wallet app — SDK only
- Commercial company means open-source governance is less community-driven

---

## 4. TrustBloc wallet-sdk

**Repos:** [trustbloc/wallet-sdk](https://github.com/trustbloc/wallet-sdk) · [trustbloc/wallet](https://github.com/trustbloc/wallet) (archived 2023)

### Overview
Go-based SDK with GoMobile bindings that generate Android (AAR) and iOS frameworks. TrustBloc is open source from Gen Digital (formerly SecureKey); it is not an LF Decentralized Trust project. Provides holder-side APIs: receive VCs via OID4VCI, present via OID4VP, manage DIDs.

### AOSP Relationship
No direct AOSP integration. The Android binding is a standard AAR that apps include. No native AOSP system service or HAL involvement.

### Credential Formats
- W3C VC (JWT-VC)
- OID4VCI / OID4VP
- DID-signed credentials

### W3C Verifiable Credentials
Full holder-side W3C VC support with DID-based proofs. Supports receiving and presenting VCs signed using W3C DIDs (did:web, did:key, did:orb). Verifiable Credential Service (VCS) in a companion repo provides issuer/verifier.

### Community Activity
- ~30 GitHub stars; small community
- Maintenance mode: 2025–2026 commits are dependency and CI fixes; last release v2.4.0 (Feb 2026)
- Primarily driven by Gen Digital engineers
- Low issue and PR activity

### Production Evidence
- Reference wallet application (`trustbloc/wallet`) is archived
- No evidence of large-scale public-facing deployments

### Strengths
- Go SDK is portable and easy to audit
- GoMobile approach allows sharing logic across Android and iOS
- Good OID4VCI/OID4VP protocol coverage

### Weaknesses
- Small community; maintenance-mode project
- No maintained end-user wallet app
- No SD-JWT VC or mdoc support
- Go dependency adds complexity for Android teams

---

## 5. Sphereon mobile-wallet

**Repos:** [Sphereon-Opensource/mobile-wallet](https://github.com/Sphereon-Opensource/mobile-wallet)

### Overview
Open-source (Apache 2.0) React Native / Expo mobile wallet from Sphereon, a Dutch identity company. Available on the Google Play Store and Apple App Store. One of six teams selected for the German SPRIND FUNKE EUDI wallet prototype challenge (stages 1 and 2). Built on Sphereon's Apache 2.0-licensed SSI SDK.

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
- ~110 GitHub stars (Sept 2026); last push July 2026
- Moderate activity; Expo SDK updates tracked
- Sphereon is an active contributor to the broader SSI ecosystem (multiple related repos)
- FUNKE branches (`funke_c2`, `feature/SPRIND-*`) show EU-specific development

### Production Evidence
- **Available on Google Play** — real end-user deployment
- Participated in JFF Plugfest 2 interoperability testing (Nov 2022)
- SPRIND FUNKE (German EUDI wallet prototype challenge)
- TNO SSI Lab (Netherlands) has a fork (`tno-ssi-lab/sphereon-mobile-wallet`), last updated Aug 2024; use in Dutch government pilots is not documented

### Strengths
- Real App Store deployment
- EU regulatory alignment (eIDAS 2.0 / FUNKE)
- Interoperability-tested via JFF Plugfests

### Weaknesses
- Expo/React Native adds bundle overhead
- Smaller community than Bifold or walt.id

---

## 6. Learner Credential Wallet (OWF Labs)

**Repo:** [openwallet-foundation-labs/learner-credential-wallet](https://github.com/openwallet-foundation-labs/learner-credential-wallet)

### Overview
Cross-platform React Native wallet from the MIT Digital Credentials Consortium (DCC), accepted into OWF Labs in August 2024 (the `digitalcredentials/learner-credential-wallet` URL redirects there) but dropped from the OWF TAC active project list in June 2026. Focused exclusively on education credentials (academic degrees, professional certifications). Originally part of the JFF/W3C VC Education effort. MIT license. The README's June 2026 note says release 2.2.10 is "our last release as the Digital Credentials Consortium at MIT"; future stewardship is unclear.

### AOSP Relationship
No AOSP-specific integration. Standard React Native Android app.

### Credential Formats
- W3C VC Data Model (JSON-LD, primarily)
- Linked Data Proofs
- VC-HTTP-API / Chapi for exchange

### W3C Verifiable Credentials
Education-sector W3C VC focus. Implements the W3C VC Data Model with JSON-LD proofs. Compatible with Open Badges v3, CLR (Comprehensive Learner Record), and EDU-specific VC vocabularies.

### Community Activity
- ~88 GitHub stars (Sept 2026)
- Low; MIT/DCC-driven, with DCC@MIT stewardship ending in 2026
- Activity peaks around plugfest and interoperability events
- Lower cadence than other projects

### Production Evidence
- Deployed for MIT and participating DCC-member universities
- Interoperability tested in JFF plugfests

### Strengths
- Best fit for education / credentialing use cases
- Strong W3C VC JSON-LD proof coverage
- OWF Labs governance

### Weaknesses
- Domain-specific — poor fit outside education
- No mdoc/mDL or OpenID4VC support (exchange is VC-API interaction URLs and deep links)
- Smaller contributor base; maintainer transition under way

---

## Cross-Cutting Observations

### W3C VC Support Depth

| Project | VC Data Model | SD-JWT VC | JSON-LD | OID4VCI | OID4VP | mdoc |
|---|---|---|---|---|---|---|
| Multipaz | No (SD-JWT VC only) | Yes | No | Yes | Yes | Yes (primary) |
| Bifold | Yes (1.1 and 2.0) | Yes | Yes | Yes | Yes | Yes (via Credo) |
| waltid-identity | Yes (deepest) | Yes | Yes | Yes | Yes | Yes |
| TrustBloc | Yes | No | No | Yes | Yes | No |
| Sphereon | Yes | Yes | No | Yes | Yes | No |
| Learner Credential | Yes | No | Yes (primary) | No | No | No |

### Best Choice by Use Case

| Use Case | Recommended Project |
|---|---|
| AOSP-native / mDL (driver's license) | **Multipaz** |
| Government SSI / citizen wallet (Aries/AnonCreds ecosystems) | **Bifold** (note OWF roster status) |
| Full W3C VC issuance/verification stack | **waltid-identity** |
| EU eIDAS 2.0 / EUDI Wallet alignment | **waltid-identity** or **Sphereon** |
| Education credentials | **Learner Credential Wallet** |
| Go-based cross-platform SDK | **TrustBloc wallet-sdk** (maintenance mode) |

### Projects Not Covered Above

Several open-source wallets have become relevant since the original survey and are assessed in the companion report [Digital Wallet for the COVESA AOSP Platform](aosp-vc-wallet-use-cases-standards.md) or noted here for completeness:

- **EU Digital Identity Wallet reference implementation** (`eu-digital-identity-wallet/eudi-app-android-wallet-ui`, EUPL-1.2 app with Apache 2.0 libraries) — the official EUDIW reference; builds on Multipaz. mdoc and SD-JWT VC only.
- **Procivis One** (`procivis/one-core`, Apache 2.0, Rust core) — Swiss e-ID lineage; W3C VC, SD-JWT VC, mdoc.
- **Paradym Wallet** (`animo/paradym-wallet`, Apache 2.0) — React Native on Credo; SPRIND FUNKE stage-2 participant.
- **wwWallet** (`wwWallet/wallet-frontend`, BSD-2) — web/PWA EUDI-style wallet used in the DC4EU and EWC pilots.
- **Inji Wallet** (`inji/inji-wallet`, MIT, MOSIP) — OpenID4VC wallet deployed in national ID programs.
- **SpruceKit Mobile** (`spruceid/sprucekit-mobile`, Apache 2.0) — SpruceID's current mobile stack; its earlier `wallet` (Credible), `mobile-sdk-*` and `didkit` repositories are archived.

---

## Sources

- [Android Developers Blog: Announcing Android support of digital credentials](https://android-developers.googleblog.com/2025/04/announcing-android-support-of-digital-credentials.html)
- [Identity Credential | Android Open Source Project](https://source.android.com/docs/security/features/identity-credentials)
- [openwallet-foundation/multipaz on GitHub](https://github.com/openwallet-foundation/multipaz)
- [OWF TAC project list (stages)](https://tac.openwallet.foundation/projects/)
- [Google Security Blog: Android StrongBox and open standards for digital credentials (Sept 2026)](https://blog.google/security/android-strongbox-and-open-standards-digital-credentials/)
- [Multipaz developer documentation](https://developer.multipaz.org/)
- [openwallet-foundation/bifold-wallet on GitHub](https://github.com/openwallet-foundation/bifold-wallet)
- [bcgov/bc-wallet-mobile on GitHub](https://github.com/bcgov/bc-wallet-mobile)
- [BC Wallet (Government of British Columbia)](https://www2.gov.bc.ca/gov/content/governments/government-id/bc-wallet)
- [Law Society of BC: Digital credentials project for lawyers expands](https://www.lawsociety.bc.ca/news-and-engagement/news/digital-credentials-project-for-lawyers-expands-in-bc)
- [Algorand Foundation Rocca Wallet](https://github.com/algorandfoundation/rocca-wallet)
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
- [SPRIND EUDI Wallet Prototypes challenge (FUNKE)](https://www.sprind.org/en/impulses/challenges/eudi-wallet-prototypes)

---

## Revision Notes (2026-09-21)

The May 2026 version was re-verified against GitHub, the OWF TAC project registry, and vendor sources. Corrections:

1. **GitHub star counts** were wrong for every project (some by 3–4×) and have been replaced with Sept 2026 figures: Multipaz 295, Bifold 204, waltid-identity 309, TrustBloc wallet-sdk 30, Sphereon 110, Learner Credential Wallet 88.
2. **OWF stages**: neither Multipaz nor Bifold has ever been an Impact-stage project. Multipaz was Labs until June 2026 and is now Growth. Bifold was Growth from Feb 2024 and was removed from the OWF active project roster in June 2026; Learner Credential Wallet was dropped from the roster at the same time.
3. **Multipaz**: the rename to Multipaz happened in March 2025 (release 0.90), not during a stage promotion; the "Q2/Q4 AOSP source publication" statement described AOSP's release cadence, not Multipaz, and was removed. Claims that US states use Multipaz for mDL issuance and that Android developer docs recommend it as the holder SDK could not be substantiated and were removed; Google's Sept 2026 statement that Google Wallet and the EUDI reference wallet build on Multipaz was added. Multipaz does not implement the W3C VC Data Model (SD-JWT VC and mdoc only).
4. **Bifold**: now supports SD-JWT, mdoc (ISO 18013-5/-7) and OID4VP 1.0 via Credo; the OrgBook BC 4M-credential figure is a registry metric, not a wallet metric; "Brazil government deployments" softened to the README's wording; BC Wallet is being folded into the BC Services Card app.
5. **walt.id**: developer count corrected to walt.id's own 30K+ figure.
6. **TrustBloc**: not an LF Decentralized Trust project (Gen Digital open source); reference wallet archived; project in maintenance mode.
7. **Sphereon**: license is Apache 2.0, not GPLv3 — the GPLv3 weakness was removed; TNO fork is stale and its pilot use undocumented.
8. **Learner Credential Wallet**: MIT license; DCC@MIT stewardship ending after release 2.2.10 (June 2026).
9. Added a "Projects Not Covered Above" section for wallets that have become relevant since May 2026 (EUDI reference wallet, Procivis One, Paradym, wwWallet, Inji, SpruceKit Mobile).
