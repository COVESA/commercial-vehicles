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
- **DeadbandValue** (DataChangeFilter) — per-MonitoredItem absolute or percentage deadband; step-from-last-value threshold
- Companion Specifications allow domain-specific data models

Used in automotive manufacturing and increasingly in vehicle ECU/domain controller communication. OPC UA PubSub is used in some automotive cloud-ingestion pipelines.

**Open source:** open62541 (C), Eclipse Milo (Java).

---

## Extended Survey — Standards Not in Original Assessment

### 20. BACnet / ASHRAE 135 — COV Subscriptions with `COVIncrement`

**What sampling metadata it can express:**
Change of Value (COV) subscriptions allow a client to receive a push notification when `Present_Value` changes by more than `COVIncrement` (type REAL, in engineering units). `COVIncrement` is set per analog object instance and can be overridden per subscription via the `SubscribeCOVProperty` service. `covLifetime` sets subscription duration. For analog output objects the same mechanism applies via `COVIncrement` on the object. COV reporting is a core service in BACnet, broadly implemented across building controllers worldwide.

**Format:** BACnet/IP or BACnet MS/TP wire protocol. Object model expressed in ASHRAE 135 specification text; not YAML-native. COVIncrement is a single REAL property value.

**Adoption:** Dominant in building automation and HVAC — all major BMS vendors (Siemens Desigo, Honeywell, Johnson Controls, Schneider EcoStruxure). Mature and stable since 1995.

**Open source:** bacpypes (Python), BACnet4J (Java), bacnet-stack (C).

**Curve logging relevance:** COVIncrement is the most mature industry deployment of per-signal configurable deadband in engineering units — structurally the closest analog to `curve_epsilon` of any standard found. Limitation: step-from-last-reported-value reference model, not interpolation-path deviation. BACnet has no minimum-interval (pmin) concept in COV. Adding a path-deviation mode alongside COV step mode would be the BACnet extension path for curve logging.

---

### 21. IEC 61850 — `deadbandMag` on Measurement Data Attributes

**What sampling metadata it can express:**
Common Data Classes (CDC) for measured values (MX functional constraint) carry a `db` (deadband) configuration attribute whose value `deadbandMag` defines the minimum change before a new buffered or unbuffered report is generated. Each data attribute within an IED can carry its own deadband. Report Control Blocks (RCB) carry `intgPd` (integrity period) — a mandatory periodic report regardless of deadband state — making IEC 61850 the only standard in this survey with both a per-signal threshold and a heartbeat as a standard paired configuration. `optFlds` can include reason-for-inclusion distinguishing deadband-filtered from integrity-period reports.

**Format:** IEC 61850 MMS (Manufacturing Message Specification) or GOOSE/Sampled Values at the protocol level. SCL (Substation Configuration Language, an XML format) for configuration. Not YAML.

**Adoption:** Power utility sector universally — transmission and distribution substations, grid protection systems, IEC 61850 Edition 2 is mandatory in many national grid standards. Also adopted in wind turbine control (IEC 61400-25) and railway signalling.

**Open source:** libIEC61850 (C), OpenIEC61850 (Java/C++), MZAutomation library.

**Curve logging relevance:** `deadbandMag` + `intgPd` is the most structurally complete existing standard match for the curve logging parameter pair (`curve_epsilon` + `curve_max_interval_ms`). The only algorithmic difference: `deadbandMag` uses step-from-last-reported-value; curve logging uses deviation from interpolated path. Proposing a `curveDev` trigger mode alongside `dchg`/`dupd` in a future IEC 61850 edition would be the standards path.

---

### 22. DNP3 / IEEE 1815 — Analog Input Deadband per Point

**What sampling metadata it can express:**
DNP3 (Distributed Network Protocol 3) supports per-point analog input deadband via Object Group 34 (`Analog Input Deadband`). A deadband value is configured per-point; the outstation generates a Class 1 event when the current value differs from the last-reported value by more than the deadband. Deadband = 0 reports every change. Integrity polls (master-initiated) send all current values regardless of change — a coarse pmax. Runtime configuration of deadband values is supported via `Direct Operate` or `Select-Before-Operate`.

**Format:** DNP3 binary application protocol over serial or TCP/IP. Configuration typically in vendor-specific files. Not YAML.

**Adoption:** Dominant in North American electric utility SCADA, water treatment, and oil and gas telemetry. IEEE 1815-2012 is the formal standardization. Very widely deployed (hundreds of thousands of RTUs and IEDs).

**Open source:** OpenDNP3 (C++/Java), dnp3 (Rust — Step Function Biosystems).

**Curve logging relevance:** Per-point deadband (Object 34) demonstrates that per-signal tolerance configuration is routine in regulated infrastructure. Step-from-last-value only; integrity poll is master-driven and not per-point. A per-point curve deviation mode could be specified as a new Object Group alongside Object 34.

---

### 23. IEC 60870-5 — Telecontrol Protocol with Parameter Loading

**What sampling metadata it can express:**
IEC 60870-5-101/104 (telecontrol companion standard for serial and TCP/IP) supports measurement parameter loading via `P_ME_NA_1` (parameter of measured values). Each analog measurement point can receive three parameter types: normalized value threshold (deadband), smoothing factor, and transmission period. A station configured with both a deadband and a transmission period will transmit when the value changes beyond the threshold OR when the transmission period expires — making IEC 60870-5 the oldest standard to explicitly standardize the ε + pmax combination as paired per-point configuration.

**Format:** IEC 60870-5 binary protocol. Parameter loading via `C_IC` (interrogation) and `P_ME` message sequences. Not YAML.

**Adoption:** Legacy global power utility telemetry. Still widely deployed in distribution automation, especially outside North America (where DNP3 dominates). Being superseded by IEC 61850 for new installations.

**Open source:** lib60870 (C/Java — libIEC61850 project), OpenMRTS.

**Curve logging relevance:** Earliest standardized expression of the ε + pmax paired configuration. The per-point `transmission period` is a per-signal pmax, which IEC 60870-5 more fully specifies than IEC 61850 (where `intgPd` lives at the RCB level). Step-from-last-value only.

---

### 24. ISO 19141 / OGC Moving Features — Trajectory Compression

**What sampling metadata it can express:**
ISO 19141:2008 (Schema for Moving Features) defines a geometry/trajectory schema — foliation, prism, leaf (instantaneous position/state), and motion curve representations. OGC Moving Features JSON encoding (OGC 19-045r3, 2021) and the OGC Moving Features Access API define representations for moving object trajectories with temporal geometry. The standard is schema-focused (what a trajectory is), not algorithm-prescriptive (how to compress it).

**Critical finding — associated research uses interpolation-path deviation:**
Academic work directly associated with OGC Moving Features uses **Synchronized Euclidean Distance (SED)** — the deviation of a sample from the *linearly interpolated position between two kept points* — as the compression metric. This is algorithmically identical to Geotab's curve logging (which uses vertical deviation, a 1D simplification of SED). Papers: LiMITS (Linear Interpolation Method for Trajectory Simplification), STTrace, DPTS, direction-based error minimization. These are referenced in OGC trajectory working group discussions.

**Format:** JSON (OGC 19-045r3), XML, CSV encodings. Schema-level standard.

**Adoption:** GIS platforms (QGIS, GeoServer, ArcGIS), OGC API implementations, smart transportation research. ISO 19141 revision underway.

**Open source:** pygeoapi (Python), OGC Moving Features API reference implementations, Trajectools (QGIS plugin).

**Curve logging relevance:** The only standards-adjacent body of work using interpolation-path deviation (SED) as the compression criterion — the same model as curve logging. SED for geospatial trajectories is directly analogous to vertical-deviation RDP for 1D vehicle signals. A VSS curve logging proposal could formally cite the OGC Moving Features SED vocabulary as precedent. This is research/informative, not normative, but it validates the model in a standards community context.

---

### 25. oneM2M TS-0001 — IoT Service Layer Subscriptions

**What sampling metadata it can express:**
oneM2M `<subscription>` resource carries: `notificationEventType` (resource update, deletion, creation), `periodicNotificationDuration` (periodic push regardless of change — pmax analog), `minimumObservableInterval` (minimum interval between notifications — pmin analog). `<semanticDescriptor>` resources allow SPARQL-based semantic annotation. No analog value deviation threshold.

**Format:** JSON or XML REST API. Moderate complexity.

**Adoption:** Strong in IoT platform market — ETSI, TSDSI (India), ARIB/TTC (Japan), ATIS (North America). HiveMQ, Eclipse om2m, OpenMTC platform implementations. Less traction in automotive than LwM2M.

**Open source:** Eclipse om2m (Java), OpenMTC (Python).

**Curve logging relevance:** `periodicNotificationDuration` (pmax) and `minimumObservableInterval` (pmin) cover the temporal parameters of curve logging. No value-deviation concept. Cannot express curve epsilon without extension.

---

### 26. DLMS/COSEM — IEC 62056 Smart Meter Data Push

**What sampling metadata it can express:**
DLMS/COSEM (Device Language Message Specification / Companion Specification for Energy Metering) defines data push via `Push Setup` (IC 40) objects. Periodic data capture via `Profile Generic` objects with configurable capture periods. Threshold-based push is available for alarm/event conditions via `Register Monitor` objects, but these are Boolean/alarm thresholds, not analog deadbands. For LPWAN deployments, SCHC (Static Context Header Compression, RFC 8724) compresses protocol headers — this is not value compression.

**Format:** DLMS/COSEM binary protocol or XML/JSON wrappers. Complex specification set.

**Adoption:** Global smart metering — dominant in European AMI (Landis+Gyr, Itron, Sagemcom, Kamstrup). IEC standard for electricity metering globally.

**Open source:** gurux.dlms (Python/Java/C#), jdlms (Java).

**Curve logging relevance:** No analog deadband or curve epsilon concept. Periodic capture period is fixed-rate only. Not applicable.

---

### 27. ISOBUS / ISO 11783 — Agricultural Vehicle Data

**What sampling metadata it can express:**
ISO 11783-10 (Task Controller) defines structured logging of machine state during field operations. ISO 11783-11 (Mobile Data Element Dictionary) standardizes 2,000+ data elements with units and scaling. Logging cadence is configured in task files (XML-based). Data elements have defined ranges and units but no per-element adaptive threshold in the normative standard. File-level compression (DEFLATE/LZ77) has been applied in research (28–63% reduction) but is outside the standard's normative scope.

**Format:** ISO 11783 XML task data, CAN bus messages (J1939-based). Not YAML.

**Adoption:** Agricultural machinery — John Deere, AGCO, CNH, Claas, Fendt, Trimble, Raven. Widely deployed in precision agriculture.

**Open source:** IsoBus-Inspector tools, ISODesigner (limited). Mostly vendor tooling.

**Curve logging relevance:** No per-element adaptive threshold. The ISO 11783-11 data element dictionary is a precedent for a domain-specific signal catalog carrying per-signal metadata — relevant as a structural analogy for the VSS signal catalog proposal. Not applicable to curve logging parameterization.

---

### 28. Asset Administration Shell (AAS) / IEC 63278

**What sampling metadata it can express:**
AAS defines a digital twin container (Submodel, SubmodelElementCollection, Property, Operation, Event). `Qualifier` elements can annotate any SubmodelElement with arbitrary semantic metadata. `EventElement` supports change notification. IDTA publishes standardized Submodel Templates (SMTs) for specific domains (Nameplate, Predictive Maintenance, Time Series Data). SMT `Time Series Data` (IDTA 02008) defines a structure for storing time-series observations including a `SamplingInterval` property. No deadband, epsilon, or trigger mode in the core metamodel.

**Format:** JSON/XML (AAS serialization), AASX package. REST API (AAS Part 2). Moderate complexity.

**Adoption:** German manufacturing industry (VDW, VDMA), European Industry 4.0 ecosystem. Catena-X supply chain. Growing in automotive supply chain (IDTA working groups).

**Open source:** Eclipse BaSyx (Java/C#/Python), PyAAS (Python), AAS Web UI.

**Curve logging relevance:** AAS Qualifier elements could carry `curve_epsilon`, `curve_algorithm`, etc. as typed annotations on a SubmodelElement — a viable carrier for curve logging metadata. The `Time Series Data` SMT could be extended with a sampling algorithm submodel. Not a vocabulary source, but a viable container for a future standardized curve logging Submodel Template.

---

### 29. Prometheus / OpenMetrics

**What sampling metadata it can express:**
Prometheus scrapes metrics at a global `scrape_interval` (default 1 minute, configurable per scrape config). `staleness markers` (special NaN) signal metric series disappearance. Recording rules pre-compute and store aggregated series. `track_timestamps_staleness` tracks when staleness markers arrive. OpenMetrics 1.0 specifies metric exposition format with TYPE, HELP, UNIT, and TIMESTAMP annotations per sample. No per-metric sampling rate, trigger mode, or analog threshold.

**Format:** Text exposition format (OpenMetrics) over HTTP; OTLP for push. Very simple.

**Adoption:** Dominant in cloud-native software observability. CNCF graduated project. Near-universal in Kubernetes ecosystems.

**Open source:** [prometheus/prometheus](https://github.com/prometheus/prometheus), OpenMetrics Go/Python clients, Grafana Alloy, VictoriaMetrics, Thanos.

**Curve logging relevance:** Staleness is a binary lifecycle marker, not an analog deviation concept. Pull-based scrape model means threshold-based filtering is not the primary design concern. Not applicable to curve logging. Downsampling in Prometheus-compatible TSDBs (Thanos, Cortex) uses aggregates (max/min/avg), which destroy signal shape — the opposite of curve logging's shape preservation.

---

### 30. Apache IoTDB — Time-Series Database Encoding

**What sampling metadata it can express:**
Per-timeseries encoding configuration: RLE (run-length encoding), GORILLA (XOR-based float compression from Facebook/Meta Beringei — very efficient for slowly changing signals), 2DIFF (second-order differential — efficient for linearly trending signals), PLAIN, CHIMP, SPRINTZ. Chunk-level compression: Snappy, LZ4, GZIP applied on top of encoding. Storage engine (TsFile) is columnar with page-level chunk management. An in-development `IoTDB-SQL` function `compress` is proposed but not normative.

**Format:** TsFile (binary columnar), IoTDB SQL, REST API. Open source (Apache).

**Adoption:** Growing in Industrial IoT and IIoT — Alibaba, THU research groups, and a growing ecosystem. Not yet widely deployed in automotive.

**Open source:** [apache/iotdb](https://github.com/apache/iotdb) (Java/C++).

**Curve logging relevance:** Storage-layer encoding algorithms are complementary to curve logging, not alternatives. Gorilla and 2DIFF reduce bits per stored point; curve logging reduces the number of points. A pipeline using both would compound savings. IoTDB does not define a collection-agent curve-logging policy; it optimizes storage of whatever points are given to it.

---

### 31. OPC UA Historical Access (HDA)

**What sampling metadata it can express:**
OPC UA Historical Access (Part 11) defines read operations over historical data: `ReadRaw` (actual recorded values), `ReadProcessed` (aggregate functions applied over intervals), `ReadAtTime` (value at specific timestamp, interpolated if not recorded), `ReadModified` (modification log). `ReadProcessed` aggregates include: `Interpolated` (linear interpolation between adjacent recorded values), `Average`, `Maximum`, `Minimum`, `Count`, `StartBound`, `EndBound`. `ExtrapolationMode` extends the last known value beyond recorded data.

**Format:** OPC UA binary or JSON protocol. Part of the full OPC UA stack.

**Adoption:** Process industry historians (OSIsoft PI, Aveva Historian, Kepware), manufacturing MES, SCADA. Widely deployed.

**Open source:** open62541 (C), Eclipse Milo (Java), opcua-asyncio (Python).

**Curve logging relevance:** The `Interpolated` aggregate in HDA's read path demonstrates that linear interpolation between kept points is an accepted industrial reconstruction technique. This is precisely the reconstruction model that curve logging assumes: the consumer uses linear interpolation between kept points to recover the signal between them. HDA validates the reconstruction side; curve logging is the compression-side dual. HDA does not drive the collection decision — it reconstructs at query time. However, it provides standards language for specifying that a signal "can be reconstructed by linear interpolation between kept points within tolerance ε" — exactly what `curve_epsilon` means.

---

### 32. ANSI/ISA-18.2 — Management of Alarm Systems

**What sampling metadata it can express:**
ISA-18.2 (Management of Alarm Systems for the Process Industries) defines deadband (also called dead zone or hysteresis) for alarm setpoints: a process variable must cross back through the deadband before an alarm can re-activate. Deadband is per-alarm configurable in engineering units. Purpose: suppress alarm chattering near the setpoint — the same noise-suppression motivation as `curve_min_interval_ms`. Also defines alarm priority (4 levels), shelving, suppression, and alarm rationalization.

**Format:** Standard specification text; implemented in DCS/SCADA alarm management systems. Not a wire protocol.

**Adoption:** Universal in petrochemical, pharmaceutical, and power generation control rooms. ISA-18.2 compliance is often required by process industry regulations.

**Open source:** No open-source implementation of ISA-18.2 alarm management as a library; embedded in DCS vendors (Emerson, Honeywell, ABB, Yokogawa).

**Curve logging relevance:** ISA-18.2 deadband is a well-established industrial concept for per-signal numeric threshold in engineering units — confirms the concept is proven in regulated environments. Alarm context (hysteresis) differs from data compression context (epsilon), but the underlying mechanism is the same. Not applicable to curve logging directly.

---

### 33. Eclipse Kuksa Databroker / COVESA DIP

**What sampling metadata it can express:**
Eclipse Kuksa Databroker is a gRPC-based VSS signal broker. `Subscribe` calls with `FieldMask` filter to specific VSS paths. `GetValue`/`SetValue` for current-value access. Kuksa supports actuator targets and current-value separation. COVESA Data Information Provisioning (DIP) architecture proposes separating signal production from consumption via a broker layer, but does not yet define sampling algorithm parameters. No native deadband, epsilon, or curve logging in published Kuksa specifications.

**Format:** gRPC + Protobuf (Kuksa wire), VSS YAML (signal catalog), COVESA JSON (DIP).

**Adoption:** Eclipse SDV (Software Defined Vehicle) reference architecture — Eclipse Leda, Eclipse Kuksa, Eclipse Velocitas. BMW, Bosch, Microsoft Azure contributing. Growing automotive platform standard.

**Open source:** [eclipse-kuksa/kuksa-databroker](https://github.com/eclipse-kuksa/kuksa-databroker) (Rust), [eclipse-kuksa/kuksa-python-sdk](https://github.com/eclipse-kuksa/kuksa-python-sdk).

**Curve logging relevance:** Kuksa Databroker is the reference implementation target for any VSS overlay sampling metadata — including `curve_epsilon`. Adding curve logging as a Databroker subscription filter (compress the stream before delivering to subscribers using RDP) would be the natural reference implementation path. Not a vocabulary source, but the deployment platform where the proposed fields would be implemented.

---

## Comparative Summary Table

**Curve Logging column key:**
- **✗** — No support; concept absent from standard
- **~step** — Nearest analog exists as step-from-last-value deadband (wrong reference model; per-signal configurable in engineering units)
- **~step+pmax** — Step deadband paired with a per-signal or per-group heartbeat (strongest structural match; still wrong reference model)
- **○ ext** — Standard is extensible; curve logging parameters could be carried as extension fields or annotations
- **★ path** — Uses or references interpolation-path deviation (correct model, though informative/research rather than normative collection policy)
- **/ read** — Interpolation in read/query path only; does not drive collection decisions
- **—** — Deprecated / not applicable

| Standard | Sampling Rate | pmin / pmax | On-Change | Threshold Trigger | Data Quality | Privacy / Access | Retention | Complexity | Vehicle Relevance | **Curve Logging** |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|---|:---|
| **W3C SOSA/SSN** | Via extension | No | Yes (Observation) | No | ssn:hasSystemCapability | No | No | RDF/OWL — high | High (research) | **○ ext** (via Procedure) |
| **OGC SensorML 3.0** | Via sml:output | Via constraints | Partial | Via constraints | swe:quality | No | No | XML/JSON — med-high | Medium | **○ ext** (Process description) |
| **OGC SWE Common** | Via DataStream | Partial | Yes | Via quality | swe:quality | No | No | XML/JSON — medium | Medium | **✗** |
| **OMA LwM2M** | pmin/pmax | ✓ pmin / pmax | ✓ st | ✓ gt / lt | Stale/Good (indirect) | No | No | CoAP attr — **low** | **High** | **~step** (st; propose cd) |
| **ETSI SAREF** | FrequencyMeasurement | PeriodMeasurement | No | No | No | No | No | OWL/RDF — high | Medium | **✗** |
| **FIWARE NGSI-LD** | Via throttling | throttling param | Yes | No | Property-of-property | No | No | JSON-LD — medium | Medium | **✗** |
| **Eclipse Vorto** | No | No | No | No | No | No | No | Deprecated DSL | **None** | **—** |
| **VSS Overlays** | interval_ms (informal) | No | No | No | No | No | No | YAML — **lowest** | **Very High** | **○ ext** (proposed curve_epsilon) |
| **OpenTelemetry** | Global SDK interval | No | No | No | Exemplar filters | No | No | OTLP/Protobuf | Low (SW only) | **✗** |
| **InfluxDB / Flux** | Telegraf poll interval | No | No | No | Via tags | No | Retention policy | Line Protocol — low | Medium (storage) | **✗** |
| **ISO 22837** | Not specified | No | No | No | No | No | No | ITS msgs — high | Medium | **✗** |
| **ISO 23150** | Implicit output rate | No | No | No | Confidence values | No | No | ARXML — high | High (ADAS) | **✗** |
| **AUTOSAR AP** | cycleTime (ARXML) | Partial | Yes (events) | No | No | No | No | ARXML — **high** | **Very High** | **✗** |
| **CoAP + Cond. Attrs** | c.pmin / c.pmax | ✓ c.pmin / c.pmax | ✓ c.st | ✓ c.gt / c.lt | No | No | No | CoAP attr — low | High | **~step** (c.st; propose c.cd) |
| **MQTT Sparkplug B** | No | No | RBE (by exception) | No | is_null, STALE | No | No | Protobuf — low | High | **✗** |
| **W3C WoT TD** | Via protocol binding | No | observable (boolean) | No | No | Security defs | No | JSON-LD — medium | High | **○ ext** (JSON-LD context) |
| **DDS QoS** | TIME_BASED_FILTER | ✓ DEADLINE / LIFESPAN | DEADLINE violation | No | LIVELINESS | No | ✓ DURABILITY / LIFESPAN | XML/API — **high** | **Very High** | **✗** (no value deviation) |
| **IEEE 1451 TEDS** | update_rate (TEDS) | Yes | No | No | Calibration, uncertainty | No | No | Binary/JSON — high | Medium | **✗** |
| **OASIS AMQP** | Via app-properties | ttl / expiry_time | No | No | No | No | ✓ ttl | Wire proto — medium | Medium | **✗** |
| **OPC UA** | MonitoredItem interval | ✓ sampling + publishing | Yes | ✓ DeadbandValue (step) | No | Security (built-in) | No | XML/binary — high | High | **~step** (DeadbandValue per item) |
| **BACnet COVIncrement** | No | covLifetime (indirect) | ✓ COV | ✓ COVIncrement (step) | No | No | No | BACnet — medium | Low (buildings) | **~step** (best-deployed ε analog) |
| **IEC 61850 deadbandMag** | No | ✓ intgPd (RCB-level) | ✓ dchg | ✓ deadbandMag (step) | optFlds reason | No | No | MMS/SCL — high | Low (utility) | **~step+pmax** (strongest structural match) |
| **DNP3 Object 34** | No | Integrity poll (master) | ✓ Class 1 event | ✓ per-point deadband | No | No | No | DNP3 — medium | Low (utility) | **~step** (per-point; proven at scale) |
| **IEC 60870-5 P_ME** | No | ✓ transmission period (per-point) | ✓ threshold crossing | ✓ deadband parameter | No | No | No | IEC 60870 — high | Low (legacy) | **~step+pmax** (per-point ε+pmax pair) |
| **ISO 19141 / OGC Moving Features** | No | No | No | No | No | No | No | JSON/XML schema | Medium (geo) | **★ path** (SED = interpolation-path deviation in associated research) |
| **oneM2M TS-0001** | No | ✓ pmin / pmax analogs | ✓ resourceUpdate | No | No | No | No | JSON/XML — medium | Medium | **✗** |
| **DLMS/COSEM IEC 62056** | Capture period (fixed) | No | No | No (alarm only) | No | No | No | Binary — high | Low (metering) | **✗** |
| **ISOBUS ISO 11783** | Capture period | No | No | No | No | No | No | CAN/XML — medium | Low (ag vehicle) | **✗** |
| **AAS / IEC 63278** | SamplingInterval (SMT) | No | EventElement | No | No | No | No | JSON/XML — medium | Medium (supply chain) | **○ ext** (Qualifier / Submodel Template) |
| **Prometheus / OpenMetrics** | scrape_interval (global) | No | No | No | staleness marker | No | No | Text — **low** | Low (SW only) | **✗** |
| **Apache IoTDB** | Per-timeseries encoding | No | No | No | No | No | No | Binary/SQL — medium | Low (storage) | **✗** (storage encoding only) |
| **OPC UA HDA** | ReadProcessed interval | No | ReadRaw | No | No | Security (built-in) | No | XML/binary — high | High | **/ read** (Interpolated aggregate validates reconstruction model) |
| **ISA-18.2** | No | No | No | ✓ alarm deadband (step) | No | No | No | Specification text | Low (process) | **✗** (alarm context only) |
| **Eclipse Kuksa / COVESA DIP** | No | No | Subscribe | No | No | No | No | gRPC/Protobuf — low | **Very High** | **○ ext** (reference implementation target) |

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
| `privacy_classification` | **Not covered by any standard** | Gap across all 34 candidates |
| `access_control` | WoT TD Security Definitions (per-device), OPC UA Security | Only per-device, not per-signal |
| `retention_policy` | DDS LIFESPAN (sample TTL), InfluxDB bucket retention, AMQP ttl | All at message/bucket level, not signal definition level |
| `curve_epsilon` | **Not covered by any standard** — nearest analog: BACnet COVIncrement, IEC 61850 deadbandMag, DNP3 Object 34 (all step-from-last-value) | Gap: no standard uses interpolation-path deviation as collection trigger |
| `curve_algorithm` (RDP/PRDP) | **Not covered by any standard** | OGC Moving Features SED research is closest (informative only) |
| `curve_max_interval_ms` | IEC 61850 intgPd (RCB-level), IEC 60870-5 transmission period (per-point), oneM2M periodicNotificationDuration | Per-signal pmax exists in IEC 60870-5 and oneM2M |
| `curve_min_interval_ms` | OMA LwM2M pmin, CoAP c.pmin, oneM2M minimumObservableInterval | Well covered |

---

## Curve Logging Support — Dedicated Assessment

Across all 34 standards surveyed, **no standard natively uses interpolation-path deviation (RDP / SED) as a collection trigger**. The gap is complete. Standards cluster into four tiers:

### Tier 1: Structural match — step-from-last-value threshold + heartbeat (wrong reference model, right structure)

These standards have the correct two-parameter architecture (`ε analog` + `pmax analog`), differing only in that they measure deviation from the last reported value rather than from the interpolated path. Replacing the reference model would convert them to curve logging.

| Standard | ε analog | pmax analog | Granularity | Deployment scale |
|----------|----------|------------|-------------|-----------------|
| **IEC 61850 deadbandMag + intgPd** | deadbandMag (per data attribute) | intgPd (per RCB, shared) | Per-signal deadband, RCB-level heartbeat | Global power grid |
| **IEC 60870-5 P_ME** | Threshold parameter (per point) | Transmission period (per point) | Fully per-point | Legacy utility SCADA |
| **BACnet COVIncrement** | COVIncrement (per object, REAL) | covLifetime (indirect) | Per-object | Global building automation |
| **DNP3 Object 34** | Per-point deadband (integer) | Integrity poll (master-driven) | Per-point, not per-signal pmax | North American utility SCADA |
| **OPC UA DeadbandValue** | DeadbandValue (per MonitoredItem) | Publishing interval (subscription-level) | Per-item, not per-signal pmax | Manufacturing, automotive |

### Tier 2: Partial match — threshold only or temporal only

These standards have one parameter but not both:

| Standard | What they have | What's missing |
|----------|---------------|----------------|
| **OMA LwM2M st** | st = change threshold (step) | No per-signal pmax (pmax is per-observation) |
| **CoAP c.st** | c.st = change threshold (step) | Same limitation as LwM2M |
| **DDS TIME_BASED_FILTER + DEADLINE** | pmin/pmax via QoS | No value-deviation concept at all |
| **oneM2M** | pmin/pmax analogs | No value-deviation concept |

### Tier 3: Extension carriers — can hold curve logging parameters without natively defining them

| Standard | Extension mechanism | What can be carried |
|----------|--------------------|--------------------|
| **VSS Overlays** | YAML fields in .vspec | `curve_epsilon`, `curve_algorithm`, etc. — direct fit |
| **AAS / IEC 63278** | Qualifier annotations + Submodel Templates | A curve logging SMT could be standardized via IDTA |
| **W3C WoT TD** | JSON-LD @context extensions | `curve_epsilon` etc. via automotive WoT extension vocabulary |
| **OGC SensorML 3.0** | Process description | RDP described as a sampling SamplingProcedure |
| **Eclipse Kuksa** | Subscription filter implementation | Databroker could apply RDP before delivering to subscribers |

### Tier 4: Path-deviation model — correct algorithm, informative/research only

| Standard | Path-deviation concept | Status |
|----------|----------------------|--------|
| **ISO 19141 / OGC Moving Features** | SED (Synchronized Euclidean Distance) in associated trajectory simplification research | Research / informative |
| **OPC UA HDA `Interpolated` aggregate** | Linear interpolation between kept points validates the reconstruction model | Read path only; not collection |

### Proposed standardization path for curve logging

| Track | Action | Target body |
|-------|--------|-------------|
| **Immediate** | Add `curve_epsilon`, `curve_algorithm`, `curve_max_interval_ms`, `curve_min_interval_ms` to COVESA VSS overlay specification | COVESA FMD WG |
| **Near-term** | Propose `cd` (curve deviation) attribute alongside `st` in OMA LwM2M notification attributes | OMA SpecWorks |
| **Near-term** | Propose `c.cd` attribute alongside `c.st` in IETF CoAP Conditional Attributes draft | IETF CoRE WG |
| **Medium-term** | Contribute normative trajectory simplification profile (SED + epsilon) to OGC Moving Features | OGC Moving Features SWG |
| **Medium-term** | Publish IDTA AAS Submodel Template for vehicle signal collection parameters | IDTA / COVESA joint |
| **Longer-term** | Propose `curveDev` trigger mode in IEC 61850 Report Control Blocks (alongside `dchg`/`dupd`) | IEC TC57 WG10 |
| **Longer-term** | Propose per-point curve deviation object in DNP3 (new Object Group alongside Object 34) | DNP3 Technical Committee |

---

## Gap Areas Not Covered by Any Existing Standard

Four critical metadata dimensions are absent from every evaluated standard:

1. **Privacy classification at the signal level** — No standard defines per-signal PII sensitivity (personal / pseudonymous / sensitive). GDPR compliance requires this; standards leave it to implementation.

2. **Retention policy at the signal catalog level** — DDS LIFESPAN covers message-level TTL; InfluxDB covers bucket-level retention; AMQP `ttl` covers per-message expiry. None define per-signal-type retention policy in a specification catalog.

3. **Access control at the signal level** — WoT TD and OPC UA define per-device/per-service access control. No standard defines which role or party may receive a specific signal's values in a signal catalog annotation.

4. **Interpolation-path deviation compression (curve logging)** — All 34 evaluated standards either use step-from-last-value thresholds or have no value-deviation concept. No standard defines deviation from the interpolated path between kept points as a collection trigger. The RDP/SED model is used in OGC Moving Features research but is not normative in any collection specification.

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
- [OPC UA Historical Access Part 11](https://reference.opcfoundation.org/Core/Part11/v104/docs/)
- [BACnet COV — Change of Value overview (Chipkin)](https://store.chipkin.com/articles/bacnet-cov-change-of-value)
- [ASHRAE 135 BACnet Standard](https://www.ashrae.org/technical-resources/bookstore/bacnet)
- [IEC 61850 Deadband Reporting and Logging (Netted Automation Blog)](https://blog.nettedautomation.com/2019/11/iec-61850-deadband-reporting-and.html)
- [libIEC61850 client tutorial](https://libiec61850.com/documentation/iec-61850-client-tutorial/)
- [OpenDNP3 — DNP3 per-point deadband](https://dnp3.github.io/)
- [IEEE 1815-2012 — DNP3 Standard](https://standards.ieee.org/ieee/1815/4414/)
- [IEC 60870-5-104 Communication Protocol Manual (ABB)](https://library.e.abb.com/public/68021e6c8f654aca98c5b10d1a02134e/1MAC306892-MB%20C%20IEC%20104%20Comm%20Protocol.pdf)
- [ISO 19141 Moving Features — ISO TC211](https://committee.iso.org/sites/tc211/home/projects/projects---complete-list/iso-19141.html)
- [OGC Moving Features JSON Encoding (OGC 19-045r3)](https://docs.ogc.org/is/19-045r3/19-045r3.html)
- [LiMITS: Linear Interpolation Method for Trajectory Simplification (arXiv)](https://arxiv.org/pdf/2010.08622)
- [Moving Object Trajectory Compression (Hindawi)](https://www.hindawi.com/journals/mpe/2016/6587309/)
- [oneM2M TS-0001 Functional Architecture](https://www.onem2m.org/images/files/deliverables/TS-0001-Functional_Architecture-V3_15_1.pdf)
- [IEC 62056 / DLMS-COSEM (Wikipedia)](https://en.wikipedia.org/wiki/IEC_62056)
- [ISOBUS ISO 11783 Introduction (CSS Electronics)](https://www.csselectronics.com/pages/isobus-introduction-tutorial-iso-11783)
- [Asset Administration Shell Metamodel — IDTA](https://industrialdigitaltwin.org/wp-content/uploads/2023/06/IDTA-01001-3-0_SpecificationAssetAdministrationShell_Part1_Metamodel.pdf)
- [IEC 63278-1 AAS — IEC Webstore](https://webstore.iec.ch/en/publication/65628)
- [Prometheus Staleness (Brian Brazil, PromCon 2017)](https://promcon.io/2017-munich/slides/staleness-in-prometheus-2-0.pdf)
- [Apache IoTDB Encoding and Compression](https://iotdb.apache.org/UserGuide/V1.2.x/Basic-Concept/Encoding-and-Compression.html)
- [Improving Time Series Compression in IoTDB (VLDB)](https://www.vldb.org/pvldb/vol18/p3406-tang.pdf)
- [Eclipse Kuksa Databroker GitHub](https://github.com/eclipse-kuksa/kuksa-databroker)
- [ANSI/ISA-18.2 Management of Alarm Systems](https://www.isa.org/products/ansi-isa-18-2-2016-management-of-alarm-systems-for)
- [Geotab Curve Algorithm Overview](https://www.geotab.com/blog/gps-logging-curve-algorithm/)
- [Geotab/curve — open source implementation (GitHub)](https://github.com/Geotab/curve)
- [Ramer-Douglas-Peucker Algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm)
