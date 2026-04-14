# SENSORIS & HERE Technologies — Deployment Analysis
**Date:** 2026-04-13

---

## SENSORIS Overview

**SENSORIS** (Sensor Interface Specification) is a vehicle-to-cloud data standard coordinated by ERTICO–ITS Europe, initiated by HERE Technologies in 2015. It defines how in-vehicle sensor/probe data is transmitted to the cloud and exchanged between clouds — primarily to enable near-real-time HD map updates for ADAS and autonomous driving.

- Spec history: v1.0 (2018), v1.1 (request messages / cloud→vehicle), v1.2.0 (latest)
- Standard body: ERTICO–ITS Europe (coordinator), hosted at sensoris.org
- Protobuf-based wire format; open specification

---

## SENSORIS Members (as of 2026-04-13)

| Category | Members |
|---|---|
| Coordinator | ERTICO–ITS Europe |
| Vehicle Manufacturers (active) | CARIAD (VW Group software), Toyota Motor Europe |
| Vehicle Manufacturers (in transition) | Renault, Nissan Motor |
| ADAS Manufacturers | Robert Bosch, Mitsubishi Electric, AISIN, Huawei |
| Tier 1 Suppliers (in transition) | Valeo Comfort & Driving Assistance, ZF |
| Location / Map Providers | HERE Global B.V., TomTom, Tencent, Hyundai Mnsoft, MXNAVI |
| Telecom / Cloud | (none currently listed) |
| Other | CTAG |

**Note:** Renault, Nissan, Valeo, and ZF listed as "in transition" — likely reducing involvement.

---

## SENSORIS Production Deployment — Assessment

SENSORIS is a **backend data pipeline standard**, not a consumer-facing feature. OEMs do not advertise it; it appears in the telematics/ADAS map-update stack.

| Deployment | Status | Notes |
|---|---|---|
| HERE HD Live Map (Mercedes DRIVE PILOT) | **Production** (2021) | SAE L3, Germany |
| HERE HD Live Map (BMW Personal Pilot) | **Production** (2023) | SAE L3 |
| CARIAD / VW Group probe data | **Implied** | CARIAD is active SENSORIS member |
| Toyota Motor Europe probe data | **Implied** | Active member, no specific model announced |
| Ko-HAF project (Germany) | Research/validation (2018) | First stated real-world SENSORIS use |

**Competition:** Mobileye (proprietary REM), Google Maps/Waze, and internal OEM data platforms limit broader adoption. Membership roster shrinkage suggests slower-than-hoped industry uptake.

---

## HERE Technologies — OEM Customers

### Shareholders (deeply committed)
- **BMW Group** — co-owner since 2015 Nokia acquisition (~15% stake)
- **Mercedes-Benz Group** — co-owner (~15%)
- **Volkswagen Group / Audi** — co-owner (~15%); CARIAD is active SENSORIS member
- **Continental AG** — 5% stake (2018)
- **Mitsubishi Corporation** — 30% stake via COCO Tech Holding (2019)

### Active OEM Customers (embedded navigation / HD maps)
| OEM | Integration |
|---|---|
| BMW | HD Live Map (Personal Pilot L3), head units |
| Mercedes-Benz | HD Live Map (DRIVE PILOT L3), head units |
| Audi / VW | Head units, ADAS maps via CARIAD |
| Toyota | Head unit maps |
| Hyundai | Maps via Hyundai Mnsoft subsidiary |
| Volvo | MapCare (live map updates, since 2009) |
| Ford | Connected services / MyFord Mobile |
| Jaguar Land Rover | HERE Auto (2016+ XF, XJ) |
| Mazda | Head unit maps |
| Sony Honda Mobility (AFEELA) | HERE Navigation SDK |
| Dacia, Lotus, VinFast, Togg | HERE Navigation |
| ~80% of Chinese OEM export volume | Per HERE CES 2025 announcement |

### Scale
- HERE ADAS solutions in **44M+ vehicles** (2024)
- Historically: "4 out of 5 cars with fully integrated in-dash navigation used HERE data" (2013)
- Ranked #1 in Omdia's 2024 Location Platform Index

---

## Relationship Between HERE and SENSORIS

HERE **initiated** SENSORIS and remains its primary map-update beneficiary. Any vehicle sending probe data to HERE is effectively a SENSORIS deployment candidate. Given HERE's penetration across BMW, Mercedes, VW, Toyota, Hyundai, and others, actual SENSORIS data flows likely touch **tens of millions of vehicles** — but as invisible infrastructure, with no OEM publicly confirming it.

---

## Sources

- [SENSORIS Members](https://sensoris.org/members/)
- [SENSORIS Ko-HAF project](https://sensoris.org/automotive-industry-to-use-sensoris-vehicle-to-cloud-data-standard-with-ko-haf-project/)
- [NDS Association on SENSORIS](https://nds-association.org/sensoris/)
- [Mercedes-Benz deploys HERE HD Live Map for DRIVE PILOT](https://www.globenewswire.com/en/news-release/2021/09/06/2291764/0/en/Mercedes-Benz-deploys-HERE-HD-Live-Map-for-DRIVE-PILOT-system.html)
- [HERE CES 2025 announcement](https://www.here.com/about/press-releases/here-technologies-brings-ai-powered-mapping-and-software-defined-vehicle)
- [HERE Technologies — Wikipedia](https://en.wikipedia.org/wiki/Here_Technologies)
- [HERE Wins Awards — Just Auto (2025)](https://www.just-auto.com/featured-company/2025-here-technologies/)
- [HERE HD Live Map for BMW and Daimler (2018)](https://www.greencarcongress.com/2018/02/20180221-here.html)
