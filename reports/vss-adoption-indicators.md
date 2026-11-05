# VSS Adoption Indicators: Where the Standard Stands in Late 2026

**Date:** November 2026
**Author:** COVESA Commercial and Fleet Vehicle Expert Group
**Audience:** OEM connected-services, fleet-data and standards leads weighing adoption of COVESA VSS and the Fleet Management Data (FMD) guidelines

> **Scope.** A condensed, decision-oriented summary of the Expert Group's full assessment, *VSS Adoption Indicators: An Evidence-Based Assessment* (data as of 1 October 2026, public sources only). Evidence grades: A = independently verifiable artifact, B = organization's own statement, C = reported but unconfirmed. One fact that changed after the snapshot is marked.

---

## Summary

In 2025 and 2026 VSS moved from a passenger-car and research vocabulary to the shared data model chosen by two large, organized OEM blocs: Europe's heavy-duty truck and bus manufacturers (through ACEA) and Japan's cross-OEM API efforts (JASPAR and the Open SDV Initiative). The complete ACEA FMS version 5 signal set is now in the core VSS tree, Adaptive AUTOSAR specifies its vehicle API gateway on the companion access standard VISS, and the main open-source vehicle software stacks (Eclipse Kuksa, Eclipse SDV blueprints, Automotive Grade Linux) are VSS-native. The weak spots: few independently verifiable production deployments, the best-known managed cloud service (AWS IoT FleetWise) closed to new customers in April 2026, Eclipse S-CORE shows no public VSS reference, and no Chinese OEM engagement has been located. Overall: **strong and rising specification- and consortium-level adoption, moderate edge implementation, thin public production proof.** The question is no longer whether a common model exists but whether the parties holding the data have decided to use it, and the two blocs most relevant to fleet data have.

## Related resources

- Full assessment: [VSS Adoption Indicators: An Evidence-Based Assessment](https://docs.google.com/document/d/1bo7h0PmPICCAMTaI3Tq7GOIdf7IBmeYKIjPfqjypsyk) (Google Doc; method, repository statistics, sources)
- [COVESA Vehicle Signal Specification repository](https://github.com/COVESA/vehicle_signal_specification)
- [Fleet Management Data guidelines spreadsheet](https://docs.google.com/spreadsheets/d/1FMtSLhJy1REgadlnSwAqPX7r57rqdLYyw4W7ZsWyg8E)
- [COVESA Commercial Vehicle BoF overview deck](https://docs.google.com/presentation/d/1zLbYQEsAZ2ULSroFDKla5FGYbS_25X5lKCUzDcCH6AM) (why fleets need standardized OEM data, pillars, use case to signal to sampling chain)
- [Commercial Vehicle Overview, COVESA Spring AMM 2024](https://docs.google.com/presentation/d/12t8N8QbB2E-CtRSHJ8uq3xFoquRqdOJSfm4KgYOy7Tg) (same core plus OEM and fleet testimonials)
- [FMD guidelines business case](fmd-guidelines-business-case.md)
- [Curve logging efficiency](curve-logging-efficiency.md)

---

## 1. Vehicle manufacturers

| Bloc or OEM | Evidence | Date | Grade |
|---|---|---|---|
| ACEA heavy-duty truck and bus OEMs (DAF, Daimler Truck, Ford, IVECO, TRATON with Scania and MAN, Volvo, Renault Trucks) | MoU with COVESA to extend VSS and build on VISS | 29 Jul 2025 | A |
| | FMS version 5 signal set (4,389 lines) merged into the ACEA-maintained `acea-namespace` branch (PR #928, TRATON author) | 3 Sep 2026 | A |
| | PR #932 integrating FMS version 5 into the core VSS `master` tree, from the ACEA onboard API working group | Merged 7 Oct 2026 (after the snapshot; verified on GitHub). Not yet in a release | A |
| | ACEA filing requirements into VISS as candidate onboard API (issue #138); VISS v3.1 added truck and trailer trees | Apr to Aug 2026 | A |
| JASPAR (led by Toyota, Honda, Nissan) | Collaboration announced at COVESA Porto meeting; MoU on standardized APIs built on VSS and VISS | Apr and 18 Jun 2026 | A (MoU) |
| | Yoriito open-source project: reports 1,000+ APIs and 370,000 lines of member code; includes Kura, a Rust VISS 3.0 server | Apr 2026 | B |
| Open SDV Initiative (Japan, about 60 companies) | Body APIs based on VSS; specification releases every six months since Mar 2025 | 2025 to 2026 | B |
| BMW | Neue Klasse described by the COVESA chair as built heavily around VSS-modeled data; BMW VSS-for-VHAL repositories in the COVESA organization | Mar to Sep 2026 | B / A |
| UD Trucks | Four merged VSS pull requests (road surface signals): a Japanese heavy-duty OEM contributing directly | May to Aug 2026 | A |
| Volvo Cars, Jaguar Land Rover, Ford | Historic core contributors; Ford edits VISS; JLR has no merged changes since 2025 | 2016 to 2026 | A |

Not confirmed: BMW's customer-facing CarData API does not reference VSS, so no published OEM VSS cloud product exists in public documentation (C).

## 2. Suppliers

Bosch is the largest contributor to the core repository (about 215 commits; roughly half of pull requests merged since 2025) and maintains Eclipse Kuksa. Renesas, Samsung, ETAS, BlackBerry, Harman, Hyundai Mobis and Korea's ETRI and ivis also contribute, the Korean share growing in 2025 and 2026 (A). Sonatus and RemotiveLabs publish material on translating OEM signals to VSS in production programs (B). The VISS explainer lists Volvo, BMW, JLR, Renesas, Bosch, Visteon, AGL and Mitsubishi Electric as implementers (B). The concentration cuts both ways: three organizations (Bosch, BMW, JLR) account for about two thirds of all commits.

## 3. Open source and tooling

| Project | Status at 1 Oct 2026 | Grade |
|---|---|---|
| Eclipse Kuksa databroker | Active VSS-native signal broker | A |
| Eclipse SDV fleet-management blueprint; Velocitas; digital.auto playground | Maps FMS to VSS over VISS; VSS-native developer tooling | A |
| Automotive Grade Linux | VSS via Kuksa; SoDeV reference platform (May 2026) | B |
| Android Automotive VHAL | VSS signal names extending VHAL, showcased Apr 2026 | A |
| Eclipse S-CORE | No VSS reference in public repositories | C |

Core repository: 446 stars, 64 all-time contributors; releases v5.0 (Oct 2024), v5.1 (Jul 2025), v6.0 (Jan 2026), v6.1 (17 Sep 2026, still the latest). Merged pull requests fell from 86 (2023) to 31 (2025), then recovered to 36 by October 2026 on sector contributions. v6.1 added QUDT unit references and integer enums, the marks of a specification being hardened for machine consumption.

## 4. Standards bodies and regulation

- **AUTOSAR.** Adaptive R24-11 (Dec 2024) specifies an Automotive API Gateway on VISS v2 with a technical report on VSS representation, carried forward in R25-11 (Nov 2025). No public deployment evidence (A for the spec).
- **VISS.** v3.1 (Apr 2026) and v3.2 (Sep 2026) released under COVESA stewardship, which took over from W3C in 2024.
- **EU Data Act.** Applying since 12 Sep 2025, it creates a right to in-scope vehicle data but mandates no format; the sector-specific in-vehicle data law was shelved in 2025. VSS is the obvious candidate format, but nothing compels it, so adoption remains voluntary and bloc-by-bloc.
- **Vehicle credentials.** The vocabulary moved into COVESA in June 2026 and is live in the California DMV Wallet; proof-of-insurance and inspection credentials, which would carry VSS signal paths, are in design (A/B).

## 5. Fleet, aftermarket and cloud

| Indicator | Evidence | Grade |
|---|---|---|
| Fleet platforms shaping the spec | Cox Automotive engineer opened VSS issue #936 on heavy-duty (J1939) fault codes, Aug 2026; Geotab contributed SENSORIS-derived road-condition signals | A |
| COVESA Fall 2026 meeting, Novi, 28 to 29 Oct | Themed "Integrating Vehicle Data in Fleets, Commercial Vehicles, and Adjacent Industries" | A |
| COVESA Fall 2025 meeting | 107 organizations, 10 OEMs, 11 Tier 1s, 45 non-members | B |
| AWS IoT FleetWise | Imports VSS-format catalogs; closed to new customers 30 Apr 2026; edge agent still released (Jun 2026) | A |
| RemotiveCloud, Sonatus | Self-reported production use | B |

The FleetWise closure is a contracting managed option, not evidence against VSS: VSS-format catalogs remain portable and AWS still documents VSS support.

## 6. Headwinds

Thin independently verified production proof; hyperscaler retreat with no OEM VSS cloud service yet to replace it; demand-side lag at AUTOSAR; S-CORE alignment unproven; Japanese code volume not visible publicly; maintainer concentration; no located Chinese participation.

## What this means for a fleet-data decision

For an OEM selling into mixed-brand fleets, the decisive fact is that the two groups a fleet platform must integrate with anyway, European heavy-duty OEMs and the Japanese OEM consortia, have chosen VSS as their signal vocabulary and VISS as their candidate access interface, and have put the artifacts in public repositories. FMS version 5 is in the core VSS tree and will ship in the next release. Adopting VSS means one mapping reused by fleets, insurers, inspection programs and credential issuers instead of a proprietary schema each partner must translate. The FMD guidelines add the data-quality conventions (sampling, timestamps, derived events) that the standard leaves open and that remain the most visible gap in cross-OEM data today. The risks are real but bounded: they concern proof of production use and cloud tooling, not the stability or direction of the specification. Watch for a VSS release containing FMS version 5, publication of the ACEA onboard API profile on VISS, outcomes of the October Novi meeting, and any OEM publishing a VSS-based cloud data service.
