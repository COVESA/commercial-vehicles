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

## Third Survey Round — Automotive Industry and Adjacent Standards

Standards in this round were selected by asking what is already widely deployed in vehicles, in automotive development toolchains, and in cloud telematics backends that the first two rounds missed. Entries with **🚗 Automotive Core** are broadly deployed across production vehicles or OEM toolchains today.

---

### 34. SOME/IP — Scalable service-Oriented MiddlewarE over IP 🚗 Automotive Core

**What sampling metadata it can express:**
AUTOSAR's primary in-vehicle service-oriented communication protocol over Ethernet. Event-driven notifiers transmit either cyclically (at a configured cycle time) or on-change (`EventHandler` with optional filters). `SOME/IP-SD` (Service Discovery) dynamically negotiates publish/subscribe relationships. Per-service event configurable: cyclic period (ms), initial-repetition count, offer-delay. Field-level change filtering is implementation-defined; the spec does not standardize a numeric change threshold.

**Format:** Binary framing over UDP/TCP (Ethernet). Configured via ARXML in AUTOSAR toolchains. Not YAML.

**Adoption:** 🚗 **Dominant in Adaptive AUTOSAR Ethernet-connected ECUs.** Developed by BMW (2011), adopted into AUTOSAR 2014. In production at BMW, Audi, Mercedes-Benz, Porsche, Volkswagen, and their Tier-1 suppliers. Standard choice for domain controllers and central computing platforms on modern vehicles.

**Open source:** vsomeip (C++ — Bosch, GENIVI/COVESA), CommonAPI C++ (COVESA), Eclipse Cyclone SOME/IP.

**Curve logging relevance:** Cyclic period = fixed pmax; on-change event = binary change trigger (no amplitude threshold). No standardized numeric threshold or epsilon. Change filtering exists but at implementation level, not in the spec. Curve logging would need to be implemented as an application-layer filter upstream of SOME/IP publication — not expressible in SOME/IP metadata.

---

### 35. ASAM MDF4 / MF4 — Measurement Data Format 4 🚗 Automotive Core

**What sampling metadata it can express:**
The dominant automotive measurement data file format. Hierarchical structure: `DG` (Data Group) → `CG` (Channel Group) → `CN` (Channel Block). Each CN block stores: signal name, byte/bit offset, data type, physical unit conversion (CompuMethod), min/max measured value, and display name. CG block carries the sampling rate as `cycle_count` and `time_values`. Supports multiple synchronization types: time, angle, distance, index. DZ blocks (MDF 4.1+) provide lossless Deflate compression at the chunk level. Variable-length samples and event-driven CG types enable on-change logging within the same file structure.

**Format:** Binary file format (`.mf4`). Read/written by all major automotive measurement tools. ASAM open specification (free download).

**Adoption:** 🚗 **De facto standard for automotive test and development measurement logging.** Originally developed by Vector Informatik and Bosch (1991); became ASAM standard 2009. Used by all OEMs and Tier-1s for CAN, CAN FD, LIN, FlexRay, Automotive Ethernet, and ECU internal signal logging during development, calibration, durability testing, and field data campaigns. MF4 files are the primary exchange format for measurement data between OEM and supplier.

**Open source:** asammdf (Python — fastest), mdfreader (Python), MDF4 Lib (C++ — PEAK System), Cantools (limited MF4).

**Curve logging relevance:** MDF4 is a *storage* format, not a *collection policy* standard — it stores whatever was sampled, at whatever rate the collection agent chose. However: (1) MDF4's event-driven CG type shows that the format can represent compressed/on-change data without a fixed rate; (2) a curve-logged data stream would store naturally in MDF4 with variable time spacing; (3) no epsilon or algorithm metadata field exists in MDF4 — a curve-logged file is indistinguishable from a sparsely-sampled file unless metadata is added via the MD (metadata) block as custom XML.

---

### 36. ASAM ASAP2 (A2L) + XCP — ECU Measurement Description and Protocol 🚗 Automotive Core

**What sampling metadata it can express:**
**A2L (ASAP2 format):** ECU measurement and calibration description file. Per-measurement object: name, address, ECU type, conversion method (CompuMethod), min/max physical range, display format. DAQ (Data Acquisition) section defines: EVENT channels with `CYCLE_TIME` and `UNIT` (ms or μs granularity), `MAX_ODT` per DAQ list, `MAX_DAQ` count, `PRESCALER` support. Multiple measurements can share an event (same sample time). `PRESCALER` allows sub-sampling: sample every nth event tick.

**XCP (Universal Measurement and Calibration Protocol, ASAM MCD-1):** Runtime protocol for configuring and streaming DAQ lists from an ECU. DAQ lists are groups of ODTs (Object Descriptor Tables); each ODT is a set of ECU memory addresses to read atomically at each event trigger. Events are ECU-side timing sources (e.g., "10ms task", "100ms task", "ignition event"). `SET_DAQ_LIST_MODE` sets the DAQ list to a specific event channel. `PRESCALER` halves or quarters effective sampling rate.

**Format:** A2L is a text file format. XCP is a binary protocol over CAN, CAN FD, Ethernet, USB, or SPI. Both are ASAM open standards.

**Adoption:** 🚗 **Universal in automotive ECU development.** Every OEM and Tier-1 supplier uses A2L + XCP during ECU development and calibration. Over 50,000 engineers use INCA (ETAS) or CANape (Vector) — the two dominant tools — both built on A2L/XCP. A2L files are delivered by ECU suppliers to OEM calibration engineers as part of the standard handoff.

**Open source:** pya2l (Python A2L parser), python-can + XCP stack (limited). Commercial dominates.

**Curve logging relevance:** XCP's DAQ mechanism is the most granular standardized ECU sampling configuration in automotive — per-measurement-object assignment to named event channels with prescaling. But it is a *fixed-rate* or *event-triggered* model (the ECU's task scheduler fires events at fixed periods). No amplitude deviation threshold: XCP transmits every sample at the configured rate. Curve logging as a downstream filter applied to XCP-captured data is feasible; encoding curve epsilon into A2L measurement descriptions would require an ASAM extension.

---

### 37. W3C VISSv2 — Vehicle Information Service Specification v2 🚗 Automotive Core

**What sampling metadata it can express:**
W3C and COVESA standard for accessing VSS signal data over HTTP/REST, WebSocket, or MQTT. `Subscribe` method accepts a `VISSubscribeFilter` dictionary with three per-signal filter types:
- **`interval`** (unsigned long, ms): Minimum sampling/delivery interval — direct pmin equivalent
- **`minChange`** (unsigned long): Minimum value change before notification is sent — **direct step threshold**, per-signal configurable by the subscriber
- **`range`** (`below` / `above` bounds): Notify only when value is within or outside a numeric range — equivalent to LwM2M `lt`/`gt`

All three filters are per-subscription, per-signal. A single subscribe call can combine interval + minChange + range. VISSv2 server implementations decide whether filtering occurs server-side or client-side.

**Format:** JSON over WebSocket, HTTP/REST, or MQTT. Simple and approachable.

**Adoption:** 🚗 **Growing automotive adoption, especially in connected vehicle platforms.** Implemented by Volvo, BMW, Jaguar Land Rover, Renesas, Bosch, Visteon, Geotab, AGL (Automotive Grade Linux), Mitsubishi Electric. AWS FleetWise and BlackBerry IVY both align with VISSv2-style VSS access. The closest standard to a native VSS subscription API.

**Open source:** [COVESA/vissr](https://github.com/COVESA/vissr) (Go — reference server), w3c-visserver (JavaScript, older).

**Curve logging relevance:** `minChange` is a **direct per-signal step threshold** — the most directly useful standard field for `curve_epsilon` analogy in the VSS ecosystem, and the only one native to the VSS/automotive stack. Limitation: step-from-last-notified-value, not interpolation-path deviation. `interval` covers pmin. No pmax (heartbeat) defined. VISSv2 is the natural place to add a `curveDeviation` filter alongside `minChange` — same JSON subscription structure, same per-signal granularity.

---

### 38. IETF SenML — Sensor Measurement Lists (RFC 8428)

**What sampling metadata it can express:**
A lightweight JSON/CBOR/XML format for batching sensor readings. Base fields shared across records: `bn` (base name), `bt` (base time), `bu` (base unit), `bv` (base value), `bs` (base sum). Per-record: `n` (signal name), `u` (unit), `v` (numeric value), `sv` (string value), `bv` (boolean), `t` (time offset), `ut` (update time — interval since last update), `s` (running sum/integral). RFC 9100 adds versioning (`bver`) and extended data types. No sampling rate, threshold, or trigger-mode field. The format carries measurements; the sampling policy is out of scope.

**Format:** JSON (primary), CBOR (binary, compact), XML, EXI. Very simple — entire format fits in one RFC.

**Adoption:** Moderate in IoT sensor networks; limited direct automotive production use. Used in IETF CoAP/LwM2M ecosystems — SenML is the natural payload format when LwM2M attributes control the trigger. The `ut` (update time) field is useful for recording the interval between curve-logged points.

**Open source:** senml (Python), senml-js (JavaScript), libsenml (C).

**Curve logging relevance:** SenML has no sampling policy metadata. Its `ut` field could record the actual inter-sample interval for a curve-logged stream, making it a natural wire format for transmitting curve-logged points. Pair with LwM2M `pmin`/`pmax`/proposed `cd` for a complete lightweight stack.

---

### 39. MQTT v5 — OASIS MQTT Version 5.0

**What sampling metadata it can express:**
MQTT v5 adds to v3.1.1: **Message Expiry Interval** (per-message TTL in seconds — direct retention hint), **Subscription Options** (no-local, retain-as-published, retain-handling), **Subscription Identifier** (links notification to originating subscription), **User Properties** (arbitrary key-value string pairs on any packet — enables per-message custom metadata), **Shared Subscriptions** (load-balanced consumer groups), **Topic Aliases** (reduce header overhead for high-frequency topics), **Flow Control** (Receive Maximum — backpressure). No native amplitude threshold or change filter.

**Format:** Binary over TCP/TLS or WebSocket. Widely supported.

**Adoption:** 🚗 **Very widely used in automotive cloud telematics.** SAIC Volkswagen deployed EMQX (MQTT v5) for their IoV platform in 2018, now handling millions of vehicles. BMW, Audi, Porsche, and Tesla use MQTT in telematics pipelines. Cellular IoT (NB-IoT, LTE-M) automotive connections predominantly use MQTT.

**Open source:** Eclipse Mosquitto, EMQX, HiveMQ, VerneMQ. Client libraries in every language.

**Curve logging relevance:** `Message Expiry Interval` maps to retention policy. `User Properties` could carry `curve_epsilon`, `curve_algorithm`, or compression metadata per-message, making curve-logged data self-describing in transit. No native change threshold. MQTT v5's User Properties are the best existing mechanism for tagging curve-logged telemetry with its compression parameters in a standards-compliant way.

---

### 40. SAE J2735 / DSRC — Basic Safety Message 🚗 Automotive Core

**What sampling metadata it can express:**
SAE J2735 defines the V2X message set dictionary for DSRC (5.9 GHz) and C-V2X. The **Basic Safety Message (BSM)** Part I contains: latitude, longitude, elevation, speed, heading, acceleration (longitudinal, lateral, vertical, yaw rate), brake system status, vehicle size. Transmission rate: **10 Hz (100 ms interval) — normative**, mandated for all DSRC-equipped vehicles. BSM Part II is event-driven (on-change), added when relevant (e.g., hazard lights on, disabled vehicle, emergency event).

**Format:** ASN.1 (J2735 uses UPER — Unaligned Packed Encoding Rules) over DSRC/C-V2X. Dense binary.

**Adoption:** 🚗 **Mandatory for V2X deployments in US, EU (C-V2X via ETSI), and China.** All DSRC-equipped vehicles transmit BSM at 10 Hz. This is one of the few automotive standards with a normatively mandated per-signal sampling rate for a defined set of safety signals.

**Open source:** ASN1C (commercial), COHDA Wireless BSM stack. Limited open source.

**Curve logging relevance:** Fixed 10 Hz is the antithesis of adaptive compression — it prioritizes deterministic latency for safety over efficiency. BSM Part II's event-driven extension is the closest concept: conditional transmission of additional data. No epsilon or path-deviation concept. The 10 Hz rate for position + kinematics matches Geotab FMD's GPS/speed collection rate before curve compression is applied.

---

### 41. Apache Kafka — Distributed Streaming Platform 🚗 Automotive Core (cloud backend)

**What sampling metadata it can express:**
Kafka topics carry byte-stream messages with: `timestamp` (producer or broker), `key` (for partitioning and log compaction), `value` (payload), and `headers` (string key-value pairs — analogous to MQTT v5 User Properties). **Log compaction**: retains only the latest message per key — equivalent to keeping the latest known state of a signal. **Time-based retention**: delete messages older than N days/hours. **Schema Registry** (Confluent): enforces Avro/Protobuf/JSON Schema per topic; version-controlled signal schema with compatibility checking. **Kafka Streams** and **Apache Flink** enable real-time windowed aggregation, anomaly detection, and per-signal processing applied to the stream.

**Format:** Binary (Avro, Protobuf, or JSON with Schema Registry). Partitioned log. Distributed.

**Adoption:** 🚗 **Widely used in automotive cloud backends for vehicle telemetry pipelines.** Rivian streams 5,500+ signals every 5 seconds per vehicle across 120+ Flink pipelines with 250+ unique consumers. BMW, Audi, Porsche, Tesla use Kafka for real-time driver behavior analysis, OTA orchestration, and autonomous vehicle training data pipelines.

**Open source:** [apache/kafka](https://github.com/apache/kafka), Confluent Schema Registry (community), kafka-python, confluent-kafka-go.

**Curve logging relevance:** Kafka headers could carry `curve_epsilon` and `curve_algorithm` as per-message metadata on curve-logged telemetry, making the compression parameters inspectable by downstream consumers. Log compaction aligns with the curve logging use case: retain only the kept points, discard intermediate samples. No native RDP or path-deviation filtering — curve compression happens upstream (at the vehicle or edge) before data enters Kafka. Kafka is the delivery and retention infrastructure, not the compression decision point.

---

### 42. CANopen / CiA 301 — CAN Application Layer Protocol 🚗 Automotive Core

**What sampling metadata it can express:**
CANopen defines Process Data Objects (PDOs) with four transmission type categories and per-PDO timing parameters:

**Transmission types:**
- **Types 1–240** (Synchronous cyclic): TPDO transmitted every nth SYNC message — configurable fixed rate
- **Type 0** (Synchronous acyclic): Event-driven but synchronized to SYNC boundary
- **Type 254** (Asynchronous cyclic): Send on **value change** AND guarantee periodic heartbeat — exact HYBRID mode analog
- **Type 255** (Asynchronous acyclic): Send on **value change** only — exact CHANGE mode analog

**Timing parameters (per-PDO, object dictionary 0x1800–0x19FF):**
- **Inhibit Time** (sub-index 0x03, unit: 100 μs): Minimum interval between successive PDO transmissions — **direct pmin equivalent**
- **Event Timer** (sub-index 0x05, ms): In asynchronous modes, TPDO sent if no change occurs within this time — **direct pmax equivalent**

**Format:** CAN frames (11-bit or 29-bit ID). Object dictionary described in EDS (Electronic Data Sheet) files — text format. Widely tooled.

**Adoption:** 🚗 **Very widely deployed in vehicles and industrial automation.** CANopen is used in automotive body electronics, ADAS sensor interfaces, electric vehicle BMS, industrial robots, and medical devices. CiA 301 is the foundational standard. PDO transmission type 254 (HYBRID) is a routine configuration in production ECUs.

**Open source:** CANopenNode (C — embedded, widely used), python-canopen, CANopen for Python.

**Curve logging relevance:** CANopen is the **strongest structural match** for curve logging transmission parameters among production automotive standards. Type 254 (HYBRID: on-change + periodic heartbeat) directly implements the `transmission_mode: HYBRID` + `curve_max_interval_ms` combination. Inhibit Time = `curve_min_interval_ms`. Event Timer = `curve_max_interval_ms`. **Missing only:** an amplitude change threshold (the decision of whether the value has changed enough to transmit is binary, not epsilon-gated). Adding a `change_threshold` (deadband) parameter to asynchronous PDO types alongside Inhibit Time and Event Timer would complete the curve logging parameter set in CANopen.

---

### 43. AUTOSAR COM — Signal Filtering Modes 🚗 Automotive Core

**What sampling metadata it can express:**
The AUTOSAR COM (Communication) module handles signal routing in Classic Platform ECUs. Per-signal/I-PDU filter configuration via `ComFilter`:
- **`ALWAYS`**: Transmit unconditionally
- **`NEVER`**: Never transmit
- **`MASKED_NEW_DIFFERS_OLD`**: Transmit if `(new & mask) ≠ (old & mask)` — bit-mask change detection
- **`MASKED_NEW_DIFFERS_MASKED_OLD`**: Transmit if `(new & mask) ≠ (old_masked & mask)`
- **`ONE_EVERY_N`**: Transmit one sample for every N updates (prescaler/decimation)
- **`NEW_IS_WITHIN`** / **`NEW_IS_OUTSIDE`**: Transmit if new value is within/outside a configured range
- **`MASKED_NEW_EQUALS_X`**: Transmit if masked value equals a specific constant

Transmission modes per I-PDU: `DIRECT` (event-driven), `PERIODIC` (cyclic), `MIXED` (both). `ComTxModeTimePeriod` sets cyclic period.

**Format:** ARXML configuration (XML). Compiled into ECU firmware via AUTOSAR toolchain.

**Adoption:** 🚗 **Universal — present in every AUTOSAR Classic Platform ECU.** All OEMs and Tier-1 suppliers. AUTOSAR CP is in tens of millions of production ECUs globally.

**Curve logging relevance:** `NEW_IS_WITHIN` / `NEW_IS_OUTSIDE` are range-based transmission triggers analogous to LwM2M `lt`/`gt`. `MASKED_NEW_DIFFERS_OLD` is a bitmask change filter — structural analog to a step threshold at the bit level. `ONE_EVERY_N` is a prescaler (rate decimation). `MIXED` mode = HYBRID transmission. The full combination (MIXED + filter + period) covers the structural parameters of curve logging minus the epsilon/interpolation model. The closest standardized per-signal filtering in the in-vehicle domain.

---

### 44. ETSI CAM / DENM — Cooperative Awareness and Environmental Notification 🚗 Automotive Core

**What sampling metadata it can express:**
**CAM (Cooperative Awareness Message, ETSI EN 302 637-2):** Mandatory V2X heartbeat message. Generation rules define a **dynamic rate between 1–10 Hz**, triggered by changes in vehicle kinematics:
- Generate CAM if heading change > 4°, speed change > 0.5 m/s, or position change > 4 m since last CAM
- OR if 1 second has elapsed since last CAM (1 Hz floor regardless of motion)
- DCC (Dynamic Congestion Control) may further reduce rate down to 1 Hz under channel load

**DENM (Decentralized Environmental Notification, ETSI TS 102 894-2):** Event-triggered hazard/incident message. Transmit when a hazard event is detected; retransmit at a configurable `repetitionInterval` while hazard persists.

**Format:** ASN.1 (UPER) over ITS-G5 (ETSI DSRC) or C-V2X. Standardized in ETSI ITS suite.

**Adoption:** 🚗 **Mandatory for V2X in EU (Day-1 services), deployed in China, Japan, US (C-V2X).** CAM/DENM are the baseline V2X messages for all connected vehicle mandates in Europe under Delegated Regulation 2019/2144.

**Curve logging relevance:** CAM's kinematic-change trigger (heading > 4°, speed > 0.5 m/s, position > 4 m) is a **multi-dimensional change threshold** — each component is a step-from-last-value trigger in its own unit. The 1 Hz floor is a pmax analog. This is structurally equivalent to the LwM2M `st` + `pmax` combination but expressed as named physical thresholds rather than a single numeric epsilon. No interpolation-path model. However, CAM demonstrates that standards bodies are willing to define per-signal-type named change thresholds for safety signals — a useful precedent for the VSS proposal.

---

### 45. IEEE 802.1 TSN — Time-Sensitive Networking 🚗 Automotive Core (Ethernet)

**What sampling metadata it can express:**
TSN is a suite of IEEE 802.1 amendments for deterministic Ethernet. Relevant to sampling:
- **Credit-Based Shaper (CBS, 802.1Qav)**: Per-traffic-class bandwidth reservation and burst shaping
- **Time-Aware Shaper (TAS, 802.1Qbv)**: Gate control lists — time slots for traffic class transmission; ensures deterministic latency
- **Frame Preemption (802.1Qbu)**: High-priority frames interrupt low-priority transmission
- **IEEE 802.1DG-2025**: Automotive in-vehicle TSN profile specifying which 802.1 mechanisms are required for vehicle Ethernet networks

**Format:** IEEE 802.1 Ethernet frames. Configured via YANG models or NETCONF. Not signal-level metadata.

**Adoption:** 🚗 **Rapidly becoming mandatory in vehicle Ethernet.** Required for ADAS sensor fusion (camera, lidar, radar) over 100BASE-T1 / 1000BASE-T1. BMW, Toyota, GM, Ford deploying TSN in new programs. IEEE 802.1DG-2025 adoption driven by AUTOSAR AP and the shift to zonal/central compute architectures.

**Curve logging relevance:** TSN operates at the network layer — it ensures deterministic delivery of frames but has no concept of signal value or change threshold. It is complementary to curve logging: TSN guarantees that curve-logged data frames arrive within bounded latency; TSN itself does not decide what to transmit. Not applicable to sampling parameterization.

---

### 46. COVESA FMD — Fleet Management Data Working Group 🚗 Automotive Core

**What sampling metadata it can express:**
COVESA's Fleet Management Data (FMD) working group defines data collection campaign specifications using VSS as the signal model. FMD documents specify per-signal: use case, required/optional status, collection methodology, sampling rate. Publicly, FMD references **"intelligent data sampling (curve logic)"** as a sampling method but does not publish normative epsilon values or algorithm parameters. The group works with commercial vehicle OEMs, fleet operators, insurers, and telematics providers.

**Adoption:** 🚗 **Directly relevant to the VSS overlay proposal — FMD is the primary COVESA working group addressing exactly this problem.** Its signal tables and use cases are the primary input for the `usecase` fields in the COVESA commercial vehicles insurance YAML.

**Curve logging relevance:** FMD **explicitly references curve logic** as a sampling method — the only standards-adjacent body to do so by name. Epsilon values and algorithm parameters are not yet published normatively. The curve logging VSS overlay fields proposed in this document series are the natural formalization of what FMD intends. Contributing `curve_epsilon`, `curve_algorithm`, etc. to FMD is the highest-priority standardization path.

---

### 47. AUTOSAR SOVD — Service-Oriented Vehicle Diagnostics

**What sampling metadata it can express:**
ISO 17978-3, AUTOSAR's REST/HTTP/JSON diagnostic API for Adaptive Platform. Supports cyclic data queries (periodic polling at a configured interval) and trigger-based queries (on diagnostic event). Cycle time configurable in the SOVD request. No per-signal amplitude threshold or epsilon. Security via OAuth 2.0. HTTP/2 for performance.

**Adoption:** Growing in Adaptive Platform diagnostic tooling. Vector DIVA, ETAS INCA, and Softing implementing. Not yet in production vehicle fleets at scale.

**Curve logging relevance:** No amplitude threshold. Cyclic query = fixed pmax polling. Not applicable.

---

### 48. ISO 20078 — Extended Vehicle (ExVe) API

**What sampling metadata it can express:**
REST API standard for OEM backend services exposing vehicle data to third parties. Defines entity model (Vehicle, ECU, Driver, Fleet), resource patterns, authorization, and push/pull access modes. Part 2 (Access) defines REST URL structure. Part 4 (Control) defines preconditions. No normative per-signal sampling rate or change threshold in publicly available documentation.

**Adoption:** Moderate — used by Denso, European OEM backend integrations. Less common in North America.

**Curve logging relevance:** Not applicable — backend API standard, not a collection policy specification.

---

### 49. ISO 26262 — Functional Safety Heartbeat Monitoring

**What sampling metadata it can express:**
ISO 26262 defines safety architecture requirements including watchdog/heartbeat monitoring. The `FTTI` (Fault Tolerant Time Interval) constrains the maximum time from fault occurrence to detection. `DTI` (Diagnostic Test Interval) sets the monitoring frequency. Heartbeat monitors enforce a maximum silence interval — any safety-relevant signal that does not update within `pmax` is treated as a fault. This makes ISO 26262 the normative basis for `curve_max_interval_ms` in safety-critical signals: the heartbeat interval must satisfy ISO 26262 FTTI requirements.

**Adoption:** 🚗 **Mandatory for all automotive functional safety — universal across all OEMs and suppliers.**

**Curve logging relevance:** ISO 26262 directly motivates `curve_max_interval_ms` (pmax / heartbeat). Any curve logging deployment on safety-relevant signals must set `curve_max_interval_ms` to a value that satisfies the FTTI requirement for those signals. This provides a normative grounding for the heartbeat parameter.

---

### 50. Eclipse ICEORYX — Zero-Copy IPC for AUTOSAR AP

**What sampling metadata it can express:**
ICEORYX provides shared-memory IPC for zero-copy data transfer in AUTOSAR Adaptive Platform. `WaitSet` aggregates events from multiple subscribers; a thread blocks until any attached subscriber receives data. Per-subscriber: `SubscribeState`, event-based triggers. No built-in change threshold, amplitude filter, or rate limiting. Binary: event-occurred or not.

**Adoption:** Growing in AUTOSAR AP implementations (Apex.AI, Apex.OS). Used in autonomous driving stacks with ROS 2 (ICEORYX as the RMW transport).

**Curve logging relevance:** No amplitude filter. ICEORYX is a transport mechanism; curve filtering would live in the application layer upstream. Not applicable.

---

### 51. OBD-II / SAE J1979 🚗 Automotive Core

**What sampling metadata it can express:**
Mandated diagnostic interface for all light-duty vehicles sold in US/EU/China. Mode 01 PIDs provide real-time powertrain data on-demand: ~190+ standardized parameters (engine speed, coolant temp, fuel level, O2 sensors, MAF, throttle position, etc.). No standardized sampling rate — the host (scan tool or telematics device) polls at its own rate. ECU returns current-value snapshots; no history or on-change push mechanism. Mode 06 (on-board monitoring) and Mode 09 (vehicle information) are additional.

**Adoption:** 🚗 **Universal — mandatory on all light-duty vehicles since 1996 (US), 2001 (EU).** The foundation of aftermarket diagnostics, fleet telematics dongles, and insurance telematics devices.

**Curve logging relevance:** OBD-II is a pull-based query protocol — the telematics device polls at whatever rate it chooses. Geotab's curve logging is applied to OBD-II-sourced signals (speed, coolant temp, battery voltage, fuel level) after polling; the curve epsilon decisions happen in the telematics firmware, not in the OBD-II layer. OBD-II has no metadata for expressing sampling policy.

---

### 52. AWS IoT FleetWise / Cloud Vehicle Data Lakes 🚗 Automotive Core (cloud)

**What sampling metadata it can express:**
**AWS IoT FleetWise:** Campaign-based vehicle data collection. Signal catalog stores per-signal metadata: name, VSS path, data type, unit. Campaign definition specifies: collection condition (time-based, event-based with `conditionLanguage` — a signal-expression precondition), collection period (ms), campaign duration. **Collection condition** supports signal-expression predicates (`Vehicle.Speed > 80`) for conditional collection — a structured analog to `sampling_condition`. No per-signal amplitude threshold or epsilon in campaign spec; campaigns are all-or-nothing per signal.

**Azure IoV / Google Cloud Fleet Routing:** Similar pattern — IoT Hub/Event Hubs ingestion, Parquet/Avro in data lake, per-vehicle telemetry pipelines. Schema defined per OEM, no standardized per-signal sampling metadata.

**Adoption:** 🚗 **Rapidly becoming the dominant cloud telematics backend architecture.** AWS FleetWise used by major automotive OEMs in production. Rivian, with 5,500 signals streamed per vehicle every 5 seconds, exemplifies the scale. Azure IoT used by Ford Pro, GM, and others. Google Cloud used by select OEMs for AI/ML workloads.

**Curve logging relevance:** AWS FleetWise `conditionLanguage` is the cloud-side equivalent of `sampling_condition` — signal-expression predicates for conditional collection. The signal catalog could carry `curve_epsilon` and `curve_algorithm` as per-signal attributes with a schema extension. Curve logging would execute on the vehicle-side FleetWise agent before data is uploaded; the cloud catalog would hold the parameters. This is the most scalable deployment path for curve logging parameters in a cloud-managed fleet.

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
| **SOME/IP 🚗** | cyclic period (ARXML) | No (cyclic only) | ✓ on-change events | No (impl-defined) | No | No | No | Binary/ARXML — high | **Very High** | **✗** (no normative threshold) |
| **ASAM MDF4 🚗** | Per-CN sample rate | No | Event-driven CG type | No | No | No | No | Binary file — medium | **Very High** | **○ ext** (MD block custom XML) |
| **ASAM ASAP2 + XCP 🚗** | EVENT cycle time + PRESCALER | No | Event-triggered DAQ | No | No | No | No | Text/binary — medium | **Very High** | **✗** (fixed-rate / event-triggered) |
| **W3C VISSv2 🚗** | ✓ interval (ms) | ✓ interval (pmin) | ✓ minChange | ✓ minChange (step) + range | No | No | No | JSON/WebSocket — **low** | **Very High** | **~step** (minChange per-signal; closest to ε in VSS ecosystem; propose curveDeviation) |
| **IETF SenML RFC 8428** | No (ut records elapsed) | No | No | No | No | No | No | JSON/CBOR — **low** | Low-Medium | **✗** (wire format; ut field useful for compressed streams) |
| **MQTT v5 🚗** | No | No | No | No | No | No | ✓ Message Expiry | Binary — low | **Very High** | **✗** (User Properties can tag curve metadata) |
| **SAE J2735 BSM 🚗** | 10 Hz (normative) | No | Part II (event) | No | No | No | No | ASN.1/binary — high | **Very High** | **✗** (fixed rate) |
| **Apache Kafka 🚗** | No | No | No | No | No | No | ✓ log compaction / TTL | Binary/Avro — medium | **Very High** | **○ ext** (headers can tag curve metadata; log compaction retains kept points) |
| **CANopen CiA 301 🚗** | SYNC cycle (types 1-240) | ✓ Inhibit Time (pmin) + Event Timer (pmax) | ✓ Type 254/255 | No (binary change only) | No | No | No | CAN/EDS — medium | **Very High** | **~step+pmax** (strongest in-vehicle match: HYBRID+pmin+pmax; missing amplitude threshold) |
| **AUTOSAR COM 🚗** | ComTxModeTimePeriod | Partial (MIXED mode) | ✓ DIRECT/MIXED | ✓ NEW_IS_WITHIN/OUTSIDE, MASKED | No | No | No | ARXML — high | **Very High** | **~step** (NEW_IS_WITHIN = range threshold; MIXED = HYBRID mode) |
| **ETSI CAM/DENM 🚗** | 1–10 Hz (dynamic DCC) | ✓ 1 Hz floor (pmax) | ✓ kinematic triggers | ✓ named thresholds (4°, 0.5 m/s, 4 m) | No | No | No | ASN.1/binary — high | **Very High** | **~step** (named per-dimension thresholds; 1 Hz pmax floor; no interpolation model) |
| **IEEE 802.1 TSN 🚗** | Per traffic class | No | No | No | No | No | No | Ethernet frames — high | **Very High** | **✗** (network layer only) |
| **COVESA FMD 🚗** | Per-signal (VSS) | Implied | Yes | Implied | No | No | No | YAML (VSS) — **low** | **Very High** | **○ ext** (**explicitly references curve logic** — primary standardization target) |
| **AUTOSAR SOVD** | Cycle time (request) | No | Event-triggered | No | No | OAuth 2.0 | No | JSON/REST — medium | High | **✗** |
| **ISO 20078 ExVe** | No | No | Push/pull | No | No | No | No | JSON/REST — medium | Medium | **✗** |
| **ISO 26262 🚗** | DTI (diagnostic interval) | ✓ FTTI (max silence) | No | No | Safety mechanisms | No | No | Process standard | **Very High** | **✗** (motivates pmax for safety signals) |
| **Eclipse ICEORYX** | No | No | WaitSet events | No | No | No | No | Shared memory — low | High | **✗** |
| **OBD-II / SAE J1979 🚗** | On-demand only | No | No | No | No | No | No | CAN/binary — low | **Very High** | **✗** (poll-on-demand; no collection policy) |
| **AWS IoT FleetWise 🚗** | Campaign period (ms) | No | conditionLanguage | conditionLanguage expressions | No | IAM | ✓ campaign duration | JSON/REST — medium | **Very High** | **○ ext** (signal catalog extensible; conditionLanguage = sampling_condition analog) |

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

These standards have the correct two-parameter architecture (`ε analog` + `pmax analog`), differing only in that they measure deviation from the last reported value rather than from the interpolated path.

| Standard | ε analog | pmin analog | pmax analog | Granularity | Deployment scale |
|----------|----------|------------|------------|-------------|-----------------|
| **CANopen Type 254 + Inhibit + Event Timer 🚗** | — (binary change only) | Inhibit Time (per PDO) | Event Timer (per PDO) | Per-PDO | Very High — vehicles + industrial |
| **IEC 61850 deadbandMag + intgPd** | deadbandMag (per data attribute) | — | intgPd (per RCB) | Per-signal deadband, shared heartbeat | Global power grid |
| **IEC 60870-5 P_ME** | Threshold parameter (per point) | — | Transmission period (per point) | Fully per-point | Legacy utility SCADA |
| **BACnet COVIncrement** | COVIncrement (per object, REAL) | — | covLifetime (indirect) | Per-object | Global building automation |
| **DNP3 Object 34** | Per-point deadband (integer) | — | Integrity poll (master-driven) | Per-point | North American utility SCADA |
| **OPC UA DeadbandValue** | DeadbandValue (per MonitoredItem) | — | Publishing interval (subscription) | Per-item | Manufacturing, automotive |
| **AUTOSAR COM NEW_IS_WITHIN/OUTSIDE 🚗** | Value range threshold (per signal) | — | ComTxModeTimePeriod (MIXED mode) | Per-signal, compiled ARXML | Universal — all CP ECUs |
| **ETSI CAM named thresholds 🚗** | Named: 4°, 0.5 m/s, 4 m (per dimension) | — | 1 Hz floor (system-wide) | Per-signal-type | Universal — all V2X vehicles |

**New finding:** CANopen PDO Type 254 is the strongest match among production automotive standards: it natively implements HYBRID mode (on-change + periodic heartbeat) with per-PDO pmin (Inhibit Time) and pmax (Event Timer). The only missing element is an amplitude threshold — adding a `change_threshold` object alongside Inhibit Time would complete the curve logging parameter set within the existing CiA 301 framework.

### Tier 1b: Step threshold only — no native heartbeat per signal

| Standard | ε analog | What's missing |
|----------|----------|----------------|
| **OMA LwM2M st** | st (step threshold) | pmax is per-resource but shared at observation level |
| **CoAP c.st** | c.st (step threshold) | Same as LwM2M |
| **W3C VISSv2 minChange 🚗** | minChange (step threshold, per-signal subscription) | No pmax; closest to ε in the VSS ecosystem |
| **OBD-II polling (implicit)** | — | Entirely poll-driven; threshold is application-level |

**New finding:** VISSv2 `minChange` is the most automotive-relevant step threshold: per-signal, expressed in the VSS subscription API, native to the COVESA ecosystem. Adding a `curveDeviation` filter alongside `minChange` in VISSv2 is the highest-leverage near-term standards contribution.

### Tier 2: Temporal parameters only (no value deviation)

| Standard | pmin analog | pmax analog | Value deviation |
|----------|------------|------------|-----------------|
| **DDS TIME_BASED_FILTER + DEADLINE 🚗** | TIME_BASED_FILTER | DEADLINE | No |
| **oneM2M** | minimumObservableInterval | periodicNotificationDuration | No |
| **ISO 26262 FTTI 🚗** | — | FTTI-derived pmax for safety signals | No (liveness only) |

### Tier 3: Extension carriers — can hold curve logging parameters without natively defining them

| Standard | Extension mechanism | Automotive relevance |
|----------|--------------------|--------------------|
| **COVESA FMD 🚗** | VSS overlay YAML — **explicitly references curve logic** | **Very High** — primary standardization target |
| **VSS Overlays 🚗** | YAML fields in .vspec | Very High — proposed curve_epsilon, curve_algorithm fields |
| **AWS IoT FleetWise 🚗** | Signal catalog + conditionLanguage | Very High — cloud-side parameter store |
| **ASAM MDF4 🚗** | MD block (custom XML metadata) | Very High — store curve params with measurement files |
| **MQTT v5 🚗** | User Properties (per-message key-value) | Very High — tag curve-logged messages in transit |
| **Kafka headers 🚗** | Per-message headers | Very High — self-describing compressed telemetry |
| **AAS / IEC 63278** | Qualifier annotations + Submodel Templates | Medium — IDTA submodel path |
| **W3C WoT TD** | JSON-LD @context extensions | Medium — bridge to semantic web |
| **OGC SensorML 3.0** | Process description | Medium — RDP as SamplingProcedure |
| **Eclipse Kuksa 🚗** | Subscription filter implementation | Very High — reference implementation target |

### Tier 4: Path-deviation model — correct algorithm, informative or read-path only

| Standard | Path-deviation concept | Status |
|----------|----------------------|--------|
| **ISO 19141 / OGC Moving Features** | SED in trajectory compression research | Research / informative |
| **OPC UA HDA `Interpolated` aggregate** | Linear interpolation between kept points | Read path only |

### Proposed standardization path for curve logging (updated)

| Track | Action | Target body | Priority |
|-------|--------|-------------|----------|
| **Immediate** | Contribute `curve_epsilon`, `curve_algorithm`, `curve_max_interval_ms`, `curve_min_interval_ms` to COVESA VSS overlay and FMD WG | COVESA FMD WG | **Highest** |
| **Near-term** | Add `curveDeviation` filter alongside `minChange` in W3C VISSv2 subscription filter API | W3C Automotive WG / COVESA VISS | **High** |
| **Near-term** | Propose `cd` (curve deviation) attribute alongside `st` in OMA LwM2M | OMA SpecWorks | **High** |
| **Near-term** | Propose `c.cd` alongside `c.st` in IETF CoAP Conditional Attributes draft | IETF CoRE WG | High |
| **Near-term** | Extend AWS IoT FleetWise signal catalog schema with `curve_epsilon` and `curve_algorithm` fields | AWS IoT / OEM partners | High |
| **Medium-term** | Propose `change_threshold` object in CANopen CiA 301 alongside Inhibit Time for asynchronous PDO types | CAN in Automation (CiA) | Medium |
| **Medium-term** | Extend ASAM MDF4 MD block schema with standard curve logging metadata vocabulary | ASAM e.V. | Medium |
| **Medium-term** | Contribute normative trajectory simplification profile (SED + epsilon) to OGC Moving Features | OGC Moving Features SWG | Medium |
| **Medium-term** | Publish IDTA AAS Submodel Template for vehicle signal collection parameters | IDTA / COVESA joint | Medium |
| **Longer-term** | Propose `curveDev` trigger mode in IEC 61850 Report Control Blocks | IEC TC57 WG10 | Lower |
| **Longer-term** | Propose per-point curve deviation in DNP3 (new Object Group alongside Object 34) | DNP3 Technical Committee | Lower |

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
- [SOME/IP Protocol Specification — AUTOSAR FO R22-11](https://www.autosar.org/fileadmin/standards/R22-11/FO/AUTOSAR_PRS_SOMEIPServiceDiscoveryProtocol.pdf)
- [vsomeip — COVESA/GENIVI open source SOME/IP](https://github.com/COVESA/vsomeip)
- [ASAM MDF4 Specification v4.3.0](https://www.asam.net/index.php?eID=dumpFile&t=f&f=9630&token=39c75c0c8841fd89a6caa29376c9483b5ecc40d4)
- [MDF4 / MF4 explainer — CSS Electronics](https://www.csselectronics.com/pages/mf4-mdf4-measurement-data-format)
- [asammdf Python library (GitHub)](https://github.com/danielhrisca/asammdf)
- [ASAM ASAP2 / A2L explainer — CSS Electronics](https://www.csselectronics.com/pages/a2l-file-asap2-intro-xcp-on-can-bus)
- [XCP Protocol overview — CSS Electronics](https://www.csselectronics.com/pages/ccp-xcp-on-can-bus-calibration-protocol)
- [XCP Protocol — MathWorks](https://www.mathworks.com/discovery/xcp-protocol.html)
- [W3C VISSv2 Core Specification](https://www.w3.org/TR/viss2-core/)
- [COVESA vehicle-information-service-specification (GitHub)](https://github.com/COVESA/vehicle-information-service-specification)
- [COVESA vissr — VISSv2 reference server (Go)](https://github.com/COVESA/vissr)
- [RFC 8428 — SenML Sensor Measurement Lists](https://www.rfc-editor.org/rfc/rfc8428.html)
- [RFC 9100 — SenML Features and Versions](https://datatracker.ietf.org/doc/rfc9100/)
- [OASIS MQTT Version 5.0 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
- [MQTT in Connected Cars — EMQX](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles)
- [SAE J2735 BSM overview — TOME Software](https://www.tomesoftware.com/wp-content/uploads/2019/08/5-2019-B2V-Workshop-Detroit-Farid-Ahmed-Zaid-BSM-Messages.pdf)
- [Apache Kafka in automotive — Kai Waehner](https://www.kai-waehner.de/blog/2021/07/19/kafka-automotive-industry-use-cases-examples-bmw-porsche-tesla-audi-connected-cars-industrial-iot-manufacturing-customer-360-mobility-services/)
- [Rivian Kafka + Flink architecture — Confluent](https://www.confluent.io/industry-solutions/automotive/)
- [Kafka Log Compaction — Confluent Docs](https://docs.confluent.io/kafka/design/log_compaction.html)
- [CANopen PDO Protocol — CAN in Automation (CiA)](https://www.can-cia.org/can-knowledge/pdo-protocol)
- [CANopenNode — embedded open source (GitHub)](https://github.com/CANopenNode/CANopenNode)
- [AUTOSAR COM SWS R23-11](https://www.autosar.org/fileadmin/standards/R23-11/CP/AUTOSAR_CP_SWS_COM.pdf)
- [COM Filters theory and configuration — AutosarToday](https://www.autosartoday.com/posts/com_filters_-_theory_and_configuration)
- [ETSI EN 302 637-2 v1.4.1 — CAM Standard](https://www.etsi.org/deliver/etsi_en/302600_302699/30263702/01.04.01_60/en_30263702v010401p.pdf)
- [ETSI TS 102 894-2 — DENM Data Dictionary](https://www.etsi.org/deliver/etsi_ts/102800_102899/10289402/02.01.01_60/ts_10289402v020101p.pdf)
- [IEEE 802.1 TSN Task Group](https://1.ieee802.org/tsn/)
- [IEEE 802.1DG — Automotive In-Vehicle TSN Profile](https://standards.ieee.org/ieee/802.1DG/10318/)
- [COVESA Fleet Management Data overview](https://covesa.global/driving-progress-in-commercial-and-fleet-vehicle-connectivity/)
- [AUTOSAR SOVD Explanation — AUTOSAR R24-11](https://www.autosar.org/fileadmin/standards/R24-11/AP/AUTOSAR_AP_EXP_SOVD.pdf)
- [ISO 20078-2:2021 Extended Vehicle API](https://www.iso.org/standard/80184.html)
- [ISO 26262-1:2018 Automotive Functional Safety](https://www.iso.org/standard/43464.html)
- [Eclipse ICEORYX — zero-copy IPC (GitHub)](https://github.com/eclipse-iceoryx/iceoryx)
- [OBD-II PIDs — Wikipedia](https://en.wikipedia.org/wiki/OBD-II_PIDs)
- [AWS IoT FleetWise Features](https://aws.amazon.com/iot-fleetwise/features/)
- [AWS Connected Vehicle Architecture](https://docs.aws.amazon.com/architecture-diagrams/latest/aws-connected-vehicle/aws-connected-vehicle.html)
