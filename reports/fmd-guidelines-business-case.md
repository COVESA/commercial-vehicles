# The Business Case for the COVESA Fleet Management Data Guidelines

**Date:** November 2026 (revision of a December 2025 draft)
**Author:** COVESA Commercial and Fleet Vehicle Expert Group
**Audience:** OEM connected-services, data platform and standards leads; fleet operators; telematics service providers (TSPs); cloud and Tier-1 partners

## Summary

Commercial fleets run on vehicle data, and the source of that data is moving from aftermarket devices to OEM clouds. Every OEM cloud exposes a different signal set, sampled differently and described in a proprietary model, so each fleet platform repeats the same bespoke integration per manufacturer and most mid-sized fleets are never served at all. The COVESA Fleet Management Data (FMD) guidelines fix the smallest part of that problem that unlocks the rest: a use-case-driven list of about 100 data points, each tied to a VSS 6.1 signal and a recommended sampling rule. For OEMs it is a ready-made product definition for a fleet data offering that any TSP can consume once; for fleets and TSPs it is one integration instead of twenty. Since the original case was written, VSS 6.1 has shipped, the ACEA heavy-duty FMS v5 signals have landed in VSS master, the FMD spreadsheet has been remapped to VSS 6.1, and OEMs are evaluating adoption. The recommendation is to package FMD as a formal COVESA specification and recruit two or three OEM reference implementations.

## Related resources

- Original source: [The Strategic Imperative for OEM Adoption of COVESA Fleet Management Data Recommendations](https://docs.google.com/document/d/1IxZuImhUrDXxoRFCukLlkybLQYlpafrkXjCm9GRahRg/edit) (draft, December 2025) and the underlying [OEM-enabled Fleet Management Data Recommendations \[PUBLIC\]](https://docs.google.com/document/d/1VM66MOVdDIRuOGBXi8G9GgLITAPwARvXWYCfqdVQ-s4/edit) (v1.1, May 2023)
- [FMD spreadsheet: Pillar -> Use Case -> Data Needs](https://docs.google.com/spreadsheets/d/1FMtSLhJy1REgadlnSwAqPX7r57rqdLYyw4W7ZsWyg8E/edit?gid=2020824572#gid=2020824572) (VSS 6.1 mapping, November 2026)
- [COVESA Commercial Vehicles repository](https://github.com/COVESA/commercial-vehicles) and [reports](https://github.com/COVESA/commercial-vehicles/tree/main/reports)
- [COVESA Vehicle Signal Specification](https://github.com/COVESA/vehicle_signal_specification) ([v6.1 release](https://github.com/COVESA/vehicle_signal_specification/releases/tag/v6.1), [ACEA FMS v5 PR #932](https://github.com/COVESA/vehicle_signal_specification/pull/932))
- [Eclipse SDV Fleet Management Blueprint](https://github.com/eclipse-sdv-blueprints/fleet-management) and [Geotab curve logging algorithm](https://github.com/Geotab/curve) (MPL-2.0)
- [COVESA Commercial Vehicle BoF overview deck](https://docs.google.com/presentation/d/1zLbYQEsAZ2ULSroFDKla5FGYbS_25X5lKCUzDcCH6AM) (why fleets need standardized OEM data, pillars, use case to signal to sampling chain)
- [Commercial Vehicle Overview, COVESA Spring AMM 2024](https://docs.google.com/presentation/d/12t8N8QbB2E-CtRSHJ8uq3xFoquRqdOJSfm4KgYOy7Tg) (same core plus OEM and fleet testimonials)
- [VSS adoption indicators](vss-adoption-indicators.md)
- [Curve logging efficiency](curve-logging-efficiency.md)

## 1. Problem: fragmented OEM data access for fleets

Fleets are mixed by nature: a utility, a last-mile carrier or a rental company runs several makes and classes and buys on total cost of operation across all of them. For twenty years they got uniform data from aftermarket telematics devices. OEMs now want that data to come from their own clouds, which is the right direction, but the offerings differ in which signals exist, how often they are sampled, what names and units they use, and how access is activated.

| Symptom | Consequence |
|---|---|
| Each OEM has its own data model and API | Every TSP builds and maintains *n* integrations; the industry pays n x m |
| Signal sets chosen by the OEM, not by fleet use cases | Odometer, fuel, battery and fault data are often missing or coarser than the device they replace |
| Fixed-interval sampling at arbitrary rates | Too much data (cost) or too little (missed events, wrong analytics) |
| Integration cost is the same for 50 vehicles as for 50,000 | TSPs prioritize OEMs by market share; smaller OEMs and mid-sized fleets wait indefinitely |

Fleet platforms and insurers describe OEM-specific integrations as complex, heterogeneous and multi-year. The lack of a standard is one of the top-cited threats to growth of the commercial telematics market.

## 2. What FMD is

FMD began as Geotab's documented experience of what fleets actually consume, brought to the COVESA Commercial Vehicle Birds of a Feather in 2023 and now maintained by the Commercial and Fleet Vehicle Expert Group. It is organized as a chain:

**Pillar -> use case -> data point -> VSS signal -> sampling rule -> importance**

| Element | Content (November 2026) |
|---|---|
| Pillars | Productivity; Efficiency / Optimization / Maintenance; Safety; Sustainability (ICE, EV, FCEV); Compliance |
| Use cases | 52, from asset tracking and idling to predictive battery health, DPF status, EV charging and hours of service |
| Data points | 98 rows: 72 "Must Have", 26 "Should Have" |
| VSS mapping | Nearly every row names a VSS 6.1 path; the few gaps (hydrogen level and consumption, idle energy, DPF regeneration) carry a proposed path for upstreaming |
| Sampling | Per row: fixed interval (1 Hz down to one heartbeat per 24 h), on-change, event-triggered (a 100 Hz burst for five seconds after `Vehicle.LowVoltageSystemState='START'` for cranking analysis), or curve logging with a stated error threshold |
| Cross-references | SAE J1939 PGN/SPN where applicable, so heavy-duty OEMs can map from existing CAN definitions |

Two design choices matter for adoption. VSS is strongly recommended but not a precondition: an OEM can deliver the right data points at the right cadence in its existing model and migrate naming later. And sampling is stated per use case, so an OEM can meet fleet needs with far less data than a naive high-rate feed. Curve logging (Ramer-Douglas-Peucker based, released by Geotab under MPL-2.0 and since open-sourced in Bosch and ETAS implementations) is preferred; fixed-rate fallbacks are given for every signal.

## 3. Value for OEMs

- **A product definition, not a research project.** FMD answers which signals, how often, and for whom; the use-case column is the justification for each signal.
- **One offering every fleet platform can consume.** TSPs integrate once and onboard the OEM's vehicles for all their customers, including mid-sized fleets that bespoke integrations never pay back.
- **Lower transport and storage cost.** Sampling with purpose moves fewer bytes while preserving the events fleets care about.
- **Procurement advantage.** Fleets increasingly write data access into RFPs. A vehicle whose OEM cloud meets FMD can be sold on that basis.
- **Alignment with heavy-duty peers.** ACEA truck and bus makers (DAF, Daimler Truck, Ford, IVECO, Traton, Volvo Group, Renault Trucks) chose VSS as the home for FMS v5. A car or van OEM adopting FMD lands in the model fleets already see from their trucks.
- **Regulatory readiness.** The EU Data Act obliges sharing connected-vehicle data with users and their chosen third parties; a standard signal set with documented purpose and sampling is the cheapest way to comply.

## 4. Value for fleets and TSPs

- One integration per data model rather than per OEM; faster onboarding of new makes.
- Comparable data across makes, so safety scoring, maintenance prediction and sustainability reporting work fleet-wide.
- A procurement checklist: "Must Have" rows become acceptance criteria for OEM data subscriptions and vehicle purchases.
- A path off the aftermarket device where the OEM feed is equivalent, and a clear statement of where it is not yet.

## 5. Costs and risks

| Item | Assessment |
|---|---|
| OEM engineering | Mapping existing cloud signals to about 100 VSS paths and adjusting sampling; small relative to a cloud platform program |
| COVESA participation | One or two engineers in Expert Group calls; membership for non-members |
| Dilution | OEMs implement "most of" FMD and interoperability is lost. Mitigation: per-row conformance statements and a public list of implementations |
| Data pricing | Some OEMs price data to recover platform cost, suppressing demand. FMD lowers delivery cost and defines the minimum viable product; pricing stays with the OEM |
| Consent and privacy | Per-signal use-case tagging is a foundation for consent, not a solution; 2026 enforcement actions in North America show the cost of getting it wrong |
| Spreadsheet as source of truth | Easy to contribute to, hard to version. The repository's `tmp/convert-spreadsheet` tooling already generates VSS overlay YAML; the group has committed to publishing FMD as YAML / JSON Schema |

## 6. What has changed since the original

The December 2025 draft argued from market size and insurance economics. Its headline figures (a USD 150 billion telematics market by 2028, a EUR 15 billion European usage-based-insurance market by 2030, 8-15% insurance commissions, 3-5x return on standards participation) were quoted without citations and are not restated here; treat them as "as of the December 2025 draft, unverified". What can be verified now is more useful:

| Then (Dec 2025) | Now (Nov 2026) |
|---|---|
| FMD mapped to VSS 4.x | Remapped to VSS 6.1 (released 17 Sep 2026), adopting new 6.x signals such as `Vehicle.Powertrain.AccumulatedBrakingEnergy` and ADAS following-distance paths |
| ACEA FMS v5 on a namespace branch | Merged into VSS master on 7 Oct 2026 (PR #932); not in 6.1, expected in the next release. The Eclipse SDV Fleet Blueprint opened an issue on 4 Nov 2026 to adopt the official names |
| CV BoF, informal | Expert Group with a public repository (19 published reports), co-chaired by Geotab and Bosch, with Ford leading the CVIS truck and trailer trees |
| No implementations claimed | Reported at the Fall 2026 AMM: a North American heavy-duty OEM cloud offering aligned to FMD, a European passenger OEM feed for a traffic agency, the Bosch Eclipse SDV Fleet Blueprint, a European OEM offering VSS data to third parties; further OEMs evaluating adoption as of November 2026 |
| Fleet data only | Companion insurance signal campaign, predictive maintenance guidelines (with Karmak and Cox Automotive), and Verifiable Vehicle Credentials supplying ownership, insurance and inspection context to the data |
| Membership pitch | Volvo Group joined; Enterprise applying; Cummins, Samsara, Karmak, Cox Automotive and Allison Transmission advancing |

The original's weakest claims, that fleet platforms were already certifying "FMD-compatible" OEMs and insurers writing FMD into procurement, were aspirational in 2025 and remain so. The validation program in the 2023 recommendations (a public listing of vehicles whose OEM data meets fleet requirements) has not been built and is still the most persuasive artifact the group could produce.

## 7. Recommendation

1. **Publish FMD as a formal COVESA specification** in 2027: YAML overlay plus JSON Schema generated from the spreadsheet, versioned against VSS releases, with the spreadsheet kept only as a contribution front end.
2. **Upstream the remaining gaps to VSS** (hydrogen, idle energy, DPF regeneration, heartbeat) so the next version needs no proposals column.
3. **Recruit two or three OEM reference implementations**, ideally a car or van OEM alongside the heavy-duty FMS work, with conformance documented per row.
4. **Stand up the validation listing** described in 2023, operated under COVESA rather than any one TSP.
5. **Keep the OEM pitch concrete**: lower delivery cost, a reusable product definition, and access to the fleet channel through every TSP at once. The market-size arguments of the earlier draft should not be repeated without sources.
