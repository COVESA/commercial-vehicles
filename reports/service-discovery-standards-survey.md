# Service Discovery Across Standards Bodies: IETF, W3C, Automotive and AOSP

**COVESA Commercial and Fleet Vehicle Expert Group**
**Date:** November 2026
**Status:** Survey and analysis, for discussion
**Audience:** VISS, VSS and AOSP App Framework contributors; fleet and aftermarket integrators; anyone deciding how a client finds a vehicle data service

---

## 1. Summary

Every standards body surveyed has converged on one of two patterns for finding a service:

1. **Multicast "shout and listen" on a single link.** mDNS/DNS-SD, SOME/IP-SD, CoAP multicast, Zenoh scouting.
2. **A registry you query.** DNS-SD over unicast via registration and proxies, CoRE Resource Directory, W3C Web of Things Thing Description Directory, Eclipse uProtocol uDiscovery, and the VISS tree itself.

The IETF and W3C now treat the multicast step as untrusted "introduction" only and put all real metadata behind an authenticated "exploration" step. Automotive in-vehicle stacks mostly skip open discovery for applications and rely on static provisioning or on a data-model tree that doubles as the service registry. The one place where IETF-style mDNS/DNS-SD has landed normatively in automotive is diagnostics, in ISO 17978 SOVD. SAE has no service-discovery standard.

VISS has left the question of how a client finds the VISS server open since 2020. Section 6 proposes three ready-made options drawn from this survey.

## 2. IETF

### 2.1 DNS-SD and mDNS

[RFC 6762](https://www.rfc-editor.org/rfc/rfc6762.html) (mDNS) and [RFC 6763](https://www.rfc-editor.org/rfc/rfc6763.html) (DNS-SD) remain the universal LAN baseline: a client queries a PTR record for `_service._tcp.local`, then resolves SRV, TXT and A/AAAA records. Android (`NsdManager`), Apple (Bonjour), Linux (Avahi) and Windows all implement it.

The IETF DNSSD working group's current agenda is about escaping single-link multicast:

| Document | Role | Status |
|---|---|---|
| [RFC 8766](https://www.rfc-editor.org/rfc/rfc8766.html) Discovery Proxy | Answers unicast DNS-SD queries on behalf of mDNS devices on another link | Published 2020 |
| [RFC 9665](https://www.rfc-editor.org/rfc/rfc9665.html) Service Registration Protocol (SRP) | A device registers itself over unicast DNS Update, authenticated with SIG(0), with a lease | Published 2024 |
| [draft-ietf-dnssd-advertising-proxy](https://datatracker.ietf.org/doc/draft-ietf-dnssd-advertising-proxy/) | Republishes SRP registrations into mDNS so legacy clients still see them | -06, July 2026; WGLC targeted March 2027 |
| draft-ietf-dnssd-tsr | Resolves conflicting updates to the same name | WGLC targeted November 2026 |
| draft-ietf-dnssd-uld Unicast Local Discovery | Combines SRP registrar, Discovery Proxy and Advertising Proxy into one infrastructure service | WGLC targeted July 2027 |
| draft-ietf-dnssd-srp-replication | Replicates SRP state between registrars | WGLC targeted March 2028 |

Sources: [DNSSD charter and milestones](https://datatracker.ietf.org/wg/dnssd/about/).

The companion SNAC working group's [draft-ietf-snac-simple](https://datatracker.ietf.org/doc/draft-ietf-snac-simple/) (-13, October 2026, in IETF Last Call) connects IPv6 stub networks such as Thread to home infrastructure and names DNS-SD as the discovery mechanism.

**Deployment driver: Matter.** Thread devices do not run mDNS. They register with SRP at the Thread Border Router, which proxies them into mDNS as `_matter._tcp` (operational) and `_matterc._udp` (commissionable), with TXT keys carrying discriminator, vendor and product IDs. Source: [Matter discovery primer](https://developers.home.google.com/matter/primer/commissionable-and-operational-discovery).

### 2.2 CoRE for constrained devices

[RFC 6690](https://www.rfc-editor.org/rfc/rfc6690.html) defines `/.well-known/core` in CoRE Link Format. [RFC 9176](https://www.rfc-editor.org/rfc/rfc9176.html) Resource Directory (2022) exists because multicast is impractical for sleepy nodes and mesh networks. It recommends locating the directory by router advertisement option, anycast, or DNS-SD, and explicitly advises against multicast discovery in meshes. The Open Connectivity Foundation uses the same idea: a multicast CoAP GET to `/oic/res`.

### 2.3 Well-known URIs

[RFC 8615](https://www.rfc-editor.org/rfc/rfc8615.html) governs the `/.well-known/` registry. [RFC 9727](https://www.rfc-editor.org/info/rfc9727/) api-catalog (June 2025) adds `/.well-known/api-catalog` as a Linkset for API discovery. Uptake is early.

## 3. W3C

### 3.1 Web of Things Discovery

[W3C WoT Discovery](https://www.w3.org/TR/wot-discovery/) became a Recommendation on 5 December 2023. It is the clearest architectural statement in this survey and splits discovery into two phases:

**Introduction** yields only a URL and carries no security or privacy controls, so it must not leak metadata. Mechanisms:

- Direct: a typed URL, QR code, or Bluetooth beacon.
- Well-known URI: `/.well-known/wot`.
- DNS-SD: `_wot._tcp` and `_wot._udp` for Things, `_directory._sub._wot._tcp` for directories, with required TXT keys `td` (path), `type` (Thing or Directory) and `scheme`.
- CoRE Link Format or Resource Directory with resource types `wot.thing` and `wot.directory`.
- DID document with a service endpoint of type `WotThing` or `WotDirectory`.

**Exploration** returns a Thing Description only after authentication, either from the Thing itself or from a Thing Description Directory offering CRUD, SPARQL or JSONPath search and Server-Sent Events for change notification.

### 3.2 W3C Automotive Working Group

The Automotive WG discussed discovery directly on [26 May 2020](https://www.w3.org/2020/05/26-auto-minutes.html), prompted by Ulf Bjorkengren's [Gen2 dynamic registry proposal](http://www.w3.org/2019/11/W3C_Gen2_dynamic_registry.pdf). In that design, service managers register subtrees with the VISS core server; clients use the VISS service discovery request to learn about the new nodes; the root of a registered subtree may carry a `serverUri` property so a client can talk to that server directly. The group concluded that the VSS tree is the service registry for VISS, and that finding the server on the network was above VISS and out of scope. BMW noted mDNS was "coming up" internally, and UPnP and DLNA were considered and rejected as too media-focused.

The W3C Automotive WG closed in 2023 and VISS moved to COVESA.

## 4. Automotive bodies

### 4.1 AUTOSAR: SOME/IP-SD and DDS

[SOME/IP Service Discovery](https://www.autosar.org/fileadmin/standards/R17-03_R1.1.0/FO/AUTOSAR_PRS_SOMEIPServiceDiscoveryProtocol.pdf) is the in-vehicle incumbent: multicast OfferService and FindService entries, with initial-wait, repetition and main phases tuned for ECU wake-up ordering, and unicast replies in the main phase. [ara::com](https://www.autosar.org/fileadmin/standards/R25-11/AP/AUTOSAR_AP_EXP_ARAComAPI.pdf) abstracts it so the same FindService API runs over SOME/IP, DDS or intra-machine IPC, selected at deployment.

DDS uses its own broker-less participant and endpoint discovery (SPDP/SEDP). Most SDV reference designs run SOME/IP in body and powertrain domains and DDS in the compute cluster, bridged at a gateway. Security guidance is consistent: service discovery must not cross zone boundaries without gateway mediation and authentication.

### 4.2 ISO 13400 DoIP and ISO 17978 SOVD

DoIP has its own pre-IP-standards discovery: a vehicle announcement broadcast three times on UDP 13400 after address assignment, and vehicle identification requests by VIN or EID, each with a randomized 0 to 500 ms delay.

[ISO 17978-3:2026 SOVD](https://standards.iteh.ai/catalog/standards/iso/64dfd515-01f0-4086-bc2d-f666d907a3ee/iso-17978-3-2026), the service-oriented successor, is the notable convergence. Clause 5.11 specifies addressing the SOVD server via mDNS and discovering it via DNS-SD for the co-located use case. Eclipse OpenSOVD already announces `_sovd._tcp` with identification and access-URL TXT records ([PR #178](https://github.com/eclipse-opensovd/opensovd-core/pull/178)). This is the first automotive standard found that adopts the IETF LAN mechanism unchanged.

### 4.3 Eclipse uProtocol uDiscovery

[uDiscovery v3](https://github.com/eclipse-uprotocol/up-spec/tree/main/up-l3/udiscovery/v3), originated by GM, is a DNS-inspired three-tier registry: a local instance per device, a domain instance per vehicle, and a central instance in the cloud. Clients call `FindServices` and `GetServiceTopics`; lookups recurse up the tree. Registration is not self-advertisement: a trusted OTA installer populates the registry through a replication API. The specification deliberately does not use mDNS or zeroconf on the wire and maps SOME/IP-SD messages into uDiscovery at the gateway. An [Android Binder implementation](https://github.com/eclipse-uprotocol/up-android-discovery) exists.

### 4.4 Eclipse Zenoh

[Zenoh](https://zenoh.io/docs/getting-started/deployment/) uses UDP multicast scouting on 224.0.0.224:7446 with gossip fallback where multicast is unavailable. It is appearing in SDV middleware products alongside DDS.

### 4.5 COVESA VISS

[VISS v3.2 Transport](https://raw.githubusercontent.com/COVESA/vehicle-information-service-specification/main/spec/VISSv3.2_Transport.html) keeps the 2020 position:

> Implementations that support additional devices or multiple VISSv3 services should provide discovery. Alternatively, the location of a particular VISSv3 Server instance on the local vehicle network may be handled by configuration, either as part of a package manifest or by consulting a registry on application install.

Default ports are recommended per transport (HTTP 443, WebSocket 6443, MQTT 8883, gRPC 5443, access token servers 7443 and 8443). "Discovery" within VISS means the `discover` action, which returns signal metadata and, since v3.1, forest discovery of the trees a server manages. It does not cover finding the server.

JASPAR's [Yoriito](https://docs.yoriito.dev/tutorials/03_VSS_VISS/03_vss_viss/) (April 2026), a gRPC-only VISS v3 profile with split Consumer and Producer services, inherits the same gap.

### 4.6 SAE

No SAE service-discovery standard was found. J3016, J3061 and J3101 cover automation levels, cybersecurity process and hardware security. SAE technical papers on vehicle SOA defer to AUTOSAR, SOVD, SOAFEE and Eclipse SDV.

## 5. AOSP, the COVESA AOSP group, and BMW

### 5.1 AOSP's model is a local registry

Android does not discover vehicle services over the network. Binder `servicemanager` is the registry, and the VINTF manifest is the static, declared list of HAL instances. Car Service binds `android.hardware.automotive.vehicle.IVehicle/default`; applications reach it through `Car.createCar` and `CarPropertyManager`. Each property is gated by a permission, and vendor properties sit behind a signature-level permission. Google steers clients to `waitForDeclaredService` rather than polling `getService`. LAN discovery exists only as `NsdManager`, a plain DNS-SD/mDNS wrapper for applications.

Sources: [AIDL backends](https://source.android.com/docs/core/architecture/aidl/aidl-backends), [VHAL overview](https://source.android.com/docs/automotive/vhal), [NSD guide](https://developer.android.com/develop/connectivity/wifi/use-nsd).

### 5.2 COVESA AOSP App Framework Standardization

The group has no service-discovery workstream. Its data track proposes a VSS-based or OEM VHAL as a "harmonized publishing layer" for vehicle data; BMW's Jan Kubovy led the hands-on OEM VHAL workshop at the Porto AMM in April 2026. The [covesa-aosp-sdk](https://github.com/COVESA/covesa-aosp-sdk) uses an AIDL client/server model where the OEM implements the server side, with UnifiedPush notifications as the first standardized API. Discovery there is implicit: a known AIDL interface name resolved through `servicemanager`.

Sources: [COVESA AOSP Vehicle Data](https://covesa.atlassian.net/wiki/spaces/WIK4/pages/262766594/COVESA+AOSP+Vehicle+Data), [Porto VHAL workshop](https://covesa.global/aosp-handson-android-oem-vhal-workshop-at-covesa-amm/).

### 5.3 BMW VISS on Android

The W3C Automotive WG minutes of [25 October 2022](https://www.w3.org/2022/10/25-auto-minutes.html) record the AMM debrief in which BMW's VISS implementation was discussed: it had been used for test and research without the v2 security features, BMW had the go-ahead to open-source it, and it might go to production on Android Automotive and allow smartphones to pair. The [2 May 2023 minutes](https://www.w3.org/2023/05/02-auto-minutes.html) note interest in exposing VSS in Android Automotive alongside the VHAL.

The deck itself is Jan Kubovy's "VISS – Android API: Closing the Gap", presented at the COVESA AMM in April 2023 ([PDF](https://covesa.atlassian.net/wiki/rest/api/content/39065584/child/attachment/att39073853/download)). The architecture:

- A vendor VISS server fronts SOME/IP and CAN.
- A common VHAL implementation speaks HTTP, WebSocket or MQTT to that VISS server.
- Applications continue to use the Java Car API (`getProperty`, `setProperty`, `registerCallback`), so the OEM avoids writing its own VHAL and the standard moves closer to application development.

Open issues listed: the hierarchical VISS model versus the flat VHAL property model needs a deterministic mapping, and third parties need an SDK. Discovery is not addressed; the VHAL knows where the VISS server is by configuration. BMW OS 9 shipped on AOSP without Google Automotive Services from 2023 ([press release](https://www.press.bmwgroup.com/global/article/detail/T0401875EN/)). Volvo Cars' 2024 Gothenburg AMM demo of a gRPC-enabled VISS feeding the AAOS emulator follows the same shape.

## 6. Comparison

| Body / spec | Mechanism | Scope | Registry? | Security posture |
|---|---|---|---|---|
| IETF DNS-SD/mDNS | Multicast PTR/SRV/TXT | Single link | No | None; introduction only |
| IETF SRP + proxies | Unicast DNS Update, proxies | Multi-link, mesh | Yes (DNS zone) | SIG(0) on registration |
| IETF CoRE RD | REST registration and lookup | Constrained, mesh | Yes | ACE recommended |
| W3C WoT Discovery | Introduction (DNS-SD, well-known, DID) then Exploration | Any | Yes (TDD) | Metadata only after auth |
| AUTOSAR SOME/IP-SD | Multicast Offer/Find | In-vehicle Ethernet | No | Zone gateways |
| DDS | SPDP/SEDP multicast | In-vehicle compute | No | DDS Security |
| ISO 13400 DoIP | UDP broadcast announcement | Diagnostic link | No | Routing activation |
| ISO 17978 SOVD | mDNS + DNS-SD `_sovd._tcp` | Co-located diagnostics | No | OAuth on API |
| Eclipse uProtocol uDiscovery | Hierarchical registry, FindServices | Device, vehicle, cloud | Yes | Populated by trusted OTA |
| Eclipse Zenoh | Multicast scouting, gossip | Any | No | Transport security |
| COVESA VISS | Configuration or app-install registry; `discover` for metadata | In-vehicle or cloud | Tree is registry | Access tokens |
| AOSP | Binder `servicemanager` + VINTF manifest | On-device | Yes (static) | Per-property permissions |
| SAE | None found | | | |

## 7. Implications and options for COVESA

The gap VISS left in 2020 is still open. Three ready-made options now exist, and they are complementary rather than exclusive:

1. **A DNS-SD service type.** Register `_viss._tcp` with TXT keys for transport, VISS version and tree or forest identifier, mirroring SOVD clause 5.11 and WoT's `_wot._tcp`. This covers the vehicle LAN, Wi-Fi hotspot and smartphone-pairing cases with no new protocol.
2. **A well-known URI.** `/.well-known/viss` for cloud-hosted and off-boarded VISS servers, following RFC 8615 and the WoT precedent.
3. **A uDiscovery node.** Register the VISS server as a uEntity in uProtocol deployments so in-vehicle services find it through the same registry as everything else.

The WoT two-phase split is the model to copy. VISS already has the exploration half in its access-grant and access-token flow and in the `discover` action; it only lacks a standard introduction step.

For AOSP, a COVESA-defined AIDL interface name is the realistic discovery mechanism, since Binder plus VINTF is the only registry OEMs will accept. The BMW and Volvo designs both assume the VHAL is configured with the VISS server location; a standard name would let the COVESA SDK find a VISS-backed VHAL without OEM-specific wiring.

Aftermarket devices, such as a telematics gateway on vehicle Ethernet, are where SRP-style unicast registration matters most: the device needs to announce a service the vehicle did not leave the factory with, across zone gateways, with authentication. No automotive body has specified that yet, and it is squarely a commercial vehicle and fleet concern.

## 8. Sources

- IETF: [RFC 6762](https://www.rfc-editor.org/rfc/rfc6762.html), [RFC 6763](https://www.rfc-editor.org/rfc/rfc6763.html), [RFC 8766](https://www.rfc-editor.org/rfc/rfc8766.html), [RFC 9665](https://www.rfc-editor.org/rfc/rfc9665.html), [RFC 9176](https://www.rfc-editor.org/rfc/rfc9176.html), [RFC 8615](https://www.rfc-editor.org/rfc/rfc8615.html), [RFC 9727](https://www.rfc-editor.org/info/rfc9727/), [DNSSD WG](https://datatracker.ietf.org/wg/dnssd/about/), [draft-ietf-dnssd-advertising-proxy](https://datatracker.ietf.org/doc/draft-ietf-dnssd-advertising-proxy/), [draft-ietf-snac-simple](https://datatracker.ietf.org/doc/draft-ietf-snac-simple/)
- W3C: [WoT Discovery](https://www.w3.org/TR/wot-discovery/), [Automotive WG minutes 26 May 2020](https://www.w3.org/2020/05/26-auto-minutes.html), [25 Oct 2022](https://www.w3.org/2022/10/25-auto-minutes.html), [2 May 2023](https://www.w3.org/2023/05/02-auto-minutes.html), [Gen2 dynamic registry proposal](http://www.w3.org/2019/11/W3C_Gen2_dynamic_registry.pdf)
- Automotive: [SOME/IP-SD](https://www.autosar.org/fileadmin/standards/R17-03_R1.1.0/FO/AUTOSAR_PRS_SOMEIPServiceDiscoveryProtocol.pdf), [ara::com R25-11](https://www.autosar.org/fileadmin/standards/R25-11/AP/AUTOSAR_AP_EXP_ARAComAPI.pdf), [ISO 17978-3](https://standards.iteh.ai/catalog/standards/iso/64dfd515-01f0-4086-bc2d-f666d907a3ee/iso-17978-3-2026), [OpenSOVD mDNS](https://github.com/eclipse-opensovd/opensovd-core/pull/178), [uDiscovery v3](https://github.com/eclipse-uprotocol/up-spec/tree/main/up-l3/udiscovery/v3), [Zenoh deployment](https://zenoh.io/docs/getting-started/deployment/), [VISS v3.2 Transport](https://raw.githubusercontent.com/COVESA/vehicle-information-service-specification/main/spec/VISSv3.2_Transport.html), [Yoriito](https://docs.yoriito.dev/tutorials/03_VSS_VISS/03_vss_viss/)
- AOSP and COVESA: [AIDL backends](https://source.android.com/docs/core/architecture/aidl/aidl-backends), [VHAL](https://source.android.com/docs/automotive/vhal), [NSD](https://developer.android.com/develop/connectivity/wifi/use-nsd), [COVESA AOSP Vehicle Data](https://covesa.atlassian.net/wiki/spaces/WIK4/pages/262766594/COVESA+AOSP+Vehicle+Data), [covesa-aosp-sdk](https://github.com/COVESA/covesa-aosp-sdk), [BMW VISS – Android API deck, April 2023](https://covesa.atlassian.net/wiki/rest/api/content/39065584/child/attachment/att39073853/download), [BMW OS 9 press release](https://www.press.bmwgroup.com/global/article/detail/T0401875EN/)
