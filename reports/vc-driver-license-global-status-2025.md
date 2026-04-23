# W3C Verifiable Credentials for Individual Identity and Driver's Licenses — Global Status (2025–2026)

> **Note on standards overlap:** Two credential formats dominate digital driver's license (mDL) deployments: **ISO/IEC 18013-5** (mdoc, proximity presentation) and **W3C Verifiable Credentials Data Model** (JSON-LD/JWT, online presentation). These converge in practice — ISO 18013-7 (online mdoc presentation, published October 2024) is being paired with W3C VC semantics in wallet architectures, and the EUDI Wallet mandate explicitly supports both formats. Where a deployment uses either or both, it is included here.

---

## Standards Baseline

| Spec | Status | Relevance |
|---|---|---|
| [W3C VC Data Model v2.0](https://www.w3.org/TR/vc-data-model-2.0/) | **W3C Recommendation**, May 2025 | Core VC format |
| [ISO/IEC 18013-5:2021](https://www.iso.org/standard/69084.html) | Published 2021 | Proximity mDL (mdoc) |
| [ISO/IEC TS 18013-7:2024](https://www.iso.org/standard/82772.html) | Published Oct 2024 | Online mDL presentation |

The [W3C press release](https://www.w3.org/press-releases/2025/verifiable-credentials-2-0/) calls VC 2.0's Recommendation status a "critical signal to governments to build digital trust upon interoperable, trustworthy, and privacy-aware open web standards." Seven related specifications were elevated simultaneously, including data integrity proofs and the bitstring status list.

---

## W3C VC vs. ISO 18013-5 (mDL/mdoc) — Comparison

These two standards emerged from different communities with different primary use cases. They are complementary rather than competing, and major deployments (notably the EUDI Wallet) mandate support for both.

### Origins and Design Philosophy

| Dimension | W3C Verifiable Credentials | ISO/IEC 18013-5 (mDL/mdoc) |
|---|---|---|
| **Origin** | Web/open identity community (W3C) | Government/DMV/ISO working group |
| **Primary use case** | Online / remote credential exchange | In-person, proximity (police stop, airport, bar) |
| **Standardization body** | W3C (with IETF for SD-JWT variant) | ISO/IEC JTC 1/SC 17 |
| **First published** | VC DM 1.0: 2019; v2.0 W3C Rec: May 2025 | ISO 18013-5:2021 |
| **Online extension** | Native (HTTP-based presentation) | ISO 18013-7:2024 (adds OID4VP) |

### Data Format and Encoding

| Dimension | W3C VC (JSON-LD / SD-JWT VC) | ISO mdoc (CBOR/COSE) |
|---|---|---|
| **Serialization** | JSON / JSON-LD (text-based, web-native) | CBOR (binary, compact — 20–50% smaller than JSON) |
| **Signature scheme** | ECDSA, EdDSA, BBS+ (via Data Integrity proofs) | COSE (CBOR Object Signing and Encryption) |
| **Transport** | HTTPS, QR, OpenID4VP | NFC, Bluetooth Low Energy, Wi-Fi Aware, QR; online via OID4VP (18013-7) |
| **Vocabulary control** | Open/extensible — schema.org-style namespaced terms | ISO-controlled; attribute names defined in the standard |
| **Developer familiarity** | High — JSON/JWT are ubiquitous in web development | Lower — CBOR/COSE requires specialized libraries |

### Selective Disclosure

Both standards support selective disclosure — the ability for a holder to reveal only a subset of credential attributes — but implement it differently.

**ISO mdoc (18013-5):**
All data elements are encrypted and hidden by default at issuance. During a session the holder's device explicitly authorizes release of specific elements. The verifier receives only what was requested. This is tightly integrated with the device engagement and session encryption protocol.

**W3C VC with SD-JWT (IETF RFC 9901 / draft SD-JWT VC):**
At issuance, each claim is individually salted and hashed. The holder receives a JWT containing hashes plus individual per-claim disclosure tokens. At presentation, the holder selects which disclosure tokens to release. Cryptographic linkability between claims is prevented by the salt/hash structure.

**W3C VC with BBS+ signatures:**
Supports *unlinkable* selective disclosure — different presentations of the same credential are cryptographically indistinguishable from each other, preventing correlation across verifiers. This is stronger privacy than SD-JWT or mdoc for high-frequency use cases.

### Privacy Properties

| Property | W3C VC (SD-JWT) | W3C VC (BBS+) | ISO mdoc |
|---|---|---|---|
| **Selective disclosure** | Yes (hash-based) | Yes (ZKP-based) | Yes (element-level release) |
| **Holder binding** | Optional (KB-JWT) | Yes | Yes (device key in MSO) |
| **Issuer unlinkability** | No | Yes | No |
| **Verifier unlinkability** | No (same credential nonce) | Yes | No (session transcript) |
| **Offline presentation** | Limited | Limited | Yes (core design goal) |
| **Revocation** | Bitstring status list, StatusList2021, OCSP | Same | MSO expiry + online check |

### Protocol Integration

Both standards now converge on **OpenID for Verifiable Presentations (OID4VP)** as the presentation protocol for online flows, enabling a single relying party integration to accept either format.

- **ISO 18013-7** (published October 2024) defines how mdoc credentials are presented over the internet using OID4VP.
- **OpenID4VCI** is the issuance protocol for both SD-JWT VCs and mdocs.
- **eIDAS 2.0 EUDI Wallet** mandates support for both mdoc and SD-JWT VC at the wallet level, with OID4VP as the presentation layer — the clearest signal that both formats will coexist long-term.

[July 2025 interoperability testing](https://www.biometricupdate.com/202507/openid-vc-spec-shows-interoperability-between-issuers-digital-wallets) demonstrated cross-vendor interoperability across OpenID4VCI v16, OID4VP High Assurance Interoperability Profile, ISO 18013-5, ISO 18013-7, and IETF SD-JWT draft 17.

### Use Case Fit

| Scenario | Best fit |
|---|---|
| Police/border officer proximity check (offline) | **ISO 18013-5 mdoc** |
| Age verification at physical retail | **ISO 18013-5 mdoc** |
| Online KYC / bank account opening | **ISO 18013-7 + OID4VP** or **SD-JWT VC** |
| Cross-border EU credential verification | **Both** (EUDI Wallet carries both) |
| Professional licence / educational credential | **W3C VC** (flexible vocabulary) |
| Privacy-critical repeated presentation (healthcare, etc.) | **W3C VC + BBS+** |
| Existing government DMV infrastructure | **ISO 18013-5** (dominant in US/AU state deployments) |

### Standards Convergence and the EUDI Wallet

The EUDI Wallet Architecture Reference Framework (ARF) explicitly mandates support for both formats. EU member-state wallet implementations must issue **mdoc** for proximity use and **SD-JWT VC** (a W3C-VC-aligned format) for online use. This dual-format mandate — backed by the world's largest digital identity regulation — is the clearest evidence that the future is multi-format. Neither standard is expected to displace the other; they address complementary layers of the identity stack.

**Key resources:**
- [Idura — How Verifiable Credentials Differ from ISO/IEC 18013-5 Ones](https://idura.eu/blog/verifiable-credentials-vs-iso-18013-5)
- [Spherical Cow Consulting — Verifiable Credentials and mdocs: A Tale of Two Protocols](https://sphericalcowconsulting.com/2024/01/03/verifiable-credentials-and-mdocs-a-tale-of-two-protocols/)
- [iGrant.io — Verifiable Credential Formats in the EUDI Wallet](https://docs.igrant.io/concepts/eudi-wallet-verifiable-credential-formats/)
- [Shane De Coninck — EUDI Credential Formats Crash Course: X.509, mDL, SD-JWT VC, and W3C VC](https://shanedeconinck.be/posts/eudi-credential-formats-crash-course/)
- [Takahiko Kawasaki (Medium) — Issuing VCs in SD-JWT VC and mdoc/mDL formats (eIDAS 2.0)](https://darutk.medium.com/issuing-verifiable-credentials-in-the-sd-jwt-vc-and-mdoc-mdl-formats-mandated-in-eidas-2-0-87a232cfcc2a)
- [NIST — Digital Identities: Getting to Know the Verifiable Digital Credential Ecosystem](https://www.nist.gov/blogs/cybersecurity-insights/digital-identities-getting-know-verifiable-digital-credential-0)
- [IETF RFC 9901 — Selective Disclosure for JSON Web Tokens (SD-JWT)](https://datatracker.ietf.org/doc/rfc9901/)
- [Identity Woman (Medium) — Where can the W3C VCs meet the ISO 18013-5 mDL?](https://medium.com/@identitywoman-in-business/where-can-the-w3c-vcs-meet-the-iso-18013-5-mdl-b2d450bb19f8)

---

## Interoperability Between W3C VC and ISO 18013-5 — Current State and Forcing Functions

### Is There Interoperability Today?

Yes — partial and growing. The two standards operate at different layers of the credential stack, which means interoperability is achieved primarily through shared **presentation protocols** and **browser-level APIs**, not by merging the underlying data formats. Four active convergence mechanisms exist:

#### 1. OpenID4VC High Assurance Interoperability Profile (HAIP)

The [OpenID4VC HAIP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-04.html) defines a single profile of [OpenID for Verifiable Presentations (OID4VP)](https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html) and [OpenID for Verifiable Credential Issuance (OID4VCI)](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) that spans **both IETF SD-JWT VC and ISO mdoc**. A relying party implementing HAIP can accept either format through a single integration. Both OID4VP v1.0 and OID4VCI v1.0 reached final OpenID Foundation specification status in 2025. July 2025 interoperability testing demonstrated cross-vendor interop across OID4VCI v16, OID4VP HAIP, ISO 18013-5, ISO 18013-7, and IETF SD-JWT draft 17.

#### 2. W3C Digital Credentials API (Browser Layer)

The [W3C Digital Credentials API](https://www.w3.org/blog/2025/w3c-digital-credentials-api-publication-the-next-step-to-privacy-preserving-identities-on-the-web/) is the browser-level abstraction that requests credentials from a wallet regardless of their underlying format (mdoc or W3C VC). Key milestones:
- **Chrome 141** and **Safari 26** shipped stable Digital Credentials API support in September 2025
- **Firefox 149** carries baseline implementation code (Q1 2026)
- **iOS 26** supports W3C Digital Credentials API for requesting mdocs from Safari/WebKit, including TSA-approved digital passports
- **ISO 18013-7 (2nd edition)** is being revised to incorporate the W3C Digital Credentials API as an Annex C transport — directly embedding the W3C browser API into the ISO standard
- The W3C FedID Working Group hardcoded OpenID4VP, OID4VCI, and ISO 18013-7 Annex C directly into the spec at TPAC (November 2025), eliminating an open registry in favour of explicit format enumeration

**Resources:**
- [W3C Blog — Digital Credentials API: the next step to privacy-preserving identities on the web](https://www.w3.org/blog/2025/w3c-digital-credentials-api-publication-the-next-step-to-privacy-preserving-identities-on-the-web/)
- [Biometric Update — Support for W3C Digital Credentials API, digital identity passports part of iOS 26](https://www.biometricupdate.com/202506/support-for-w3c-digital-credentials-api-digital-identity-passports-part-of-ios-26)
- [Corbado — Digital Credentials API (2026): Chrome, Safari & Firefox](https://www.corbado.com/blog/digital-credentials-api)

#### 3. W3C CCG Verifiable Driver's License Vocabulary

The W3C Credentials Community Group publishes the [Verifiable Driver's License (VDL) Vocabulary](https://w3c-ccg.github.io/vdl-vocab/), an experimental specification that maps W3C VC JSON-LD terms to the ISO 18013 mDL data model. A verifier that understands the VDL vocabulary can consume a W3C VC containing mDL-equivalent attributes. This is the semantic bridge — allowing a W3C VC to carry the same claims as an mdoc in an interoperable, human-readable, extensible format.

**Resource:**
- [W3C CCG — Verifiable Driver's License Vocabulary v0.1](https://w3c-ccg.github.io/vdl-vocab/)
- [Identity Woman — Where the W3C Verifiable Credentials meets the ISO 18013-5 Mobile Driving License](https://medium.com/@identitywoman-in-business/where-the-w3c-verifiable-credentials-meets-the-iso-18013-5-mobile-driving-license-2b0a6c992920)

#### 4. EUDI Wallet Architecture (Dual-Format Mandate)

The EUDI Wallet Architecture Reference Framework mandates that member-state wallets carry **both** mdoc and SD-JWT VC for the same credential (e.g., driving licence), presented over OID4VP. This forces issuer and verifier ecosystems to support both, and in doing so creates a de-facto interoperability layer at the wallet level. The same document, same holder — two formats, one wallet. This is the most consequential practical forcing function for convergence globally.

---

### Forcing Functions: UNECE, EU Digital Product Passport, W3C DPP Vocabulary

#### UNECE — UN Transparency Protocol (UNTP)

The UN Economic Commission for Europe, through its UN Centre for Trade Facilitation and Electronic Business (UN/CEFACT), has published **UNECE Recommendation No. 49** and the associated [UN Transparency Protocol (UNTP)](https://untp.unece.org/docs/specification/). The UNTP is the most direct forcing function for W3C VC adoption in supply chain and product contexts:

- **All Digital Product Passports (DPPs) in UNTP MUST be issued as W3C Verifiable Credentials**, conforming to VCDM 2.0, with `@context` referencing both W3C VCDM and UNTP context URIs
- All UNTP data objects — Digital Product Passport (DPP), Digital Conformity Credential (DCC), Digital Traceability Events (DTE), Digital Identity Anchor (DIA) — are W3C VCs
- The architecture is **fully decentralized**: no central repository, credentials linked via DIDs, readable by parties at any technical maturity level
- JSON-LD syntax is mandated for all issued credentials to ensure semantic interoperability across supply chains
- A joint **UNECE/ISO initiative on Digital Product Passport** was launched to align these two bodies' DPP work, acknowledging that ISO controls attribute vocabularies while UNECE/W3C controls the credential wrapper

**ISO 18013-5 relevance:** The UNTP explicitly acknowledges that sustainability evidence in value chains may be presented as "W3C VCs, ISO mDL credentials, Hyperledger AnonCreds, or human-readable PDF documents." Rather than mandating one format, UNTP recommends "the narrowest practical set of technical options for a given business requirement" — which in practice means W3C VC VCDM 2.0 for supply chain/product credentials, and allows ISO mdoc for identity bearer credentials that accompany supply chain actors.

**Resources:**
- [UNTP — Digital Product Passport specification](https://untp.unece.org/docs/specification/DigitalProductPassport/)
- [UNTP — Verifiable Credentials](https://untp.unece.org/docs/0.6.0/specification/VerifiableCredentials/)
- [UNECE — UNECE and ISO launch joint initiative on Digital Product Passport](https://unece.org/digitalization/news/unece-and-iso-launch-joint-initiative-digital-product-passport-advance)
- [UNCTAD — Unlocking transparency: The promise of the UN Transparency Protocol for global trade](https://unctad.org/news/unlocking-transparency-promise-un-transparency-protocol-global-trade)

#### EU Digital Product Passport — ESPR and the European Business Wallet

The **Ecodesign for Sustainable Products Regulation (ESPR)**, in force since July 2024, creates the legal basis for DPP obligations across product categories being phased in 2026–2030 (batteries first, then textiles, electronics, construction). The DPP must use "secure, verifiable digital credentials in a standardized format" — in practice, W3C VCs.

The **European Business Wallet (EBW)**, a business-facing counterpart to the EUDI citizen wallet, enables companies to issue and receive verifiable credentials including DPPs, licences, and power-of-attorney attestations. It connects the EUDI/eIDAS identity infrastructure directly to the DPP supply chain use case — the same wallet infrastructure that carries a driving licence as an mdoc or SD-JWT VC can carry a DPP as a W3C VC.

This is a significant forcing function: the EU is mandating that **identity credentials** (driving licence → EUDI wallet) and **product credentials** (DPP → European Business Wallet) share the same trust infrastructure, credential formats, and presentation protocols — pushing the entire ecosystem toward format convergence.

**Resources:**
- [Spherity — European Business Wallet (EIDA)](https://www.spherity.com/eida)
- [Spherity Medium — Implementing Digital Product Passports using decentralized identity standards](https://medium.com/spherity/implementing-digital-product-passports-using-decentralized-identity-standards-f1102c452020)
- [arXiv — Digital Product Passport Management with DIDs and VCs (extended version)](https://arxiv.org/html/2410.15758v1)
- [Cyber3Lab — Why We're Excited About Digital Product Passports, EUDI and European Business Wallets](https://cyber3lab.howest.be/en/news/why-were-excited-about-digital-product-passports-eudi-and-european-business-wallets)
- [ITICP — EU Digital Product Passports: What's New in 2025–2026](https://www.iticp.org/l/eu-digital-product-passports-what-s-new-in-2025-2026/)

> **Note on "EU WEBUILD":** This specific name did not surface in current documentation. If you are referring to a particular EU Building Blocks programme (CEF Digital / European Digital Building Blocks), the Digital Europe Programme, or a specific consortium project, please clarify — the closest matching initiative found is the European Business Wallet and the EU Digital Building Blocks infrastructure.

#### W3C Digital Product Passport Vocabulary Work

The W3C VC Working Group charter explicitly includes developing **vocabularies for product credentials** — expressing facts such as origin, materials, repairability, and recyclability as VCs, "in line with the upcoming European Business Wallet, contributing to the EU's and W3C's sustainability goals." This is an active standardization track that will canonicalize the vocabulary bridge between ESPR/UNTP and the W3C VC ecosystem, analogous to what the VDL vocabulary does for driving licences.

---

### Data Exchange Protocols Under Consideration

#### IETF GNAP (RFC 9635) — Published, VC-Ready

The **Grant Negotiation and Authorization Protocol** ([GNAP, RFC 9635](https://datatracker.ietf.org/doc/html/rfc9635), published October 2024) is the IETF's next-generation authorization protocol, designed to overcome the limitations of OAuth 2.0. The GNAP working group charter explicitly includes conveying **Verifiable Credentials** as assertions within the protocol — a client can present unverified identifiers and verifiable assertions (including VCs) to an Authorization Server as part of its access request.

GNAP is architecturally richer than OAuth 2.0: it supports multiple interaction modes, continuation tokens, asymmetric key-bound requests, and negotiated access — making it a natural fit for the multi-party, multi-credential flows that DPP and identity wallet use cases require. A companion spec, [RFC 9767 — GNAP Resource Server Connections](https://datatracker.ietf.org/doc/rfc9767/), was also finalized to cover RS-to-AS communication.

#### GNAP4VP — GNAP Extended for Verifiable Presentations in Data Spaces

A May 2025 paper ([arXiv:2505.24698](https://arxiv.org/abs/2505.24698), presented at MobiSPC, Leuven, August 2025) proposes **GNAP4VP**: an extension of GNAP that integrates OpenID Connect for Verifiable Presentations (OIDC4VP) and Linked Verifiable Presentations (LVP) for use in **Data Spaces** — the federated, sector-specific data exchange environments (e.g., Gaia-X, Catena-X, IDSA) gaining traction in Europe.

GNAP4VP offers two interaction flows:
- **Wallet-Driven Interaction** — uses OIDC4VP; the holder's wallet drives credential selection and presentation
- **LVP Authorization** — fully automated machine-to-machine communication using Linked Verifiable Presentations, suitable for IoT and supply chain endpoints with no human in the loop

The protocol adheres to Self-Sovereign Identity (SSI) principles — decentralized, user-centric — while preserving flexibility for negotiated authorization. Though currently in the research stage, it is directly relevant to the DPP supply chain use case where automated M2M exchange of product credentials (W3C VCs) needs to co-exist with identity credential presentation (mdoc or SD-JWT VC).

#### Protocol Landscape Summary

| Protocol | Status | Role | VC/mdoc Support |
|---|---|---|---|
| **OID4VP v1.0** | OpenID Final Spec (2025) | Presentation layer for both formats | Both W3C VC and mdoc |
| **OID4VCI v1.0** | OpenID Final Spec (2025) | Issuance protocol | Both W3C VC and mdoc |
| **OpenID4VC HAIP** | Draft 04 (active) | High-assurance profile unifying both | SD-JWT VC + mdoc |
| **W3C Digital Credentials API** | W3C draft (browser impl 2025) | Browser-level wallet request | Both (format-agnostic) |
| **GNAP (RFC 9635)** | IETF RFC (Oct 2024) | Next-gen authorization; VC assertions supported | W3C VC assertions |
| **GNAP4VP** | Research / preprint (May 2025) | GNAP + VP for Data Spaces, M2M | W3C VC + SSI |
| **UNTP / JSON-LD** | UNECE Rec. 49 (active) | DPP supply chain data exchange | W3C VC VCDM 2.0 (mandatory) |

**Resources:**
- [IETF GNAP WG — datatracker.ietf.org](https://datatracker.ietf.org/wg/gnap/about/)
- [RFC 9635 — Grant Negotiation and Authorization Protocol](https://datatracker.ietf.org/doc/html/rfc9635)
- [RFC 9767 — GNAP Resource Server Connections](https://datatracker.ietf.org/doc/rfc9767/)
- [arXiv:2505.24698 — GNAP4VP: Next Generation Authentication for Data Spaces](https://arxiv.org/abs/2505.24698)
- [oauth.net — GNAP overview](https://oauth.net/gnap/)
- [Biometric Update — OpenID VC spec shows interoperability between issuers, digital wallets (July 2025)](https://www.biometricupdate.com/202507/openid-vc-spec-shows-interoperability-between-issuers-digital-wallets)

---

## North America

### United States

**Production deployments — TSA-accepted mDLs**

As of early 2026, **21 US states plus Puerto Rico** have TSA-accepted mDL programs: Alaska, Arizona, Arkansas, California, Colorado, Delaware, Georgia, Hawaii, Illinois, Iowa, Kentucky, Louisiana, Maryland, Montana, New Mexico, New York, North Dakota, Ohio, Utah, Virginia, and West Virginia. The TSA published a final rule in October 2024 permitting mobile IDs at airport security checkpoints.

Selected enrollment figures:
- **Louisiana**: ~2 million mDLs issued (leading nationally)
- **California**: 2,654,774 mDLs as of August 2025
- **Arizona**: ~23% of licensed drivers hold an mDL
- **New York**: >200,000 Mobile IDs as of March 2025
- **National total**: ~8 million mDLs as of mid-2025

**Online presentation (ISO 18013-7 / W3C VC):** Remote ID verification via 18013-7 is in early-adopter stage; full W3C VC interoperability across states is an ongoing fragmentation challenge.

**Resources:**
- [Trinsic — State of Mobile Driver's Licenses in the U.S.](https://trinsic.id/state-of-mobile-drivers-licenses-in-the-u-s/)
- [Digital Government Hub — mDL Resource Guide](https://digitalgovernmenthub.org/publications/resource-guide-understanding-the-technology-risks-and-opportunities-for-mobile-drivers-licenses-mdls/)
- [Regula — Mobile Driver's License Global Status 2026](https://regulaforensics.com/blog/mobile-drivers-license-verification/)
- [Biometric Update — mDL fragmentation clouds US digital ID landscape](https://www.biometricupdate.com/202510/mdl-fragmentation-clouds-us-digital-id-landscape-as-adoption-ticks-steadily-up)

### Canada

**Status: Active pilots, provincial rollouts announced for 2026**

Digital Driver's Licences (DDLs) are launching as opt-in mobile apps in **Ontario, British Columbia, Alberta, and Saskatchewan**, using encrypted QR codes verified by RCMP scanners. Quebec has a Digital ID initiative planned for 2025 incorporating driver's licences into a provincial wallet alongside health insurance cards and birth certificates. A federal API is being developed for inter-provincial suspension/status interoperability ("Fit-to-Drive" protocol). Nationwide DDL alignment is targeted for 2026 via intergovernmental pact.

**Resources:**
- [IT World Canada — State of Digital ID in Canada](https://www.itworldcanada.com/article/the-state-of-digital-id-in-canada/484618)
- [Canada.ca — Trusted access to digital services](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/digital-credentials.html)
- [Biometric Update — Mobile driver's licenses, digital ID find support in US, Canada](https://www.biometricupdate.com/202509/mobile-drivers-licenses-digital-id-find-support-in-us-canada)

---

## Europe

### European Union — EUDI Wallet / eIDAS 2.0

**Status: Mandated, large-scale pilots concluded, member-state wallets due by end of 2026**

eIDAS 2.0 was formally adopted in **March 2024** and represents the most comprehensive government mandate for VC-based identity globally. All 27 EU member states must provide citizens with [European Digital Identity (EUDI) Wallets](https://digital-strategy.ec.europa.eu/en/policies/eudi-regulation) by **December 2026**. The wallet must carry electronic attestations including **driving licences, professional qualifications, and bank account access** as W3C VCs or mdoc credentials.

The **POTENTIAL large-scale pilot**, conducted across **19 EU Member States** and concluded September 2025, is the single largest government VC deployment globally. It demonstrated:
- Cross-border issuance and verification (credential issued in one state, verified by service provider in another)
- Use cases: banking account opening, SIM registration, e-government, age-restricted purchases
- Participation from **350+ companies and government agencies**

**Timeline:**

| Date | Milestone |
|---|---|
| March 2024 | eIDAS 2.0 formally adopted |
| Sept 2024 | First member-state wallet functionalities integrated |
| Oct 2024 | ISO 18013-7 standard published (online mDL) |
| Sept 2025 | POTENTIAL pilot concluded |
| End 2025 | Core trust services in place |
| End 2026 | All member states must offer EUDI wallets |

**Resources:**
- [European Commission — EUDI Regulation](https://digital-strategy.ec.europa.eu/en/policies/eudi-regulation)
- [EUDI Wallet Hub](https://www.eudi-wallet.eu/)
- [Entrust — What is eIDAS 2?](https://www.entrust.com/resources/learn/eidas-2)
- [Everycred — 2025 State of Verifiable Credential Report](https://everycred.com/blog/2025-state-of-verifiable-credential-report/)

### United Kingdom

**Status: GOV.UK Wallet live (2025), digital driving licence announced**

Post-Brexit, the UK operates under its own [Digital Identity and Attributes Trust Framework (DIATF)](https://www.gov.uk/government/publications/uk-digital-identity-and-attributes-trust-framework-04), now statutory under the **Data (Use and Access) Act 2025** (gamma v0.4, in force December 2025).

The GOV.UK Wallet hosts government-issued W3C Verifiable Credentials. The DVLA (Driver and Vehicle Licensing Agency) will issue **digitally-signed mDLs** into the wallet. Rollout: HM Armed Forces Veteran Card from summer 2025; **full driving licence later in 2025**. UK digital ID sector actors have raised concerns about wallet interoperability and market access.

**Resources:**
- [GOV.UK — UK Digital Identity and Attributes Trust Framework](https://www.gov.uk/government/publications/uk-digital-identity-and-attributes-trust-framework-04)
- [CMS Law — Digital identity in the UK: DUA Bill](https://cms-lawnow.com/en/ealerts/2025/05/digital-identity-in-the-uk-a-new-legislative-framework-under-the-dua-bill)
- [Biometric Update — UK digital ID sector warns of legal action if mDL limited to GOV.UK Wallet](https://www.biometricupdate.com/202602/uk-digital-id-sector-warns-of-legal-action-if-mdl-limited-to-gov-uk-wallet)

---

## Asia-Pacific

### Australia

**Status: Production deployments, ISO 18013-5 aligned, international interoperability work underway**

Multiple states have operational mDL programs:
- **Queensland**: First Australian mDL aligned with ISO 18013-5; >640,000 app downloads in first 7 months post-launch (late 2023), representing ~15% digital penetration among licence holders. Cited as a potential global model for mDL deployment architecture.
- **Victoria**: Adopted mDLs as valid digital ID in **April 2024**.

Australia is working with **Japan and South Korea** on mutual recognition and interoperability of Verifiable Digital Credentials (VDCs).

**Resources:**
- [Biometric Update — Queensland mDL could be model for global mDL deployment](https://www.biometricupdate.com/202502/queensland-mobile-drivers-license-could-be-model-for-global-mdl-deployment)
- [Biometric Update — More Australians can now use mDLs (April 2024)](https://www.biometricupdate.com/202404/more-australians-can-now-use-mdls)

### Japan

**Status: Digital National ID issued on smartphones (2025), mDL/mdoc format**

Japan began issuing its **My Number Card digitally on iPhones** on **June 24, 2025**, in mdoc format, with Android support planned for 2026. Japan is coordinating with South Korea and Australia on VDC interoperability. A broader ecosystem of driving licence integration into smartphone wallets follows the My Number Card rollout.

**Resources:**
- [Everycred — 2025 State of Verifiable Credential Report](https://everycred.com/blog/2025-state-of-verifiable-credential-report/)
- [Mobile driver's license — Wikipedia](https://en.wikipedia.org/wiki/Mobile_driver%27s_license)

### South Korea

**Status: Active mDL expansion, interoperability cooperation**

South Korea has an operational mDL programme and is participating in trilateral interoperability discussions with Japan and Australia on standardized Verifiable Digital Credentials, aligning with ISO 18013-5 and W3C VC frameworks.

### India

**Status: World's largest government VC platform (DigiLocker) — driving licences legally accepted digitally**

India's [DigiLocker](https://www.digilocker.gov.in/) platform, launched 2015 under Digital India / MeitY, has scaled to:
- **513 million registered users** (~40% of population)
- **5.6 billion+ documents issued**

Driving licences stored in DigiLocker are **legally accepted at traffic checkpoints** and for vehicle registration, insurance, and transport services. The platform supports selective disclosure of attributes from credentials such as Aadhaar and driving licence. While DigiLocker uses cryptographically signed documents, interoperability with the W3C VC Data Model is a stated direction as India refines its national digital identity architecture.

In October 2024, DigiLocker integrated with UMANG for access to 1,658+ central and state government services.

**Resources:**
- [DigiLocker — Official portal](https://www.digilocker.gov.in/)
- [Everycred — Top 5 Use Cases for Verifiable Credentials in a DigiLocker](https://everycred.com/blog/verifiable-credentials-digilocker/)
- [1Kosmos — Digital Identity Spotlight: India](https://www.1kosmos.com/identity-management/digital-identity-spotlight-india/)

### Singapore

**Status: Leading digital ID infrastructure, VC adoption underway**

Singapore is identified as a regional leader in digital identity systems alongside India and South Korea, with robust national digital ID underpinning VC adoption. Specific mDL details remain limited in public reporting.

---

## Latin America

### Brazil

**Status: Verifiable Credentials adopted for gov.br platform; digital CNH (driver's licence) live**

Brazil's **"Identidade Digital Gov.br"** project unifies documents in a mobile app with QR codes and biometric verification. The **digital CNH (Carteira Nacional de Habilitação)** is live and accepted as valid identification. Brazil adopted a **Decentralized Credentials-as-a-Service (DaaS)** model for issuance in 2025.

Brazil and Uruguay operationalized the **first cross-border digital ID integration in Latin America** in production by October 2024 — 77 million Brazilians can use their Gov.br digital ID for services on Uruguayan government platforms. By end-2025, 39 services are covered.

**Resources:**
- [Biometric Update — Brazil adopts DaaS for verifiable credentials](https://www.biometricupdate.com/202507/brazil-adopts-daas-for-verifiable-credentials)
- [ID Tech Wire — Uruguay and Brazil plan digital ID broker for cross-border services](https://idtechwire.com/uruguay-and-brazil-plan-digital-id-broker-for-cross-border-services-by-late-2025/)
- [VisaHQ — Cross-border digital ID deal lets 77 million Brazilians access foreign services](https://www.visahq.com/news/2025-12-27/br/cross-border-digital-id-deal-with-uruguay-lets-77-million-brazilians-access-foreign-services/)

### Mercosur Region (Argentina, Paraguay, Uruguay)

**Status: Cross-border interoperability framework active**

The **Mercosur Digital Citizen** programme enables citizens of Argentina, Brazil, Paraguay, and Uruguay to use national digital IDs for government services across borders. Argentina and Paraguay are expected to join the full interoperability framework in 2026.

**Verifiable Credentials pilot (mid-2025+):** First-wave participants include **Argentina, Brazil, Costa Rica, Dominican Republic, Paraguay, and Uruguay**. The Dominican Republic is separately piloting VCs for small businesses.

**Resources:**
- [Biometric Update — Mercosur nations launch cross-border digital ID initiative](https://www.biometricupdate.com/202411/mercosur-nations-launch-cross-border-digital-id-initiative)
- [Namirial — Digital identity in Latin America: progress, challenges and outlook for 2025](https://www.namirial.com/en/blog/ecosystem/digital-identity-in-latin-america-progress-challenges-and-outlook-for-2025/)
- [50-in-5 — Building Trust Across Borders: Latin America's Path to Interoperable Digital ID](https://50in5.net/building-trust-across-borders-latin-americas-path-to-interoperable-digital-id/)

---

## Middle East & Africa

### Oman

**Status: Legal recognition granted for digital national ID and driver's licence (2025)**

Digital versions of Oman's national identity card and **driver's licence now carry equal legal standing** to their physical counterparts.

**Resources:**
- [Biometric Update — Digital versions of Oman's national ID, driver's license get legal recognition](https://www.biometricupdate.com/202509/digital-versions-of-omans-national-id-drivers-license-get-legal-recognition)

### UAE

UAE Pass is a leading regional digital identity system (~60% adult digital ID coverage across the Middle East region). Specific VC/mDL driving licence details are in the broader UAE Pass ecosystem.

### South Africa

**Status: mDL announced, timeline 2027–2028**

South Africa's Department of Transport has announced a mobile driver's licence (mDL) as part of the **MyMzansi** functional ID component. The mDL will be one of multiple Verifiable Credentials accessible via a secure mobile wallet. Nationwide rollout is targeted for 2028; hosting infrastructure deadline is March 2027. The president announced the digital ID and mDL in early 2026.

**Resources:**
- [Biometric Update — South Africa builds mDL as part of MyMzansi](https://www.biometricupdate.com/202512/south-africa-builds-mdl-as-part-of-mymzansi-functional-id-component)
- [Biometric Update — South Africa digital ID and mDL to launch this year, president promises](https://www.biometricupdate.com/202602/south-africa-digital-id-and-mdl-to-launch-this-year-president-promises)
- [TechCentral — South Africa's digital ID gets a targeted launch date](https://techcentral.co.za/south-africas-digital-id-gets-a-launch-date/280460/)

---

## Summary Table

| Region | Jurisdiction | Status | Format | Notes |
|---|---|---|---|---|
| **NA** | USA (21 states + PR) | Production | ISO 18013-5 / mdoc | TSA-accepted; ~8M issued |
| **NA** | Canada (ON/BC/AB/SK) | Pilot / rollout | Encrypted QR / DDL | Federal interop API in progress |
| **EU** | EU 27 member states | Mandated law (EUDI) | W3C VC + mdoc | Dec 2026 deadline; POTENTIAL pilot done |
| **EU** | UK | Rolling out 2025 | W3C VC (mDL via DVLA) | GOV.UK Wallet; DUA Act 2025 |
| **APAC** | Australia (QLD, VIC…) | Production | ISO 18013-5 | QLD model cited globally |
| **APAC** | Japan | Production (2025) | mdoc (My Number) | iPhone first; Android 2026 |
| **APAC** | South Korea | Production | ISO 18013-5 | Trilateral interop (JP, AU) |
| **APAC** | India | Production (DigiLocker) | Signed docs → W3C VC direction | 513M users; DL legally accepted |
| **LATAM** | Brazil | Production | Gov.br VC / DaaS | Digital CNH live; cross-border w/ UY |
| **LATAM** | Uruguay / Mercosur | Production / pilot | W3C VC | Cross-border with Brazil live |
| **LATAM** | Dominican Republic | Pilot | W3C VC | Small business credentials |
| **MEA** | Oman | Production | National ID / DL digital | Legal parity granted 2025 |
| **MEA** | South Africa | Announced | mDL (MyMzansi) | 2027–2028 rollout |

---

## Key Cross-Cutting Resources

- [W3C — Verifiable Credentials 2.0 press release](https://www.w3.org/press-releases/2025/verifiable-credentials-2-0/)
- [Everycred — 2025 State of Verifiable Credential Report](https://everycred.com/blog/2025-state-of-verifiable-credential-report/)
- [Trinsic — 2025 Landscape of Global Digital ID Adoption](https://trinsic.id/2025-landscape-of-global-digital-id-adoption/)
- [FIDO Alliance — Passkeys and Verifiable Digital Credentials (White Paper, 2025)](https://fidoalliance.org/passkeys-and-verifiable-digital-credentials-a-harmonized-path-to-secure-digital-identity/)
- [GS1 — VCs and DIDs Technical Landscape](https://ref.gs1.org/docs/2025/VCs-and-DIDs-tech-landscape)
- [Regula — Mobile Driver's License 2026 Global Status](https://regulaforensics.com/blog/mobile-drivers-license-verification/)
- [Corbado — ISO 18013-7 mDLs in Bank Onboarding and KYC (2026)](https://www.corbado.com/blog/iso-18013-7-mdl-bank-kyc-onboarding)
