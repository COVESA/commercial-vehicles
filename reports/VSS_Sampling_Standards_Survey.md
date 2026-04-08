# Data Sampling Conventions and Standards — Survey for VSS Extensions

**Purpose:** Identify existing standards and conventions for expressing how sensor/telemetry data should be collected, evaluated for fitness as the metadata vocabulary behind VSS signal overlay extensions (e.g., `transmission_mode`, `sampling_rate`, `quality_factor`, `privacy_classification`, `retention_policy`).

**Companion documents:**
- [COVESA VSS Gaps Feb 2025 Analysis](COVESA_VSS_Gaps_Feb2025_Analysis.md)
- [VSS Data Collection Conventions Proposal](VSS_DataCollection_Conventions_Proposal.md)

---

## Candidate Standards

### 1. W3C SOSA/SSN — Semantic Sensor Network Ontology

**What sampling metadata it can express:**
Most semantically rich vocabulary for describing observations and sampling. Models `sosa:Sensor`, `sosa:Observation`, `sosa:Sampler`, `sosa:SamplingProcedure`, `ssn:System`. Key properties: `sosa:phenomenonTime`, `sosa:resultTime`, `sosa:usedProcedure`, `ssn:hasSystemCapability`. **Does not define `hasFrequency` or `samplingPeriod` natively** — these must be expressed via a linked Procedure or extension (e.g., SAREF4ENVI). Aligned with ISO 19156:2023. 2023 edition published by joint W3C/OGC effort.

**Format:** RDF/OWL (Turtle, JSON-LD, N-Triples). Requires ontology tooling to author. Not directly expressible in plain YAML without a mapping layer.

**Adoption:** Smart cities, environmental monitoring, earth observation, scientific instrumentation. Growing in SDV/vehicle IoT research. Implemented by OGC SensorThings API (FROST-Server), Apache Jena, Eclipse RDF4J, pySSN.

**Open source:** [w3c/sdw-sosa-ssn](https://github.com/w3c/sdw-sosa-ssn), FROST-Server (Java), Apache Jena, owlready2 (Python).

---

### 2. OGC SensorML 3.0 — Sensor Model Language

**What sampling metadata it can express:**
Describes sensors as processes. Expresses output data rates, sampling constraints, measurement ranges, input/output signal types, and calibration procedures. Data quality via SWE Common `swe:quality` union type (uncertainty, accuracy, status flags). The `sml:Event` can describe timed sampling events. SensorML 3.0 (July 2025) adds JSON encoding via OGC API – Connected Systems.

**Format:** XML (legacy); JSON (v3.0). Not YAML-native but JSON is close. Medium-to-high complexity.

**Adoption:** Earth observation, environmental monitoring, oceanography (NOAA, NASA, ESA). Limited direct automotive/fleet use. Growing use in digital twin research.

**Open source:** 52°North SOS (Java), FROST-Server (Java), lib52n-xml-sensorML.

---

### 3. OGC SWE Common — Sensor Web Enablement Common Data Model

**What sampling metadata it can express:**
Foundational data type layer used by SensorML and OGC SensorThings API. Defines `swe:Quantity`, `swe:DataRecord`, `swe:DataArray`, `swe:DataStream` (with sampling time element). Critical: `swe:quality` union type — standardized quality flags including uncertainty, accuracy bounds, and status codes. Timeseries Profile (OGC 15-043r3) adds `DataQualityCode` as a standardized code list. SWE Common 3.0 (2024/2025) adds JSON encoding.

**Format:** XML (legacy); JSON (v3.0). Not self-sufficient — requires pairing with SensorML or SensorThings API.

**Adoption:** Core to OGC SWE ecosystem; wherever SensorML or SensorThings API is deployed. Environmental monitoring, smart grids.

**Open source:** 52°North SWE Common library (Java), OWS-Lib (Python), FROST-Server.

---

### 4. OMA LwM2M — Lightweight Machine to Machine / IPSO Smart Objects

**What sampling metadata it can express:**
The most directly deployable sampling vocabulary. **Notification Attributes** via CoAP Link Format:
- `pmin` — minimum period (seconds between notifications, even if value unchanged)
- `pmax` — maximum period (heartbeat — send even if value unchanged)
- `st` — step (minimum value change before notification — on-change threshold)
- `gt` / `lt` — greater-than / less-than threshold triggers
- `epmin` / `epmax` — min/max evaluation period (LwM2M 1.1+)
- `edge` — edge detection trigger (LwM2M 1.1+)
- `con` — confirmable notification flag

These directly encode PERIODIC (`pmax`), ON_CHANGE (`st`), and CONDITIONAL (`gt`/`lt`/`edge`) modes in a simple attribute syntax. IPSO Smart Objects (IDs 3300–3341+) define standardized sensor objects with min/max measured values.

**Format:** CoAP Link Format attribute strings (e.g., `<path>;pmin=10;pmax=60;st=0.5`). Extremely simple; analogous to YAML key-value pairs. Object definitions in XML with mature tooling.

**Adoption:** Very widely deployed — cellular IoT (NB-IoT, LTE-M), smart meters, industrial sensors. Sierra Wireless, u-blox, Nordic Semiconductor, STMicro all ship implementations. AWS IoT, Azure IoT Hub, Leshan support it.

**Open source:** Eclipse Leshan (Java — server+client), Anjay (C — embedded), Zephyr RTOS built-in LwM2M stack, Contiki-NG.

---

### 5. ETSI SAREF — Smart Applications REFerence Ontology

**What sampling metadata it can express:**
OWL ontology suite. Core `saref:` defines `saref:Measurement`, `saref:hasValue`, `saref:hasTimestamp`. **SAREF4ENVI** extension explicitly adds:
- `saref4envi:FrequencyMeasurement` — sampling frequency (Hz) as a typed Measurement
- `saref4envi:PeriodMeasurement` — sampling period as a typed Measurement
- `saref4envi:hasFrequencyMeasurement` / `saref4envi:hasPeriodMeasurement` — links device to frequency/period
**SAREF4AUTO** (ETSI TS 103 410-7) adds automotive classes including `saref4auto:Confidence`, position, speed, heading for platooning and automated parking use cases.

**Format:** OWL/RDF (Turtle, RDF/XML); JSON-LD serializable. Requires OWL tooling to author.

**Adoption:** European smart city, energy, building management. SAREF4AUTO is newer (2020) and not yet widely deployed in automotive production. Used in EU research projects; Google, Amazon, SmartThings use SAREF in smart home.

**Open source:** [saref.etsi.org](https://saref.etsi.org/) — Turtle/OWL files downloadable. Protégé for authoring. No dedicated automotive runtime library.

---

### 6. FIWARE NGSI-LD

**What sampling metadata it can express:**
ETSI-standardized (GS CIM 009) API and information model using JSON-LD. Metadata:
- `observedAt` — ISO 8601 timestamp of observation (mandatory for temporal queries)
- `unitCode` — UN/CEFACT unit code
- `datasetId` — multiple concurrent property values from different sensors
- Property-of-Property nesting for accuracy, quality, source
- Subscription API: `watchedAttributes` + `throttling` (minimum notification period — equivalent to `pmin`)

**Format:** JSON-LD (approachable JSON with `@context`). Simple for consumers; moderate for producers.

**Adoption:** Strong in smart cities (European cities, EU Digital Innovation Hubs), smart agriculture, Industry 4.0. Limited fleet telematics adoption outside EU research.

**Open source:** Orion-LD (C++), Stellio (Kotlin), Mintaka temporal query (Kotlin), NGSI-LD Python/JS clients.

---

### 7. Eclipse Vorto *(deprecated — do not use)*

Vorto provided a DSL (Vortolang) for IoT device descriptions. **No standardized sampling metadata** in core vocabulary. Bosch IoT Device Management discontinued mid-2024. Project archived on GitHub. Use cases absorbed by W3C WoT TD and Eclipse Ditto.

**Open source:** [eclipse-vorto/vorto](https://github.com/eclipse-vorto/vorto) — archived.

---

### 8. COVESA VSS Overlays — YAML extension mechanism

**What sampling metadata it can express:**
VSS uses `.vspec` YAML files defining a tree of nodes (`branch`, `sensor`, `actuator`, `attribute`) with core attributes (`type`, `datatype`, `unit`, `min`, `max`, `description`). The overlay mechanism allows adding custom attributes to existing nodes without modifying the upstream catalog.

Current informal practice:
- `interval_ms` — CAN bus sampling interval in milliseconds (used in Eclipse KUKSA/Leda CAN bridge mappings)
- Source-mapping attributes (`dbc.message`, `dbc.signal`) for CAN signal provenance

The COVESA **Fleet Management Data (FMD)** working group is actively defining data collection campaign metadata using VSS. Gaps: no standardized pmin/pmax, trigger mode, data quality, privacy classification, or retention.

**Format:** Simple YAML — most approachable format on this list.

**Adoption:** Dominant vehicle signal taxonomy. BMW, Mercedes-Benz, VW, Ford, Volvo, Bosch, Continental, NXP, Sonatus. Eclipse SDV (KUKSA, Leda) built on VSS.

**Open source:** [COVESA/vehicle_signal_specification](https://github.com/COVESA/vehicle_signal_specification), [COVESA/vss-tools](https://github.com/COVESA/vss-tools) (Python converters to JSON, CSV, Protobuf, DDS IDL, GraphQL), Eclipse KUKSA.val, Eclipse Leda.

---

### 9. OpenTelemetry (OTel)

**What sampling metadata it can express:**
Covers software observability (metrics, traces, logs). Metrics data model: `Gauge`, `Sum`, `Histogram`, cumulative vs. delta `Temporality`. Sampling-relevant: global SDK collection interval (not per-signal), tail-based sampling for traces, `Exemplar` filters for linking individual measurements to trace context. **No per-signal sampling rate, trigger mode, quality, or privacy metadata.**

**Format:** OTLP (gRPC + Protobuf, or HTTP + JSON). Simple SDK APIs.

**Adoption:** Dominant in cloud-native software observability. CNCF project. AWS, Google Cloud, Azure, Datadog, Grafana, Jaeger all support it.

**Open source:** SDKs in 11+ languages at [opentelemetry.io](https://opentelemetry.io/), OpenTelemetry Collector (Go).

---

### 10. InfluxDB Line Protocol / Flux

**What sampling metadata it can express:**
Time-series wire format and query language. Retention policies (v1) / bucket retention duration (v2/v3) express data lifetime. Tags can carry arbitrary metadata by convention. Telegraf collection agent configures per-plugin poll intervals. **No standardized per-signal sampling rate or trigger mode annotation** — all metadata is by convention.

**Format:** Line Protocol (plain text); Flux (functional scripting). Very simple wire format.

**Adoption:** Very widely adopted for IoT and embedded telemetry time-series storage. Industrial IoT, smart home, embedded automotive data logging.

**Open source:** [InfluxDB OSS](https://github.com/influxdata/influxdb), Telegraf (200+ plugins), influxdb-client-python/go/java/c++.

---

### 11. ISO 22837 / ISO 23150

**ISO 22837:2009 — Vehicle probe data for wide area communications:**
Reference architecture and data elements for probe vehicle systems. Mandatory: location + timestamp. Application-specific elements for traffic, weather, safety. Data collection frequency is implementation-specific — not defined as per-signal metadata.

**ISO 23150:2023 — Sensor-to-fusion-unit interface:**
Logical interface for in-vehicle environmental perception (radar, lidar, camera, ultrasonic) to data fusion unit. Sub-parts per sensor modality. Addresses real-time in-vehicle data structures with timestamps and confidence values. **Not a collection policy standard.**

**Adoption:** ISO 22837 referenced in ITS deployments. ISO 23150 actively implemented by Continental, Bosch, Valeo, Aptiv, Mobileye and adopted in AUTOSAR workflows.

**Open source:** None public. Behind ISO paywall.

---

### 12. AUTOSAR Adaptive Platform — ara::com / Service-Oriented Architecture

**What sampling metadata it can express:**
`cycleTime` in ARXML (AUTOSAR XML model) specifies periodic update period for service events. ara::com supports polling (`GetNewSamples()` with depth limit) and subscription models. DDS Network Binding (R22-11+) introduces DDS QoS policies into AP services including deadline, liveliness, history depth, and reliability. Minimum/maximum signal values, units, and CompuMethod conversions are part of the ARXML signal model.

**Format:** ARXML (XML). Commercial OEM tooling (Vector, EB/Continental, ETAS). Not open-source.

**Adoption:** All major OEMs (BMW, Mercedes, VW, Toyota, GM, Ford) and Tier-1s. AUTOSAR Classic in nearly every production ECU; Adaptive growing in domain controllers and ADAS.

**Open source:** None for Adaptive Platform. ERIKA Enterprise RTOS covers Classic only.

---

### 13. IETF CoAP + Observe (RFC 7641) + Conditional Attributes Draft

**What sampling metadata it can express:**
CoAP (RFC 7252) REST protocol for constrained IoT. Observe (RFC 7641) enables push notifications. **CoRE Conditional Attributes draft** (`draft-ietf-core-conditional-attributes`) defines:
- `c.pmin` — minimum period between notifications
- `c.pmax` — maximum period (heartbeat)
- `c.st` — step / minimum value change before notification
- `c.gt` / `c.lt` — greater-than / less-than threshold triggers
- `c.band` — band trigger (notify when value exits a range)

Sent as query parameters on CoAP Observe requests; registered in CoAP Link Format (RFC 6690). LwM2M inherits directly from this mechanism. Draft is IETF-approved but not yet RFC.

**Format:** CoAP Link Format attributes. Simple string parameters.

**Adoption:** Widely implemented in constrained IoT (6LoWPAN, NB-IoT, Thread). LwM2M implementations all support it.

**Open source:** libcoap (C), Californium (Java — Eclipse), CoAPthon3 (Python), Zephyr CoAP stack.

---

### 14. MQTT with Sparkplug B

**What sampling metadata it can express:**
Sparkplug B (Eclipse Foundation v3.0.0) defines MQTT topic namespace, session management (birth/death certificates), and Protobuf payload format. Per-metric: `timestamp` (mandatory, ms since epoch), `is_historical` (stored/forwarded data), `is_transient` (do not historize), `is_null` (invalid value). Quality: STALE state triggered by Death Certificate; GOOD state from live data. **No per-metric sampling rate, pmin/pmax, or trigger mode annotation.** Default mode is Report by Exception (RBE — send on change).

**Format:** Protobuf payload over MQTT. Approachable wire protocol.

**Adoption:** Strong in industrial automation and SCADA. Ignition (Inductive Automation), HiveMQ, EMQX, Canary Labs. Growing use in vehicle-to-cloud pipelines.

**Open source:** [Eclipse Tahu](https://github.com/eclipse/tahu), [Eclipse Sparkplug](https://github.com/eclipse-sparkplug/sparkplug), EMQX and HiveMQ broker support.

---

### 15. W3C Web of Things (WoT) Thing Description 1.1 / 2.0

**What sampling metadata it can express:**
Describes IoT devices through affordances: `PropertyAffordance` (with `observable` boolean), `ActionAffordance`, `EventAffordance`. `readOnly`/`writeOnly` as access control hints. JSON Schema for value type, format, min/max, unit. Protocol bindings in `forms` carry protocol-specific sampling control (e.g., CoAP Observe parameters). Security definitions: `nosec`, `basic`, `bearer`, `oauth2`, etc. — per-device access control mode. **No native sampling rate, pmin/pmax, trigger condition, quality flag, or retention policy** in core vocabulary. Context extensions (JSON-LD) can add these.

**Format:** JSON-LD. Compatible with SOSA/SSN and NGSI-LD context. Approachable.

**Adoption:** W3C Recommendation (v1.1). Siemens, Bosch, Panasonic, Mozilla WebThings, Eclipse Thingweb.

**Open source:** [Eclipse Thingweb / node-wot](https://github.com/eclipse-thingweb/node-wot) (TypeScript), wot-td (Rust), wot-py (Python).

---

### 16. OMG DDS — Data Distribution Service QoS Policies

**What sampling metadata it can express:**
Most complete standardized QoS vocabulary. Per-DataWriter/DataReader policies:
- **DEADLINE** (`period`) — maximum acceptable gap between data updates; notifies on violation
- **LIVELINESS** (`kind`, `lease_duration`) — detect publisher silence
- **TIME_BASED_FILTER** (`minimum_separation`) — subscriber-side rate-limiting: at most one sample per minimum_separation
- **HISTORY** (`kind`: KEEP_LAST/KEEP_ALL; `depth`) — middleware sample queue depth
- **DURABILITY** (`kind`: VOLATILE, TRANSIENT_LOCAL, TRANSIENT, PERSISTENT) — sample persistence for late joiners
- **RELIABILITY** (`kind`: BEST_EFFORT/RELIABLE)
- **LATENCY_BUDGET** — acceptable delivery latency
- **LIFESPAN** (`duration`) — sample TTL before discard (per-sample retention)
- **OWNERSHIP** + **OWNERSHIP_STRENGTH** — redundant sensor arbitration
- **PARTITION** — logical topic namespacing

**Format:** XML profiles or programmatic API (C++/Java/Python). Not YAML-native. Requires DDS expertise.

**Adoption:** Defense, aerospace, robotics (ROS 2), autonomous vehicles. AUTOSAR Adaptive Platform DDS binding. RTI Connext, Eclipse Cyclone DDS, eProsima Fast DDS, OpenDDS. NASA, US DoD, BMW, Nvidia DRIVE.

**Open source:** [Eclipse Cyclone DDS](https://github.com/eclipse-cyclonedds/cyclonedds) (C), [eProsima Fast DDS](https://github.com/eProsima/Fast-DDS) (C++), [OpenDDS](https://github.com/OpenDDS/OpenDDS) (C++).

---

### 17. IEEE 1451 — Smart Transducer Interface / TEDS

**What sampling metadata it can express:**
Transducer Electronic Data Sheet (TEDS) — a small memory on/near the transducer that stores:
- Physical measurement range (min, max)
- SI unit encoding
- **Update rate / sampling rate** (standardized TEDS field)
- Measurement uncertainty
- Calibration data (reference, correction)
- Warm-up time, response time
- Self-test capabilities
- Sensor type, model, serial number, manufacturer

IEEE 1451.0-2024 (June 2024, led by NIST) adds JSON encoding alongside legacy binary TEDS. Supports wired (1451.2) and wireless (1451.5, Wi-Fi, Bluetooth, ZigBee) interfaces.

**Format:** Binary TEDS (legacy); JSON (2024). Binary is complex; JSON is new and not yet widely implemented.

**Adoption:** Instrumentation and test/measurement: National Instruments, Brüel & Kjær, Dytran, PCB Piezotronics. Limited automotive production use (test benches and calibration rigs, not ECUs). NIST promotes for smart manufacturing.

**Open source:** IEEE 1451 Playground (UBI Portugal), NIST reference implementations (limited), pyIEEE1451 (Python, limited).

---

### 18. OASIS AMQP 1.0

**What sampling metadata it can express:**
Rich message structure. Sampling-relevant fields: `ttl` (header — message lifetime in ms), `absolute_expiry_time` (properties — when message expires), `creation_time` (when sampled), `application-properties` (map of string→scalar for arbitrary metadata by convention). **No standardized sampling rate, trigger mode, or quality vocabulary** — all in application-properties by convention.

**Format:** Binary wire protocol. Application-properties can be YAML-like key-value.

**Adoption:** Enterprise messaging and cloud IoT. Azure IoT Hub, Apache ActiveMQ Artemis, Apache Qpid, RabbitMQ (plugin), IBM MQ.

**Open source:** Apache Qpid, Apache ActiveMQ Artemis, AMQP.Net Lite, rhea (JS), python-qpid-proton.

---

### Bonus: OPC UA (IEC 62541)

Not on the original list but highly relevant to automotive:
- **MonitoredItem sampling interval** — per-item server-side check rate
- **Publishing interval** — subscription-level notification rate
- **Queue size** — buffered samples between publications
- **PubSub WriterGroup publishing interval** — data set writer publication rate
- **Time-based filter** — minimum notification period
- Companion Specifications allow domain-specific data models

Used in automotive manufacturing and increasingly in vehicle ECU/domain controller communication. OPC UA PubSub is used in some automotive cloud-ingestion pipelines.

**Open source:** open62541 (C), Eclipse Milo (Java).

---

## Comparative Summary Table

| Standard | Sampling Rate | Min / Max Period (pmin/pmax) | On-Change Trigger | Threshold Trigger | Data Quality | Privacy / Access Control | Retention / Lifespan | Complexity | Vehicle Relevance |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|---|
| **W3C SOSA/SSN** | Via extension | No | Yes (Observation) | No | Via ssn:hasSystemCapability | No | No | RDF/OWL — high | High (research) |
| **OGC SensorML 3.0** | Via sml:output | Via constraints | Partial | Via constraints | swe:quality (built-in) | No | No | XML/JSON — medium-high | Medium |
| **OGC SWE Common** | Via DataStream | Partial | Yes | Via quality | swe:quality (built-in) | No | No | XML/JSON — medium | Medium |
| **OMA LwM2M** | pmin/pmax (direct) | ✓ pmin / pmax | ✓ st | ✓ gt / lt | Stale/Good (indirect) | No | No | CoAP attr — **low** | **High** |
| **ETSI SAREF** | saref4envi:FrequencyMeasurement | saref4envi:PeriodMeasurement | No | No | No | No | No | OWL/RDF — high | Medium |
| **FIWARE NGSI-LD** | Via throttling | throttling param | Yes (subscription) | No | Property-of-property | No | No | JSON-LD — medium | Medium |
| **Eclipse Vorto** | No | No | No | No | No | No | No | Deprecated DSL | **None** |
| **VSS Overlays** | interval_ms (informal) | No | No | No | No | No | No | YAML — **lowest** | **Very High** |
| **OpenTelemetry** | Global SDK interval | No | No | No | Exemplar filters | No | No | OTLP/Protobuf | **Low** (SW only) |
| **InfluxDB / Flux** | Telegraf poll interval | No | No | No | Via tags (convention) | No | Retention policy | Line Protocol — low | Medium (storage) |
| **ISO 22837** | Not specified | No | No | No | No | No | No | ITS msgs — high | Medium |
| **ISO 23150** | Implicit output rate | No | No | No | Confidence values | No | No | ARXML — high | High (ADAS) |
| **AUTOSAR AP** | cycleTime (ARXML) | Partial | Yes (events) | No | No | No | No | ARXML — **high** | **Very High** |
| **CoAP + Cond. Attrs** | c.pmin / c.pmax | ✓ c.pmin / c.pmax | ✓ c.st | ✓ c.gt / c.lt | No | No | No | CoAP attr — low | High |
| **MQTT Sparkplug B** | No | No | RBE (by exception) | No | is_null, STALE flag | No | No | Protobuf — low | High |
| **W3C WoT TD** | Via protocol binding | No | observable (boolean) | No | No | Security defs | No | JSON-LD — medium | High |
| **DDS QoS** | TIME_BASED_FILTER | ✓ DEADLINE / LIFESPAN | DEADLINE violation | No | LIVELINESS | No | ✓ DURABILITY / LIFESPAN | XML/API — **high** | **Very High** |
| **IEEE 1451 TEDS** | update_rate (TEDS) | Yes | No | No | Calibration, uncertainty | No | No | Binary/JSON — high | Medium |
| **OASIS AMQP** | Via app-properties | ttl / expiry_time | No | No | No | No | ✓ ttl | Wire proto — medium | Medium |
| **OPC UA** | MonitoredItem interval | ✓ sampling + publishing | Yes (subscription) | Via data change filter | No | Security (built-in) | No | XML/binary — high | High |

---

## Coverage of Proposed VSS Extension Fields

| Proposed field (from Conventions doc) | Best standard source | Notes |
|---------------------------------------|---------------------|-------|
| `transmission_mode` | OMA LwM2M / CoAP Cond. Attrs | CHANGE = st-only; PERIODIC = pmax; HYBRID = pmin+pmax |
| `sampling_rate` | OMA LwM2M pmin/pmax, AUTOSAR cycleTime, IEEE 1451 update_rate | All express the concept differently |
| `sampling_condition` | CoAP Cond. Attrs c.gt/c.lt, VSS overlay informal | Signal-reference expression needs formalization |
| `co_sample_group` | DDS Partition / AUTOSAR SWC grouping | No single standard; DDS closest |
| `quality_factor_signal` | OGC SWE Common swe:quality, IEEE 1451 TEDS uncertainty | SWE Common most standardized |
| `signal_validity` | OMA LwM2M epmin/epmax, Ford signal_context | No direct standard; LwM2M closest |
| `signal_type` (cumulative/instantaneous) | OpenTelemetry Temporality (DELTA/CUMULATIVE), Sparkplug is_historical | OTel Temporality closest |
| `privacy_classification` | **Not covered by any standard** | Gap across all candidates |
| `access_control` | WoT TD Security Definitions (per-device), OPC UA Security | Only per-device, not per-signal |
| `retention_policy` | DDS LIFESPAN (sample TTL), InfluxDB bucket retention, AMQP ttl | All at message/bucket level, not signal definition level |

---

## Gap Areas Not Covered by Any Existing Standard

Three critical metadata dimensions are absent from every evaluated standard:

1. **Privacy classification at the signal level** — No standard defines per-signal PII sensitivity (personal / pseudonymous / sensitive). GDPR compliance requires this; standards leave it to implementation.

2. **Retention policy at the signal catalog level** — DDS LIFESPAN covers message-level TTL; InfluxDB covers bucket-level retention; AMQP `ttl` covers per-message expiry. None define per-signal-type retention policy in a specification catalog.

3. **Access control at the signal level** — WoT TD and OPC UA define per-device/per-service access control. No standard defines which role or party may receive a specific signal's values in a signal catalog annotation.

---

## Ranked Recommendations

### For simple YAML overlay (extend what VSS already does)

| Rank | Standard | Rationale |
|------|----------|-----------|
| 1 | **OMA LwM2M notification attributes** | pmin/pmax/st/gt/lt are the most directly usable vocabulary. Simple attribute strings map cleanly to YAML key-value pairs. `pmin` = minimum delivery period, `pmax` = heartbeat, `st` = change threshold. Could be adopted verbatim without requiring CoAP. |
| 2 | **IETF CoAP Conditional Attributes draft** | Extends LwM2M vocabulary with `c.band`. Same simple attribute syntax. Not yet RFC, but stable. Represents the vocabulary LwM2M is built on. |
| 3 | **VSS interval_ms + proposed extensions** | Already in use by Eclipse KUKSA/Leda. Formalizing and extending with pmax (heartbeat), change_threshold (st), trigger_mode, and signal_type would be the path of least resistance for the COVESA community. FMD WG already heading this direction. |
| 4 | **OpenTelemetry Temporality** | Borrow `DELTA` / `CUMULATIVE` distinction for `signal_type` field — widely understood by backend engineers who will consume the data. |
| 5 | **MQTT Sparkplug B** | Borrow `is_historical`, `is_transient`, `is_null` as quality flag vocabulary for collection agents. |

### For ontology / RDF expression (if linking to semantic web or VSSo)

| Rank | Standard | Rationale |
|------|----------|-----------|
| 1 | **W3C SOSA/SSN** | The canonical W3C/OGC standard for sensor observations. COVESA VSSo already uses SSN concepts. Should be the RDF base for any semantic VSS overlay. |
| 2 | **ETSI SAREF4ENVI** | Only standard with `FrequencyMeasurement` and `PeriodMeasurement` as typed OWL classes — directly fills the sampling rate gap in SOSA/SSN. |
| 3 | **OGC SWE Common** | Best standardized quality vocabulary (`swe:quality`). Should inform the `quality_factor_signal` extension. |
| 4 | **W3C WoT Thing Description** | JSON-LD and compatible with SOSA/SSN. Use context extensions to add LwM2M sampling attributes into WoT property affordances. Bridges the YAML/ontology gap. |
| 5 | **FIWARE NGSI-LD** | Good option if fleet data is consumed by a context broker. Subscription `throttling` = pmin; property-of-property nesting for quality. |

### For in-vehicle / automotive production (if annotations need to match in-vehicle middleware)

| Rank | Standard | Rationale |
|------|----------|-----------|
| 1 | **AUTOSAR Adaptive + DDS QoS** | Most complete vocabulary (DEADLINE, TIME_BASED_FILTER, LIFESPAN, DURABILITY, HISTORY). `cycleTime` in ARXML is directly a sampling period. Any VSS overlay intended to configure in-vehicle data brokers should borrow DDS QoS terminology. |
| 2 | **OPC UA** | Strong in domain controllers and manufacturing. MonitoredItem sampling interval + data change filter covers periodic + threshold triggering. Built-in security covers access control. |
| 3 | **ISO 23150** | If the signals originate from ADAS sensors, ISO 23150 confidence values should inform the quality_factor vocabulary. |

---

## Overall Top Recommendation

For the VSS data collection conventions use case — where the goal is simple, human-readable YAML annotations that prescribe collection behavior for a separate collection agent — the **recommended vocabulary synthesis** is:

> **LwM2M attribute names as the sampling vocabulary** (pmin, pmax, st, gt, lt) → expressed as YAML key-value pairs in a VSS overlay → supplemented by **OTel Temporality** for signal_type → **WoT TD** observable + security definitions as the bridge to semantic expression → **SOSA/SSN + SAREF4ENVI** as the RDF/OWL serialization when semantic interoperability is required.

Privacy, access control, and retention remain gaps in all evaluated standards and must be defined as new fields without a directly borrowable standard vocabulary — making them the highest-priority contribution opportunity.

---

## Sources

- [W3C SOSA/SSN 2023 Edition](https://w3c.github.io/sdw-sosa-ssn/ssn/)
- [OGC SensorML Encoding Standard](https://docs.ogc.org/is/23-000/23-000.html)
- [OGC SWE Common 3.0](https://docs.ogc.org/is/24-014/24-014.html)
- [OGC API Connected Systems (July 2025)](https://www.ogc.org/announcement/ogc-announces-publication-of-ogc-api-connected-systems-and-updates-to-supporting-standards/)
- [OMA LwM2M Registry](https://www.openmobilealliance.org/wp/OMNA/LwM2M/LwM2MRegistry.html)
- [Anjay LwM2M Docs — pmin/pmax](https://avsystem.github.io/Anjay-doc/LwM2M.html)
- [SAREF Portal](https://saref.etsi.org/)
- [SAREF4ENVI FrequencyMeasurement](https://saref.etsi.org/saref4envi/FrequencyMeasurement)
- [SAREF4AUTO v1.1.1](https://saref.etsi.org/saref4auto/v1.1.1/)
- [FIWARE NGSI-LD FAQ](https://fiware.github.io/data-models/specs/ngsi-ld_faq.html)
- [COVESA VSS GitHub](https://github.com/COVESA/vehicle_signal_specification)
- [Eclipse Leda — custom VSS mappings with interval_ms](https://eclipse-leda.github.io/leda/docs/app-deployment/kuksa-databroker/custom-vss-mappings/)
- [OpenTelemetry Metrics Data Model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/)
- [InfluxDB Line Protocol](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/)
- [ISO 23150:2023](https://www.iso.org/standard/83293.html)
- [ISO 22837:2009](https://www.iso.org/standard/45418.html)
- [AUTOSAR Adaptive Platform](https://www.autosar.org/standards/adaptive-platform)
- [RTI: Integrating DDS into AUTOSAR AP](https://www.rti.com/blog/integrating-dds-into-the-autosar-adaptive-platform)
- [RFC 7252 — CoAP](https://www.rfc-editor.org/rfc/rfc7252.html)
- [RFC 7641 — CoAP Observe](https://www.rfc-editor.org/rfc/rfc7641.html)
- [IETF CoRE Conditional Attributes Draft](https://datatracker.ietf.org/doc/html/draft-ietf-core-conditional-attributes-06)
- [Sparkplug 3.0 Specification](https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf)
- [W3C WoT Thing Description 1.1](https://www.w3.org/TR/wot-thing-description11/)
- [OMG DDS — Fast DDS QoS Policies](https://fast-dds.docs.eprosima.com/en/latest/fastdds/dds_layer/core/policy/standardQosPolicies.html)
- [ROS 2 QoS — Deadline, Liveliness, Lifespan](https://design.ros2.org/articles/qos_deadline_liveliness_lifespan.html)
- [IEEE 1451.0-2024 — NIST announcement](https://www.nist.gov/news-events/news/2024/07/ieee-14510-2024-standard-published-under-leadership-nist-researchers)
- [OASIS AMQP Core Messaging](https://docs.oasis-open.org/amqp/core/v1.0/amqp-core-messaging-v1.0.html)
- [OPC UA Sampling Interval](https://reference.opcfoundation.org/Core/Part4/v104/docs/5.12.1.2)
