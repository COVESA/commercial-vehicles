# Vehicle Inspection Credential: Required Data Points

**Jurisdictions covered:** United States, Canada, European Union, Japan, South Korea, China, India  
**Last updated:** 2026-10-27 (section 14 on automated vehicles added; 2026-09-21 fact-checked revision of the 2026-07-23 draft — see Revision Notes at end)  
**Related work:** [Connected Vehicle FNOL via Verifiable Credentials](connected-vehicle-fnol-vc-standards.md) and the POI/FNOL credential sketches in `tmp/poi-credential/` — W3C VC Data Model 2.0 and the [COVESA Vehicle Credentials Vocabulary](`https://w3id.org/vvc`); [Digital Wallet for the COVESA AOSP Platform](aosp-vc-wallet-use-cases-standards.md); [Insuring Autonomous Vehicles: Data Requirements](COVESA_Whitepaper_Insuring_Autonomous_Vehicles_Data_Requirements.md) (companion for the automated-vehicle material in section 14)

---

## Overview

A **vehicle inspection credential** (analogous to the Proof of Insurance credential in the COVESA Vehicle Credentials Vocabulary) would represent the outcome of a legally mandated roadworthiness, safety, or emissions inspection. This document catalogs:

1. **Inspection types** required per jurisdiction (safety, emissions, combined roadworthiness)
2. **Data fields** on the standard inspection certificate or pass document
3. **Inspection frequency / intervals**
4. **Cross-jurisdictional comparison** of common data points

The goal is to identify the canonical data set for a `VehicleInspectionCredential` that could be:
- Issued by an authorized inspection station (the issuer DID)
- Held by the vehicle owner (wallet / telematics system)
- Presented to law enforcement, registration authorities, or border agents
- Referenced by the `VehicleRegistrationCredential` or a future `VehicleComplianceCredential`

Sections 1 to 13 address vehicles with a human driver. Section 14 extends the credential to automated vehicles (SAE Level 3 and above), where regulators additionally require approval of the automated driving system, verification of its software identity and sensor state at inspection, and continuous in-service monitoring and reporting by the manufacturer or operator; the regimes surveyed there (UN R157/R156/GTR 26, EU 2022/1426, Germany's AFGBV, the UK Automated Vehicles Act, NHTSA's Standing General Order, California's 2026 regulations, CVSA's Enhanced CMV Inspection, Japan, China, Korea) are mapped to credential fields and VSS signals in 14.3.

---

## 1. United States

### 1.1 Inspection Landscape

The US has no federal vehicle inspection mandate for light vehicles. Programs are entirely state-run and fall into two families, and the safety-inspection family is shrinking: Texas ended non-commercial safety inspection on 1 January 2025, New Hampshire's program ended in early 2026 (litigation ongoing), and Louisiana's repeal takes effect 1 January 2027.

| Type | Description | States with mandate (Sept 2026) |
|------|-------------|-------------------|
| **Periodic safety inspection** | Brakes, lights, tires, steering, windshield, emissions equipment | Annual: HI, ME, MA, NY, NC, PA, VT, VA. Biennial: RI, DE, WV, MO (vehicles >10 years or ≥150,000 mi only). Sunsetting: NH (2026), LA (2027). |
| **OBD / emissions inspection (I/M)** | On-board diagnostics readiness check (OBD-II port scan), often metro-area only | 27 states + DC: AZ, CA, CO, CT, DE, GA, IL, IN, LA, ME, MD, MA, MO, NV, NJ, NM, NY, NC, OH, OR, PA, RI, TX, UT, VT, VA, WI, DC |
| **Combined safety + emissions** | Single station performs both | NY, PA, NC, MA, VT, VA (NoVA), RI |

States with **no** periodic safety or emissions inspection of private vehicles: AK, AL, AR, FL, IA, ID, KS, KY, MI, MN, MS, MT, ND, NE, OK, SC, SD, TN (emissions ended 2022), WA (emissions ended 2020), WY. Several states have emissions programs but no safety inspection (AZ, CO, OR, WI, UT, MD, TX, NJ, DC).

### 1.2 Standard Inspection Certificate / Sticker Data Fields

Fields that appear on state inspection certificates and OBD-II inspection reports:

| Field | Description | Notes |
|-------|-------------|-------|
| **Vehicle Identification Number (VIN)** | 17-character VIN | Present on all state programs |
| **License plate number** | State registration plate | Required |
| **Vehicle year / make / model** | Basic vehicle description | Required |
| **Odometer reading** | Mileage at time of inspection | Required in most states; used to detect rollback |
| **Inspection date** | Date test was performed | Required |
| **Certificate expiration date** | Date by which next inspection is due | Required (typically 1 year; VA safety = 1 year, VA emissions = 2 years) |
| **Inspection station identifier** | State-assigned station number / name | Required |
| **Inspector / technician ID** | State-licensed inspector number | Required |
| **Overall result** | PASS / FAIL / CONDITIONAL PASS | Required |
| **Items inspected** | Checklist of safety/emissions components tested | Required (varies by state program) |
| **Failure reasons** | Specific item(s) that caused a failure | Required on failures |
| **OBD-II readiness monitors** | Pass/Fail per monitor (e.g., catalyst, O2 sensor, EVAP) | Emissions programs |
| **OBD-II DTC codes** | Diagnostic Trouble Codes triggering failure | Emissions programs |
| **Re-inspection eligibility date** | Earliest date for free or discounted retest | Some states |
| **Repair cost waiver threshold** | Dollar limit triggering emissions waiver | Some states (e.g., CA, NY) |
| **Certificate / sticker number** | Unique document identifier | Required (anti-counterfeiting) |

### 1.3 Inspection Frequency by State (Selected)

| State | Safety | Emissions | Interval | Notes |
|-------|--------|-----------|----------|-------|
| **California** | No | Yes (Smog Check) | Every 2 years | On registration renewal; gasoline/hybrid vehicles ≤8 model years pay a smog abatement fee instead; EVs and diesel MY1997 and older exempt |
| **New York** | Yes | Yes (OBD) | Annual | Both combined at inspection station |
| **Texas** | No (ended 1 Jan 2025; $7.50 replacement fee) | Yes (OBD, 17 counties; Bexar added Nov 2026) | Annual | Commercial vehicles still safety-inspected |
| **Pennsylvania** | Yes | Yes (OBD in 25 counties) | Annual | |
| **New Jersey** | No (ended 2010) | Yes (OBD) | Every 2 years; new vehicles exempt 5 years | |
| **Virginia** | Yes | Yes (Northern Virginia, 10 localities) | Safety annual; emissions every 2 years | |
| **Maryland** | At titling only | Yes (VEIP) | Every 2 years | |
| **Illinois** | No | Yes (OBD — Chicago and Metro-East) | Every 2 years | |
| **Colorado** | No | Yes (OBD — 9 Front Range counties) | Every 2 years | 7 newest model years exempt |
| **Massachusetts** | Yes | Yes (OBD) | Annual | |
| **Maine** | Yes | Yes (Cumberland County OBD) | Annual | |
| **New Hampshire** | Repealed 2026 (HB 649) | No | — | First Circuit stayed injunction Apr 2026; treat as ended |
| **Rhode Island** | Yes | Yes (OBD) | Every 2 years | |
| **District of Columbia** | No (ended 2009) | Yes (OBD) | Every 2 years | |
| **Hawaii** | Yes | No | Annual; new vehicles 2 years | Safety only |
| **Missouri** | Yes (vehicles >10 yrs or ≥150k mi) | Yes (St. Louis area only) | Every 2 years | No Kansas City program |
| **North Carolina** | Yes | Yes (OBD — 19 counties) | Annual | Further counties pending EPA removal |
| **Georgia** | No | Yes (OBD — 13 Atlanta metro counties) | Annual | |
| **Vermont** | Yes | Yes (OBD) | Annual | |
| **Wisconsin** | No | Yes (7 SE counties) | Every 2 years | |
| **Louisiana** | Yes until 1 Jan 2027 (HB 1085) | Yes (5 Baton Rouge parishes) | Annual | Safety no longer enforced from 30 Jun 2026 |

### 1.4 Why States Are Ending Safety Inspection

The public record on repeals is consistent. The stated drivers are the cost and inconvenience to motorists, a "personal responsibility" framing, claims that the programs are gamed (upselling by stations, stickers sold without inspection), and the absence of clear crash-rate evidence. Direct state budget savings was the primary rationale only in New Jersey's 2010 repeal, and the two most recent repeals kept the revenue: Texas replaced the safety sticker with a $7.50 ["inspection program replacement fee"](https://capitol.texas.gov/tlodocs/88R/analysis/html/HB03297H.htm) and Louisiana with a [$6 registration QR code](https://www.legis.la.gov/Legis/ViewDocument.aspx?d=1475467).

The language is blunt. Texas HB 3297's author, Rep. Cody Harris, called inspections ["a waste of time for Texas citizens and a money-making Ponzi scheme used by some shady dealerships to upsell consumers with unnecessary repairs"](https://www.keranews.org/politics/2023-06-01/cars-registered-in-texas-after-2025-will-no-longer-need-to-pass-a-safety-inspection); the bill analysis noted that most states dropped inspection after the federal mandate lapsed in 1976 and that the safety "impact no longer justifies its existence." Utah's sponsor called the program ["a feel-good effort that yields little to no verifiable results"](https://www.deseret.com/2017/3/9/20607904/lawmakers-remove-requirement-for-vehicle-safety-inspections), with a fiscal note returning about $25M a year to motorists. New Hampshire's House leadership framed the 2025 repeal as relief for ["everyday drivers stuck with an outdated, costly requirement"](https://www.nhpr.org/nh-news/2025-12-22/vehicle-inspections-car-new-hampshire-nh-ending); New Jersey's MVC said that with only about 6% of 1.9 million inspections failing for serious defects, ["with a lack of conclusive data, and the current fiscal crisis, we cannot justify this expense"](https://www.automotive-fleet.com/news/new-jersey-changes-vehicle-inspection-requirements) (savings put at $11–17M a year). Mississippi's 2015 repeal turned on the $5 sticker being ["no longer used in a uniform way"](https://meridianstar.com/2015/04/15/inspection-sticker-law-still-in-effect-for-now/) and unenforceable.

The evidence base cited on both sides is thin. [GAO-15-705](https://www.gao.gov/products/gao-15-705) (2015) found vehicle component failure in roughly 2–7% of crashes and could not establish a clear effect of inspection programs on crash rates; New Jersey and Oklahoma showed no significant change after repeal, and economists (Merrell, Poitras & Sutter 1999; Poitras & Sutter 2002; [Hoagland & Woolley 2018](https://doi.org/10.1111/coep.12284) on New Jersey) found no effect on fatalities. On the other side, [Peck et al. (Carnegie Mellon, 2015)](https://www.cmu.edu/news/stories/archives/2015/july/vehicle-safety-inspections.html) put Pennsylvania's true failure rate at 12–18% rather than the 2% used in repeal debates, and later CMU/Imperial work cited by the [Auto Care Association](https://www.autocare.org/docs/default-source/government-affairs/safety_im_jan-2022.pdf) estimates several percent fewer fatalities per registered vehicle in inspection states; a 2017 Texas legislative study finding defective vehicles roughly three times more likely in fatal crashes was raised — unsuccessfully — against HB 3297. Opposition to repeal has come from inspection-station and repair trade associations, law-enforcement bodies and, in New Hampshire, the emissions contractor whose Clean Air Act suit produced an injunction and a 2026 rewrite that replaced periodic inspection with an owner duty to maintain plus roadside checks.

**Where insurers stand.** Strikingly, the insurance industry has been almost absent from these debates. Press coverage of the Texas, New Hampshire and Virginia repeals quotes legislators, mechanics, inspection-station associations and emissions-equipment vendors, but no insurer, and GAO's 2015 review lists state officials, NHTSA, safety groups and automotive industry groups as its stakeholders — no insurers or insurer-funded researchers. No IIHS/HLDI, Insurance Research Council, Triple-I, NAMIC or APCIA publication on periodic inspection programs could be located, and the insurer-funded German accident research unit (UDV) lists none either; the defect-rate figures in the EU's own [2012 roadworthiness impact assessment](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52012SC0206) come from DEKRA and Monash University, not insurers, and the [inspection industry's own compilation of PTI studies](https://citainsp.org/the-value-of-pti-in-road-safety/) contains no insurer-produced work. The [Pennsylvania 2009 study](https://gis.penndot.gov/BPR_PDF_FILES/Documents/Research/Complete%20Projects/Operations/Vehicle%20Safety%20Inspection%20Program%20Effectiveness.pdf) was PennDOT-funded and itself notes that claims of lower insurance costs from inspection have "no rigorous publicly available data." The single direct insurer position found is the **Missouri Insurance Coalition**, which [testified in February 2025](https://citizenportal.ai/articles/6351404/Missouri-committee-hears-bills-to-eliminate-passenger-vehicle-safety-inspections) that it "supports maintaining some form of inspection" and opposed full elimination while not objecting to age/mileage exemptions — the position the legislature ultimately adopted. The only study in GAO's review to use insurance claims data at all (Christensen & Elvik, Norway, 2007) found inspections improved vehicle condition but had no significant effect on crashes. In short, insurers have neither produced the evidence nor lobbied on it, which leaves the field open for the consent-based programme in section 13.5 to generate the first defect-versus-claims data set.

For this report the implication is direct. Legislators are abandoning periodic physical inspection because it is inconvenient, costly, poorly enforced and unproven — not because vehicle condition has stopped mattering; Missouri, Pennsylvania and Virginia have kept theirs after contested debates on exactly these grounds. An inspection credential that draws most of its evidence from the vehicle itself (section 13) removes the station visit and the upselling incentive, produces the per-vehicle defect data that the crash-rate studies lacked, and gives states that have repealed inspection a low-friction way to reintroduce a roadworthiness check tied to registration.

**Resources:**
- [EPA Vehicle Emissions Inspection and Maintenance (I/M)](https://www.epa.gov/state-and-local-transportation/vehicle-emissions-inspection-and-maintenance-im); [40 CFR Part 51 Subpart S](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-51/subpart-S)
- [Smog Check — California BAR](https://www.bar.ca.gov/smog-check); [CA DMV smog inspections](https://www.dmv.ca.gov/portal/vehicle-registration/smog-inspections/)
- [Texas DPS: Vehicle safety inspection program changes](https://www.dps.texas.gov/news/vehicle-safety-inspection-program-changes-now-effect); [TCEQ I/M overview](https://www.tceq.texas.gov/airquality/mobilesource/vim/overview.html)
- [Virginia DMV emissions inspections](https://www.dmv.virginia.gov/vehicles/registration/emissions); [Va. Code §46.2-1158](https://law.lis.virginia.gov/vacode/title46.2/chapter10/section46.2-1158/)
- [Washington: Emission Check ended](https://ecology.wa.gov/air-climate/air-quality/vehicle-emissions/emissions-check-ends); [New Hampshire HB 649](https://legiscan.com/NH/text/HB649/id/3073747)

---

## 2. Canada

### 2.1 Inspection Landscape

Like the US, Canada has no federal vehicle inspection mandate for passenger vehicles. Each province operates its own program, and — with the exception of Prince Edward Island — no province currently requires a periodic inspection of private passenger cars: inspections are triggered by ownership transfer, import, or rebuilding. Commercial vehicles are governed by provincial programs implementing **National Safety Code (NSC) Standard 11 — Commercial Vehicle Maintenance and Periodic Inspection** (Part B, Periodic Motor Vehicle Inspection, PMVI).

| Inspection Type | Description |
|-----------------|-------------|
| **Safety Standards Certificate (SSC) / Certificate of Inspection** | Required when transferring ownership (Ontario), importing, or re-registering a rebuilt or out-of-province vehicle; certifies roadworthiness at that point in time |
| **Periodic private-vehicle inspection** | Only Prince Edward Island (annual) and Nova Scotia / New Brunswick (every 2 years, new vehicles 3 years) |
| **Emissions** | No active light-duty program: BC AirCare ended 31 Dec 2014, Ontario Drive Clean (light-duty) ended 1 Apr 2019 |
| **Periodic commercial vehicle inspection (PMVI)** | NSC Standard 11 Part B implemented provincially — Alberta and BC call it CVIP, Ontario runs Annual/Semi-Annual Inspections under DriveON (since April 2025), Quebec's SAAQ runs Mandatory Periodic Mechanical Inspection |

### 2.2 Safety Standards Certificate (SSC) Data Fields

The Ontario SSC is the closest Canadian analogue to a US safety inspection certificate. Province-specific certificates share a common core:

| Field | Description |
|-------|-------------|
| **Vehicle Identification Number (VIN)** | 17-character VIN |
| **License plate / registration number** | Provincial plate |
| **Vehicle year / make / model** | Vehicle description |
| **Odometer reading** | Mileage at inspection |
| **Inspection date** | Date certificate was issued |
| **Certificate expiration date** | SSC is valid for a limited period (36 days in Ontario) |
| **Inspection station name / number** | Provincially licensed facility identifier |
| **Inspector ID / technician name** | Licensed mechanic or inspection technician |
| **Pass / fail result** | Certificate only issued on pass |
| **Items inspected** | Checklist of required components (brakes, lights, tires, steering, suspension, etc.) |
| **Defects found / repaired** | Items that required correction before pass |
| **Certificate number** | Unique document identifier |
| **Province identifier** | Issuing province |

### 2.3 Inspection Programs by Province

| Province / Territory | Private vehicles | Commercial (NSC 11 PMVI) | Emissions |
|----------------------|------------------|--------------------------|-----------|
| **Alberta** | Out-of-province and salvage inspections only (Vehicle Inspection Program); no inspection on in-province private sale | CVIP, annual/semi-annual | None |
| **British Columbia** | Import / rebuilt only; AirCare retired 2014 | CVSE inspections for vehicles >8,200 kg GVW | None |
| **Manitoba** | Certificate of Inspection on ownership change or import only | Periodic | None |
| **New Brunswick** | Motor Vehicle Inspection every 2 years (since 2020); new vehicles 3 years | Annual | None |
| **Newfoundland & Labrador** | Transfer / import only (annual inspection abolished 1994) | Annual | None |
| **Nova Scotia** | Every 2 years (since 2009); new vehicles 3 years | Annual | None |
| **Ontario** | Safety Standards Certificate on transfer/import; Drive Clean (light-duty) retired 2019 | Annual / semi-annual under DriveON | Heavy-duty emissions under DriveON |
| **Prince Edward Island** | Annual Motor Vehicle Inspection — the only province with periodic private-car inspection | Annual | None |
| **Québec** | No periodic inspection for private cars; import, rebuilt and long-storage vehicles only | Mandatory periodic mechanical inspection every 6 or 12 months (heavy vehicles, buses, taxis) | None |
| **Saskatchewan** | Inspection on import (out-of-province); SGI inspection stations | Periodic | None |
| **Yukon / Northwest Territories / Nunavut** | Import / salvage only; no periodic private inspection | Periodic | None |

**Resources:**
- [Safety Standards Certificate — Ontario](https://www.ontario.ca/page/safety-standards-certificate); [Drive Clean light-duty program ended — Ontario ERO](https://ero.ontario.ca/notice/013-3867)
- [Vehicle inspections — Alberta](https://www.alberta.ca/vehicle-inspections); [Commercial vehicle inspection program — Alberta](https://www.alberta.ca/vehicle-inspection-program-commercial-vehicles)
- [Certificate of Inspection — Manitoba Public Insurance](https://www.mpi.mb.ca/certificate-of-inspection/)
- [Motor Vehicle Inspection — Nova Scotia](https://novascotia.ca/sns/rmv/registration/safeinsp.asp); [Changes to inspections — New Brunswick](https://www2.gnb.ca/content/gnb/en/departments/public-safety/community_safety/content/drivers_vehicles/content/changes-to-motor-vehicle-inspections-in-new-brunswick.html)
- [Vehicle mechanical inspection — Québec SAAQ](https://saaq.gouv.qc.ca/en/vehicle-registration/vehicle-mechanical-inspection)
- [Inspection requirements — Newfoundland & Labrador](https://www.gov.nl.ca/motorregistration/vehicle-ownership/inspection-requirements/)
- [Motor Vehicle Inspection Programs — Canadian Jurisdictional Scan (PEI, Nov 2024)](https://www.princeedwardisland.ca/sites/default/files/7e26/Motor%20Vehicle%20Inspection%20Programs%20Canadian%20Jurisdictional%20Scan%202024.11.18.pdf)
- [BC CVSE vehicle inspections](https://www.cvse.ca/vehicle_inspections.htm); [CCMTA National Safety Code](https://www.ccmta.ca/en/national-safety-code)

---

## 3. European Union

### 3.1 Roadworthiness Testing Framework

EU vehicle roadworthiness testing is harmonized under **Directive 2014/45/EU** (periodic roadworthiness tests for motor vehicles and their trailers), part of the 2014 Roadworthiness Package with Directive 2014/46/EU (registration documents) and 2014/47/EU (roadside inspection of commercial vehicles). It sets a common minimum standard while allowing member states to exceed the floor.

All EU member states must:
- Test vehicles at defined minimum intervals
- Issue a **roadworthiness certificate** (or equivalent national document)
- Record test results electronically and make them available for registration and cross-border recognition (2014/46/EU)
- Apply a **roadworthiness test proof** (sticker or equivalent) to the vehicle

Known nationally as:

| Country | Name |
|---------|------|
| Germany | **HU** (Hauptuntersuchung), which since 2010 incorporates the emissions test (AU, Abgasuntersuchung) — TÜV, DEKRA, GTÜ, KÜS stations |
| France | **Contrôle Technique (CT)** |
| Spain | **ITV** (Inspección Técnica de Vehículos) |
| Italy | **Revisione** |
| Netherlands | **APK** (Algemene Periodieke Keuring) |
| Belgium | **Contrôle Technique / Technische Controle** |
| Sweden | **Kontrollbesiktning** (Besikta, Opus Bilprovning, Carspect, DEKRA and others) |
| Poland | **Badanie Techniczne** |
| Czech Republic | **STK** (Stanice Technické Kontroly) |
| Austria | **Pickerl** (§57a KFG 1967 test) |
| Ireland | **NCT** (National Car Test, cars) and **CVRT** (Commercial Vehicle Roadworthiness Test) |
| United Kingdom (post-Brexit) | **MOT** test — aligned with the EU regime but no longer covered by 2014/45/EU |

### 3.2 EU Roadworthiness Certificate Data Fields

Directive 2014/45/EU Annex II specifies the **minimum** content of the roadworthiness certificate. Member states routinely add further fields (make/model, first registration date, measured emissions values, report number) from their national registers and test protocols.

| Field | Annex II minimum? | Description |
|-------|-------------------|-------------|
| **Vehicle Identification Number (VIN)** | Yes | 17-character VIN |
| **Vehicle registration number** | Yes | National plate identifier plus country symbol |
| **Place and date of test** | Yes | Testing centre location and test date |
| **Odometer reading** | Yes (if available) | Mileage at time of test |
| **Vehicle category** | Yes (if available) | EU type-approval category (M1, M2, N1, etc.) |
| **Deficiencies identified and their severity** | Yes | Per Article 7 / Annex I classification |
| **Result of the test** | Yes | Pass / fail |
| **Date of next test or expiry of current certificate** | Yes (unless provided otherwise) | Validity end date |
| **Testing organisation and inspector** | Yes | Name of testing centre / organisation; inspector signature or identification |
| **Other information** | Yes (optional) | National additions |
| Vehicle make / model / type | National | From registration records |
| First registration date | National | Used to determine test interval |
| Emissions test result | National | Exhaust gas opacity, lambda value, CO/HC levels (where applicable) |
| Test report number | National | Unique identifier for this test |

**Defect classification (Article 7(2), applied per item in Annex I):**

| Class | Definition | Effect on vehicle |
|-------|------------|-------------------|
| **Minor** | Deficiency with no significant effect on vehicle safety or the environment, and other minor non-compliances | Pass; repair recommended |
| **Major** | Deficiency that may prejudice vehicle safety, affect the environment, or put other road users at risk | Fail; vehicle may be driven to repair facility |
| **Dangerous** | Direct and immediate risk to road safety or impact on the environment | Fail; vehicle must not be used on public roads |

### 3.3 Test Intervals by EU Vehicle Category (Directive 2014/45/EU, Article 5)

| Vehicle Category | Description | EU minimum schedule |
|-----------------|-------------|---------------|
| **M1, N1** | Passenger cars, light commercial ≤3.5 t | First test 4 years after first registration, then every 2 years |
| **M1 used as taxis or ambulances; M2, M3** | Commercial passenger transport, minibuses, buses/coaches | Annual from year 1 |
| **N2, N3** | Lorries, heavy trucks >3.5 t | Annual from year 1 |
| **O3, O4** | Heavy trailers >3.5 t | Annual from year 1 |
| **L3e, L4e, L5e, L7e >125 cm³** | Motorcycles, tricycles, heavy quadricycles | In scope since 1 Jan 2022; intervals set nationally; member states with effective alternative road-safety measures may opt out (e.g. FI, IE, NL) |

> Member states may apply more frequent intervals (several test M1 annually after 10 years — e.g. Ireland and, from 2027, Austria), but this is not required by the Directive. The Commission's April 2025 proposal (see 3.4) would make annual testing of vehicles over 10 years the EU minimum; Parliament and Council have so far rejected that element.

### 3.4 Digital Roadworthiness Certificates — the 2025 Roadworthiness Package Revision

Directly relevant to a `VehicleInspectionCredential`: on 24 April 2025 the Commission proposed revising the package — **COM(2025) 180** amending Directives 2014/45/EU and 2014/47/EU (procedure 2025/0097(COD)) and **COM(2025) 179**, a new registration-documents directive replacing 1999/37/EC (2025/0096(COD)). Key elements:

- **Roadworthiness certificates and registration certificates mandatory in electronic (digital) format**, with a common EU data set and exchange via MOVE-HUB
- Odometer readings recorded at every test and exchanged cross-border to combat mileage fraud
- New emissions tests (particle number for petrol and diesel, NOx) and checks of electronic safety systems (ePTI), ADAS and EV components; battery-health check for EVs under discussion
- Six-month temporary cross-border certificate for vehicles re-registered in another member state
- Removal of the motorcycle opt-out and annual testing of vehicles over 10 years (both contested)

**Status (September 2026):** Council general approach adopted 4 December 2025 (kept current test frequencies and the motorcycle opt-out); European Parliament TRAN vote 5 May 2026 and plenary mandate 21 May 2026 (rejected annual testing for >10-year vehicles, supported motorcycle PTI); trilogues held 2 July, 7 September and 10 September 2026 with the aim of agreement by end of 2026. No provisional agreement yet. Whatever the final text, the EU is moving to a mandatory machine-readable inspection record, which makes the EU the most likely first large jurisdiction to consume or issue an inspection credential.

**Resources:**
- [Directive 2014/45/EU (consolidated) — EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02014L0045-20220927)
- [Directive 2014/46/EU (registration documents, electronic recording)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32014L0046)
- [Vehicle inspection — European Commission road safety](https://road-safety.transport.ec.europa.eu/eu-road-safety-policy/priorities/safe-vehicles/vehicle-inspection_en)
- [COM(2025) 180 — proposal amending 2014/45/EU and 2014/47/EU](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2025%3A180%3AFIN); [Commission press release, 24 Apr 2025](https://transport.ec.europa.eu/news-events/news/updated-rules-safer-roads-less-air-pollution-and-digital-vehicle-documents-2025-04-24_en)
- [Legislative Observatory 2025/0097(COD)](https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0097(COD)); [Council general approach, 4 Dec 2025](https://www.consilium.europa.eu/en/press/press-releases/2025/12/04/council-sets-position-on-updated-eu-rules-on-inspections-of-vehicles-and-their-registration/); [EP Legislative Train](https://www.europarl.europa.eu/legislative-train/theme-transport-and-tourism-tran/file-revision-of-pti-directive-201445eu-and-rsi-directive-201447eu)
- [MOT Test — UK DVSA](https://www.gov.uk/getting-an-mot)

---

## 4. Japan

### 4.1 Shaken (車検) — Vehicle Inspection

Japan operates one of the world's most rigorous mandatory vehicle inspection systems, known as **Shaken** (車検, *sha-ken* = "vehicle inspection"), under the Road Vehicles Act (道路運送車両法). It is administered by the Ministry of Land, Infrastructure, Transport and Tourism (MLIT); inspections are performed at MLIT district transport bureaus and the National Agency for Automobile and Land Transport Technology (NALTEC, 自動車技術総合機構) inspection offices, at the Light Motor Vehicle Inspection Organization (軽自動車検査協会) for kei vehicles, or at MLIT-designated private garages (指定整備工場, 民間車検場).

### 4.2 Shaken Certificate (自動車検査証) Data Fields

Since 4 January 2023 (registered vehicles) and January 2024 (kei vehicles) the certificate is the **電子車検証**, an A6 card with an IC chip. Some fields are printed; others are held only on the chip and read with the MLIT 車検証閲覧アプリ.

| Field | Where | Description |
|-------|-------|-------------|
| **Vehicle Identification / chassis number (車台番号)** | Printed | Japanese chassis number |
| **License plate number** | Printed | Japanese registration plate (ナンバープレート) |
| **Vehicle name / model code (車名 / 型式)** | Printed | Type-approval designation |
| **Dimensions and weights** | Printed | Length, width, height, vehicle weight, gross weight (weight-based tax) |
| **First registration date (初度登録年月)** | Printed | Date of first registration in Japan |
| **Fuel type / engine displacement** | Printed | For tax and environmental classification |
| **Seating capacity** | Printed | |
| **Vehicle ID (車両ID)** | Printed | Identifier for the electronic certificate system |
| **Certificate validity expiry (有効期間の満了する日)** | IC chip only | Date by which next Shaken must occur |
| **Owner name and address; user address; base of use (使用の本拠)** | IC chip only | Personal data moved off the printed face |
| **Odometer reading** | Certificate record | Recorded at each inspection since 2004 (kei since 2009) |

Documents handled *at* the Shaken but not part of the certificate itself: the inspection result / emissions measurement record (CO, HC, NOx, diesel opacity against MLIT standards), the windshield **inspection sticker (検査標章)** showing expiry month/year, the **weight tax** (自動車重量税) payment, and confirmation of valid compulsory liability insurance (**自賠責保険**, Jibaiseki).

### 4.3 Shaken Intervals (道路運送車両法 §61)

| Vehicle Type | New vehicle | Subsequent |
|-------------|-----|----------|
| **Passenger car (private)** | 3 years | Every 2 years |
| **Light motor vehicle (軽自動車), passenger** | 3 years | Every 2 years |
| **Motorcycle (>250 cc)** | 3 years | Every 2 years (≤250 cc: no Shaken) |
| **Trucks, GVW <8 t (private and business)** | 2 years | Annual |
| **Trucks, GVW ≥8 t** | 1 year | Annual |
| **Taxis, buses (commercial passenger)** | 1 year | Annual |
| **Rental cars** | 2 years | Annual |
| **Light cargo (軽貨物)** | 2 years | Every 2 years |

**Resources:**
- [Road Vehicles Act (道路運送車両法) — e-Gov](https://laws.e-gov.go.jp/law/326AC0000000185)
- [Inspection validity periods — MLIT vehicle registration portal](https://www.jidoushatouroku-portal.mlit.go.jp/jidousha/kensatoroku/about/inspect/validity-period/index.html)
- [電子車検証 (electronic inspection certificate) — MLIT](https://www.denshishakensho-portal.mlit.go.jp/user/about/)
- [NALTEC — National Agency for Automobile and Land Transport Technology](https://www.naltec.go.jp/)

---

## 5. South Korea

### 5.1 Vehicle Inspection Program

South Korea's mandatory vehicle inspection (자동차검사) is administered by the **Korea Transportation Safety Authority (KOTSA / TS, 한국교통안전공단)** under the Motor Vehicle Management Act (자동차관리법), at KOTSA inspection centres and designated private garages. It covers safety and emissions in one visit. Since October 2021 the inspection result is recorded electronically only — it is no longer stamped on the registration certificate (자동차등록증).

### 5.2 Korean Inspection Certificate Data Fields

| Field | Description |
|-------|-------------|
| **Vehicle registration number** | Korean plate (차량번호) |
| **Vehicle Identification Number (VIN)** | Chassis number (차대번호) |
| **Vehicle make / model** | Korean or international designation |
| **Engine type / fuel** | Gasoline, diesel, LPG, electric, hybrid |
| **Inspection date** | Date of test |
| **Certificate validity date** | Expiry of inspection |
| **Inspection station name / ID** | KOTSA centre or designated private garage |
| **Inspector ID** | Certified inspection technician |
| **Overall result** | Pass (적합) / Fail (부적합) |
| **Safety inspection items** | Brakes, lights, steering, tires, suspension (per KOTSA checklist) |
| **Emissions test result** | CO, HC, NOx levels; smoke opacity (diesel); OBD readiness |
| **Inspection report number** | Unique document number |

### 5.3 Inspection Intervals (자동차관리법 시행규칙 별표 15의2, as amended Dec 2024)

| Vehicle Type | Interval |
|-------------|----------|
| **Private passenger car** | First inspection 5 years after registration (4 years for vehicles registered before 2025), then every 2 years — no age-based annual tier |
| **Taxi (사업용 승용)** | First 2 years, then annual |
| **Medium/large passenger vans and buses (승합) over 8 years; commercial large trucks over 2 years** | Every 6 months |
| **Other commercial vehicles** | Annual |
| **Motorcycles** | No safety inspection; emissions/noise inspection (대기환경보전법) for >260 cc since 2014 and 50–260 cc MY2018+ since 2021: 3 years then every 2 years |

**Resources:**
- [KOTSA — Korea Transportation Safety Authority](https://www.kotsa.or.kr/); [English portal](https://main.kotsa.or.kr/eng/engMain.do); [inspection portal (cyberTS)](https://www.cyberts.kr/)
- [Vehicle inspection overview — KOTSA](https://main.kotsa.or.kr/portal/contents.do?menuCode=01010200)

---

## 6. China

### 6.1 Vehicle Inspection Program

China's mandatory inspection (机动车检验) is administered by the **Ministry of Public Security (公安部)** traffic management bureaus under the Road Traffic Safety Law and its Implementing Regulations (Article 16), as reformed by 公交管〔2022〕295号 effective 1 October 2022. Inspections are carried out by inspection stations (机动车检验机构) accredited by the **market regulation authorities (市场监管部门, CMA 资质认定)**, with emissions stations also supervised by the ecology and environment authorities. Safety, emissions and technical compliance are handled in one visit.

### 6.2 Chinese Inspection Certificate Data Fields

| Field | Description |
|-------|-------------|
| **Vehicle Identification Number (VIN)** | 车辆识别代号 |
| **License plate number** | 车牌号码 |
| **Vehicle make / model** | 品牌型号 |
| **Vehicle type category** | Passenger car, commercial vehicle, motorcycle, etc. |
| **Engine number** | 发动机号 |
| **Fuel type** | Gasoline, diesel, CNG, NEV (New Energy Vehicle) |
| **First registration date** | 初次登记日期 |
| **Odometer reading** | 行驶里程 |
| **Inspection date** | 检验日期 |
| **Certificate validity period** | 检验有效期 |
| **Inspection station name / accreditation number** | Station name + CMA accreditation code |
| **Inspector / technician ID** | Certified inspector identifier |
| **Overall result** | Pass (合格) / Fail (不合格) |
| **Safety inspection items** | Per GB 38900-2020: brakes, steering, lights, tires, windshield, horn, mirrors, etc. |
| **Emissions test result** | OBD check + tailpipe measurement per GB 18285-2018 (petrol) / GB 3847-2018 (diesel) |
| **Inspection mark (检验标志)** | Electronic mark since 2020; physical sticker optional |

### 6.3 Inspection Intervals (post-October 2022 reform)

| Vehicle Type | Interval |
|-------------|----------|
| **Non-commercial small/mini passenger car (excl. 面包车), ≤10 years** | Inspection mark issued every 2 years; on-site inspection only at years 6 and 10 |
| **Non-commercial small passenger car, >10 years** | Annual (the former 6-monthly rule for vehicles over 15 years was abolished in 2022) |
| **Motorcycles** | Same 6- and 10-year on-site regime; annual after 10 years |
| **Commercial passenger vehicles (taxi, bus)** | Annual for the first 5 years; every 6 months thereafter |
| **Trucks and large/medium non-commercial passenger vehicles** | Annual for the first 10 years; every 6 months thereafter |

**Resources:**
- [公交管〔2022〕295号 — inspection reform notice (gov.cn)](https://www.gov.cn/zhengce/zhengceku/2022-10/19/content_5719521.htm)
- [GB 38900-2020 Items and methods for safety technology inspection of motor vehicles (replaced GB 21861-2014)](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=87CD5EFD73BF52CB08C07C81CA78E291)
- [GB 18285-2018 and GB 3847-2018 in-use emissions standards — MEE](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/dqhjbh/dqydywrwpfbz/201811/t20181113_673593.shtml)
- [Ministry of Public Security](https://www.mps.gov.cn/) (access-restricted outside China)

---

## 7. India

### 7.1 Fitness Certificate Program

India's vehicle inspection framework is governed by the **Motor Vehicles Act, 1988** and the **Central Motor Vehicles Rules, 1989** (Rule 62, fitness), administered at the state level through **State Transport Departments / Regional Transport Offices (RTOs)**. The Motor Vehicles (Amendment) Act 2019 and subsequent rules introduced **Automated Testing Stations (ATS)**: since 1 April 2025 (GSR 709(E)) fitness testing of transport vehicles must be done at an ATS wherever one exists in the registering authority's jurisdiction.

### 7.2 Fitness Certificate Data Fields

| Field | Description |
|-------|-------------|
| **Vehicle Registration Number** | State registration plate |
| **Vehicle Identification Number (VIN / Chassis Number)** | As per RC |
| **Engine number** | As per RC |
| **Vehicle make / model / type** | Per registration certificate |
| **Category** | LMV, HMV, transport, non-transport |
| **Fuel type** | Petrol, diesel, CNG, LPG, electric |
| **Gross Vehicle Weight (GVW)** | For commercial vehicles |
| **Inspection date** | Date of test |
| **Certificate validity date** | See intervals below |
| **Inspection centre / RTO name** | Regional Transport Office or ATS |
| **Inspector / MVI designation** | Motor Vehicle Inspector (government) or ATS |
| **Overall result** | Fit / Unfit |
| **Defects found** | Itemized list on failure |
| **Emissions test result** | PUC (Pollution Under Control) certificate number and expiry |
| **Fitness certificate number** | Unique FC document number |

> **PUC (Pollution Under Control) Certificate:** A separate emissions-only credential (CMVR Rule 115(7)); required from one year after first registration; valid 6 months, or 12 months for BS-IV and BS-VI vehicles. Data fields: registration number, fuel type, test date, expiry date, CO/HC/smoke opacity levels, testing centre, test equipment ID.

### 7.3 Inspection Intervals (CMVR Rule 62)

| Vehicle Category | New Vehicle | Subsequent |
|-----------------|-------------|------------|
| **Transport vehicle (taxi, goods, bus)** | Fitness certificate valid 2 years | Renewed every 2 years until the vehicle is 8 years old, then annually |
| **Non-transport vehicle (private car/motorcycle)** | Deemed fit for 15 years from registration (registration validity) | Registration renewed every 5 years thereafter, subject to a fitness test |
| **Construction equipment / special purpose** | Per transport-vehicle schedule | Annual |

**Resources:**
- [Parivahan Portal (MoRTH)](https://parivahan.gov.in/); [Automated Fitness Management System (AFMS)](https://vahan.parivahan.gov.in/AFMS)
- [GSR 709(E), 14 Nov 2024 — ATS fitness testing from 1 April 2025 (PIB)](https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2091508&reg=48&lang=2)
- [Central Motor Vehicles Rules 1989 (Rules 62, 115)](https://indiankanoon.org/doc/104735461/)
- [Central Pollution Control Board](https://cpcb.gov.in/)

---

## 8. Cross-Jurisdictional Comparison — Core Data Points

The following data points appear on inspection certificates across all or most jurisdictions and form the natural basis for a `VehicleInspectionCredential`:

| Data Point | US | CA | EU | JP | KR | CN | IN |
|------------|----|----|----|----|----|----|-----|
| VIN | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| License plate / registration number | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Vehicle make / model | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Inspection date | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Certificate expiration date | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Inspection station identifier | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Inspector / technician ID | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Overall result (pass/fail) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Odometer reading | ✓ | ✓ | ✓ (if available) | ✓ | — | ✓ | — |
| Emissions test result | ✓ (varies) | ✓ (limited) | ✓ | ✓ | ✓ | ✓ | ✓ (PUC) |
| Defect items / failure reasons | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Defect severity classification | — | — | ✓ (Minor/Major/Dangerous) | — | — | — | — |
| Electronic certificate / record | Some states | ON DriveON (commercial) | Electronic record (2014/46/EU); electronic certificate proposed 2025 | ✓ 電子車検証 (IC card, 2023) | ✓ (electronic only since 2021) | ✓ electronic mark (2020) | ✓ Parivahan/AFMS |
| Certificate / report number | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Vehicle category / type-approval class | — | — | ✓ (M/N/L) | ✓ | — | ✓ | ✓ |
| First registration date | — | — | ✓ | ✓ | ✓ | ✓ | — |
| Fuel type | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Insurance validity confirmation | — | — | — | ✓ (Jibaiseki checked at Shaken) | — | — | — |
| Weight (GVW) | Commercial | Commercial | Commercial | ✓ | — | ✓ | ✓ |
| OBD-II monitor readiness | ✓ (where OBD) | — | ✓ | — | ✓ | ✓ | — |
| Emissions standard reference | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 9. Proposed `VehicleInspectionCredential` Core Schema

Following the design pattern of the POI and FNOL credentials, a `VehicleInspectionCredential` would:

- Reference the `VehicleRegistrationCredential` by UUID (VIN, plate, make/model live there — not restated)
- Be issued by a DID representing the authorized inspection authority or inspection station
- Encode the inspection result, expiry, and defect data

### Minimal cross-jurisdictional field set

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/vvc/v1"
  ],
  "type": ["VerifiableCredential", "VehicleInspectionCredential"],
  "issuer": "did:example:inspection-station-12345",
  "validFrom": "2026-07-22T00:00:00Z",
  "validUntil": "2028-07-22T00:00:00Z",
  "credentialSubject": {
    "registrationCredential": "urn:uuid:...",
    "inspectionType": "safety+emissions",
    "inspectionDate": "2026-07-22",
    "expirationDate": "2028-07-22",
    "odometer": { "value": 48500, "unit": "km" },
    "result": "PASS",
    "defects": [],
    "emissionsResult": {
      "standard": "EU6d",
      "co_ppm": 142,
      "hc_ppm": 18,
      "nox_ppm": 45,
      "result": "PASS"
    },
    "stationIdentifier": "DE-TUV-089-0042",
    "inspectorId": "TUV-INSP-7821",
    "jurisdiction": "DE",
    "reportNumber": "HU-2026-DE-089-000981234"
  }
}
```

### Extension points by jurisdiction

| Extension field | Jurisdictions | Purpose |
|----------------|---------------|---------|
| `defectSeverity` | EU | MINOR / MAJOR / DANGEROUS per 2014/45/EU Art. 7 / Annex I |
| `vehicleCategory` | EU, JP, CN, IN | M1/N1/L-category; Japanese type code |
| `weightTaxReceipt` | JP | 自動車重量税 payment confirmation (handled at Shaken, not a certificate field) |
| `jibaisekiConfirmation` | JP | Mandatory insurance validity checked at Shaken |
| `tireTreadDepth` | All | Per-tire mm readings and measurement source — not recorded numerically by any jurisdiction today (see section 12) |
| `pucCertificateNumber` | IN | Separate emissions sub-credential reference |
| `obdMonitorStatus` | US, KR, CN | Per-monitor readiness bitmap |
| `repairCostWaiver` | US | Emissions waiver threshold exceeded flag |
| `reInspectionDeadline` | US, CA | Deadline for free retest after failure |

---

## 10. Key Regulatory References

| Jurisdiction | Authority | Key Instrument |
|-------------|-----------|----------------|
| USA | State DMVs / DPS; EPA (emissions) | State vehicle inspection statutes; 40 CFR Part 51 Subpart S (EPA I/M program requirements); FMVSS 138 (TPMS) |
| Canada | Provincial transport ministries; CCMTA | Provincial Motor Vehicle / Highway Traffic Acts; NSC Standard 11 — Commercial Vehicle Maintenance and Periodic Inspection |
| EU | European Commission DG MOVE | Directive 2014/45/EU (periodic roadworthiness), 2014/46/EU (registration documents), 2014/47/EU (roadside inspection); UN Regulation 141 (TPMS); COM(2025) 179/180 revision (pending) |
| Germany | KBA; TÜV/DEKRA/GTÜ/KÜS | StVZO §29 with Anlage VIIIa (HU including emissions test; former §47a AU repealed 2009) |
| France | Ministry of Transport (DGEC/OTC), DREAL | Arrêté du 18 juin 1991 (Contrôle Technique, light vehicles ≤3.5 t); Arrêté du 27 juillet 2004 (heavy vehicles) |
| UK (post-Brexit) | DVSA | Road Traffic Act 1988 ss.45–47; Motor Vehicles (Tests) Regulations 1981 (SI 1981/1694); MOT scheme |
| Japan | MLIT; NALTEC | Road Vehicles Act (道路運送車両法) §61 et seq.; Safety Regulations for Road Vehicles (保安基準) |
| South Korea | MOLIT; KOTSA | Motor Vehicle Management Act (자동차관리법) and Enforcement Rules 별표 15의2 |
| China | MPS; SAMR (station accreditation); MEE (emissions) | Road Traffic Safety Law Implementing Regulations Art. 16; 公交管〔2022〕295号; GB 38900-2020 (safety); GB 18285-2018 (petrol emissions); GB 3847-2018 (diesel); GB 7258-2017 (technical conditions incl. tread depth) |
| India | MoRTH; State Transport Departments | Motor Vehicles Act 1988; CMVR 1989 Rules 62 and 115; AIS standards; ATS rules (GSR 709(E)) |

---

*Research compiled from public regulatory sources, transport ministry publications, and official legal texts; re-verified September 2026. Inspection requirements, intervals, and data fields are subject to change; verify with the applicable transport authority for current requirements.*

---

## 11. Inspection Data Points Mapped to COVESA VSS

This section maps individual inspection pass/fail criteria to COVESA Vehicle Signal Specification (VSS) signal paths. Source: VSS 6.1 (September 2026), read from the `spec/` and `overlays/` directories of the [vehicle_signal_specification](https://github.com/COVESA/vehicle_signal_specification) repository.

**Key caveats:**
- VSS signals describe *live sensor readings* from a running or recently stopped vehicle. Inspection criteria are *point-in-time pass/fail thresholds* — the mapping below identifies which VSS signal feeds the criterion, not that the criterion is directly encoded in VSS.
- The `Vehicle.OBD.*` branch was deprecated in VSS 5.x and **removed from the standard catalogue in VSS 6.0**. It survives as an optional overlay (`overlays/extensions/OBD/OBD.vspec`) for implementations that need one-to-one OBD PID mapping. The canonical in-catalogue signals are `Vehicle.Diagnostics.*` and `Vehicle.Powertrain.CombustionEngine.*`. OBD-overlay paths are marked as such below.
- VSS 6.1 added a `Vehicle.Safety` branch (`Rollover`, `IsFire`, `IsSubmersed`, `RoadIcingState`, `VisibilityImpairment`) — relevant to incident credentials rather than inspection, but listed for completeness.
- Tire tread depth is **not currently a VSS signal** — see gap analysis below.
- Signal paths use the standard VSS dot notation; all paths are rooted at `Vehicle.`.

---

### 11.1 Brakes

Brakes are the most universally inspected safety system across all seven jurisdictions.

#### Brake Pad Wear

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.PadWear` | sensor | percent | Brake pad wear 0–100%; 0 = new, 100 = fully worn |
| `Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.PadWear` | sensor | percent | Per-wheel, Row 1 right |
| `Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.PadWear` | sensor | percent | Per-wheel, Row 2 left |
| `Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.PadWear` | sensor | percent | Per-wheel, Row 2 right |
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Brake.IsBrakesWorn` | sensor | boolean | Threshold boolean — True = worn beyond acceptable limit |

**Inspection threshold mapping:** Jurisdictions do not publish a single universal PadWear% threshold; failure is triggered when friction material reaches the wear indicator (typically 2–3 mm remaining). An inspection credential could encode the measured `PadWear` value plus a jurisdiction-specific `wornThreshold` field.

**Source vspec:** `spec/Chassis/Wheel.vspec`

#### Brake Fluid

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Brake.FluidLevel` | sensor | percent | Fluid level 0–100% |
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Brake.IsFluidLevelLow` | sensor | boolean | True = fluid below minimum |

**Source vspec:** `spec/Chassis/Wheel.vspec`

#### Brake Pedal / Hydraulic System

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.Brake.PedalPosition` | sensor | percent | Pedal depression 0–100% (used to verify pedal feel / travel under load test) |
| `Vehicle.Chassis.Brake.IsDriverEmergencyBrakingDetected` | sensor | boolean | Emergency braking detection — relevant for ABS/EBA function verification |

**Source vspec:** `spec/Chassis/Chassis.vspec`

#### Parking Brake

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.ParkingBrake.IsEngaged` | actuator | boolean | True = parking brake engaged (holds on gradient test) |

**Source vspec:** `spec/Chassis/Chassis.vspec`

---

### 11.2 Tires

#### Tire Pressure (TPMS)

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.Pressure` | sensor | kPa | Absolute tire pressure |
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.IsPressureLow` | sensor | boolean | True = pressure below minimum threshold |

**Inspection use:** TPMS fitment is mandated in the US (FMVSS 138), the EU (UN Regulation 141, extended to heavy vehicles from 2022/2024) and Korea (KMVSS); Japan applies R141 as a performance standard without a confirmed fitment mandate. Where fitted, TPMS function is an inspection item. The credential can record live kPa values at time of inspection alongside the vehicle-reported `IsPressureLow` status.

#### Tire Temperature

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.RubberTemperature` | sensor | °C | Tire rubber temperature (replaces `Tire.Temperature`, deprecated in v6.0) |
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.AirTemperature` | sensor | °C | Internal air temperature |
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.WinterStatus` | sensor | enum | Winter/all-season/summer tire classification — relevant where seasonal tire rules are inspected (e.g. Germany, Quebec) |

**Source vspec:** `spec/Chassis/Wheel.vspec`

#### Tire Tread Depth — VSS Gap

> **Gap:** COVESA VSS 6.1 (September 2026) has **no signal for tire tread depth** (mm remaining) or tread wear indicators. The `Tire` branch provides `Pressure`, `IsPressureLow`, `RubberTemperature`, `AirTemperature` and `WinterStatus` — no `Tire.TreadDepth`. SAE J1939 likewise has no tread-depth SPN.
>
> **Implication for inspection credential:** Tread depth (the most commonly failed tire item — legal minimum 1.6 mm in the EU, US (2/32"), Canada, Japan, Korea and India; 3.2 mm on steer axles in China and for US commercial vehicles under 49 CFR 393.75) must be captured as a **credential field** until VSS adds a tread depth signal. Proposed paths: `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.TreadDepth` (mm, minimum), `Tire.TreadDepthInner/Center/Outer`, `Tire.TreadDepthSource`, `Tire.TreadDepthTimestamp`, `Tire.Identifier`. A VSS pull request or a COVESA commercial-vehicle overlay is the right vehicle; the COVESA FMS overlay has no tread signal either. See section 12 for the state of the art in estimating tread depth from sensors and a programme to build the data.

#### Tire Size / Specification Compliance

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.Axle.TireDiameter` | attribute | inch | Outer tire diameter (ETRTO/TRA) |
| `Vehicle.Chassis.Axle.TireWidth` | attribute | mm | Nominal section width |
| `Vehicle.Chassis.Axle.TireAspectRatio` | attribute | percent | Aspect ratio |
| `Vehicle.Chassis.Axle.WheelDiameter` | attribute | inch | Rim diameter |

**Inspection use:** Confirms fitted tires match the vehicle type-approval specification. These are `attribute` (static) signals — read from vehicle configuration, not measured live.

**Source vspec:** `spec/Chassis/Chassis.vspec`

---

### 11.3 Emissions

This is the most complex inspection category, spanning ICE tailpipe measurements, OBD-II readiness monitors, diesel particulate systems, and EV-specific assessments.

#### OBD-II Diagnostic Trouble Codes (DTCs) and MIL

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Diagnostics.DTCCount` | sensor | count | Number of active DTCs (canonical v5.0+ path) |
| `Vehicle.Diagnostics.DTCList` | sensor | string[] | Active DTC codes in SAE-J2012DA format (e.g. `P0420`) |
| `Vehicle.OBD.Status.IsMILOn` | *(OBD overlay only)* | boolean | Malfunction Indicator Light state |
| `Vehicle.OBD.Status.DTCCount` | *(OBD overlay only)* | — | Superseded in the catalogue by `Vehicle.Diagnostics.DTCCount` |

> **MIL state gap:** the MIL state exists only in the OBD overlay; there is **no `Vehicle.Diagnostics.IsMILOn` in the VSS 6.1 catalogue**. Implementations bridging to OBD inspection systems should carry `isMILOn` as a credential field (from the overlay or a direct OBD read) and treat a non-zero `DTCCount` as a proxy where the overlay is absent, until a catalogue signal is introduced.

**Source vspec:** `spec/Vehicle/Diagnostics.vspec`, `overlays/extensions/OBD/OBD.vspec`

#### OBD-II Readiness Monitors

OBD-II readiness monitors are the primary emissions pass/fail gate in US I/M programs and are used in Korea and China. VSS has no `ReadinessMonitor.*` signals in the catalogue — the OBD PID mappings live in the OBD overlay.

| Relevant OBD PIDs (via VSS OBD overlay) | Monitor |
|---------------------------------------------|---------|
| PID 01 `Status` / PID 41 `DriveCycleStatus` (`IsMILOn`, `DTCCount`, `IgnitionType`) | Monitor status bytes: Catalyst, O2 Sensor, EVAP, EGR, Secondary Air |
| `Vehicle.OBD.O2WR.Sensor[N].Lambda` | Wide-band lambda (air-fuel equivalence ratio) |
| `Vehicle.OBD.CommandedEGR` / `EGRError` | EGR system commanded position and error |
| `Vehicle.OBD.CommandedEVAP` / `EVAPVaporPressure` | EVAP system status |
| `Vehicle.OBD.Catalyst.Bank1.Temperature1` / `Temperature2` | Catalyst brick temperature — proxy for catalyst efficiency |

**For a credential:** The cleanest approach is to record the raw readiness monitor bitmask (from PID 01/41) as a `uint16` field `obdReadinessBitmask` alongside individual per-monitor `PASS`/`NOT_READY`/`INCOMPLETE` strings. This avoids a dependency on the optional OBD overlay while preserving full information.

#### ICE Exhaust Gas — Tailpipe Measurement

Standard tailpipe gas analyser measurements are **not directly available as VSS sensor signals** — they are measured externally by the inspection station's analyser equipment, not reported by the vehicle ECU. However, VSS has relevant supporting signals:

| VSS Signal Path | Type | Unit | Description | Inspection relevance |
|-----------------|------|------|-------------|----------------------|
| `Vehicle.Powertrain.CombustionEngine.EngineOil.Temperature` | sensor | °C | Engine oil temperature | Confirms warm engine (required for valid emissions test) |
| `Vehicle.Powertrain.CombustionEngine.EngineCoolant.Temperature` | sensor | °C | Coolant temperature | Warm-up verification |
| `Vehicle.Powertrain.CombustionEngine.Speed` | sensor | rpm | Engine RPM | Test must be at idle / 2500 rpm depending on protocol |
| `Vehicle.OBD.O2WR.SensorN.Lambda` *(OBD overlay)* | sensor | ratio | Lambda (air-fuel equivalence) — proxy for combustion efficiency | High lambda deviation = rich/lean misfire |
| `Vehicle.OBD.ShortTermFuelTrim1` / `LongTermFuelTrim1` *(OBD overlay)* | sensor | percent | Short/long-term fuel correction | Sustained trim deviation indicates catalyst or injector fault |

**Conclusion:** The tailpipe CO, HC, NOx, and smoke opacity values reported on an inspection certificate come from the analyser, not the vehicle. These are **inspector-measured fields** and should be encoded as direct credential data points (e.g. `co_ppm`, `hc_ppm`, `opacity_pct`) rather than VSS signal references.

#### Diesel Particulate Filter (DPF)

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Powertrain.CombustionEngine.DieselParticulateFilter.InletTemperature` | sensor | °C | DPF upstream temperature |
| `Vehicle.Powertrain.CombustionEngine.DieselParticulateFilter.OutletTemperature` | sensor | °C | DPF downstream temperature |
| `Vehicle.Powertrain.CombustionEngine.DieselParticulateFilter.DeltaPressure` | sensor | Pa | Pressure drop across filter — high ΔP indicates blockage or failed regeneration |

**Inspection use:** EU Directive 2014/45/EU Annex I includes particulate filter presence and integrity in the exhaust emissions items for diesel vehicles, and the 2025 revision proposal adds particle-number testing. DPF delta-pressure is the primary sensor-based indicator of filter condition alongside smoke opacity measurement.

**Source vspec:** `spec/Powertrain/CombustionEngine.vspec`

#### Diesel Exhaust Fluid (DEF / AdBlue / AUS32)

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Powertrain.CombustionEngine.DieselExhaustFluid.Level` | sensor | percent | DEF tank fill level 0–100% |
| `Vehicle.Powertrain.CombustionEngine.DieselExhaustFluid.IsLevelLow` | sensor | boolean | True = DEF critically low |
| `Vehicle.Powertrain.CombustionEngine.DieselExhaustFluid.Range` | sensor | m | Remaining range on current DEF level |

**Inspection use:** Required check in EU (Euro 6 SCR systems), Japan (post-2016 heavy-duty), China (China 6). Low DEF triggers an engine derate — confirmed by inspection. Commercial vehicle roadworthiness tests (EU Annex I, Category N2/N3) require DEF system integrity.

**Source vspec:** `spec/Powertrain/CombustionEngine.vspec`

#### EV / BEV Battery Health (State of Health)

For BEVs and PHEVs, emissions inspection shifts to battery health and EV system integrity. The EU Battery Regulation (2023/1542) requires state-of-health data to be available in-vehicle from 2027 and the 2025 Roadworthiness Package proposal adds EV component checks; several EU testing organisations already offer battery-health tests as part of or alongside the periodic inspection.

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Powertrain.TractionBattery.StateOfHealth` | sensor | percent | Battery state of health — 100% = new capacity, degraded over life |
| `Vehicle.Powertrain.TractionBattery.NetCapacity` | sensor | kWh | Usable battery capacity at current SoH |
| `Vehicle.Powertrain.TractionBattery.GrossCapacity` | attribute | kWh | Nominal rated capacity |
| `Vehicle.Powertrain.TractionBattery.StateOfCharge.Current` | sensor | percent | Current SoC |
| `Vehicle.Powertrain.TractionBattery.Temperature.Average` | sensor | °C | Average pack temperature |
| `Vehicle.Powertrain.TractionBattery.Temperature.Max` | sensor | °C | Maximum cell temperature |
| `Vehicle.Powertrain.TractionBattery.CellVoltage.Min` | sensor | V | Minimum cell voltage (indicates cell imbalance) |
| `Vehicle.Powertrain.TractionBattery.CellVoltage.Max` | sensor | V | Maximum cell voltage |

**Source vspec:** `spec/Powertrain/TractionBattery.vspec`

---

### 11.4 Lighting

EU Directive 2014/45/EU Annex I and the equivalent national programs list lighting as a mandatory inspection item. VSS provides per-light `IsOn` and `IsDefect` signals via the `StaticLights.vspec` template, instantiated under `Vehicle.Body.Lights.*`.

| VSS Signal Path (pattern) | Type | Description |
|--------------------------|------|-------------|
| `Vehicle.Body.Lights.Beam.Low.IsOn` | actuator | Low-beam headlight commanded state |
| `Vehicle.Body.Lights.Beam.Low.IsDefect` | sensor | True = low-beam has a detected fault |
| `Vehicle.Body.Lights.Beam.High.IsOn` | actuator | High-beam state |
| `Vehicle.Body.Lights.Beam.High.IsDefect` | sensor | High-beam defect |
| `Vehicle.Body.Lights.Running.IsOn` | actuator | Daytime running lights |
| `Vehicle.Body.Lights.Running.IsDefect` | sensor | DRL defect |
| `Vehicle.Body.Lights.Backup.IsOn` | actuator | Reverse lights |
| `Vehicle.Body.Lights.Backup.IsDefect` | sensor | Reverse light defect |
| `Vehicle.Body.Lights.Parking.IsOn` | actuator | Parking lights |
| `Vehicle.Body.Lights.Parking.IsDefect` | sensor | Parking light defect |
| `Vehicle.Body.Lights.Brake.IsActive` *(via BrakeLights.vspec)* | sensor | Brake lights active |
| `Vehicle.Body.Lights.Brake.IsDefect` | sensor | Brake light defect |
| `Vehicle.Body.Lights.DirectionIndicator.Left/Right.IsSignaling` / `.IsDefect` *(via SignalingLights.vspec)* | sensor | Turn indicators active / defect |
| `Vehicle.Body.Lights.Hazard.IsSignaling` / `.IsDefect` | sensor | Hazard lights active / defect |
| `Vehicle.Body.Lights.Fog.Front/Rear.IsOn` / `.IsDefect` | actuator / sensor | Fog lights |
| `Vehicle.Body.Lights.LicensePlate.IsOn` / `.IsDefect` | actuator / sensor | Number-plate illumination — an explicit inspection item in the EU and UK |

**Source vspec:** `spec/Body/StaticLights.vspec`, `spec/Body/BrakeLights.vspec`, `spec/Body/SignalingLights.vspec`, `spec/Body/Body.vspec`

**Coverage note:** VSS `IsDefect` is a vehicle-self-reported boolean (typically from a bulb monitoring circuit). Physical headlight aim/alignment is tested by inspection station equipment (optical aim testers) — this is **inspector-measured** and not capturable from a VSS snapshot.

---

### 11.5 Wipers and Windshield Washer

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Body.Windshield.Front.Wiping.WiperWear` | sensor | percent | Front wiper wear 0–100% |
| `Vehicle.Body.Windshield.Front.Wiping.IsWipersWorn` | sensor | boolean | True = replacement recommended |
| `Vehicle.Body.Windshield.Rear.Wiping.WiperWear` | sensor | percent | Rear wiper wear (where fitted) |
| `Vehicle.Body.Windshield.Rear.Wiping.IsWipersWorn` | sensor | boolean | Rear wiper worn |
| `Vehicle.Body.Windshield.Front.WasherFluid.IsLevelLow` | sensor | boolean | Washer fluid level low |
| `Vehicle.Body.Windshield.Front.WasherFluid.Level` | sensor | percent | Fluid level 0–100% |

**Source vspec:** `spec/Body/Body.vspec`

---

### 11.6 Horn

| VSS Signal Path | Type | Description |
|-----------------|------|-------------|
| `Vehicle.Body.Horn.IsActive` | sensor | True = horn is sounding (functional test) |

**Inspection use:** Horn function is a required check in most jurisdictions. VSS captures whether the horn is active but does not have a `IsDefect` boolean — a failed horn would typically surface as a workshop-reported item rather than a self-reported vehicle signal.

**Source vspec:** `spec/Body/Body.vspec`

---

### 11.7 Engine Oil and Coolant (Fluid Levels / Condition)

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Powertrain.CombustionEngine.EngineOil.Level` | sensor | enum | `CRITICALLY_LOW` / `LOW` / `NORMAL` / `HIGH` / `CRITICALLY_HIGH` |
| `Vehicle.Powertrain.CombustionEngine.EngineOil.LifeRemaining` | sensor | seconds | Remaining oil life (negative = overdue) |
| `Vehicle.Powertrain.CombustionEngine.EngineOil.Temperature` | sensor | °C | Oil temperature |
| `Vehicle.Powertrain.CombustionEngine.EngineCoolant.Temperature` | sensor | °C | Coolant temperature |
| `Vehicle.Powertrain.CombustionEngine.EngineCoolant.Level` | sensor | enum | Coolant level status |

**Source vspec:** `spec/Powertrain/CombustionEngine.vspec`

---

### 11.8 Drivetrain Wear

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Powertrain.Transmission.ClutchWear` | sensor | percent | Clutch friction material wear 0–100% |

**Source vspec:** `spec/Powertrain/Transmission.vspec`

---

### 11.8a Braking / Stability Control Systems, Mirrors, Battery, Service and Weight

Additional catalogue signals that map to common inspection items:

| VSS Signal Path | Type | Description | Inspection relevance |
|-----------------|------|-------------|----------------------|
| `Vehicle.ADAS.ABS.IsError` / `IsEnabled` / `IsEngaged` | sensor | Anti-lock braking fault / state | ABS warning-lamp check (EU Annex I, US states) |
| `Vehicle.ADAS.ESC.IsError`, `Vehicle.ADAS.TCS.IsError`, `Vehicle.ADAS.EBD.IsError`, `Vehicle.ADAS.EBA.IsError` | sensor | Stability, traction, brake-force distribution and brake-assist faults | Electronic safety system checks (ePTI in the 2025 EU proposal) |
| `Vehicle.ADAS.ESC.RoadFriction.*` | sensor | Estimated road friction | Context for tire-health estimation (section 12) |
| `Vehicle.Body.Mirrors.DriverSide/PassengerSide.IsFolded` / `IsHeatingOn` / `Tilt` / `Pan` | actuator | Exterior mirror state | Presence and adjustability of mirrors is an inspection item; condition remains visual |
| `Vehicle.LowVoltageBattery.CurrentVoltage` / `NominalVoltage` | sensor / attribute | 12/24 V battery | Battery and charging-system check |
| `Vehicle.Service.IsServiceDue` / `DistanceToService` / `TimeToService` | sensor | Manufacturer service schedule | Supporting evidence, not an inspection item |
| `Vehicle.CurrentOverallWeight`, `Vehicle.GrossWeight`, `Vehicle.CurbWeight` | sensor / attribute | Vehicle weights | GVW confirmation (Japan weight tax, commercial vehicles) |
| `Vehicle.Cabin.Seat.RowN.*.Airbag.IsEnabled` | sensor | Airbag system enabled | Airbag warning-lamp check; `IsDeployed` is incident evidence |

**Source vspec:** `spec/ADAS/ADAS.vspec`, `spec/Body/ExteriorMirrors.vspec`, `spec/Vehicle/Battery.vspec`, `spec/Vehicle/Service.vspec`, `spec/Vehicle/Vehicle.vspec`, `spec/Cabin/Seat.vspec`

---

### 11.9 VSS Gap Summary — Fields Needed in Inspection Credential with No VSS Coverage

The following inspection data points have **no corresponding VSS signal** in VSS 6.1 and must be carried as credential-specific fields or covered by a VSS extension/overlay:

| Inspection Item | Gap | Suggested credential field | Priority |
|----------------|-----|---------------------------|----------|
| **Tire tread depth** | No VSS signal (nor J1939 SPN) | `tire.treadDepth_mm` per wheel, with measurement source | High — the most common failure item; see section 12 |
| **Headlight aim / alignment** | Inspector-measured only (optical tester) | `lighting.beamAim.result` (PASS/FAIL) | High |
| **Tailpipe CO ppm** | Analyser-measured; not from ECU | `emissions.co_ppm` | High |
| **Tailpipe HC ppm** | Analyser-measured | `emissions.hc_ppm` | High |
| **Tailpipe NOx ppm** | Analyser-measured | `emissions.nox_ppm` | High |
| **Diesel smoke opacity (%)** | Analyser-measured | `emissions.opacity_pct` | High |
| **OBD readiness monitor bitmap** | OBD overlay only | `emissions.obdReadinessBitmask` (uint16) | Medium |
| **MIL (Check Engine Light) state** | OBD overlay only; no catalogue replacement | `emissions.isMILOn` (boolean) | Medium — critical for US/KR/CN I/M |
| **Seat belt condition / anchorage** | No VSS condition signal (only occupant belt-fastened state) | `restraints.result` (PASS/FAIL) | Medium |
| **Steering play / power-steering condition** | `SteeringWheel.Angle` only; no wear or fault signal | `steering.result` (PASS/FAIL) | Medium |
| **Horn defect** | `Horn.IsActive` only; no `IsDefect` | `horn.result` (PASS/FAIL) | Low |
| **Windshield condition (cracks, tint)** | No VSS signal | `glazing.result` (PASS/FAIL) | Low (visual) |
| **Exhaust system integrity / noise** | No VSS signal | `exhaust.result`, `noise_dBA` | Medium — noise limits inspected in EU, JP, KR |
| **Suspension geometry (camber, toe, caster)** | No VSS signal | `suspension.alignment.result` (PASS/FAIL) | Medium |
| **Brake efficiency (%) / deceleration rate** | Rollerbrake tester output | `brakes.efficiency_pct` per axle | Medium |
| **Structural integrity / bodywork** | Visual inspection only | `bodywork.result` (PASS/FAIL) | Low (not automatable) |
| **Weight tax / GVW confirmation** (Japan) | Administrative | `weight.gvw_kg`, `weight.taxPaidConfirmed` | Japan-specific |
| **ADS software identification (RxSWIN, ADS version, update state)** | No VSS signal; `Vehicle.VersionVSS` is the catalogue version, `ControlUnit` has no software identification field | `software.rxswin[]`, `software.adsVersion` | High for automated vehicles; the hinge of ADS roadworthiness in every regime surveyed (section 14) |
| **ADS sensor calibration / degradation** | No sensor branch in VSS 6.1 | `sensors[].isCalibrated`, `.isDegraded` | High for automated vehicles (section 14.3) |
| **ODD declaration and in-ODD status, DSSAD availability, remote supervision, ADS event counters** | Only `ADAS.ActiveAutonomyLevel`/`SupportedAutonomyLevel`, per-system `IsError` and `Connectivity.IsConnectivityAvailable` exist | `odd.*`, `dssad.*`, `remoteSupervision.*`, `counters.*` | Medium; required by in-service reporting regimes (section 14.3) |

---

### 11.10 VSS Signal Snapshot Pattern for Inspection Credential

Following the `VSSSnapshot` pattern established for the FNOL credential, an inspection evidence block would look like:

```json
"inspectionEvidence": {
  "type": "VSSSnapshot",
  "capturedAt": "2026-07-23T09:14:00Z",
  "odometer": { "signal": "Vehicle.TraveledDistance", "value": 48500, "unit": "km" },
  "brakes": {
    "row1Left":  { "signal": "Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.PadWear",  "value": 62, "unit": "percent" },
    "row1Right": { "signal": "Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.PadWear", "value": 58, "unit": "percent" },
    "row2Left":  { "signal": "Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.PadWear",  "value": 44, "unit": "percent" },
    "row2Right": { "signal": "Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.PadWear", "value": 41, "unit": "percent" },
    "fluidLevel": { "signal": "Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.FluidLevel", "value": 85, "unit": "percent" }
  },
  "tires": {
    "row1Left":  {
      "pressure": { "signal": "Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure", "value": 230, "unit": "kPa" },
      "treadDepth_mm": 6.2,
      "treadDepthSource": "inspector-measured",
      "tireIdentifier": "DOT-XXXX-XXXX-1225"
    },
    "row1Right": {
      "pressure": { "signal": "Vehicle.Chassis.Axle.Row1.Wheel.Right.Tire.Pressure", "value": 228, "unit": "kPa" },
      "treadDepth_mm": 5.9,
      "treadDepthSource": "inspector-measured",
      "tireIdentifier": "DOT-XXXX-XXXX-1225"
    }
  },
  "engine": {
    "oilLevel":         { "signal": "Vehicle.Powertrain.CombustionEngine.EngineOil.Level", "value": "NORMAL" },
    "oilLifeRemaining": { "signal": "Vehicle.Powertrain.CombustionEngine.EngineOil.LifeRemaining", "value": 4320000, "unit": "s" },
    "coolantTemp":      { "signal": "Vehicle.Powertrain.CombustionEngine.EngineCoolant.Temperature", "value": 91.5, "unit": "Celsius" }
  },
  "emissions": {
    "dtcCount": { "signal": "Vehicle.Diagnostics.DTCCount", "value": 0 },
    "dtcList":  { "signal": "Vehicle.Diagnostics.DTCList",  "value": [] },
    "isMILOn":  false,
    "obdReadinessBitmask": "0x0000",
    "dpfDeltaPressure": { "signal": "Vehicle.Powertrain.CombustionEngine.DieselParticulateFilter.DeltaPressure", "value": 2100, "unit": "Pa" },
    "tailpipe": {
      "co_ppm":      142,
      "hc_ppm":      18,
      "nox_ppm":     45,
      "opacity_pct": 8.2,
      "standard":    "EU6d",
      "measuredBy":  "Horiba MEXA-584L",
      "source":      "inspector-measured"
    }
  },
  "lighting": {
    "lowBeamDefect": { "signal": "Vehicle.Body.Lights.Beam.Low.IsDefect", "value": false },
    "highBeamDefect": { "signal": "Vehicle.Body.Lights.Beam.High.IsDefect", "value": false },
    "brakeLightDefect": { "signal": "Vehicle.Body.Lights.Brake.IsDefect", "value": false },
    "indicatorDefectLeft": { "signal": "Vehicle.Body.Lights.DirectionIndicator.Left.IsDefect", "value": false },
    "absError": { "signal": "Vehicle.ADAS.ABS.IsError", "value": false },
    "beamAim": { "result": "PASS", "source": "inspector-measured" }
  },
  "wipers": {
    "frontWear": { "signal": "Vehicle.Body.Windshield.Front.Wiping.WiperWear", "value": 22, "unit": "percent" },
    "washerFluidLow": { "signal": "Vehicle.Body.Windshield.Front.WasherFluid.IsLevelLow", "value": false }
  }
}
```

**Design note:** Fields with a `"signal"` key are VSS-sourced snapshots (read from the vehicle); fields without are inspector-measured and attributed to the inspection station's equipment. This mirrors the `VSSSnapshot` + `evidence` pattern from the FNOL credential and makes the provenance of each data point explicit in the credential.

**Source vspec files consulted:**
- `spec/Chassis/Wheel.vspec` — brake pad wear, tire pressure/temperature
- `spec/Chassis/Chassis.vspec` — tire dimensions, brake pedal, parking brake, steering
- `spec/Body/Body.vspec`, `StaticLights.vspec`, `BrakeLights.vspec` — lighting, wipers
- `spec/Powertrain/CombustionEngine.vspec` — engine oil/coolant, DPF, DEF
- `spec/Powertrain/TractionBattery.vspec` — EV/BEV battery SoH
- `spec/Powertrain/Transmission.vspec` — clutch wear
- `spec/Vehicle/Diagnostics.vspec` — DTC count/list (catalogue paths)
- `spec/ADAS/ADAS.vspec` — ABS/ESC/TCS/EBD/EBA state and error
- `spec/Body/SignalingLights.vspec`, `spec/Body/ExteriorMirrors.vspec` — indicators, hazards, mirrors
- `spec/Vehicle/Battery.vspec`, `spec/Vehicle/Service.vspec`, `spec/Safety/Safety.vspec` — 12 V battery, service, safety branch
- `overlays/extensions/OBD/OBD.vspec` — OBD PID mappings (removed from catalogue in VSS 6.0; overlay only)

---

### 11.11 Proposed VSS Additions for Inspection Evidence

The proposal below covers every item in 11.9, in three tiers, so that an inspection credential can be assembled entirely from VSS paths regardless of how each value was obtained:

1. **Sensor-backed signals** — state the vehicle can report today or with modest ECU work (tread depth where a sensor or estimator exists, MIL state, readiness monitors, defect flags for horn, power steering, dampers, seat belts, exhaust leaks).
2. **Derived signals** — no direct sensor, but a value can be calculated from other signals; each description states the computation and how the value is assigned (tire wear rate and remaining distance from successive tread depths and distance; steering free play from steering-wheel angle versus axle steering angle; damper effectiveness from vertical-acceleration decay; headlamp aim from the ADAS camera's view of the beam cut-off; catalyst efficiency from oxygen-sensor switching). Where a signal can be either measured or estimated, a companion `*Source` enum records which.
3. **Inspector-assessed signals** under a new `Vehicle.Inspection` branch — items that today require a human (bodywork, underbody, glazing, mirrors, steering and suspension play, alignment, exhaust condition, restraints) or station equipment (gas analyser, opacimeter, particle counter, roller brake tester, side-slip plate). The inspector or the station device assigns the value; the description says how (visual/tactile check, play detector, full-extension belt pull, analyser at prescribed idle). Condition items use the Directive 2014/45/EU Article 7 grades `NONE / MINOR / MAJOR / DANGEROUS` plus `NOT_ASSESSED`; pass/fail jurisdictions map PASS→NONE and FAIL→MAJOR. Writing these to the vehicle means they travel with it, can be compared at the next inspection, and give the head-unit assistant of section 13 a place to pre-populate from the previous result.

The overlay is at `tmp/inspection-vss-extension/inspection.vspec` and validates against VSS 6.1 with `vspec export json … -l inspection.vspec`. Wheel-level signals are written for `Row1.Wheel.Left` and instantiate across all axles and wheels; seat-level signals for `Row1.DriverSide`.

**Tier 1 — sensor-backed**

| Proposed signal | Type / datatype / unit | Purpose | Inspection item |
|---|---|---|---|
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.TreadDepth` | sensor, float, mm | Minimum remaining tread depth across main grooves | Tread depth (all jurisdictions) |
| `…Tire.TreadDepthInner` / `TreadDepthCenter` / `TreadDepthOuter` | sensor, float, mm | Per-groove depth; detects uneven wear (alignment, pressure) | Tread depth; alignment proxy |
| `…Tire.IsTreadDepthLow` | sensor, boolean | At or below legal/fleet threshold (analogue of `IsPressureLow`) | Tread depth |
| `…Tire.TreadDepthSource` | sensor, string enum: `MEASURED_GAUGE`, `MEASURED_SCANNER`, `ESTIMATED_WHEEL_SPEED`, `ESTIMATED_TIRE_SENSOR`, `UNKNOWN` | Provenance of the value — essential while estimates are uncertified | Tread depth |
| `…Tire.TreadDepthTimestamp` | sensor, string, iso8601 | When measured or estimated | Tread depth |
| `…Tire.Identifier` | attribute, string | DOT/TIN serial or RFID EPC; wear history follows the tire across rotations | Tire identity (fleet programmes, section 12.5) |
| `…Tire.IsRetread` | attribute, boolean | Retread status (commercial vehicles) | Tire condition |
| `Vehicle.Diagnostics.IsMILOn` | sensor, boolean | Catalogue home for the MIL state lost with the OBD branch removal in 6.0 | Emissions I/M (US, KR, CN) |
| `Vehicle.Diagnostics.ReadinessMonitors` | sensor, string[] enum of monitor names | Monitors reporting complete since last clear; complements `DTCList` | OBD readiness (I/M pass/fail gate) |
| `Vehicle.Diagnostics.DistanceSinceDTCClear` | sensor, float, km | Detects codes cleared just before the test | Emissions I/M anti-gaming |
| `Vehicle.Body.Lights.Beam.Low.AimDeviation` | sensor, float, percent | Vertical aim deviation from nominal, from aim tester or automatic-levelling diagnostics | Headlight aim (EU, JP, US states) |
| `Vehicle.Body.Horn.IsDefect` | sensor, boolean | Horn circuit fault; `IsActive` alone cannot show a failed horn | Horn |
| `Vehicle.Chassis.SteeringWheel.IsPowerSteeringError` | sensor, boolean | Power-steering fault | Steering |
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Suspension.IsDamperDefect` | sensor, boolean | Damper fault on vehicles with electronic damping / ride-height sensing | Suspension |
| `Vehicle.Chassis.Axle.RowN.Brake.EfficiencyRatio` | sensor, float, percent | Braking force ÷ axle load (roller tester or deceleration-derived) | Brake efficiency (EU Annex I thresholds) |
| `Vehicle.Chassis.Axle.RowN.Brake.ImbalanceRatio` | sensor, float, percent | Left/right imbalance across the axle | Brake balance |
| `Vehicle.Powertrain.CombustionEngine.Exhaust.IsLeakDetected` | sensor, boolean | Exhaust leak / aftertreatment tamper flagged by the engine controller | Exhaust integrity |
| `Vehicle.Exterior.NoiseLevel` | sensor, float, dB | Stationary or pass-by noise measured at inspection | Noise (EU, JP, KR) |
| `Vehicle.Cabin.Seat.RowN.*.Seatbelt.IsDefect` | sensor, boolean | Buckle / pretensioner / retractor fault | Restraints |

**Tier 2 — derived (description states the computation)**

| Proposed signal | Type / datatype / unit | Derived from | Assigned how |
|---|---|---|---|
| `…Tire.WearRate` | sensor, float, mm per 10,000 km | Successive `TreadDepth` values ÷ `TraveledDistance` between them | Recomputed at each new tread reading; refined by load, pressure and road-class history |
| `…Tire.EstimatedRemainingDistance` | sensor, float, km | (`TreadDepth` − threshold) ÷ `WearRate` | 0 when `IsTreadDepthLow` |
| `Vehicle.Chassis.SteeringWheel.FreePlayAngle` | sensor, float, degrees | `SteeringWheel.Angle` travelled before `Axle.Row1.SteeringAngle` responds, over slow reversals at standstill | Equivalent of the inspector's manual play check; limits typically 10–30° by class |
| `…Wheel.*.Suspension.DampingRatio` | sensor, float, percent | Decay of vertical acceleration after a road input, or shaker-plate tester | Below tester threshold (commonly 40 %) = worn damper |
| `Vehicle.Body.Lights.Beam.Low.AimDeviationSource` | sensor, enum `MEASURED_AIM_TESTER / ESTIMATED_ADAS_CAMERA / ESTIMATED_LEVELLING_SYSTEM / UNKNOWN` | Companion to `AimDeviation` | Camera estimate uses the vehicle's own beam cut-off on a flat surface |
| `Vehicle.Powertrain.CombustionEngine.EstimatedCatalystEfficiency` | sensor, float, percent | Upstream/downstream O₂ sensor switching ratio (OBD catalyst monitor) | Proxy only where the jurisdiction does not require an analyser value |
| `Vehicle.Inspection.WheelAlignment.Condition` (see tier 3) | — | May be inferred between inspections from `TreadDepthInner` vs `TreadDepthOuter` divergence | Confirmed by side-slip plate at inspection |

**Tier 3 — inspector-assessed (`Vehicle.Inspection` branch)**

| Proposed signal | Type / datatype | Assigned how |
|---|---|---|
| `Vehicle.Inspection.Timestamp`, `.Result` (`PASS / PASS_WITH_MINOR_DEFICIENCIES / FAIL / FAIL_DANGEROUS`), `.NextDueDate`, `.Jurisdiction` (ISO 3166-2), `.CredentialReference` | sensor | Written by the inspection workflow when the credential is issued |
| `Vehicle.Inspection.Bodywork.Condition` | sensor, grade enum | Visual/tactile check for corrosion, cracks, sharp edges, insecure parts |
| `Vehicle.Inspection.Underbody.Condition` | sensor, grade enum | Visual and probe/hammer test of structural sections, brake and fuel lines, on lift or pit |
| `Vehicle.Inspection.Glazing.Condition` | sensor, grade enum | Visual check of driver's field of view; tint by light-transmission meter where limited |
| `Vehicle.Inspection.Mirrors.Condition` | sensor, grade enum | Presence, security, glass, adjustability; electrical state from `Body.Mirrors` |
| `Vehicle.Inspection.Steering.Condition` | sensor, grade enum | Wheel rocking and steering turn at standstill; free play from `FreePlayAngle` where computed |
| `Vehicle.Inspection.Suspension.Condition` | sensor, grade enum | Visual plus play detector; damping from `DampingRatio` where computed |
| `Vehicle.Inspection.WheelAlignment.Condition`, `.SideSlip` (mm/m) | sensor | Side-slip plate or alignment rig |
| `Vehicle.Inspection.Exhaust.Condition`; `.CO` (%), `.HC` (ppm), `.NOx` (ppm), `.Lambda`, `.Opacity` (%), `.ParticleNumber` (#/cm³) | sensor | Visual/audible check; station gas analyser, opacimeter and PN counter at the prescribed test condition |
| `Vehicle.Inspection.Restraints.Condition` | sensor, grade enum | Full-extension pull, buckle load, anchorage check; electrical faults from `Seat.*.Seatbelt.IsDefect` |
| `Vehicle.Inspection.Lights.Condition` | sensor, grade enum | Lens condition, colour, security; function from `Body.Lights.*` cycled during inspection, aim from `AimDeviation` |
| `Vehicle.Inspection.Brakes.Condition`, `.ParkingBrakeEfficiency` (%) | sensor | Visual check of discs, drums, hoses; performance from `Axle.*.Brake.EfficiencyRatio` / `ImbalanceRatio` on the roller tester |

Three design points. First, `TreadDepthSource` (and the `"source"` key in the credential snapshot) is what lets a regulator accept estimated values selectively: a `MEASURED_SCANNER` reading and an `ESTIMATED_WHEEL_SPEED` reading can carry different evidentiary weight in the same field. Second, several of these (`ReadinessMonitors`, `DistanceSinceDTCClear`, `IsMILOn`) duplicate content of the optional OBD overlay; proposing them in the catalogue reflects that they are inspection and compliance state that outlives any particular OBD PID mapping, which was the argument for removing the one-to-one OBD branch in the first place. Third, tier 3 deliberately puts human judgement into VSS as data with a stated provenance rather than leaving it outside the model: it is what lets the transition of section 13 proceed item by item — each `Vehicle.Inspection.*.Condition` can be retired from the physical checklist once a tier 1 or tier 2 signal has been shown, across enough paired inspections, to predict it. The automated-vehicle additions (`Vehicle.Software`, `Vehicle.ADAS.ADS`, `Vehicle.ADAS.Sensor`, `Vehicle.Inspection.ADS` and `.PreTrip`) follow the same three tiers and are set out in section 14.3.

---

## 12. Tire Health and Remaining Tread Depth — State of the Art and a Data Programme

Tread depth is the single most common inspection failure item in most jurisdictions (it heads the German HU defect statistics), it is measured only by hand or by drive-over scanner, and no vehicle-data standard carries it — VSS has no `Tire.TreadDepth`, and SAE J1939 PGN 65268 carries tire pressure (SPN 241), temperature (SPN 242) and location (SPN 929) but no tread signal. This section summarises what the market and the literature support, and outlines how inspection data could be used to build a tire-health capability.

### 12.1 Legal minimums

| Jurisdiction | Minimum tread depth |
|---|---|
| EU / UK | 1.6 mm across the central three-quarters of the tread |
| US | 2/32" (1.6 mm) wear bars (FMVSS); FMCSA 49 CFR 393.75: 4/32" steer axle, 2/32" other axles on commercial vehicles |
| Canada | 1.6 mm (provincial regulations) |
| Japan | 1.6 mm; on expressways 2.4 mm for small trucks and 3.2 mm for large trucks and buses |
| South Korea | 1.6 mm |
| China | GB 7258-2017: 3.2 mm steer axle, 1.6 mm other axles |
| India | 1.6 mm |

No jurisdiction surveyed records a numeric tread depth in its periodic inspection record: the UK MOT stores pass/fail plus advisory text ("worn close to legal limit"), and Germany's HU records coded defects. A `VehicleInspectionCredential` that carries per-tire millimetre readings would therefore be new ground-truth data, not a digitisation of an existing field.

### 12.2 Can TPMS plus temperature and vibration sensing estimate tread depth today?

**Pressure and temperature alone: no.** No product or peer-reviewed paper estimates tread depth from TPMS pressure and temperature; they appear only as covariates in wear models (e.g. MegaRide/VESEVO thermal-wear models) and in Goodyear patents for load estimation. Acoustic sensing likewise has no validated tread-depth method — tire-cavity microphone work (Masino et al., 2017) classifies *pavement* wear, not tire wear.

**Adding a tire-mounted accelerometer: partly, at roughly half-millimetre accuracy in controlled conditions.** The physical basis is that a thinner, more flexible tread changes contact-patch length and the radial-acceleration signature at patch entry and exit.

| Study | Method | Data | Reported accuracy |
|---|---|---|---|
| Park et al., *Sensors* 2024 | Inner-liner 3-axis accelerometer at 12.8 kHz, 1-D CNN | 16 tires of one model, buffed to 0/2/4/6 mm, 144 proving-ground runs, 176,047 rotations | RMSE 0.42 mm (5.2 %) accelerometer only; 4.6 % adding pressure and load |
| Kim et al., *Sensors* 2023 | Finite-element simulation validated on drum; compares wheel-speed, accelerometer and fused inputs | 180 training / 60 test simulations, 0–90 % wear | RMSE 1.2 mm wheel-speed only; 0.6 mm accelerometer; 0.34 mm wheel-speed + pressure + load; 0.21 mm all inputs |
| Han et al., *IEEE Access* 2023 | Accelerometer intelligent tire, deep-network classifier, 30–80 km/h on road | Proving ground | 95.5 % wear-class accuracy |
| Ge et al., *Measurement* 2025; Prasshanth & Sugumaran 2024 | Accelerometer + PVDF film / vibration feature fusion | Bench and road | Wear-level classification |

Commercially, **Continental ContiConnect** (new sensor generation, launched 2025 for truck and bus tires) combines a radial accelerometer with pressure, temperature and mileage in an AI model that reports tread depth and remaining mileage daily — the first shipping automated tread-depth estimate, but with no published accuracy. **Sensata's Tire Mounted Sensor / Tread Depth Monitor** (2023) is reported at about ±1 mm. **Pirelli Cyber Tyre** (in production on McLaren and Pagani models, with Bosch) and **Bridgestone's Smart Strain Sensor** claim wear estimation but have not published accuracy, and Pirelli's CTO describes wear-rate algorithms as still being worked on. Goodyear's own 2025 SightLine white paper states that "no mature or scalable direct sensing technologies are currently available for monitoring tire wear or grip."

**Software-only estimation from wheel speed: works for mean wear, needs calibration.** Because roughly 3 mm of tread loss reduces effective rolling radius by about 1 mm (Goodyear), wear can be inferred from per-wheel speed and rolling-radius drift already on the CAN bus. **NIRA Dynamics' Tread Wear Indicator** (launched February 2025, building on its indirect TPMS used across Audi/VW), **Sumitomo SENSING CORE** (tread-rigidity method, 2021; production so far limited to wheel-detachment and load functions) and **Michelin SmartWear** (wheel speed, vehicle speed, pressure, temperature, RPM; deployed in-vehicle via Sonatus, CES 2026) all take this route. Limitations are consistent: mean wear across the patch only, degraded performance on permanent all-wheel drive, and recalibration whenever tires, road surface or compound change.

**Cameras.** Drive-over laser/camera scanners are accurate (Goodyear CheckPoint ±0.3 mm; Sigmavision TreadReader <0.2 mm; Michelin QuickScan electromagnetic 0.1 mm) and handheld smartphone scanning (Anyline) is available, but these are depot or inspection-station equipment. Vehicle-mounted cameras and edge inference could in principle measure tread, but standard ADAS and surround-view cameras see at most the tire sidewall, not the tread face. Onboard camera-based tread measurement would need either a dedicated wheel-well camera or an ADAS/AV use case — automated parking or an autonomous vehicle's pre-trip self-check are the plausible candidates — that justifies that field of view. Until then, onboard tread estimation comes from accelerometer or wheel-speed models, and camera measurement stays at the depot gate.

**Bottom line:** TPMS + temperature + vibration is sufficient to estimate remaining tread depth only if "vibration" means a tire-mounted accelerometer, and only to ~0.4–1 mm today, validated on single tire models under controlled conditions. Combining wheel-speed drift, TPMS pressure and temperature, load and mileage with periodic ground-truth measurements is the practical path — and fleets and inspection stations are the only place the ground truth exists at scale.

### 12.3 Public data

No public dataset pairs tire-mounted sensor or wheel-speed telemetry with measured tread depth. The nearest are a synthetic Kaggle tire-wear set, a Mendeley vehicle-dynamics set with low-pressure variants but no tread, NHTSA UTQG treadwear grades (no sensor data), and the JRC's 2025 literature synthesis of wear rates (front tires roughly 1.0–1.2 mm and rear 0.5–0.6 mm per 10,000 km; about 250 g of rubber per millimetre). The academic results above rest on 16 tires. This is the gap an inspection-credential programme can close.

### 12.4 Standards context

- **UN R141 (TPMS)**: 01 series extended scope to M2/M3, N1–N3 and O3/O4; mandatory for all new heavy vehicles in the EU from July 2024. Pressure only — no wear provision, but it guarantees per-wheel pressure and (on most sensors) temperature data exist on new vehicles.
- **Tire abrasion**: Euro 7 (Regulation (EU) 2024/1257) introduces tyre abrasion limits from 2028 using the UN R117 abrasion test methods adopted in 2024; WP.29 adopted C1 limits in June 2026. This creates regulatory demand for in-service wear data.
- **COVESA VSS**: the `Tire` branch holds `Pressure`, `IsPressureLow`, `RubberTemperature`, `AirTemperature` and `WinterStatus` only. Proposed additions: `Tire.TreadDepth` (mm, minimum across grooves), `Tire.TreadDepthInner/Center/Outer` (uneven-wear detection), `Tire.TreadDepthSource` (MEASURED_GAUGE, MEASURED_SCANNER, ESTIMATED_WHEELSPEED, ESTIMATED_SENSOR), `Tire.TreadDepthTimestamp`, and a `Tire.Identifier` (DOT/RFID) so wear history follows the tire, not the wheel position. These belong in a VSS pull request or a COVESA commercial-vehicle overlay.

### 12.5 Programme outline: inspection-collected data as the training set

The programme uses the inspection credential itself as the ground-truth collection instrument, then pairs it with telemetry the vehicle already produces.

1. **Ground truth at every inspection touchpoint.** Each periodic inspection, and ideally each fleet yard return, records per-tire, per-groove tread depth (drive-over scanner at ±0.2–0.3 mm or calibrated gauge), timestamp, wheel position (axle, side, inner/outer dual), tire identity (DOT serial or RFID), retread status, and inspector/equipment ID. These become fields of the `VehicleInspectionCredential` (section 11.10), signed by the station, so the data carry provenance.
2. **Continuous telemetry between touchpoints.** From the vehicle: per-wheel TPMS pressure and temperature (R141 fitted on new heavy vehicles), per-wheel speed and derived rolling radius, vehicle speed, odometer, ambient temperature, brake and accelerator activity, and — where fitted — tire-mounted accelerometer features (contact-patch length, radial-acceleration signature). From the telematics platform: axle load (weigh-in or rolling-radius-derived), route/road class, weather, driver.
3. **Pairing.** Each ground-truth reading is joined to the telemetry window since the previous reading, giving labelled wear-per-distance samples under known load, temperature and road conditions. Tire identity keeps the label with the tire across rotations and vehicle changes.
4. **Scale.** The literature uses 16 tires and one model. A credible fleet model needs hundreds to low thousands of tires across several tire models and duty cycles, with wear spanning new to legal limit; Michelin's 2020–22 study of 6,806 dismounted truck tires shows the order of magnitude fleets already generate. Goodyear notes that outdoor treadwear calibration "is impractical on a large scale" — which is precisely what paired inspection data would replace.
5. **Outputs.** First a per-tire wear-rate and remaining-life estimate with confidence, then a threshold alert (`IsTreadDepthLow`) analogous to `IsPressureLow`, and finally an *estimated* tread depth that can be pre-populated into the next inspection credential for the inspector to confirm or correct — closing the loop and improving the model with every inspection.
6. **Governance.** Tire-level data identify vehicles and drivers indirectly; collection should run under the same consent and data-minimisation model as the FNOL and UBI credentials, with the credential carrying the consent scope. A COVESA-hosted schema for the paired records would let fleets, tire makers and inspection bodies pool data without pooling raw telemetry.

---

## 13. Transition Path: From Inspector-Issued Credentials to Automated Online Inspection

The inspection credential can be introduced without waiting for sensors or regulation to catch up, and each stage generates the data that justifies the next.

### Stage 1 — Physical inspection, inspector-issued credential

The authorised inspector performs today's inspection unchanged, but the outcome is issued as a `VehicleInspectionCredential` signed by the station's DID and referencing the `VehicleRegistrationCredential`. The credential holds exactly what the paper certificate holds (section 9) plus inspector-measured values that most jurisdictions do not currently record numerically — tread depth per tire, headlight aim, brake-tester efficiency, tailpipe values. The holder (owner's wallet or the vehicle) presents it to the registration authority, enforcement or an insurer. No vehicle software is needed, and the EU's pending mandatory electronic certificate (section 3.4) would be satisfied by this stage alone.

### Stage 2 — Head-unit inspection assistant capturing VSS evidence

An application on the head unit (COVESA AOSP SDK, AAOS, or another IVI platform with a VSS data path such as a Kuksa/VISS broker) is opened by the inspector or triggered by the station's verifier. As the inspector walks the standard checklist and cycles the systems — low and high beam, indicators and hazards, brake and reverse lights, horn, wipers and washer, parking brake, ABS/ESC self-test — the app reads the corresponding VSS signals (`Body.Lights.*.IsOn` with `IsDefect`, `Body.Lights.Brake.IsActive`, `Body.Horn.IsActive`, `Body.Windshield.*.Wiping.*`, `Chassis.ParkingBrake.IsEngaged`, `ADAS.ABS/ESC/TCS/EBD/EBA.IsError`), plus the state signals that need no interaction (`Diagnostics.DTCList`, brake pad wear, tire pressure and temperature, oil and coolant level, DPF differential pressure, DEF level, traction-battery state of health, odometer, `Vehicle.Safety.*`). It assembles the `VSSSnapshot` evidence block of section 11.10, signed by the vehicle's DID, and hands it to the station's issuance workflow. The inspector adds the items the vehicle cannot see — tread depth, headlight aim, structural condition, tailpipe analyser readings — and the two evidence sets are issued together in one credential, each field carrying its provenance (`"source": "vehicle"` or `"inspector-measured"`).

Two things happen at this stage. First, the inspection gets faster and more repeatable because the vehicle confirms what the inspector observes. Second, every inspection now produces a paired record: vehicle-reported state next to inspector-measured ground truth for the same moment. That is the training set of section 12.5, and it also reveals where vehicle self-reporting disagrees with physical findings (a lamp with `IsDefect=false` that is dim, a brake `PadWear` that does not match the measured lining).

### Stage 3 — Continuous evidence and pre-populated inspections

With telemetry flowing between inspections, the vehicle or its telematics platform maintains a rolling inspection-readiness view: estimated tread depth and wear rate, brake wear trend, lamp faults as they occur, DTC history, emissions-readiness monitors, battery health. Before the inspection date the head unit pre-populates the credential draft; the inspector's role shifts to verifying the estimates, measuring what remains uninstrumented, and signing. Estimation models improve as each confirmed or corrected value feeds back. Items whose estimates prove reliable over a statistically adequate history can be accepted from the vehicle without physical measurement — a decision that belongs to the regulator, informed by the accuracy data the programme itself produces.

### Stage 4 — Automated, online routine inspection with regulatory submission

For the subset of items a jurisdiction accepts from vehicle evidence, routine inspection becomes an online event: on schedule (or continuously), the vehicle assembles a signed `VSSSnapshot`, an authorised issuer (the OEM, a certified telematics provider, or the inspection body acting remotely) verifies it against the jurisdiction's thresholds, issues the `VehicleInspectionCredential`, and the holder submits it to the DMV or transport authority through the same channel used for the registration credential — OpenID4VCI/VC API issuance and OpenID4VP presentation, or the cloud-to-cloud pattern of the FNOL report. The registration authority verifies signatures and revocation status, links the inspection credential to the `VehicleRegistrationCredential`, and renews registration without a station visit. Physical inspection persists only for items that remain uninstrumented (structural integrity, headlight aim until standardised, tread depth until estimates are certified) and for random or risk-based audits, which also continue to supply ground truth.

### 13.5 Business Use Case: Consent-Based Routine Inspection Credentials for Insurers

The regulatory path above depends on states and provinces choosing to accept vehicle evidence, and section 1.4 shows many US states have no periodic inspection at all. A parallel commercial path does not wait for them. An insurer can offer a **"well-maintained vehicle" premium discount** to policyholders who elect to submit a routine inspection credential — monthly or quarterly — generated by the vehicle and, where available, confirmed by a service visit. The insurer's interest is direct: worn tires, worn brakes, failed lamps and ignored warning lamps are causal factors in the claims it pays, and today it has no visibility of them between policy inception and a loss. This is the maintenance analogue of usage-based insurance, and it works in a state with no inspection mandate exactly as it does in one with a strict regime.

**Mechanics.** The policyholder opts in through the insurer's app or the head unit; consent is recorded as a scoped `VehicleInsuranceCredential` term (which signals, at what cadence, for how long — the same consent-record pattern as the UBI credential in the AOSP wallet report, ISO/IEC TS 27560). On each cycle the vehicle assembles a `VehicleInspectionCredential` with `inspectionType: "routine-self"` containing the tier 1 and tier 2 evidence of section 11.11 — tread depth (measured or estimated, with source), brake pad wear, tire pressure history, lamp defect flags, DTC list and MIL state, oil and coolant level, DPF and DEF status, traction-battery health, odometer — signed by the vehicle's DID (co-signed by an attached telematics device where present), and submits it to an insurer endpoint published in the POI credential, mirroring the FNOL `fnolEndpoint`. The insurer verifies signatures and revocation, scores the evidence against its own maintenance thresholds, and applies the discount at renewal or as a running credit. A service-shop visit can add tier 3 items (inspector-assessed bodywork, alignment, analyser values) as a second credential referencing the routine one, at a higher discount tier.

**Why it is attractive to each party.** For the policyholder, the discount is earned by maintenance they already ought to do, with selective disclosure limiting what the insurer sees to the maintenance summary rather than trips or location — the credential can prove "all tires above 3 mm and no active DTCs" without disclosing where the vehicle has been. For the insurer, it is loss prevention with a verifiable audit trail: the same credential that earned the discount is evidence at claim time that the vehicle was roadworthy, and the nudge effect (an app notification that a tire is approaching the threshold and the discount is at risk) reduces the defect-related losses it would otherwise pay. For fleets, the credential doubles as the maintenance record for compliance and resale and can be shared with the leasing company or a buyer. For regulators, a voluntary insurer-driven programme produces the paired vehicle-state and outcome data (defects versus claims) that the crash-rate debate of section 1.4 has lacked — data the insurance industry, which has been conspicuously absent from that debate apart from the Missouri Insurance Coalition's 2025 testimony, is uniquely placed to supply, and it seeds the estimation models of section 12.5 in jurisdictions that have no inspection stations to collect ground truth.

**Design constraints.** The programme must be opt-in with revocable consent and a clear data-minimisation statement; the insurer receives the credential, not a telemetry feed. Discounts must not become a de facto penalty for owners of vehicles without the sensors to produce the evidence — the credential should carry `NOT_ASSESSED` rather than a fail for items the vehicle cannot report, and the discount schedule should reward what is proven rather than penalise what is unknown. Where a jurisdiction does mandate inspection, the routine-self credential complements rather than replaces it, and insurers should accept the regulatory credential as satisfying the same evidence. Rate filings in regulated insurance markets (US state insurance departments, provincial regulators, EU national supervisors) will need the scoring criteria disclosed, which argues for the criteria being expressed in the published VVC vocabulary and VSS signals rather than proprietary scores.

**What it needs from COVESA.** An `inspectionType` enumeration in the credential covering `periodic-regulatory`, `routine-self`, `service-visit` and `pre-trip` (the commercial-vehicle driver inspection required under 49 CFR 396.11/396.13 and NSC Standard 13 is the same credential with a different issuer); an `inspectionEndpoint` property on `VehicleInsuranceCredential` alongside `fnolEndpoint`; and agreement with insurance-industry bodies (ACORD, CSIO, GDV/BiPRO, as surveyed in the FNOL report) on how a maintenance-evidence credential is referenced in policy and claims messages.

### What COVESA needs to specify

- The `VehicleInspectionCredential` type and its evidence provenance fields (section 9, 11.10) in the Vehicle Credentials Vocabulary
- The inspection VSS evidence set and interaction sequence (which signals are captured during which inspector action), as a profile alongside the FNOL evidence set
- An `inspectionType` enumeration (`periodic-regulatory`, `routine-self`, `service-visit`, `pre-trip`) and an `inspectionEndpoint` property on `VehicleInsuranceCredential` for the consent-based insurer programme of 13.5
- VSS additions for the gaps in section 11.9, starting with `Tire.TreadDepth*` and `Diagnostics.IsMILOn`
- The paired-record schema for section 12.5 so ground truth and telemetry can be pooled across fleets and stations
- Alignment with the EU electronic roadworthiness certificate data set once COM(2025) 180 is adopted, and with CA DMV's vehicle credentials programme, so the same credential is accepted on both sides of the Atlantic
- The automated-vehicle extension of section 14: `ads-periodic` and `ads-in-service` inspection types, the `adsCompliance` block, and the driverless `pre-trip` properties

---

## 14. Automated Vehicles: Regulator-Required Inspection and In-Service Monitoring

Sections 1 to 13 cover the roadworthiness, safety and emissions inspection of vehicles that a human drives. Vehicles equipped with an automated driving system (ADS, SAE J3016 Level 3 and above) are subject to a second layer of regulator-required checks that does not exist for conventional vehicles: approval of the ADS itself, periodic verification that the ADS and its sensors are still the approved configuration, and continuous in-service monitoring and reporting by the manufacturer or operator. This section catalogues those obligations as of October 2026, derives the data an ADS inspection or in-service credential would carry, and shows how it fits the `VehicleInspectionCredential` and the transition path of section 13. The companion report [Insuring Autonomous Vehicles: Data Requirements](COVESA_Whitepaper_Insuring_Autonomous_Vehicles_Data_Requirements.md) covers the event-level ADS data (activation, transitions of control, emergency manoeuvres, remote operations, DSSAD alignment) that the insurer and investigator need; this section covers the compliance state of the ADS that the inspector and the in-use regulator need, and the two are designed to reference each other.

### 14.1 Why automated vehicles change inspection

1. **The safety-critical component is software, and it changes.** A conventional inspection assumes the vehicle presented is the vehicle that was approved. An ADS is updated over the air, so the approved state is a software identification, not a part number. UN Regulation No. 156 defines the RxSWIN (RX Software Identification Number, §2.2, "a dedicated identifier, defined by the vehicle manufacturer, representing information about the type approval relevant software of the Electronic Control System") and requires it, or the software versions it covers, to be readable "in a standardized way via the use of an electronic communication interface, at least by the standard interface (OBD port)", and requires the software update management system information to be available for periodic technical inspection ([UN R156 text](https://unece.org/sites/default/files/2024-03/R156e%20(2).pdf); [EU publication, OJ L 82/60](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A42021X0388)). Reading the software identification therefore becomes an inspection item in its own right.
2. **Sensors drift and can be damaged without raising a fault.** CITA's ADAS task force reported in October 2026 that "degradation affecting sensors or ADAS performance may not always generate a stored diagnostic fault", and is developing static radar tests for sensor misalignment and signal attenuation and vehicle-in-the-loop methods for PTI ([CITA, 2 Oct 2026](https://citainsp.org/2026/10/02/advancing-adas-testing-for-pti/)). CITA's 2021 input to the EU Roadworthiness Package already argued that for Level 3 and above "self-diagnostics cannot replace an impartial PTI" and that the self-diagnosis itself, including ODD boundary recognition, should be tested ([CITA, 7 Jul 2021, §2.8–2.9](https://citainsp.org/wp-content/uploads/2021/10/Review-of-the-Roadworthiness-Package-CITAs-input-7-July-2021.pdf)).
3. **The approval is conditional on an operational design domain (ODD).** EU Implementing Regulation 2022/1426 requires the ODD to be declared (precipitation, time of day, light, fog, road markings, road category, geographic area; Annex II §3.1.4) and the ADS to perform a minimal risk manoeuvre at its boundary. Whether the vehicle is operating inside the ODD it was approved for is a compliance question with no analogue in conventional inspection. ISO 34503:2023 provides the ODD taxonomy ([ISO 34503](https://www.iso.org/standard/78952.html)).
4. **Cybersecurity state is part of roadworthiness.** UN R155 requires a certified cybersecurity management system (CSMS) and R156 a software update management system; both apply in the EU to all new vehicles from 7 July 2024 under [Regulation (EU) 2019/2144](https://eur-lex.europa.eu/eli/reg/2019/2144/oj/eng). An ADS whose update channel is compromised is not roadworthy however good its brakes.
5. **There is no driver to do the pre-trip inspection.** 49 CFR 396.13 begins "Before driving a motor vehicle, the driver shall: (a) Be satisfied that the motor vehicle is in safe operating condition" and 396.11 requires the driver to prepare and sign a daily report ([396.11](https://www.ecfr.gov/current/title-49/section-396.11), [396.13](https://www.ecfr.gov/current/title-49/section-396.13)). Germany's AFGBV answers this with a daily "erweiterte Abfahrkontrolle" and a 90-day whole-vehicle check performed by the keeper's qualified staff (§13); CVSA answers it with the Enhanced CMV Inspection performed by certified carrier personnel at the point of origin. Either way the pre-trip inspection becomes an operator-issued record that a roadside officer needs to verify without a driver to question.
6. **Continuous self-monitoring and reporting are already mandated.** Every ADS regime surveyed below requires event recording (DSSAD or equivalent), and most require the manufacturer or operator to report occurrences to the regulator on a schedule. The vehicle is therefore already producing the evidence that Stage 3 and 4 of section 13 rely on; what is missing is a standard way to carry its compliance state.

### 14.2 What regulators require, by jurisdiction

Verified against the primary texts linked. Where a provision could only be confirmed from secondary coverage it is marked (secondary); unece.org blocks automated retrieval, so UN texts were read from mirrors or the GlobalAutoRegs document register.

| Jurisdiction / instrument | Initial approval or permit | Periodic inspection of the ADS | In-service monitoring and reporting | Incident reporting | Who inspects or supervises |
|---|---|---|---|---|---|
| **UN R157 (ALKS, L3)**, original series in force 22 Jan 2021, 01 series (130 km/h, system-initiated lane change) in force 4 Jan 2023 ([UNECE](https://unece.org/sustainable-development/press/un-regulation-extends-automated-driving-130-kmh-certain-conditions); [text mirror, original series Supplement 1](https://www.marklines.com/statics/unece/pdf_202207/R157am1e_0.pdf); 01 series text ECE/TRANS/WP.29/2022/59/Rev.1) | Type approval incl. Annex 4 audit of the safety approach | Annex 4 §3.1: documentation must describe how the operational status of the system, its software version(s) and failure-warning status can be checked via electronic interface, at least the OBD port; Appendix 1 item 3.7 "Provisions for the periodic technical inspection" is a mandatory assessment-report item. No PTI test procedure prescribed | None on the manufacturer (verified negative). DSSAD (§8) records activation, deactivation by each means, transition demands by cause, emergency and minimum risk manoeuvres, EDR trigger, collision, severe failures, and (01 series, §8.2.1(l) to (p)) lane change start, end and abortion; §8.3.2 software version identifiable per occurrence; FIFO overwrite with documented capacity, readable via OBD | Not addressed | Technical Service and type-approval authority |
| **UN R155 (CSMS) / R156 (SUMS, RxSWIN)**, in force 22 Jan 2021; EU: new types 6 Jul 2022, all new vehicles 7 Jul 2024 ([GSR Art. 4, Annex II](https://eur-lex.europa.eu/eli/reg/2019/2144/oj/eng)) | CSMS certificate of compliance and SUMS certificate as preconditions for vehicle type approval | R156: RxSWIN or software versions readable via OBD (§7.2.1.2.2); SUMS information to be available for PTI (§7.1.1.12) | Manufacturer monitors threats and updates throughout the vehicle lifecycle | Not addressed | Approval authority; PTI reads RxSWIN |
| **UN R171 (DCAS, L2)**, in force 22 Sep 2024 ([UNECE](https://unece.org/media/press/395206)); 02 series adopted WP.29 June 2026 ([WP.29/2026/86](https://globalautoregs.com/documents/42373)) | Type approval | Not addressed | 02 series adds a safety management system, mandatory reporting of safety-critical occurrences and periodic reporting with defined metrics, in-service monitoring as a validation method, and software identification aligned with R156; entry into force expected 2027 (secondary) | Per 02 series, to the approval authority | Approval authority |
| **UN GTR No. 26 and UN R185 (ADS)**, adopted WP.29 24 June 2026 ([UNECE press release via CCAM](https://www.connectedautomateddriving.eu/blog/unece-adopts-first-ever-global-rules-allowing-fully-autonomous-vehicles/); [R185, WP.29/2026/137](https://globalautoregs.com/documents/42313); [GTR 26, WP.29/2026/139](https://globalautoregs.com/documents/42319); entry into force of R185 expected January 2027 (secondary)) | Safety management system audited across the lifecycle, safety case ("no unreasonable risk", at least as safe as a competent and careful human driver), obligations extend to suppliers | No PTI test of the ADS itself; §6.3.5.1 requires vehicles without manual controls to provide suitable means (special controls, test modes, ADS functions) so that mandated inspections of other vehicle systems, including periodical technical inspection, can be performed, and §6.3.5 an interface for maintenance and repair | Three-tier in-service monitoring and reporting (§7.4.3): initial notification of critical occurrences without unreasonable delay (§7.4.7.1), short-term reports within 30 days of knowledge of the occurrence (§7.4.8.2), periodic reporting at least every year as aggregated data per hour of operation and distance driven (§7.4.9.3); templates in GTR Annexes 1–4 (R185 Annexes 3–6) | Critical occurrences notified without unreasonable delay | Approval authority; US, EU, Japan, China, UK, Canada voted in favour |
| **UNECE 1997 Agreement (PTI Rules 1–4)** and WP.29 IWG on PTI ([text](https://unece.org/transportvehicle-regulations/text-1997-agreement); [IWG PTI documents](https://globalautoregs.com/groups/94)) | n/a | Rule No. 2 (roadworthiness) and Rule No. 4 (electric/hybrid); IWG PTI proposal PTI-44-02/Rev.1 (Japan and Russia, 18 Sep 2026) for PTI scan-tool provisions in R.E.3 §8.40 (access to in-vehicle data and DTCs through the electronic vehicle interface without affecting software integrity; software version and checksum items unverified). No Rule specific to ADAS/ADS yet | n/a | n/a | National PTI bodies |
| **EU Implementing Regulation 2022/1426** (ADS type approval; predefined area, hub-to-hub, automated valet parking) as amended by [2026/481](https://eur-lex.europa.eu/eli/reg_impl/2026/481/oj) ([2022/1426](https://eur-lex.europa.eu/eli/reg_impl/2022/1426/oj)) | Type approval with scenario assessment, safety-concept assessment and SMS audit (Annex III Parts 1–4); valid SMS certificate required; 2026/481 extends the SMS to suppliers and service providers and opens AVP to unlimited numbers | Annex II point 12 "Provisions for periodic roadworthiness tests": operational status verifiable via the failure-warning signal; "correct functionality and the software integrity" verifiable via the electronic vehicle interface per Directive 2014/45/EU Annex III I.(14), with technical information made available under Implementing Regulation 2019/621 Art. 6 | Annex III Part 5: SMS data-collection processes; Appendix 1 occurrence list (safety-critical occurrences, operation outside ODD, failure to reach MRC, connectivity, cybersecurity, remote-operator interaction, misuse, requests to intervene, maintenance and repair problems, tampering, new scenarios); Annex II §9 on-board recording (activation, remote-operator requests, MRM, MRC, failures, lane changes, EDR trigger) | Safety-critical occurrences "without delay"; occurrences needing remedy within one month; annual aggregated report per hour/km of ADS operation to the granting authority | Type-approval authority, market surveillance, Commission |
| **Directive 2014/45/EU** and **COM(2025) 180** (see 3.4) ([proposal](https://www.europarl.europa.eu/RegData/docs_autres_institutions/commission_europeenne/com/2025/0180/COM_COM(2025)0180_EN.pdf); [EPRS briefing, Jan 2026](https://www.europarl.europa.eu/RegData/etudes/BRIE/2026/782608/EPRS_BRI(2026)782608_EN.pdf)) | n/a | Proposal adds Annex I Section 10 "testing electronic safety systems using the vehicle's electronic interface" and Art. 4(5)–(6) implementing acts covering "the electronic vehicle interface, diagnostic trouble codes, and software versions", supplied free of charge in machine-readable form; recital 14 cites ADAS deterioration and tampering and "safe operation of automated vehicles". Trilogue of 20 Oct 2026 closed most of the test-content annex; conclusive trilogue expected 2 Dec 2026 (secondary) | n/a | n/a | National PTI bodies |
| **Germany: StVG §§1d–1l** (2021) and **AFGBV** (in force 1 Jul 2022, last amended BGBl. 2026 I Nr. 142) ([§1d–1l](https://www.gesetze-im-internet.de/stvg/__1d.html); [AFGBV](https://www.gesetze-im-internet.de/afgbv/BJNR098610022.html)) | KBA Betriebserlaubnis for the vehicle type (§1e(4)); the competent Land authority approves the operating area (§1e(1) Nr. 3, AFGBV §§7–10); Anlage 1 Nr. 7.3 requires the vehicle to be designed so PTI is feasible (manual driving mode, brake tester, headlamp aiming, brake access); Nr. 13.2 non-volatile storage readable via the 16-pin OBD connector | AFGBV §13(1): regular checks of active and passive safety systems per manufacturer repair information; **daily** extended departure check incl. test drive, brakes, steering, lights, tyres, chassis, sensors (§13(7)); **whole-vehicle check every 90 days** (§13(1) Nr. 3); Hauptuntersuchung within six months of registration (§13(8)); records kept 6 months (§13(4)) | Technische Aufsicht (§1d(3), §1f(2)) continuously evaluates status signals, releases alternative manoeuvres, can deactivate; §1g data list incl. VIN, position, activation/deactivation counts and times, system monitoring data **including software state (Softwarestand)** (Nr. 5), connectivity latency and bandwidth, safety-system status, commands received; transmitted to KBA and the competent authority on request, deleted by KBA at the latest 3 years after the vehicle ceases operation | §1g(2) triggers: Technische Aufsicht interventions, conflict scenarios incl. near-misses, unplanned manoeuvres, malfunctions | Keeper's staff with Kfz-Meister qualification and manufacturer training (§13(2)), not a Technical Service; KBA may commission a Technical Service (§3(7)) |
| **France: Ordonnance 2021-443 and Décret 2021-873** (Code des transports L.3151-1 ff., R.3151-1 to R.3153-1; STRA provisions in force 1 Sep 2022) ([ordonnance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043370894); [décret](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043729532); [ministry explainer](https://www.ecologie.gouv.fr/sites/default/files/documents/2021%2007%2001%20-%20Communication%20d%C3%A9cret%20STPA%20-%20Vdef.pdf)) | Vehicle type approval plus a safety demonstration certified by an accredited qualified body (OQA) before entry into service (R.3152-5 to 9) | No STRA-specific PTI provision found; relies on type approval, the operator's maintenance duty (R.3151-1) and SMS (R.3152-11) and the OQA audit | Annual report (R.3152-14) and **annual external audit** (R.3152-15); EDR conforming to UNECE instruments on every vehicle (R.3152-4); remote intervention only by a licensed person with 3-year training attestation and medical certificate (L.3151-3, R.3152-3) | Accidents with injury or significant damage reported without delay (R.3152-22); prefect may order a diagnostic (R.3152-16); STRMTG analyses incidents and publishes an annual report (R.3152-1) | OQA; STRMTG |
| **UK: Automated Vehicles Act 2024** (Royal Assent 20 May 2024) ([Act](https://www.legislation.gov.uk/ukpga/2024/10/contents); [SI 2026/439](https://www.legislation.gov.uk/uksi/2026/439/made); [implementation programme](https://www.gov.uk/guidance/automated-vehicles-act-implementation-programme)) | Authorisation of the vehicle against the statement of safety principles (ss.2–6); Authorised Self-Driving Entity (ASDE, s.6); no-user-in-charge operator licence (ss.12–13); automated passenger service permits up to 5 years (Part 5; regulations in force 15 May 2026) | MOT treatment of authorised AVs not yet addressed by DVSA (unverified) | Part 1 Ch. 3 information duties on ASDEs and operators (information and interview notices); Ch. 5 civil sanctions; the Law Commissions' 2022 report called this the in-use safety regulator ([Law Com 404](https://cdn.websitebuilder.service.justice.gov.uk/uploads/sites/54/2025/12/Automated-vehicles-joint-report-cvr-03-02-22.pdf)) | s.39 duty to detect and investigate incidents; Part 3 Ch. 2 statutory incident inspectors | Secretary of State / DfT with DVSA, VCA, DVLA; full implementation planned 2027; statement of safety principles consulted 30 May to 9 Sep 2026 |
| **US federal (NHTSA)** ([SGO Third Amended](https://www.nhtsa.gov/sites/nhtsa.gov/files/2025-04/third-amended-SGO-2021-01_2025.pdf); [91 FR 48485, 31 Jul 2026](https://www.federalregister.gov/documents/2026/07/31/2026-15483/av-framework-updates-and-request-for-comments-on-interim-guidance); [AV STEP withdrawal, 91 FR 38619](https://www.federalregister.gov/documents/2026/06/26/2026-12980/ads-equipped-vehicle-safety-transparency-and-evaluation-program-withdrawal)) | Self-certification to FMVSS; Part 555 exemptions (up to 2,500 vehicles/yr) now carry modifiable "operational authorization" terms (June 2025); 2026 NPRMs modernise FMVSS 102/103/104/110/135 for vehicles without manual controls; ADS performance rulemaking announced 10 Mar 2026, nothing published | None federal | Standing General Order 2021-01 (Third Amended, effective 16 Jun 2025): 5-calendar-day report for crashes with fatality, hospital transport, vulnerable road user, airbag or (ADS only) tow-away where ADS or L2 engaged within 30 s; monthly report by the 15th for other ADS crashes (property damage over $1,000, or any single-vehicle or struck-object crash); NHTSA is drafting a rule to codify the SGO (RIN 2127-AM63). AV STEP (voluntary independent assessment, quarterly reporting) withdrawn 26 Jun 2026 | 5 days / monthly as above | NHTSA; states for operation |
| **California DMV, 13 CCR Art. 3.7–3.8** (adopted 28 Apr 2026; some provisions in immediate effect, the reporting sections operative 120 days after the effective date) ([DMV release](https://www.dmv.ca.gov/portal/news-and-media/new-autonomous-vehicle-regulations-strengthen-oversight-and-enforcement-authorize-trucks-and-transit/); [Art. 3.7 text](https://www.dmv.ca.gov/portal/file/order-to-adopt-article-3-7-regulations-pdf/); [Art. 3.8 text](https://www.dmv.ca.gov/portal/file/order-to-adopt-article-3-8-regulations-pdf/)) | Drivered testing, driverless testing and deployment permits with mileage gates (50,000 autonomous miles per stage light-duty; 500,000 per stage heavy-duty with 100,000 in the California ODD; §227.42, §228.08) and a safety case; heavy-duty vehicles over 10,001 lb now permitted | No AV-specific periodic inspection; the safety case (defined in §227.02) must include processes for maintenance inspections and schedules; heavy-duty AVs must still stop at CHP weigh stations and meet state and federal CMV requirements, with remote-driver records held under the CHP Basic Inspection of Terminals programme (VC 34501.12, §227.38); CHP terminal inspection reports within 30 business days are required only of the public-entity passenger-bus exemption (§227.26) | Monthly under testing permits, quarterly under deployment permits: DDT-performance-relevant system failures with test-driver takeover (§227.56; the former annual disengagement report no longer appears in the adopted text), vehicle immobilizations (§227.58, §228.36), VMT by permit type (§227.60, §228.40), hard-braking events (deceleration above 5 m/s² for at least 0.5 s with a speed decrease of at least 3 m/s on roads posted 35 mph or more; §227.66); Notice of AV Noncompliance from 1 Jul 2026 (§227.68, §228.42) | Collisions: the full NHTSA SGO crash report filed with DMV within SGO timeframes (§227.54, §228.34; the former form OL 316 no longer appears in the adopted text); certified 30-second pre-crash sensor recorder with 3-year retention | DMV; CHP for heavy-duty terminals |
| **California PUC** ([D.24-11-002](https://docs.cpuc.ca.gov/PublishedDocs/Published/G000/M546/K031/546031802.PDF); [quarterly reporting](https://www.cpuc.ca.gov/regulatory-services/licensing/transportation-licensing-and-analysis-branch/autonomous-vehicle-programs/quarterly-reporting)) | Drivered/driverless pilot and deployment permits for passenger service | n/a | Quarterly reports from Q1 2025: VMT, waiting time, vehicle occupancy, trips, wheelchair-accessible rides; stoppage events (incident-level ≥2 min, fleet-level ≥30 s) for operators over 300 trips/quarter | Unredacted NHTSA SGO collision reports filed simultaneously with CPUC for collisions in passenger service | CPUC |
| **Texas SB 2807** (effective 1 Sep 2025; TxDMV authorization enforceable 28 May 2026) ([bill](https://capitol.texas.gov/tlodocs/89R/billtext/html/SB02807F.HTM); [TxDMV](https://www.txdmv.gov/AVprogram)); **Arizona A.R.S. §28-9702** ([statute](https://www.azleg.gov/ars/28/09702.htm)) | TX: TxDMV authorization for commercial driverless operation, emergency-responder interaction plan filed with DPS, vehicle must achieve a minimal risk condition on ADS failure (§545.455); 30-day duty to update (§545.456); suspension/revocation (§545.459). AZ: law-enforcement interaction plan to ADOT and DPS and written self-certification to ADOT | None | TX: none beyond authorization upkeep; AZ: none | Not specified beyond general traffic law | TxDMV / DPS; ADOT / DPS |
| **FMCSA and CVSA** (driverless CMVs) ([FMCSA ANPRM 84 FR 24449, 2019](https://www.federalregister.gov/documents/2019/05/28/2019-11038/safe-integration-of-automated-driving-systems-equipped-commercial-motor-vehicles); [CVSA Enhanced Inspection, UGPTI deck Sep 2025](https://www.ugpti.org/resources/proceedings/downloads/2025-09-16-ATC-enhanced-inspection-procedures.pdf); [CVSA announcement, Oct 2022](https://cvsa.org/news/new-enhanced-cmv-inspection-program/); [warning-beacon exemption, 91 FR 64736](https://www.federalregister.gov/documents/2026/10/09/2026-20734/parts-and-accessories-necessary-for-safe-operation-application-for-exemption-from-aurora-operations)) | USDOT number and FMCSA safety fitness as for any carrier; no ADS-specific federal rule since the 2019 ANPRM | 49 CFR 396.11/396.13 driver pre-trip and daily report presuppose a driver. CVSA Enhanced CMV Inspection Standard, checklist and 40-hour course approved Sep 2022; Operational Policy 20 (May 2025) covers the electronic decal and roadside, post-crash and terminal inspections: a **no-defect, point-of-origin inspection by CVSA-certified motor-carrier personnel** before dispatch and periodically in transit, uploaded to the Vehicle Inspection Program Repository (VIPR) as an electronic decal; an in-transit inspection is required within 24 hours and each inspection starts a new 24-hour period | ADS-engaged vehicle with a current electronic decal bypasses inspection stations; roadside stops limited to imminent hazard | Crash reporting per 49 CFR 390 and SGO | Carrier's CVSA-certified inspectors; state CMV enforcement |
| **Japan: Road Vehicles Act** (自動運行装置 in safety standards from 1 Apr 2020) and **Road Traffic Act** (特定自動運行 Level 4 permits from 1 Apr 2023) ([MLIT framework](https://www.mlit.go.jp/jidosha/content/001851520.pdf); [NPA](https://www.npa.go.jp/english/bureau/traffic/selfdriving.html); [OBD検査](https://www.mlit.go.jp/jidosha/jidosha_OBD.html)) | MLIT approval of the automated driving device against 保安基準 Art. 41; program changes to the device, including OTA, need prior MLIT permission (特定改造等の許可, Art. 99-3); Level 4 operation permit from the prefectural Public Safety Commission, revocable or suspendable up to 6 months | Shaken includes **OBD検査** from 1 Oct 2024 (domestic; imports 1 Oct 2025) for new models from Oct 2021 (imports Oct 2022): DTCs of driver-assistance devices, the automated driving device and emissions controls read against the NALTEC 特定DTC server; workshops touching the ADS need 特定整備 certification | 作動状態記録装置 (operating-state recorder) records ADS on/off, takeover requests, driver state and failures; retention 6 months or 2,500 records; 特定自動運行主任者 performs remote monitoring (no driving licence required unless the supervisor will drive the vehicle; NPA guidance, secondary) | Permit conditions; 12 Level 4 permits cumulative by May 2026 (secondary) | MLIT / NALTEC; prefectural Public Safety Commission |
| **China: four-ministry L3/L4 pilot notice** (17 Nov 2023), **GB 44497-2024** DSSAD (in force 1 Jan 2026), **Beijing AV Regulation** (in force 1 Apr 2025), **Shenzhen ICV Regulation** (2022, amended 2026) ([notice](https://www.gov.cn/zhengce/zhengceku/202311/content_6915788.htm); [GB 44497-2024](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=96DC64D0633EEFBAFCA545EF906757C2); [Beijing](https://www.beijing.gov.cn/zhengce/dfxfg/202501/t20250103_3980149.html); [Shenzhen 2026](https://www.sz.gov.cn/zfgb/2026/gb1418/content/post_12873301.html)) | Product 准入 pilot then road-use pilot in designated zones; first 9 consortia June 2024; Beijing Art. 26 safety assessment by expert review or recognised third-party laboratory before plates; Art. 27 operator qualification incl. cyber and data security | Beijing Art. 36: real-time safety monitoring platform **and periodic third-party safety inspection** (procedure set by the economy and IT department); Shenzhen Art. 28: on-board safety data connected to the government platform as a registration condition | Vehicles connected to the MIIT pilot management system; software updates subject to filing; no unauthorised ADS changes; Beijing Art. 28 operating data recorded and submitted, Art. 37 mandatory safety officers and platform monitors; GB 44497-2024 mandates the on-board DSSAD for M and N vehicles (with GB 44495 cybersecurity and GB 44496 software update) | "Timely" (及时) reporting to the provincial authority; Beijing Art. 31–32 immediate report to traffic police and provision of accident process data on request | MIIT / MPS / MOT; Beijing municipal departments |
| **South Korea: AV Commercialisation Act** (in force 1 May 2020) and Level 4 performance certification (in force 20 Mar 2025) ([Act](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%9E%90%EC%9C%A8%EC%A3%BC%ED%96%89%EC%9E%90%EB%8F%99%EC%B0%A8%EC%83%81%EC%9A%A9%ED%99%94%EC%B4%89%EC%A7%84%EB%B0%8F%EC%A7%80%EC%9B%90%EC%97%90%EA%B4%80%ED%95%9C%EB%B2%95%EB%A5%A0); [MOLIT L3 standard 2020](https://www.molit.go.kr/USR/NEWS/m_71/dtl.jsp?lcmspage=2&id=95083365); [2025 regime](https://www.law-lin.com/ko/newsletter/1042)) | Temporary operation permit (Motor Vehicle Management Act Art. 27) confirmed by the performance-testing agent (KOTSA); Level 3 safety standard (Rules Art. 111-3, 별표 27, 2020, aligned to R157 in 2022); Level 4 성능인증 and 적합성 승인 for public bodies and licensed carriers | Enforcement Rules Art. 25 (under Act Art. 43(3)) provide periodic inspection of certified AVs at MOLIT-designated sites by the dedicated agency, items incl. malfunction of the EDR and the autonomous-driving information recorder; interval to be reviewed every 3 years from 1 Jan 2025 (Rules Art. 33) (secondary mirror) | Act Art. 43(2) with Enforcement Decree Art. 35-7: EDR and autonomous-driving information recorder data retained at least 6 months; Act Art. 49 and Decree Art. 35-12: dedicated agency | Not specified in sources consulted | MOLIT; KOTSA |
| **Singapore** ([Rules 2017](https://sso.agc.gov.sg/SL/RTA1961-S464-2017?DocDate=20170823); [LTA AV page](https://www.lta.gov.sg/content/ltagov/en/industry_innovations/technologies/autonomous_vehicles.html); [TR 68:2021](https://www.lta.gov.sg/content/ltagov/en/newsroom/2021/9/news-releases/enhanced-national-standards-for-the-safe-deployment-of-autonomou.html)) | LTA authorisation under the Road Traffic (Autonomous Motor Vehicles) Rules 2017; CETRAN M1 closed-circuit and M2 complex/driverless assessments, remote-operations assessment, Deployment Readiness Assessment (continuous on-road, data-backed) | No periodic re-inspection regime described | Black-box telematics recorder; TR 68 Parts 1–4 (behaviour, safety, cybersecurity, data formats) voluntary unless mandated | Incident-reporting duty in the Rules | LTA; CETRAN |
| **Australia: Automated Vehicle Safety Law** (Commonwealth, decided Feb 2022) ([ITMM communique](https://www.infrastructure.gov.au/sites/default/files/documents/16th_itmm_communique_11_februrary_2022.pdf); [NTC](https://www.ntc.gov.au/transport-reform/automated-vehicle-program)) | First supply via ADRs under the Road Vehicle Standards Act 2018, informed by the UN GTR; Automated Driving System Entity (ADSE) with a general safety duty for in-service operation | Not yet legislated | ADSE general safety duty; national in-service regulator proposed; framework to be finalised by 2027, conditional deployment from 2027 in selected locations (Nov 2025 ministers' decision, secondary); no bill introduced as of Oct 2026 | Not yet legislated | Proposed national AV regulator; state trial laws meanwhile |
| **Canada** ([TC testing guidelines v2.0, 2021](https://tc.canada.ca/en/road-transportation/innovative-technologies/connected-automated-vehicles/guidelines-testing-automated-driving-systems-canada); [Safety Framework 2.0, Feb 2025](https://tc.canada.ca/en/road-transportation/innovative-technologies/connected-automated-vehicles/canada-s-safety-framework-connected-automated-vehicles-20); [GTR consultation 2026](https://tc.canada.ca/en/corporate-services/consultations/united-nations-global-technical-regulation-automated-driving-systems); [Ontario pilot](https://www.ontario.ca/page/automated-vehicle-pilot-program)) | Voluntary Safety Assessment (2019); MVSA s.9 exemptions; provinces authorise trials (Ontario O. Reg. 306/15 pilot for passenger, commercial and streetcar vehicles; Automated Commercial Motor Vehicle Pilot for trucks over 4,500 kg, 1 Aug 2025 to 1 Aug 2035) | Not addressed federally; provincial PMVI applies to CMVs (section 2) | Transport Canada consulted 6 Mar to 1 May 2026 on the UN GTR as a basis for a future CMVSS | Guidelines: preliminary report of injury or fatal collisions to the provincial road administrator within 24 h and pause trials; Ontario ACMV pilot: MTO notified within 24 h of any safety incident or collision | Transport Canada; provinces |

Two patterns stand out. First, every regime makes **software identification readable at inspection** the hinge of ADS roadworthiness: R156 RxSWIN via OBD, R157 Annex 4 §3.1, 2022/1426 Annex II point 12 "software integrity", AFGBV §1g Nr. 5, Japan's 特定改造等の許可 and OBD検査, COM(2025) 180 Art. 4(5). Second, **in-service reporting is replacing periodic inspection as the main compliance instrument** for the ADS itself: monthly (California), quarterly (CPUC), annual (2022/1426, France), or occurrence-driven (SGO 5-day, 2022/1426 "without delay" and one month, GTR 26 three tiers), while the periodic physical inspection of the ADS, where it exists at all, is either a DTC read (Japan), an operator duty (Germany's 90 days, CVSA's point-of-origin inspection) or a provision that only requires the vehicle to be *inspectable* (R157, 2022/1426, AFGBV Anlage 1 Nr. 7.3).

### 14.3 Data an ADS inspection or in-service credential would carry

The fields below are the compliance state of the ADS at a point in time. They extend the section 9 schema with an `adsCompliance` block, carried under two new `inspectionType` values: `ads-periodic` (a station or operator check of the ADS configuration, Germany's 90-day Gesamtprüfung, Beijing's third-party inspection, Japan's OBD検査, a future 2014/45/EU Section 10 test) and `ads-in-service` (the periodic report the manufacturer or operator already owes the regulator, 2022/1426 Part 5, California §227.56–66, CPUC quarterly, GTR 26 periodic reporting). VSS status is against VSS 6.1, read from `spec/ADAS/ADAS.vspec`, `spec/Vehicle/Vehicle.vspec`, `spec/Vehicle/Diagnostics.vspec`, `spec/Vehicle/Connectivity.vspec` and `spec/Vehicle/ControlUnit/`.

| Credential field | Regulatory source | VSS 6.1 | Proposed VSS signal (extends 11.11) |
|---|---|---|---|
| `ads.supportedLevel` | SAE J3016 (revised J3016_202609, Sep 2026); permit class | `Vehicle.ADAS.SupportedAutonomyLevel` (attribute, SAE_0–SAE_5) | none needed |
| `ads.activeLevelAtCapture` | R157 §8, 2022/1426 Annex II §9 | `Vehicle.ADAS.ActiveAutonomyLevel` (incl. `*_DISENGAGING`) | none needed |
| `ads.manufacturer`, `ads.systemName`, `ads.featureList` | 2022/1426 Annex I; GTR 26 "ADS feature"; UK ASDE identity | none | `Vehicle.ADAS.ADS.Manufacturer`, `.SystemName`, `.Features` (string[]; attribute) |
| `ads.approvalReference` | R157/R185/2022/1426 approval number; KBA Betriebserlaubnis; CA DMV permit number; TxDMV authorization; Japan 認可 | none (administrative) | credential field only; optionally `Vehicle.ADAS.ADS.ApprovalNumber` (attribute) |
| `software.rxswin[]`, `software.adsVersion` | R156; R157 §8.3.2; 2022/1426 Annex II 12.1(b); StVG §1g Nr. 5; COM(2025) 180 Art. 4(5) | none (`Vehicle.VersionVSS` is the VSS catalogue version, not vehicle software) | new `Vehicle.Software` branch: `Vehicle.Software.RxSWIN` (string[]), `Vehicle.ADAS.ADS.SoftwareVersion` (string), `Vehicle.ControlUnit.*.SoftwareVersion` (the `ControlUnit` branch has `ID` and a `Health` branch only) |
| `software.lastUpdate`, `software.updateHistory[]` | R156 SUMS; Japan Art. 99-3 permission; China filing of updates | none | `Vehicle.Software.LastUpdateTimestamp`, `.LastUpdateCampaignId`, `.IsUpdatePending`, `.IsIntegrityVerified` |
| `cybersecurity.csmsCertificate`, `.vulnerabilityStatus` | R155; GB 44495-2024; Beijing Art. 38 graded protection | none | credential field (certificate reference, validity); `Vehicle.Software.IsIntegrityVerified` as the on-board check |
| `sensors[].type`, `.isCalibrated`, `.calibrationTimestamp`, `.isDegraded` | CITA ADAS PTI work; AFGBV §13(7) daily sensor check; 2022/1426 Annex II failure-warning | none (no sensor branch in VSS 6.1) | `Vehicle.ADAS.Sensor.<instance>.Type` (CAMERA/RADAR/LIDAR/ULTRASONIC/GNSS/IMU), `.IsCalibrated`, `.CalibrationTimestamp`, `.IsDegraded`, `.IsError`, instantiated per mounting position |
| `ads.health`, `ads.failureWarning` | R157 Annex 4 §3.1 failure-warning status; 2022/1426 12.1(a) | partial: `Vehicle.ADAS.{ABS,ESC,TCS,EBD,EBA,CruiseControl,LaneDepartureDetection,ObstacleDetection,DMS}.IsError`; no ADS-level flag | `Vehicle.ADAS.ADS.IsError`, `.IsEnabled`, `.FailureWarningState` (NONE/WARNING/SEVERE_ADS_FAILURE/SEVERE_VEHICLE_FAILURE, derived from the R157 §8.2.1 occurrences (j) and (k)) |
| `dtc` | Japan OBD検査 特定DTC; COM(2025) 180 Art. 4(5); CITA | `Vehicle.Diagnostics.DTCCount`, `.DTCList` | `Vehicle.Diagnostics.IsMILOn`, `.DistanceSinceDTCClear` (already proposed in 11.11) |
| `odd.declaration`, `odd.isWithinODD`, `odd.exitCount` | 2022/1426 Annex II §3.1.4, Part 5 App. 1 "operation outside ODD"; ISO 34503; GTR 26 Annex 5 (R185 Annex 7) | none | `Vehicle.ADAS.ADS.ODD.Identifier` (attribute, reference to the declared ODD), `.IsWithinODD` (sensor), `.ExitCount` (counter since last report) |
| `dssad.isPresent`, `.isAvailable`, `.recordCount`, `.capacityRecords`, `.lastRecordTimestamp` | R157 §8.4; GTR 26 Annex 6 (R185 Annex 8); GB 44497-2024; Japan 作動状態記録装置 (6 months / 2,500 records); Korea Act Art. 43(2) and Decree Art. 35-7 (6 months); CA §227.54 (30 s, 3 years) | none | `Vehicle.ADAS.ADS.DSSAD.IsAvailable`, `.RecordCount`, `.CapacityRecords`, `.LastRecordTimestamp`; `Vehicle.EDR.IsAvailable` for the GSR Art. 6 / GB 39732 recorder |
| `remoteSupervision.mode`, `.isConnected`, `.latency_ms`, `.supervisorRef` | StVG §1f(2) Technische Aufsicht and §1g connectivity parameters; France R.3152-3; Japan 特定自動運行主任者; 2022/1426 remote intervention operator; Beijing Art. 37 | `Vehicle.Connectivity.IsConnectivityAvailable` only | `Vehicle.ADAS.ADS.RemoteSupervision.Mode` (NONE/MONITORING/INTERVENTION), `.IsConnected`, `.Latency`, `.Bandwidth`, `.SupervisorReference` (pseudonymous) |
| `counters.ddtFailureTakeovers`, `.immobilizations`, `.mrmEngagements`, `.hardBrakingEvents`, `.remoteInterventions`, `.vmtAutonomous_km` | CA §227.56/58/60/66; CPUC stoppage events; 2022/1426 Part 5 App. 1 (per hour/km); GTR 26 periodic template; AFGBV §1g counts | `Vehicle.TraveledDistance` for total distance; none for ADS-engaged distance or event counters | `Vehicle.ADAS.ADS.Counters.*` (reset at each report, with `.PeriodStart`) and `Vehicle.ADAS.ADS.EngagedDistance` (km) |
| `pretrip.result`, `.performedBy`, `.validUntil` | AFGBV §13(1) Nr. 2 daily check; CVSA Enhanced Inspection electronic decal (VIPR) | none | `Vehicle.Inspection.PreTrip.Result`, `.Timestamp`, `.ValidUntil`, `.InspectorQualification` (tier 3 pattern of 11.11) |
| `ads.inspectionCondition` | AFGBV §13 90-day check; Beijing Art. 36; 2014/45/EU Section 10 (proposed) | none | `Vehicle.Inspection.ADS.Condition` (grade enum of 11.11 tier 3), `.SensorAlignment.Condition`, `.SoftwareIdentity.Condition` (MATCHES_APPROVAL / MISMATCH / NOT_ASSESSED) |

Everything in the right-hand column except the two J3016 level signals is a gap in VSS 6.1; the autonomy-level signals and the per-system `IsError` flags are the only ADS-relevant catalogue content today. The proposal keeps to the conventions of 11.11: attributes for approved configuration, sensors for state, counters that state their reset rule in the description, and a `*Source` or qualification companion wherever a human rather than the vehicle assigns the value.

A minimal `ads-periodic` credential, following section 9:

```json
{
  "type": ["VerifiableCredential", "VehicleInspectionCredential"],
  "issuer": "did:example:operator-technical-supervision-0042",
  "credentialSubject": {
    "registrationCredential": "urn:uuid:...",
    "inspectionType": "ads-periodic",
    "inspectionDate": "2026-10-20",
    "expirationDate": "2027-01-18",
    "jurisdiction": "DE",
    "legalBasis": "AFGBV §13(1) Nr. 3",
    "result": "PASS",
    "adsCompliance": {
      "supportedLevel":   { "signal": "Vehicle.ADAS.SupportedAutonomyLevel", "value": "SAE_4" },
      "approvalReference": "KBA-BE-AF-2025-00017",
      "software": { "rxswin": ["RX-ADS-7.4.2-A"], "adsVersion": "7.4.2", "lastUpdate": "2026-09-30T02:10:00Z", "integrityVerified": true, "source": "vehicle" },
      "cybersecurity": { "csmsCertificate": "E1*155R00/01*0042*00", "validUntil": "2027-06-30" },
      "sensors": [
        { "position": "FrontCenter", "type": "LIDAR", "isCalibrated": true, "calibrationTimestamp": "2026-10-20T07:40:00Z", "source": "inspector-measured" },
        { "position": "FrontCenter", "type": "RADAR", "isCalibrated": true, "isDegraded": false, "source": "vehicle" }
      ],
      "odd": { "declaration": "urn:odd:operator:route-17:v3", "exitCount": 2, "source": "vehicle" },
      "dssad": { "isAvailable": true, "recordCount": 1840, "capacityRecords": 2500, "source": "vehicle" },
      "remoteSupervision": { "mode": "MONITORING", "isConnected": true, "supervisorRef": "ta-anon-9f3e" },
      "counters": { "periodStart": "2026-07-22", "ddtFailureTakeovers": 0, "mrmEngagements": 1, "immobilizations": 3, "vmtAutonomous_km": 11840 },
      "dtc": { "signal": "Vehicle.Diagnostics.DTCList", "value": [] }
    },
    "inspectorQualification": "Kfz-Meister; manufacturer training 2026-02",
    "reportNumber": "DE-AF-2026-0042-000311"
  }
}
```

The `expirationDate` of an `ads-periodic` credential is the next due date of the regime that produced it (90 days in Germany), and the `ads-in-service` variant uses `validFrom`/`validUntil` for the reporting period instead. The DSSAD and counter blocks are summaries; the event-level records themselves belong in the FNOL and incident credentials of the companion report, which this credential references by `registrationCredential` and period rather than restating.

### 14.4 Fit with the transition path and the driverless pre-trip inspection

The AV case does not add a stage to section 13; it enters the path at Stage 3 and shows why the credential has to carry provenance per field.

- **Stage 1 (physical, inspector-issued)** is where the conventional roadworthiness of an AV sits. Nothing in the regimes above removes the periodic test of brakes, tyres, lights and emissions: AFGBV §13(8) requires the HU within six months of registration and Anlage 1 Nr. 7.3 requires the vehicle to be inspectable; Japan's Shaken applies; California's heavy-duty AVs must still stop at CHP weigh stations and meet CMV requirements. The Stage 1 credential for an AV is the section 9 credential unchanged, and the ADS block is a second credential or an extension of it.
- **Stage 2 (head-unit assistant)** is the natural home of the software-identity check. The inspector's device reads RxSWIN, ADS version, DTCs and sensor self-test state over the electronic interface, exactly as R157 Annex 4 §3.1, 2022/1426 Annex II point 12, Japan's OBD検査 and the proposed 2014/45/EU Section 10 describe, and compares them with the approval record. This is the check CITA argued for in 2021 when it said it is "no longer sufficient to simply verify the system installation and analyse tell-tales or electronic status bits" (§2.8). Radar alignment and attenuation measured with station equipment are inspector-measured fields alongside the vehicle-read ones.
- **Stage 3 (continuous evidence, pre-populated)** is where AVs already are by regulation. The DSSAD, the German §1g data set, the California monthly reports and the 2022/1426 annual report are continuous evidence streams that pre-populate the `ads-in-service` credential; the regulator's acceptance of vehicle-reported counts in place of a physical check is already the rule for these items, which is the decision section 13 says belongs to the regulator.
- **Stage 4 (automated online inspection with submission)** maps directly onto the reporting duty: the operator or manufacturer assembles the signed credential on the regulator's cadence and submits it through the same channel as the registration credential. For a Level 4 fleet, Stage 4 is not a future state but the compliance process the permit already requires, with the credential replacing a CSV template (California's Collision Reporting Template, CPUC's quarterly workbook, the GTR 26 Annex 2 and 3 templates (R185 Annexes 4 and 5)).

**The pre-trip inspection without a driver.** Section 13.5 added `pre-trip` to the `inspectionType` enumeration for the 49 CFR 396.11/396.13 and NSC Standard 13 driver inspection. For a driverless CMV the same type is issued by a different party and needs three additional properties: `performedBy` with the inspector's qualification (CVSA Enhanced Inspection certification; AFGBV §13(2) Kfz-Meister and manufacturer training), `validUntil` (the dispatch window; the 24-hour in-transit cycle of the CVSA programme, the daily cycle of AFGBV §13(1) Nr. 2), and the ADS readiness subset of 14.3 (software identity matches approval, no sensor degradation, DSSAD available, remote supervision connected, ODD of the planned route within the declared ODD). This is the data the CVSA electronic decal in VIPR carries today for participating carriers; expressing it as a `VehicleInspectionCredential` presented over OpenID4VP at a weigh station or by cloud lookup gives the roadside officer a verifiable record of a check no driver can be asked about, and gives jurisdictions without a CVSA-style programme (the EU, Japan, China) the same instrument. Where a jurisdiction grants inspection-station bypass to ADS-engaged vehicles holding a current no-defect inspection, as CVSA's programme does, the credential is the bypass token.

### 14.5 What COVESA needs to specify for automated vehicles

- The `adsCompliance` block of 14.3 in the Vehicle Credentials Vocabulary, with `inspectionType` values `ads-periodic` and `ads-in-service`, and the `performedBy`/`validUntil` properties on `pre-trip` together with `legalBasis` (the regulation and article under which the inspection or report is required) and `inspectorQualification` (the credential of the person or body performing it), both used in the sample credential above.
- The VSS additions of 14.3: `Vehicle.Software` (RxSWIN, update state, integrity), `Vehicle.ADAS.ADS` (identity, health, ODD, DSSAD, remote supervision, counters, engaged distance), `Vehicle.ADAS.Sensor` (per-position calibration and degradation), `Vehicle.EDR`, and the `Vehicle.Inspection.ADS` and `.PreTrip` tier 3 signals; to be developed with the Commercial and Fleet Vehicles Expert Group's ADS data points (companion report, section 4.2) so that the event-level signals and the compliance-state signals share one `Vehicle.ADAS.ADS` branch
- A mapping from the credential to the reporting templates that already exist: GTR 26 Annexes 1–4 (R185 Annexes 3–6), 2022/1426 Annex III Part 5 Appendix 1, California 13 CCR §227.54–66 and §228.34–40 and the DMV Collision Reporting Template, CPUC D.24-11-002, and the CVSA Enhanced Inspection checklist, so that one signed credential can be rendered into each
- Engagement with the WP.29 IWG on PTI (scan-tool provisions in R.E.3) and CITA's ADAS task force on the electronic-interface read set, since both are defining what an inspection device may read from an ADS vehicle and neither has yet named a data vocabulary

**Resources (in addition to those linked in the table):**
- [ISO 34502:2022 Scenario-based safety evaluation framework](https://www.iso.org/standard/78951.html); [ISO/TS 5083:2025 Safety for ADS](https://www.iso.org/standard/81920.html); [ISO/SAE 21434:2021](https://www.iso.org/standard/70918.html); [ISO 26262:2018](https://www.iso.org/standard/68383.html)
- [SAE J3016_202609](https://saemobilus.sae.org/standards/j3016_202104-taxonomy-definitions-terms-related-driving-automation-systems-road-motor-vehicles) (revised 20 Sep 2026; the linked 202104 page lists it as historical); [SAE J3018_202012 On-road testing of prototype ADS](https://www.sae.org/standards/content/j3018_202012/); [SAE J3197_202107 ADS Data Logger](https://saemobilus.sae.org/standards/j3197_202107-automated-driving-system-data-logger)
- [UL 4600, 3rd edition (2023)](https://webstore.ansi.org/standards/ul/ul4600ed2023); [IEEE 2846-2022](https://standards.ieee.org/ieee/2846/10831/); [IEEE 2851-2023](https://standards.ieee.org/ieee/2851/10780/)
- [IAMTS/CITA whitepaper IAMTS0004202304, Assuring Regulatory Compliance of Connected and Automated Vehicles during their Operational Lifetime (Apr 2023)](https://citainsp.org/wp-content/uploads/2023/04/IAMTS0004202304_V1.1.pdf); [CITA Annual Report 2025](https://citainsp.org/wp-content/uploads/2026/03/CITA-ANNUAL-REPORT-2025.pdf)
- [AAMVA Guidelines for Regulating Vehicles with Automated Driving Systems, Edition 4 (Mar 2024)](https://www.aamva.org/getmedia/c95fd480-5917-471a-b7ee-da88ec6cb7b5/Guidelines-for-Regulating-Vehicles-with-Automated-Driving-Systems-Ed-4_final.pdf)
- [NHTSA AV STEP NPRM, 90 FR 4130 (Jan 2025)](https://www.nhtsa.gov/sites/nhtsa.gov/files/2024-12/nprm-av-step-2024-web.pdf); [NHTSA Part 555 guidance](https://www.nhtsa.gov/part-555-guidance-and-enhanced-application-instructions)
- [UK DfT call for evidence on the AV regulatory framework (Dec 2025 to Mar 2026)](https://www.gov.uk/government/calls-for-evidence/developing-the-automated-vehicles-regulatory-framework); [Statement of safety principles consultation (Jun 2026)](https://www.gov.uk/government/consultations/automated-vehicles-statement-of-safety-principles)
- [MIIT first pilot batch, 4 Jun 2024](https://www.miit.gov.cn/jgsj/zbys/gzdt/art/2024/art_50b60c6a6aae42fbbc18690002255d85.html); [GB 47955-2026 combined driver assistance (scheduled to take effect 1 Jan 2027)](https://std.samr.gov.cn/gb/search/gbDetailed?id=3E4662D12F5C90CDE06397BE0A0AA168)
- [Shenzhen ICV Regulation 2022](http://www.sz.gov.cn/zfgb/2022/gb1250/content/post_9967816.html); [MLIT press release on OBD検査, 4 Sep 2024](https://www.mlit.go.jp/report/press/jidosha09_hh_000326.html); [NTC policy paper, Feb 2022](https://www.ntc.gov.au/sites/default/files/assets/files/NTC%20Policy%20Paper%20-%20regulatory%20framework%20for%20automated%20vehicles%20in%20Australia.pdf)

---

## Revision Notes (2026-10-27 and 2026-09-21)

**2026-10-27.** New section 14 covers regulator-required inspection and in-service monitoring of automated vehicles: rationale (software identity, sensor drift, ODD, cybersecurity, no driver for the pre-trip inspection, mandated self-monitoring); a jurisdiction table verified against primary texts (UN R157 incl. its Annex 4 PTI documentation requirement and DSSAD, R155/R156 RxSWIN, R171 02 series, UN GTR 26 / R185 adopted 24 June 2026, the 1997 Agreement PTI Rules and WP.29 IWG PTI scan-tool work, EU 2022/1426 Annex II point 12 and Part 5 reporting as amended by 2026/481, COM(2025) 180 Section 10, Germany StVG §1g and AFGBV §13 daily and 90-day checks, France's OQA annual audit, the UK Automated Vehicles Act 2024 and SI 2026/439, NHTSA SGO Third Amended and the June 2026 withdrawal of AV STEP, California's 13 CCR Art. 3.7–3.8 as adopted 28 April 2026 with monthly test-permit and quarterly deployment reporting in place of the former annual disengagement report and SGO crash reports in place of form OL 316, CPUC D.24-11-002, Texas SB 2807, Arizona, FMCSA 396.11/13 and the CVSA Enhanced CMV Inspection electronic decal, Japan's 2020/2023 Acts and OBD検査, China's 2023 pilot notice, GB 44497-2024 and the Beijing and Shenzhen regulations, Korea's 2025 Level 4 certification regime, Singapore, Australia, Canada); the `adsCompliance` credential block and its VSS 6.1 mapping (only `ADAS.ActiveAutonomyLevel`/`SupportedAutonomyLevel` and per-system `IsError` exist; `Vehicle.Software`, `Vehicle.ADAS.ADS`, `Vehicle.ADAS.Sensor`, `Vehicle.EDR` and `Vehicle.Inspection.ADS`/`.PreTrip` proposed); and its fit with the section 13 stages and the driverless `pre-trip` inspection. Items confirmed only from secondary coverage are marked as such in 14.2; unece.org blocks automated retrieval, so UN texts were read from mirrors and the GlobalAutoRegs register. Cross-references added to the Overview, 11.9, 11.11 and 13. Note for the companion whitepaper: the GlobalAutoRegs register and the UN document system list ECE/TRANS/WP.29/2026/137 as the UN R185 proposal and WP.29/2026/139 as the GTR proposal; the whitepaper cites 2026/137 for the GTR and should swap the two numbers. Its 30-day short-term report and annual periodic report are confirmed in the adopted text (R185 §7.4.8.2 and §7.4.9.3); note that the R185 annexes are numbered 3 to 8 where the GTR's are 1 to 6, so the whitepaper's "Annex 6" DSSAD reference is correct for the GTR only.

**2026-09-21.** The July 2026 draft was re-verified against primary regulatory sources, VSS 6.1 (September 2026), and the tire-sensing literature. Substantive corrections:

1. **United States**: safety-inspection state count corrected from "~17 + DC" to 12 (plus NH and LA sunsetting); DC has had no safety inspection since 2009. Texas ended non-commercial safety inspection on 1 Jan 2025; Virginia's Northern Virginia emissions program is active (the report said it was removed in 2020); California's new-vehicle smog exemption is 8 model years, not 6; Colorado, Wisconsin and Missouri are biennial (no Kansas City program); North Carolina emissions covers 19 counties, not 48; New Hampshire's program was repealed in 2026; Maryland safety inspection is at titling only. The "no inspection" state list wrongly included AZ, CO, OR, WI, HI and LA and omitted NE, KS, SC. EPA I/M citation corrected from 40 CFR Part 85 to Part 51 Subpart S. Dead resource links replaced.
2. **Canada**: the provincial table overstated periodic inspection. Only PEI inspects private cars annually; Nova Scotia and New Brunswick are biennial; Manitoba, Newfoundland (no "AVI"), Alberta (no "Private Vehicle Inspection Program"), BC, Ontario and Saskatchewan inspect on transfer/import only; Quebec has no periodic private-car inspection; the territories have none. "CVIP" is Alberta/BC terminology, not pan-Canadian — the NSC Standard 11 term is PMVI.
3. **EU**: the Directive's M1/N1 minimum is 4 years then every 2 years — "annual after 10 years" is a national choice and a pending Commission proposal, not the Directive; Article 5 covers "taxis or ambulances", not "hire"; L-category scope since 2022 with member-state opt-out added. The Annex II field list was overstated and is now split into the ten actual minimum items and national additions. Germany's AU has been part of the HU since 2010 (§47a StVZO repealed); UK legal basis corrected to Road Traffic Act 1988 and the 1981 Tests Regulations; Sweden operator list and Ireland's CVRT added. New section 3.4 covers the April 2025 Roadworthiness Package proposal (mandatory electronic certificates) and its status.
4. **Japan**: trucks under 8 t GVW are 2 years then annual (not all annual); motorcycles >250 cc; rental cars added. The 2023/2024 電子車検証 IC-chip certificate and its printed vs chip-only fields added; emissions results, sticker, weight tax and Jibaiseki reclassified as documents handled at inspection rather than certificate fields. MLIT and JVIA links (wrong page / wrong body) replaced with the MLIT portal and NALTEC.
5. **Korea**: no annual tier for cars over 5 years; first inspection now 5 years (Dec 2024 amendment) then every 2 years; taxi 2/1; 6-month tiers for heavy buses and trucks; motorcycles have emissions/noise inspection only. Dead ts2020.kr links replaced with KOTSA.
6. **China**: intervals updated to the October 2022 reform (on-site inspection at years 6 and 10, annual after 10; the 6-monthly rule for >15-year cars was abolished; commercial passenger 6-monthly after 5 years; trucks 6-monthly after 10 years). GB 21861-2014 was replaced by GB 38900-2020; "China 6b" is a type-approval standard, in-use tests are GB 18285/3847-2018; station accreditation is by market-regulation authorities, not CNCA.
7. **India**: transport-vehicle fitness is 2 years, renewed biennially to age 8 then annually (not annual from new); non-transport vehicles renew registration every 5 years after 15 with a fitness test (not annual); ATS mandate date 1 April 2025; PUC validity 6 or 12 months; "VICC" removed.
8. **TPMS references**: EU TPMS is UN Regulation 141 (2017), not R64; Japan has no confirmed TPMS fitment mandate.
9. **VSS mapping (section 11)**: new §11.11 proposes concrete VSS signals in three tiers (vspec overlay in `tmp/inspection-vss-extension/`, validated against VSS 6.1): sensor-backed (tread depth family, `Diagnostics.IsMILOn`/`ReadinessMonitors`/`DistanceSinceDTCClear`, horn/steering/damper/seatbelt defects, brake efficiency and imbalance, exhaust leak, noise), derived with stated computations (tire wear rate and remaining distance, steering free play, damping ratio, headlamp aim from ADAS camera, catalyst efficiency), and a `Vehicle.Inspection` branch for inspector-assessed items (bodywork, underbody, glazing, mirrors, steering, suspension, alignment, exhaust and analyser values, restraints, lights, brakes) graded NONE/MINOR/MAJOR/DANGEROUS. source updated from the December 2025 spec to VSS 6.1. The `Vehicle.OBD` branch was *removed* in VSS 6.0 (the report said deprecated with removal planned) and now exists only as `overlays/extensions/OBD/OBD.vspec`; `Tire.Temperature` was deprecated in v6.0, not v5.0; brake lights use `IsActive`, not `IsOn`. Added inspection-relevant signals the report omitted: ABS/ESC/TCS/EBD/EBA `IsError`, direction-indicator and hazard `IsDefect`, fog and licence-plate lights, exterior mirrors, low-voltage battery, service-due, vehicle weight, tire winter status and the new `Vehicle.Safety` branch. Tread depth remains absent from VSS 6.1.
10. **New sections**: 1.4 (documented rationale for US safety-inspection repeals, the evidence base, and the near-absence of insurer research or positions), 12 (tire health and tread-depth estimation — market, literature, standards, data programme) and 13 (transition path from inspector-issued credentials to automated online inspection, including a consent-based insurer "well-maintained vehicle" discount use case in 13.5 that operates independently of any regulatory inspection mandate).
