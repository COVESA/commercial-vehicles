# W3C Verifiable Credentials for Individual Identity and Driver's Licenses — Global Status (2025–2026)

*Updated September 2026. Facts verified against primary sources where available; see Unverified Claims at the end.*

> **Note on standards overlap:** Two credential formats dominate digital driver's license (mDL) deployments: **ISO/IEC 18013-5** (mdoc, proximity presentation) and **W3C Verifiable Credentials Data Model** (JSON-LD/JWT, online presentation). These converge in practice — ISO/IEC TS 18013-7 (online mdoc presentation; first edition October 2024, second edition May 2025 adding the W3C Digital Credentials API as a normative transport) is being paired with W3C VC semantics in wallet architectures, and the EUDI Wallet mandate explicitly supports both formats. Where a deployment uses either or both, it is included here.

---

## Standards Baseline

| Spec | Status | Relevance |
|---|---|---|
| [W3C VC Data Model v2.0](https://www.w3.org/TR/vc-data-model-2.0/) | **W3C Recommendation**, May 2025 | Core VC format |
| [ISO/IEC 18013-5:2021](https://www.iso.org/standard/69084.html) | Published 2021; [revision at DIS stage](https://www.iso.org/standard/91081.html) (2026) | Proximity mDL (mdoc) |
| [ISO/IEC TS 18013-7:2025](https://www.iso.org/standard/91154.html) | Ed. 2 published May 2025 (supersedes 2024 Ed. 1); adds normative Annex C for W3C Digital Credentials API | Online mDL presentation |
| [ISO/IEC TS 23220 series](https://www.iso.org/standard/86783.html) | Parts 2, 3 and 4 published 2026; Part 5 in development | Building blocks for mobile eID / mdoc-based credentials |
| [IETF RFC 9901 (SD-JWT)](https://datatracker.ietf.org/doc/rfc9901/) | Proposed Standard, Nov 2025 | Selective disclosure for JWT-based VCs |
| [IETF SD-JWT VC](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/) | Draft -19 (Aug 2026), in IESG evaluation | VC profile of SD-JWT used by EUDI |
| [IETF BBS Signatures](https://datatracker.ietf.org/doc/draft-irtf-cfrg-bbs-signatures/) | IRTF draft -12 (Sep 2026), not an RFC | Unlinkable selective disclosure |

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
| **Online extension** | Native (HTTP-based presentation) | ISO/IEC TS 18013-7:2025 (OID4VP and W3C Digital Credentials API) |

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

**W3C VC with SD-JWT (IETF RFC 9901; SD-JWT VC profile at draft -19, in IESG evaluation as of September 2026):**
At issuance, each claim is individually salted and hashed. The holder receives a JWT containing hashes plus individual per-claim disclosure tokens. At presentation, the holder selects which disclosure tokens to release. Cryptographic linkability between claims is prevented by the salt/hash structure.

**W3C VC with BBS+ signatures:**
Supports *unlinkable* selective disclosure — different presentations of the same credential are cryptographically indistinguishable from each other, preventing correlation across verifiers. This is stronger privacy than SD-JWT or mdoc for high-frequency use cases. BBS remains an IRTF draft (draft-irtf-cfrg-bbs-signatures-12, September 2026) with no RFC yet, so production deployments today rely on SD-JWT or mdoc selective disclosure.

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

- **ISO/IEC TS 18013-7** (Ed. 1 October 2024; Ed. 2 May 2025) defines how mdoc credentials are presented over the internet using OID4VP and, since Ed. 2, the W3C Digital Credentials API (Annex C).
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

The [OpenID4VC HAIP 1.0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html) (Final, 24 December 2025) defines a single profile of [OpenID for Verifiable Presentations (OID4VP)](https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html) and [OpenID for Verifiable Credential Issuance (OID4VCI)](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) that spans **both IETF SD-JWT VC and ISO mdoc**. A relying party implementing HAIP can accept either format through a single integration. OID4VP 1.0 reached Final status on 9 July 2025 and OID4VCI 1.0 on 16 September 2025; the OpenID Foundation [completed its conformance programme](https://openid.net/oidf-completes-conformance-programme-for-widely-adopted-digital-identity-standards/) for both, with HAIP, in July 2026. July 2025 interoperability testing demonstrated cross-vendor interop across OID4VCI v16, OID4VP HAIP, ISO 18013-5, ISO 18013-7, and IETF SD-JWT draft 17.

#### 2. W3C Digital Credentials API (Browser Layer)

The [W3C Digital Credentials API](https://www.w3.org/blog/2025/w3c-digital-credentials-api-publication-the-next-step-to-privacy-preserving-identities-on-the-web/) is the browser-level abstraction that requests credentials from a wallet regardless of their underlying format (mdoc or W3C VC). Key milestones:
- **Chrome 141** (October 2025) and **Safari 26** shipped Digital Credentials API support; Chrome supports OpenID4VP and ISO 18013-7 Annex C, Safari supports mdoc (`org-iso-mdoc`) only. Chrome 143 added an issuance origin trial (`navigator.credentials.create()` over OpenID4VCI, Android only).
- **Firefox**: Mozilla's [standards position](https://github.com/mozilla/standards-positions/issues/1003) remains negative and no shipping implementation has been confirmed.
- **iOS 26.1** ships [Apple Digital ID](https://www.apple.com/newsroom/2025/11/apple-introduces-digital-id-a-new-way-to-create-and-present-an-id-in-apple-wallet/) (November 2025), a US-passport-derived ID accepted at 250+ TSA checkpoints, and supports the Digital Credentials API for requesting mdocs from Safari/WebKit.
- **ISO/IEC TS 18013-7:2025 (Ed. 2)** incorporates the W3C Digital Credentials API as a normative Annex C transport, embedding the W3C browser API in the ISO standard.
- The W3C specification enumerates OpenID4VP and ISO 18013-7 Annex C as its exchange protocols. In June 2026 the [W3C Council overruled a formal objection](https://www.w3.org/2026/06/council-digital-credentials-report.html) to the normative reference to the fee-gated ISO Annex C, treating it as a narrow exception. The spec is a Working Draft (latest September 2026).

**Resources:**
- [W3C Blog — Digital Credentials API: the next step to privacy-preserving identities on the web](https://www.w3.org/blog/2025/w3c-digital-credentials-api-publication-the-next-step-to-privacy-preserving-identities-on-the-web/)
- [Biometric Update — Support for W3C Digital Credentials API, digital identity passports part of iOS 26](https://www.biometricupdate.com/202506/support-for-w3c-digital-credentials-api-digital-identity-passports-part-of-ios-26)
- [Corbado — Digital Credentials API (2026): Chrome, Safari & Firefox](https://www.corbado.com/blog/digital-credentials-api)
- [Chrome — Digital Credentials API shipped](https://developer.chrome.com/blog/digital-credentials-api-shipped) · [Chrome 143 issuance origin trial](https://developer.chrome.com/blog/digital-credentials-api-143-issuance-ot)
- [W3C Council report on the Digital Credentials API formal objection (June 2026)](https://www.w3.org/2026/06/council-digital-credentials-report.html)

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

The **European Business Wallet (EBW)**, a business-facing counterpart to the EUDI citizen wallet, is at present a legislative [proposal](https://digital-strategy.ec.europa.eu/en/library/proposal-regulation-establishment-european-business-wallets) (Commission, 19 November 2025; [Council negotiating position](https://www.consilium.europa.eu/en/press/press-releases/2026/06/09/european-business-wallets-council-adopts-negotiating-position/) adopted 9 June 2026; political agreement targeted for end-2026). Once adopted it would enable companies to issue and receive verifiable credentials including DPPs, licences, and power-of-attorney attestations. It connects the EUDI/eIDAS identity infrastructure directly to the DPP supply chain use case — the same wallet infrastructure that carries a driving licence as an mdoc or SD-JWT VC can carry a DPP as a W3C VC.

This is a significant forcing function: the EU intends that **identity credentials** (driving licence → EUDI wallet) and **product credentials** (DPP → European Business Wallet) share the same trust infrastructure, credential formats, and presentation protocols — pushing the entire ecosystem toward format convergence.

**Resources:**
- [Spherity — European Business Wallet (EIDA)](https://www.spherity.com/eida)
- [Spherity Medium — Implementing Digital Product Passports using decentralized identity standards](https://medium.com/spherity/implementing-digital-product-passports-using-decentralized-identity-standards-f1102c452020)
- [arXiv — Digital Product Passport Management with DIDs and VCs (extended version)](https://arxiv.org/html/2410.15758v1)
- [Cyber3Lab — Why We're Excited About Digital Product Passports, EUDI and European Business Wallets](https://cyber3lab.howest.be/en/news/why-were-excited-about-digital-product-passports-eudi-and-european-business-wallets)
- [ITICP — EU Digital Product Passports: What's New in 2025–2026](https://www.iticp.org/l/eu-digital-product-passports-what-s-new-in-2025-2026/)

> **WE BUILD:** the EU's second-wave large-scale pilot on business and organisational wallets (launched 2025, alongside APTITUDE), which prepares the ground for the European Business Wallet. See the [EC list of Large Scale Pilot projects](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/694487808/What+are+the+Large+Scale+Pilot+Projects).

#### W3C Digital Product Passport Vocabulary Work

The W3C VC Working Group's [2026 charter](https://w3c.github.io/vc-charter-2026/) (March 2026 to March 2028) lists **vocabularies for Digital Product Passports** as a tentative deliverable — expressing facts such as origin, materials, repairability, and recyclability as VCs, "in line with the upcoming European Business Wallet, contributing to the EU's and W3C's sustainability goals." If taken up, this track would canonicalize the vocabulary bridge between ESPR/UNTP and the W3C VC ecosystem, analogous to what the VDL vocabulary does for driving licences.

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
| **OID4VP 1.0** | OpenID Final (9 Jul 2025) | Presentation layer for both formats | Both W3C VC and mdoc |
| **OID4VCI 1.0** | OpenID Final (16 Sep 2025) | Issuance protocol | Both W3C VC and mdoc |
| **OpenID4VC HAIP 1.0** | OpenID Final (24 Dec 2025) | High-assurance profile unifying both | SD-JWT VC + mdoc |
| **W3C Digital Credentials API** | W3C Working Draft (Sep 2026); shipped in Chrome 141+, Safari 26 | Browser-level wallet request | Both (format-agnostic) |
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

As of September 2026, **21 US states plus Puerto Rico** have [TSA-accepted mDL programs](https://www.tsa.gov/digital-id/participating-states): Alaska, Arizona, Arkansas, California, Colorado, Georgia, Hawaii, Illinois, Iowa, Kentucky, Louisiana, Maryland, Montana, New Mexico, New York, North Dakota, Ohio, Oklahoma, Utah, Virginia, and West Virginia. Delaware's state app is not ISO 18013-5-based and is not TSA-accepted. The TSA published a final rule in October 2024 permitting mobile IDs at airport security checkpoints; since REAL ID enforcement began on 7 May 2025, TSA accepts only mDLs derived from REAL ID-compliant cards.

Platform wallets: Apple Wallet holds state IDs for 16 states plus Puerto Rico (Virginia added August 2026, Oklahoma September 2026), Google Wallet for 11 states plus Puerto Rico, and Samsung Wallet for about nine states (California added April 2026). In June 2026 TSA and Google launched [TSA PreCheck Touchless ID via Google Wallet](https://www.tsa.gov/news/press/releases/2026/06/24/tsa-google-wallet-launch-new-tsa-precheck-touchless-id-opt) at 65 airports.

Selected enrollment figures:
- **California**: more than [3.5 million applications](https://www.gov.ca.gov/2026/07/13/governor-newsom-signs-dmv-modernization-law-expands-mobile-drivers-license-access-for-millions-of-californians/) by July 2026, now leading nationally. SB 169 (signed 13 July 2026) raised the pilot cap from 15% to 60% of licensed drivers.
- **Louisiana**: ~1.8 million LA Wallet users (last public figure, May 2024)
- **Arizona**: ~23% of licensed drivers (about 1.1 million) hold an mDL
- **Georgia**: >800,000 downloads (GA DDS)
- **New York**: ~260,000 Mobile IDs one year after launch (June 2025)

No authoritative national total exists; AAMVA does not publish one.

**Trust infrastructure:** AAMVA's Digital Trust Service is the US trust anchor for mDL verification, and its [mDL Implementation Guidelines v1.6](https://www.aamva.org/identity/mobile-driver-license-digital-trust-service/for-issuing-authorities) (July 2026) are now required for participating issuers.

**Regulatory acceptance:** On 8 September 2026 FinCEN, together with the OCC, FDIC, Federal Reserve and NCUA, issued [FAQs](https://www.fincen.gov/news/news-releases/fincen-issues-frequently-asked-questions-regarding-treatment-verifiable-digital) confirming that an unexpired government-issued verifiable digital credential such as an mDL can satisfy the Customer Identification Program rule's "government-issued identification" requirement for in-person or remote account opening. The rule neither requires nor prohibits acceptance.

**Online presentation (ISO 18013-7 / W3C VC):** Remote ID verification via 18013-7 is in early-adopter stage; full W3C VC interoperability across states is an ongoing fragmentation challenge.

**Resources:**
- [Trinsic — State of Mobile Driver's Licenses in the U.S.](https://trinsic.id/state-of-mobile-drivers-licenses-in-the-u-s/)
- [Digital Government Hub — mDL Resource Guide](https://digitalgovernmenthub.org/publications/resource-guide-understanding-the-technology-risks-and-opportunities-for-mobile-drivers-licenses-mdls/)
- [Regula — Mobile Driver's License Global Status 2026](https://regulaforensics.com/blog/mobile-drivers-license-verification/)
- [Biometric Update — mDL fragmentation clouds US digital ID landscape](https://www.biometricupdate.com/202510/mdl-fragmentation-clouds-us-digital-id-landscape-as-adoption-ticks-steadily-up)
- [TSA — Participating states and eligible digital IDs](https://www.tsa.gov/digital-id/participating-states) · [Credence ID — US mDL state tracker](https://credenceid.com/resources/blog/us-mobile-drivers-license-mdl-state-tracker/)
- [FinCEN — FAQs on verifiable digital credentials under the CIP Rule (Sep 2026)](https://www.fincen.gov/news/news-releases/fincen-issues-frequently-asked-questions-regarding-treatment-verifiable-digital)

### Canada

**Status: No provincial digital driver's licence in production; legislative and wallet groundwork under way**

No Canadian province has launched a digital driver's licence. **Alberta** launched the [Alberta Wallet](https://www.alberta.ca/alberta-wallet) in August 2025 with a mobile health card; a driver's licence is listed only as a potential future document. **British Columbia** offers the BC Services Card app (the former BC Wallet functions were folded into it), which is a login and identity credential rather than a driving licence. **Ontario** paused its digital ID programme in 2024 and **Saskatchewan** halted its digital ID plan in 2022. **Quebec** adopted [Bill 82, the Act respecting the national digital identity](https://www.assnat.qc.ca/fr/travaux-parlementaires/projets-loi/projet-loi-82-43-1.html), on 22 October 2025; rollout of the provincial wallet is phased with no published launch date for the driver's licence. Earlier reports of RCMP-verified QR licences, a federal "Fit-to-Drive" status API and a 2026 intergovernmental pact could not be confirmed against any government source and have been removed.

**Resources:**
- [Alberta Wallet](https://www.alberta.ca/alberta-wallet)
- [BC Services Card / BC Wallet](https://www2.gov.bc.ca/gov/content/governments/government-id/bc-wallet)
- [Assemblée nationale du Québec — Bill 82](https://www.assnat.qc.ca/fr/travaux-parlementaires/projets-loi/projet-loi-82-43-1.html) · [ID Tech Wire — Quebec passes landmark digital ID law](https://idtechwire.com/quebec-passes-landmark-digital-id-law-emphasizing-privacy-and-user-control/)
- [Canada.ca — Trusted access to digital services](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/digital-credentials.html)

---

## Europe

### European Union — EUDI Wallet / eIDAS 2.0

**Status: Mandated; first-wave pilots concluded; first national wallets in production; all member-state wallets due by end of 2026**

eIDAS 2.0 (Regulation (EU) 2024/1183) was published on 30 April 2024 and entered into force on 20 May 2024. It is the most comprehensive government mandate for VC-based identity globally. Following the implementing acts adopted on 28 November 2024, all 27 EU member states must provide citizens with [European Digital Identity (EUDI) Wallets](https://digital-strategy.ec.europa.eu/en/policies/eudi-regulation) by **December 2026**, and regulated private relying parties (banks, telecoms, transport, health and others) must accept them from **24 December 2027**. The wallet must carry electronic attestations including **driving licences, professional qualifications, and bank account access** as SD-JWT VC or mdoc credentials.

The **4th Driving Licence Directive** ([Directive (EU) 2025/2205](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025L2205), in force 25 November 2025) makes a mobile driving licence issued into the EUDI Wallet the main format across the EU. Member states must apply it by 26 November 2029, with the digital licence available EU-wide by 2030.

**First national wallets are live.** Italy's IT-Wallet has operated inside the IO app since December 2024. Denmark launched [AltID](https://www.biometricupdate.com/202606/denmark-launches-altid-digital-wallet-for-proof-of-age-identity) on 3 June 2026, the first Nordic EUDI wallet in production, with zero-knowledge age verification. Denmark, France and Italy are in production pending EU notification; Germany targets 2 January 2027.

The **POTENTIAL large-scale pilot**, conducted across **19 EU Member States plus Ukraine** and concluded in 2025, was the largest of the four first-wave pilots (POTENTIAL, EWC, DC4EU, NOBID), all of which have now concluded. Its [final report](https://www.digital-identity-wallet.eu/wp-content/uploads/2025/10/Potential-Final-Press-Release.docx.pdf) counts more than 140 organisations, 1,300+ tests and 1,000+ successful transactions, 249 of them cross-border, covering bank account opening, SIM registration, e-government, driving licence and age-restricted purchases. Second-wave pilots **APTITUDE** and **WE BUILD** (business wallets) launched in 2025 and are active.

**Timeline:**

| Date | Milestone |
|---|---|
| 20 May 2024 | eIDAS 2.0 (Regulation 2024/1183) in force |
| Oct 2024 / May 2025 | ISO/IEC TS 18013-7 Ed. 1 / Ed. 2 published (online mDL) |
| 28 Nov 2024 | Implementing acts adopted; 24- and 36-month clocks start |
| Dec 2024 | Italy IT-Wallet live in IO app |
| 2025 | First-wave pilots (POTENTIAL, EWC, DC4EU, NOBID) conclude; APTITUDE and WE BUILD start |
| 25 Nov 2025 | 4th Driving Licence Directive in force (mDL in EUDI Wallet as main format) |
| 3 Jun 2026 | Denmark AltID launched |
| End 2026 | All member states must offer EUDI wallets |
| 24 Dec 2027 | Regulated private relying parties must accept EUDI wallets |
| 26 Nov 2029 | Driving Licence Directive application deadline; EU-wide digital licence by 2030 |

**Resources:**
- [European Commission — EUDI Regulation](https://digital-strategy.ec.europa.eu/en/policies/eudi-regulation)
- [EUDI Wallet Hub](https://www.eudi-wallet.eu/)
- [EC — Large Scale Pilot projects](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/694487808/What+are+the+Large+Scale+Pilot+Projects) · [POTENTIAL final press release](https://www.digital-identity-wallet.eu/wp-content/uploads/2025/10/Potential-Final-Press-Release.docx.pdf)
- [EC — Modernised EU rules on driving licences enter into force (Nov 2025)](https://transport.ec.europa.eu/news-events/news/modernised-eu-rules-driving-licences-and-driving-disqualifications-enter-force-2025-11-25_en)
- [eIDAS Pro — EUDI wallet rollout by member state (Apr 2026)](https://www.eidas-pro.com/blog/eudi-wallet-rollout-member-states-april-2026)
- [Entrust — What is eIDAS 2?](https://www.entrust.com/resources/learn/eidas-2)
- [Everycred — 2025 State of Verifiable Credential Report](https://everycred.com/blog/2025-state-of-verifiable-credential-report/)

### United Kingdom

**Status: GOV.UK Wallet live (2025); digital driving licence in private testing, public launch pending**

Post-Brexit, the UK operates under its own [Digital Identity and Attributes Trust Framework (DIATF)](https://www.gov.uk/government/publications/uk-digital-identity-and-attributes-trust-framework-04), now statutory under the **Data (Use and Access) Act 2025** (gamma v0.4 became the first statutory trust framework on 1 December 2025; OfDIA will announce during 2026 when [version 1.0](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-1-0/uk-digital-verification-services-trust-framework-1-0-pre-release) replaces it).

The GOV.UK Wallet hosts government-issued W3C Verifiable Credentials. The DVLA (Driver and Vehicle Licensing Agency) will issue **digitally-signed mDLs** into the wallet. Rollout: HM Armed Forces Veteran Card went live in 2025. The driving licence entered private testing in December 2025 and GDS said in [January 2026](https://gds.blog.gov.uk/2026/01/21/making-the-governments-first-digital-wallet-a-reality/) it would launch "later this year"; as of September 2026 it is still listed as forthcoming. UK digital ID sector actors have raised concerns about wallet interoperability and market access.

**Resources:**
- [GOV.UK — UK Digital Identity and Attributes Trust Framework](https://www.gov.uk/government/publications/uk-digital-identity-and-attributes-trust-framework-04)
- [GDS blog — Making the government's first digital wallet a reality (Jan 2026)](https://gds.blog.gov.uk/2026/01/21/making-the-governments-first-digital-wallet-a-reality/)
- [CMS Law — Digital identity in the UK: DUA Bill](https://cms-lawnow.com/en/ealerts/2025/05/digital-identity-in-the-uk-a-new-legislative-framework-under-the-dua-bill)
- [Biometric Update — UK digital ID sector warns of legal action if mDL limited to GOV.UK Wallet](https://www.biometricupdate.com/202602/uk-digital-id-sector-warns-of-legal-action-if-mdl-limited-to-gov-uk-wallet)

---

## Asia-Pacific

### Australia

**Status: Production deployments, ISO 18013-5 aligned, international interoperability work underway**

Digital driver licences are live in **New South Wales, Victoria, Queensland and South Australia**; the **Northern Territory** is launching before the end of 2026, **Western Australia** plans 2027, and Tasmania and the ACT are exploring. All jurisdictions agreed in June 2024 to align on ISO/IEC 18013 and 23220, and Austroads' [Digital Trust Service](https://austroads.gov.au/drivers-and-vehicles/digital-trust-service) is harmonising verification nationally.
- **Queensland**: First Australian mDL aligned with ISO 18013-5 (November 2023); more than [1.4 million Digital Licence app customers](https://statements.qld.gov.au/statements/105727) by July 2026. Cited as a potential global model for mDL deployment architecture.
- **Victoria**: statewide digital driver licence launched **May 2024**.

Australia is working with **Japan and South Korea** on mutual recognition and interoperability of Verifiable Digital Credentials (VDCs).

**Resources:**
- [Biometric Update — Queensland mDL could be model for global mDL deployment](https://www.biometricupdate.com/202502/queensland-mobile-drivers-license-could-be-model-for-global-mdl-deployment)
- [Biometric Update — More Australians can now use mDLs (April 2024)](https://www.biometricupdate.com/202404/more-australians-can-now-use-mdls)
- [Biometric Update — Northern Territory brings Australia closer to nationwide mDL rollout (Sep 2026)](https://www.biometricupdate.com/202609/northern-territory-brings-australia-closer-to-nationwide-mdl-rollout)
- [Austroads — Digital Trust Service](https://austroads.gov.au/drivers-and-vehicles/digital-trust-service)

### Japan

**Status: National ID on smartphones (Android since 2023, iPhone since 2025); driver's licence on the physical My Number Card since March 2025**

Japan's My Number Card electronic certificates have been available on [Android smartphones since May 2023](https://www.digital.go.jp/en/policies/mynumber/smartphone-certification) and on **iPhone since 24 June 2025**. Since [24 March 2025](https://www.digital.go.jp/en/policies/mynumber/drivers-license) holders can record their driving licence on the physical My Number Card's IC chip (the "Myna driver's licence"); the smartphone versions cannot yet be used as a driving licence. Japan is coordinating with South Korea and Australia on VDC interoperability: a Japan–Korea trust-framework proof of concept began in [July 2026](https://www.holdings.toppan.com/en/news/2026/07/newsrelease260709_1.html), targeting an interoperability method by 2027, and Japan and the EU [validated cross-border wallet interoperability](https://www.biometricupdate.com/202607/japan-eu-validate-cross-border-digital-wallet-interoperability) in July 2026.

**Resources:**
- [Digital Agency — Smartphone electronic certificates](https://www.digital.go.jp/en/policies/mynumber/smartphone-certification)
- [Digital Agency — My Number Card as driver's licence](https://www.digital.go.jp/en/policies/mynumber/drivers-license)
- [Mobile driver's license — Wikipedia](https://en.wikipedia.org/wiki/Mobile_driver%27s_license)

### South Korea

**Status: Active mDL expansion, interoperability cooperation**

South Korea has had an operational mDL since July 2022 (Samsung Wallet support since March 2024) and launched the Mobile Resident Registration Card nationwide on 14 March 2025. It is participating in trilateral interoperability discussions with Japan and Australia on standardized Verifiable Digital Credentials, aligning with ISO 18013-5 and W3C VC frameworks.

### India

**Status: World's largest government VC platform (DigiLocker) — driving licences legally accepted digitally**

India's [DigiLocker](https://www.digilocker.gov.in/) platform, launched 2015 under Digital India / MeitY, has scaled to:
- **~717 million registered users** (71.66 crore, MeitY, July 2026)
- **~9.4 billion documents issued** (936 crore)

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

Brazil's **"Identidade Digital Gov.br"** project unifies documents in a mobile app with QR codes and biometric verification. The **digital CNH (Carteira Nacional de Habilitação)** has been live since 2017 and is accepted as valid identification. Separately, in 2025 Brazil adopted a "DPI as a Packaged Solution" (DaaS) approach to issue W3C-style verifiable credentials for social programmes, starting with a rural-property credential piloted with about 2,000 farmers in Rio Grande do Sul; this does not yet cover the CNH.

Brazil and Uruguay operationalized the **first cross-border digital ID integration in Latin America** in production by October 2024 — 77 million Brazilians can use their Gov.br digital ID for services on Uruguayan government platforms. By end-2025, 39 services are covered.

**Resources:**
- [Biometric Update — Brazil adopts DaaS for verifiable credentials](https://www.biometricupdate.com/202507/brazil-adopts-daas-for-verifiable-credentials)
- [ID Tech Wire — Uruguay and Brazil plan digital ID broker for cross-border services](https://idtechwire.com/uruguay-and-brazil-plan-digital-id-broker-for-cross-border-services-by-late-2025/)
- [VisaHQ — Cross-border digital ID deal lets 77 million Brazilians access foreign services](https://www.visahq.com/news/2025-12-27/br/cross-border-digital-id-deal-with-uruguay-lets-77-million-brazilians-access-foreign-services/)

### Mercosur Region (Argentina, Paraguay, Uruguay)

**Status: Cross-border interoperability framework active**

The **Mercosur Digital Citizen** programme enables citizens of Argentina, Brazil, Paraguay, and Uruguay to use national digital IDs for government services across borders. At the June 2026 Asunción summit the four members finalised an [agreement on mutual recognition of electronic identification](https://www.biometricupdate.com/202607/mercosur-advances-cross-border-digital-id-for-south-america), now subject to national ratification; Bolivia and Chile are seeking to join.

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

**Status: Digital ID and mDL committed for launch in 2026, phased rollout**

South Africa's Department of Transport has announced a mobile driver's licence (mDL) as part of the **MyMzansi** functional ID component. The mDL will be one of multiple Verifiable Credentials accessible via a secure mobile wallet. In the February 2026 State of the Nation Address the president committed to launching the digital ID, including the digital driving licence, during 2026, and the Department of Home Affairs targets a first release before year-end with a phased rollout thereafter ([MyMzansi roadmap](https://www.mymzansi.gov.za/roadmap/initiative-1)).

**Resources:**
- [Biometric Update — South Africa builds mDL as part of MyMzansi](https://www.biometricupdate.com/202512/south-africa-builds-mdl-as-part-of-mymzansi-functional-id-component)
- [Biometric Update — South Africa digital ID and mDL to launch this year, president promises](https://www.biometricupdate.com/202602/south-africa-digital-id-and-mdl-to-launch-this-year-president-promises)
- [TechCentral — South Africa's digital ID gets a targeted launch date](https://techcentral.co.za/south-africas-digital-id-gets-a-launch-date/280460/)

---

## Summary Table

| Region | Jurisdiction | Status | Format | Notes |
|---|---|---|---|---|
| **NA** | USA (21 states + PR) | Production | ISO 18013-5 / mdoc | TSA-accepted; CA >3.5M applications; FinCEN CIP acceptance Sep 2026 |
| **NA** | Canada | No DDL in production | — | Alberta Wallet (health card) 2025; Quebec Bill 82 adopted Oct 2025 |
| **EU** | EU 27 member states | Mandated law (EUDI) | SD-JWT VC + mdoc | Dec 2026 deadline; DK/IT/FR live; mDL directive in force Nov 2025 |
| **EU** | UK | Wallet live; mDL pending | W3C VC (mDL via DVLA) | GOV.UK Wallet; DUA Act 2025; licence in private testing |
| **APAC** | Australia (NSW, VIC, QLD, SA; NT 2026) | Production | ISO 18013-5 / 23220 | QLD >1.4M users; Austroads Digital Trust Service |
| **APAC** | Japan | Production | My Number Card (Android 2023, iPhone 2025) | Licence on physical card chip since Mar 2025; not yet on phone |
| **APAC** | South Korea | Production | ISO 18013-5 | Trilateral interop (JP, AU) |
| **APAC** | India | Production (DigiLocker) | Signed docs → W3C VC direction | ~717M users; DL legally accepted |
| **LATAM** | Brazil | Production | Gov.br VC / DaaS | Digital CNH live; cross-border w/ UY |
| **LATAM** | Uruguay / Mercosur | Production / agreement | W3C VC | BR–UY live; mutual-recognition agreement Jun 2026 |
| **LATAM** | Dominican Republic | Pilot | W3C VC | Small business credentials |
| **MEA** | Oman | Production | National ID / DL digital | Legal parity granted 2025 |
| **MEA** | South Africa | Launch committed 2026 | mDL (MyMzansi) | Phased rollout from late 2026 |

---

## Unverified Claims

The following statements are retained from earlier drafts but could not be confirmed against a primary source in the September 2026 review: Queensland's early "~15% digital penetration"; the Brazil–Uruguay "39 services by end-2025" figure; the Latin American VC pilot participant list (Argentina, Brazil, Costa Rica, Dominican Republic, Paraguay, Uruguay); the UAE "~60% adult digital ID coverage" figure; and the exact credential format used for My Number Card on iPhone.

---

## Key Cross-Cutting Resources

- [W3C — Verifiable Credentials 2.0 press release](https://www.w3.org/press-releases/2025/verifiable-credentials-2-0/)
- [Everycred — 2025 State of Verifiable Credential Report](https://everycred.com/blog/2025-state-of-verifiable-credential-report/)
- [Trinsic — 2025 Landscape of Global Digital ID Adoption](https://trinsic.id/2025-landscape-of-global-digital-id-adoption/)
- [FIDO Alliance — Passkeys and Verifiable Digital Credentials (White Paper, 2025)](https://fidoalliance.org/passkeys-and-verifiable-digital-credentials-a-harmonized-path-to-secure-digital-identity/)
- [GS1 — VCs and DIDs Technical Landscape](https://ref.gs1.org/docs/2025/VCs-and-DIDs-tech-landscape)
- [Regula — Mobile Driver's License 2026 Global Status](https://regulaforensics.com/blog/mobile-drivers-license-verification/)
- [Corbado — ISO 18013-7 mDLs in Bank Onboarding and KYC (2026)](https://www.corbado.com/blog/iso-18013-7-mdl-bank-kyc-onboarding)
