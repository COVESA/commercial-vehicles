# Streamlining Connected Vehicle Incident Reporting to Insurers
## Standards Landscape, Ecosystem, and the Verifiable Credentials Opportunity

*May 2026*

---

## Executive Summary

First Notice of Loss (FNOL), theft reporting, and incident data submission from connected vehicles to insurers remain largely manual, fragmented, and latency-prone despite mature telematics infrastructure. A compelling architectural opportunity exists at the intersection of three converging developments: (1) the W3C Verifiable Credentials (VC) v2.0 standard reaching full Recommendation status in May 2025; (2) the eIDAS 2.0 regulation mandating that European insurers accept digital credential wallets by 2026; and (3) COVESA's Vehicle Signal Specification (VSS) providing a normalized signal taxonomy capable of encoding incident data.

The core proposal — embedding a `claimsSubmissionEndpoint` URI inside an insurer-issued proof-of-insurance VC, and enabling the vehicle itself to submit a vehicle-signed incident report (potentially also a VC) to that endpoint — is architecturally sound and technically novel. No existing standard covers the full end-to-end flow from vehicle sensor event through VC-encoded FNOL submission. This represents both a standards gap and a leadership opportunity for the connected vehicle and insurance standards communities.

---

## 1. The Problem

Current FNOL and incident reporting processes suffer from several structural weaknesses:

- **Latency**: Human-reported FNOL averages days after incident; automated telematics FNOL (eFNOL) can narrow this to minutes but requires insurer-specific integrations.
- **Fragmentation**: No universal protocol governs how a vehicle communicates an incident to its insurer. Each telematics data provider builds proprietary pipelines.
- **Identity gaps**: At the scene of an incident, the identity of the insurer and the routing address for an electronic claim are not machine-readable or verifiable. A paper or app-displayed insurance card cannot be programmatically acted upon.
- **Carrier-to-carrier, not vehicle-to-carrier**: Existing blockchain-based sharing platforms (e.g., RiskStream RAPID X) address inter-carrier coordination *after* an insurer receives a claim — they do not address vehicle-originated submission.
- **Theft**: Vehicle theft reporting relies on manual owner notification. Connected vehicles that detect unauthorized movement, geofence breach, or ignition events could initiate standardized theft VCs, but no protocol exists for this.

---

## 2. Existing Standards and Technologies to Build On

### 2.1 FNOL / Claims Reporting Standards

**ACORD (Association for Cooperative Operations Research and Development)**

The de facto data standard for the insurance industry globally. ACORD's XML and JSON schemas cover over 1,200 transaction types, including:

- **ACORD 810**: First Notice of Loss Submission — the canonical claims message for electronic FNOL submission between brokers, carriers, and claims systems.
- **ACORD NGDS (Next-Generation Digital Standards) Object Model** (launched August 2025): Modernized object model for insurance data exchange, now explicitly supporting IoT devices as virtual parties in the information model.
- ACORD standards are published through an industry consortium and are the primary integration target for any claims API.

The key limitation: ACORD 810 is designed for broker/BMS-to-carrier transmission, not vehicle-to-insurer. Mapping VSS-encoded incident data to ACORD 810 payload formats is feasible but not yet standardized.

**RiskStream RAPID X** (The Institutes RiskStream Collaborative)

A production blockchain platform launched February 2026 for inter-carrier FNOL data sharing. RAPID X:

- Uses a permissioned blockchain to synchronize claim data between participating carriers.
- Reduces FNOL latency by approximately 7 days carrier-to-carrier.
- Generates estimated industry savings of $53M/year across claims processing.
- Is integrated with Guidewire (major carrier claims platform).
- Scope: carrier-to-carrier coordination, not vehicle-originated submission. However, RAPID X is the logical downstream recipient of vehicle-initiated FNOL.

**CSIO (Centre for Study of Insurance Operations)**

Canadian equivalent to ACORD, provides FNOL reusable service specifications aligned with ACORD messaging standards.

**eCall / AECS (UNECE Regulation 144)**

The EU-mandated Automatic Emergency Call System, mandatory in all new EU vehicles since April 2018:

- Automatically dials 112 (emergency services) and transmits GPS coordinates, airbag/sensor data, and impact information on serious accident.
- Governed by UNECE WP.29 (World Forum for Harmonization of Vehicle Regulations).
- Scope: emergency services only. Data protection and format are explicitly out of scope ("must be supplemented by national/regional legislation").
- Insurance notification is not in scope, but eCall triggering events (airbag deployment, severe g-force) are the same triggers that would initiate FNOL.

eCall establishes the *detection and transmission* model. The gap is that it routes exclusively to emergency services (PSAP — Public Safety Answering Points), not to insurers. A parallel or downstream channel to the insurer's `claimsSubmissionEndpoint` would complement, not compete with, eCall.

### 2.2 Vehicle Data and Signal Standards

**COVESA Vehicle Signal Specification (VSS)**

The open taxonomy for describing vehicle signals and data, spanning thousands of standardized signal paths (e.g., `Vehicle.Accident.AirbagDeployed`, `Vehicle.CurrentLocation`, `Vehicle.Speed`). VSS is the foundational data model for incident encoding and is the natural source schema for a standardized incident report VC.

**COVESA S2DM (Signal to Data Model)**

A GraphQL-based schema projection of VSS that enables typed, queryable access to vehicle data. An incident report VC could use S2DM-defined types as its credential subject schema, enabling interoperable querying by insurance claims systems.

**COVESA FMD (Fleet Management Data) / Commercial and Fleet Vehicle Expert Group**

The CV Expert Group is actively specifying data collection campaigns for fleet and insurance use cases, with the first versions targeted for 2025. This working group is the natural home within COVESA for a standardized incident-report data structure.

**COVESA Data Sampling and Collection Campaigns**

COVESA has started creating data campaigns addressing fleet management and insurance data needs — universal data collection campaigns covering use cases, data required, collection sampling rate, and methodology — targeting insurance verticals as a primary consumer.

**ISO TC22 / SAE**

Various ISO standards govern automotive data interfaces. ISO 18013-5 (mDL) and ISO 18013-7 (mDL over internet) are relevant infrastructure for vehicle-bound identity and credential storage. ISO 21434 governs vehicle cybersecurity, including the key management foundations required for a vehicle acting as a VC issuer.

### 2.3 Verifiable Credentials and Identity Standards

**W3C Verifiable Credentials Data Model v2.0** (W3C Recommendation, May 15, 2025)

The foundational standard for tamper-evident, machine-verifiable digital credentials. Key architectural properties relevant to FNOL:

- **`credentialSubject`**: Contains the insurance policy claims (policy number, coverage dates, VIN, insurer identity).
- **`credentialStatus`**: Points to a verifiable revocation/status endpoint — demonstrates the pattern for embedding actionable URIs in a VC.
- **`relatedResource`** (new in v2.0): Allows linking to associated documents or endpoints.
- **`termsOfUse`**: Can constrain how the credential may be presented or acted upon.

The VC data model does not define an application-layer property for a claims submission endpoint — this is an identified gap and an opportunity for extension work.

**W3C Decentralized Identifiers (DIDs) v1.0**

DIDs provide resolvable, cryptographically verifiable identifiers for issuers (insurers), holders (vehicles/drivers), and verifiers (repair shops, law enforcement, other parties). An insurer's DID Document can express service endpoints including a `claims` service type — this is already within scope of the DID spec's `service` property and provides one valid mechanism for endpoint discovery without modifying the VC body.

**OpenID for Verifiable Credentials Suite (OID4VC)**

- **OpenID4VCI** (Credential Issuance): Protocol for how an insurer issues a proof-of-insurance VC to a vehicle wallet or mobile app.
- **OpenID4VP** (Verifiable Presentations): Protocol for presenting a VC at incident time — e.g., presenting proof of insurance to another party at the scene, or submitting an incident report VC to the insurer's claims endpoint.

These are the transport-layer protocols that complement the W3C VC data model for online FNOL submission.

**ISO 18013-5 / 18013-7 (mDL)**

The mobile driver's license standard is now widely deployed. ISO 18013-7 (published October 2024) standardizes mDL use over the internet via a relying-party-to-holder secure connection. The mDL credential format (`mdoc`) is a distinct encoding from W3C VCs but is supported in the same digital wallet ecosystem (EUDIW, Google/Apple Wallet). Proof of insurance could be issued in either mdoc or VC format — alignment matters for the EU market.

**DIF (Decentralized Identity Foundation)**

- **Presentation Exchange**: Protocol for a verifier (insurer's claims endpoint) to declare what credential attributes it requires, and for the holder (vehicle/app) to construct a matching Verifiable Presentation.
- **WACI (Wallet and Credential Interactions)**: Extends DIDComm v2.0 for wallet-to-service interactions, which could underpin the incident submission flow.
- **Claims and Credentials Working Group**: Natural venue for proposing a profile covering insurance FNOL via VC presentation.

**Trust Over IP (ToIP) Foundation**

Provides the governance framework layer above the technical VC stack. Insurers are recognized as a named role (as "issuers") in ToIP governance frameworks. ToIP's Trust Registry Query Protocol (v2.0 Implementers Draft, 2024) enables verifying whether an issuer (e.g., an insurer issuing proof-of-insurance VCs) is authoritative. A ToIP governance framework for automotive insurance credentials would provide the policy layer that the W3C VC spec deliberately omits.

### 2.4 Regulatory Frameworks Creating Demand

**eIDAS 2.0 / European Digital Identity Wallet (EUDIW)**

Adopted February 2024, in force May 2024. Key implications:

- All EU member states must offer at least one EUDIW to citizens/residents by late 2026.
- **Regulated sectors including insurance are required to accept the EUDIW** for authentication and identity verification.
- Insurance cards are explicitly listed as credential types the EUDIW will support.
- This creates a regulatory mandate for interoperable, VC-compatible proof of insurance in Europe by 2026 — the market pull for standardization is immediate.

**EU Data Act (effective September 2025)**

Establishes user rights to access and share data generated by connected products, including vehicles. Fleet operators and individual owners gain enforceable data portability rights against OEMs. This directly supports the flow of vehicle-generated incident data to insurers at the owner's direction, removing a key barrier to vehicle-originated FNOL.

**EU ESPR / Digital Product Passport (DPP)**

Under the Ecodesign for Sustainable Products Regulation, vehicles will require machine-readable DPPs encoding lifecycle data. While primarily sustainability-focused, the DPP credential infrastructure (UNECE EU WEBUILD working group, W3C VC-based) is the same infrastructure that could carry insurance-relevant vehicle history data. Shared governance and schema work is an efficiency opportunity.

---

## 3. Trade Associations and Collaborative Bodies

| Organization | Relevance | Engagement Type |
|---|---|---|
| **ACORD** | De facto insurance data standard (FNOL 810 message) | Propose VSS-to-ACORD mapping; request IoT/vehicle-originated FNOL profile |
| **RiskStream Collaborative** (The Institutes) | Production FNOL blockchain network (RAPID X, Feb 2026) | Explore vehicle-originated FNOL as input layer to RAPID X |
| **COVESA CV Expert Group** | VSS data model, insurance data campaigns | Specify incident report data structure; host VC schema work |
| **W3C VC Working Group** | VC v2.0 standard | Propose `claimsSubmissionEndpoint` extension or W3C community group |
| **DIF Claims & Credentials WG** | Credential exchange protocols | Propose FNOL Presentation Exchange profile |
| **Trust Over IP Foundation** | Governance frameworks for VC ecosystems | Develop automotive insurance credential governance framework |
| **OpenWallet Foundation** | Wallet infrastructure (GDC organizing member) | Ensure wallet support for vehicle-bound insurance VCs |
| **UNECE WP.29 / GRSG** | eCall/AECS Regulation 144; vehicle regulations | Advocate for insurance notification as complement to emergency eCall |
| **ISO TC22 SC31** | Vehicle cybersecurity (ISO 21434); data standards | Align on vehicle key management for signing incident VCs |
| **ACEA / AIAM** | OEM interface standards; FMS standard | FMS extension to include incident report data structures |
| **Global Digital Collaboration (GDC)** | EC, ITU, UNECE, W3C, DIF, OpenWallet all present | Cross-sector venue to advance vehicle insurance VC standards |
| **PTOLEMUS Consulting** | eFNOL ecosystem mapping; insurance telematics advisory | Reference for market and product context |
| **LexisNexis Telematics Exchange** | Data aggregation between telematics providers and insurers | Potential recipient / routing layer for standardized incident VCs |

---

## 4. The Novel Architecture: Proof-of-Insurance VC with Embedded Claims Endpoint

The following architecture is proposed. It is not yet standardized — this is the primary innovation opportunity.

### 4.1 Proof-of-Insurance VC Structure

```json
{
  "@context": ["https://www.w3.org/ns/credentials/v2"],
  "type": ["VerifiableCredential", "MotorInsuranceCertificate"],
  "issuer": "did:web:insurer.example.com",
  "validFrom": "2026-01-01T00:00:00Z",
  "validUntil": "2027-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:vehicle:VIN_1234567890",
    "policyNumber": "POL-987654",
    "vin": "1HGCM82633A123456",
    "coverageTypes": ["liability", "collision", "comprehensive", "theft"],
    "insurer": {
      "id": "did:web:insurer.example.com",
      "name": "Example Insurance Co.",
      "claimsEndpoint": "https://claims.insurer.example.com/fnol/v1/submit",
      "theftReportEndpoint": "https://claims.insurer.example.com/theft/v1/report"
    }
  }
}
```

The `claimsEndpoint` and `theftReportEndpoint` URIs are the routing addresses embedded in the credential. When the vehicle or its operator encounters an incident:

1. The vehicle (or mobile app) reads the proof-of-insurance VC from the wallet.
2. It extracts the appropriate endpoint URI.
3. It constructs an incident report — potentially as a signed Verifiable Credential — using VSS/S2DM signal data.
4. It submits the incident report to the insurer's endpoint via OID4VP or a REST POST.

### 4.2 Incident Report as a Verifiable Credential

The incident report itself can be structured as a VC, signed by the vehicle using an HSM or TPM-backed key:

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://covesa.global/ns/incident/v1"
  ],
  "type": ["VerifiableCredential", "VehicleIncidentReport"],
  "issuer": "did:example:vehicle:VIN_1234567890",
  "issuanceDate": "2026-05-05T14:23:11Z",
  "credentialSubject": {
    "incidentType": "collision",
    "location": { "latitude": 43.7, "longitude": -79.4 },
    "speed": { "value": 47, "unit": "km/h" },
    "airbagDeployed": true,
    "impactSeverityG": 8.3,
    "ecallTriggered": true,
    "vehicleState": "post-collision-immobile",
    "telematics": {
      "provider": "did:web:telematics-provider.example.com",
      "deviceId": "DEVICE-SERIAL-12345"
    }
  }
}
```

The vehicle signs this VC using its Hardware Security Module (HSM) or TPM-backed key, providing cryptographic assurance of data integrity and vehicle identity — substantially stronger than a human-reported claim. The connected vehicle data collector (telematics provider) may co-sign or countersign the VC to attest to data provenance and collection methodology.

### 4.3 Theft Reporting Flow

For theft:

1. Vehicle detects unauthorized movement, geofence breach, or unrecognized ignition credential.
2. The vehicle or fleet data platform generates a signed `VehicleTheftAlert` VC containing timestamp, GPS trajectory, and anomaly signals.
3. The VC is submitted to the `theftReportEndpoint` from the proof-of-insurance VC.
4. The insurer receives machine-verified, tamper-evident theft notification — potentially with continuous location updates as additional VCs or a streaming Verifiable Presentation.

This flow is aligned with COVESA's existing S2DM `VehicleTheft` incident data model.

### 4.4 Endpoint Discovery via DID Document (Alternative)

Rather than embedding the endpoint in the VC body, the insurer's DID Document can express service endpoints:

```json
{
  "service": [
    {
      "id": "did:web:insurer.example.com#claims",
      "type": "InsuranceClaimsService",
      "serviceEndpoint": "https://claims.insurer.example.com/fnol/v1/submit"
    }
  ]
}
```

The `issuer` DID in the proof-of-insurance VC is resolved, and the claims endpoint is retrieved from the DID Document. This keeps the VC itself stable while allowing the insurer to update routing without reissuing credentials. Both approaches (embedded URI and DID Document service) can coexist, with the embedded URI serving as a cached default.

### 4.5 Role of the Telematics Data Collector

In this architecture, the telematics data collector (fleet management provider, OBD device provider, or OEM embedded telematics) plays several roles:

- **Data aggregator**: Collects and buffers VSS-encoded signals from the vehicle.
- **VC constructor**: Assembles the `VehicleIncidentReport` VC payload from raw signals.
- **Co-signer / attestor**: Optionally co-signs the VC to attest to device calibration, data integrity, and collection methodology — providing insurance-grade evidence for the data chain of custody.
- **Submission agent**: Submits the VC to the `claimsEndpoint` on behalf of the vehicle, particularly where the vehicle lacks direct internet connectivity.

The data collector does not hold or control the proof-of-insurance VC — that remains with the vehicle owner/operator wallet. The collector acts as a delegated submission agent, authorized by the credential holder.

---

## 5. Standards Gaps: Where New Work Is Needed

| Gap | Current State | What Is Needed |
|---|---|---|
| **`claimsSubmissionEndpoint` in insurance VCs** | No standard property exists in W3C VC v2.0 or ACORD | A VC extension schema or W3C community group specification |
| **Vehicle-as-issuer identity** | ISO 21434 covers vehicle cybersecurity; no VC issuer profile for a vehicle DID exists | COVESA or W3C automotive group: vehicle DID method specification |
| **Incident report VC schema** | COVESA VSS has signal taxonomy; S2DM has GraphQL model; no VC schema exists | COVESA CV Expert Group: define `VehicleIncidentReport` VC credential type |
| **Telematics provider co-signature profile** | No standard for data collector attestation on vehicle-signed VCs | COVESA + DIF: data provenance attestation profile |
| **eCall-to-insurance bridge** | eCall routes to PSAP (emergency) only; insurance notification out of scope of UNECE Reg 144 | Advocate at UNECE WP.29 for optional parallel insurance notification channel |
| **ACORD / VSS mapping** | ACORD 810 FNOL message exists; VSS signals exist; no mapping between them | COVESA + ACORD joint working item |
| **ToIP governance framework for automotive insurance** | ToIP has generic governance specs; no automotive insurance credential governance framework | ToIP + COVESA + insurance industry: automotive insurance credential governance framework |
| **Theft VC continuous update protocol** | No standard for multi-event credential streams (vehicle location updates post-theft) | DIF or W3C: streaming Verifiable Presentation profile |
| **Privacy / data minimization** | GDPR applies; incident data is sensitive personal data | Selective disclosure profile for incident VCs using SD-JWT or BBS+ signatures |

---

## 6. Recommended Engagement Strategy

### Immediate (Connected Vehicle Standards Community)

1. **Define a `VehicleIncidentReport` data campaign** using VSS/S2DM signals as the canonical incident data structure within COVESA. Scope to cover collision, theft, and unsafe driving events. Align with the existing S2DM incident data model.
2. **Draft a proof-of-insurance VC schema** with `claimsSubmissionEndpoint` and `theftReportEndpoint` properties, and circulate to insurance industry partners.
3. **Engage RiskStream RAPID X** on vehicle-originated FNOL as the upstream input to their inter-carrier platform. RAPID X is the natural downstream recipient once vehicle-to-insurer submission is standardized.

### Standards Bodies (6–18 months)

4. **W3C VC Working Group**: Propose a community group or extension specification for `InsuranceClaimsService` endpoint conventions in VCs and DID Documents.
5. **DIF Claims and Credentials WG**: Propose an automotive insurance Presentation Exchange profile defining the credential attributes required for FNOL submission.
6. **ACORD**: Engage the NGDS working group to define a mapping between VSS-encoded incident data and ACORD 810 FNOL message format, and to add an IoT/vehicle-originated FNOL transaction profile.
7. **ToIP Foundation**: Initiate an Automotive Insurance Credential Governance Framework, defining trust anchors, issuer policies, and verification procedures for insurer-issued proof-of-insurance VCs.

### Regulatory Alignment

8. **EUDIW / eIDAS 2.0**: Monitor the implementing acts for insurance credential requirements. Ensure the proof-of-insurance VC schema is submitted to EU Commission working groups defining EUDIW attestation formats.
9. **UNECE WP.29**: Propose that AECS/eCall architecture be extended to optionally include an insurance notification channel, coordinated with but separate from emergency PSAP notification.
10. **Global Digital Collaboration (GDC)**: Use COVESA's organizing member status to advance a cross-sector working paper on vehicle insurance credential infrastructure, engaging DIF, OpenWallet Foundation, W3C, and UNECE counterparts who are already present in GDC.

---

## 7. Summary of Key Organizations and Standards

| Standard / Organization | Layer | Relevance to FNOL VC |
|---|---|---|
| [W3C VC v2.0](https://www.w3.org/TR/vc-data-model-2.0/) | Data model | Foundation for proof-of-insurance and incident report VCs |
| [W3C DID v1.0](https://www.w3.org/TR/did-1.0/) | Identity | Vehicle DID; insurer DID with claims service endpoint |
| [OpenID4VCI](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) | Issuance protocol | Insurer issues proof-of-insurance VC to vehicle wallet |
| [OpenID4VP](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) | Presentation protocol | Vehicle submits incident report VC to insurer endpoint |
| [DIF Presentation Exchange](https://identity.foundation/presentation-exchange/) | Exchange protocol | Insurer declares required FNOL attributes; vehicle constructs response |
| [ISO 18013-7](https://www.iso.org/standard/82772.html) | mDL over internet | Complementary to W3C VC for EU mobile credential ecosystem |
| [ACORD 810](https://www.acord.org/standards-architecture/acord-data-standards) | Insurance data | Target format for vehicle-to-insurer FNOL payload |
| [RiskStream RAPID X](https://www.riskstream.org/rapidx) | Inter-carrier network | Downstream from vehicle-originated FNOL; distributes claims data between carriers |
| [UNECE Regulation 144 / eCall](https://unece.org/transport/press/new-un-regulation-automatic-emergency-call-system-road-traffic-accidents-will) | Emergency notification | Detection model; FNOL insurance channel would complement eCall |
| [COVESA VSS](https://covesa.global/vehicle-signal-specification/) | Vehicle data model | Canonical signal taxonomy for encoding incident data |
| [eIDAS 2.0 / EUDIW](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/) | Regulatory mandate | Forces insurer acceptance of VC-format insurance credentials in EU by 2026 |
| [Trust Over IP Foundation](https://trustoverip.org/) | Governance | Credential governance framework for automotive insurance VCs |
| [Global Digital Collaboration](https://globaldigitalcollaboration.org/) | Cross-sector forum | Venue to align vehicle, wallet, and credential standards communities |

---

## References

- [ACORD Data Standards](https://www.acord.org/standards-architecture/acord-data-standards)
- [ACORD 810 First Notice of Loss Factsheet](https://www.acord.org/docs/default-source/standards-la-factsheets/acord_la_claims810firstnotice_factsheet_v01.pdf)
- [ACORD NGDS Object Model Launch (August 2025)](https://www.acord.org/ACORD-about/acord-news/2025/08/28/acord-launches-new-asset-for-streamlining-digital-data-exchange-across-the-insurance-ecosystem)
- [RiskStream RAPID X](https://www.riskstream.org/rapidx)
- [RiskStream RAPID X Launch with Leading Auto Insurers](https://insurancenewsnet.com/oarticle/the-institutes-riskstream-collaborative-launches-rapid-x-with-leading-auto-insurers)
- [W3C Verifiable Credentials Data Model v2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [W3C VC v2.0 Press Release (May 2025)](https://www.w3.org/press-releases/2025/verifiable-credentials-2-0/)
- [W3C Verifiable Credentials Use Cases](https://www.w3.org/TR/vc-use-cases/)
- [W3C Decentralized Identifiers v1.0](https://www.w3.org/TR/did-1.0/)
- [OpenID for Verifiable Credential Issuance 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html)
- [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)
- [DIF Presentation Exchange](https://identity.foundation/presentation-exchange/)
- [DIF Claims and Credentials Working Group](https://identity.foundation/working-groups/claims-credentials.html)
- [DIF Wallet and Credential Interactions (WACI)](https://identity.foundation/waci-presentation-exchange/)
- [ISO 18013-5 mDL](https://www.iso.org/standard/69084.html)
- [ISO 18013-7 mDL over Internet](https://www.iso.org/standard/82772.html)
- [UNECE Regulation 144 / eCall](https://unece.org/transport/press/new-un-regulation-automatic-emergency-call-system-road-traffic-accidents-will)
- [UNECE WP.29 Overview](https://unece.org/transport/vehicle-regulations/wp29-presentation)
- [eIDAS 2.0 / EUDIW Overview](https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/)
- [EUDI Wallet Guide](https://www.eudi-wallet.eu/)
- [Trust Over IP Foundation](https://trustoverip.org/)
- [ToIP Trust Registry Query Protocol v2.0](https://www.trustoverip.org/blog/2024/04/03/toip-announces-the-implementers-draft-of-thetrust-registry-protocol-specification-v2-0/)
- [COVESA Vehicle Signal Specification](https://covesa.global/vehicle-signal-specification/)
- [COVESA Commercial and Fleet Vehicle Expert Group](https://covesa.global/blog-the-commercial-and-fleet-vehicle-expert-group/)
- [eFNOL Overview — PTOLEMUS](https://www.ptolemus.com/what-is-efnol/)
- [Tomorrow's FNOL Has Arrived — Insurance Thought Leadership](https://www.insurancethoughtleadership.com/blockchain/tomorrows-fnol-has-arrived-early)
- [Global Digital Collaboration](https://globaldigitalcollaboration.org/)
