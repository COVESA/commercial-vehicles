# Vehicle Inspection Credential: Required Data Points

**Jurisdictions covered:** United States, Canada, European Union, Japan, South Korea, China, India  
**Last updated:** 2026-07-23  
**Related work:** [`~/Documents/poi-credential/`](poi-credential/README.md) — POI + FNOL VC design using W3C VC Data Model 2.0 and `https://w3id.org/vvc`

---

## Overview

A **vehicle inspection credential** (analogous to the Proof of Insurance VC sketched in `~/Documents/poi-credential/`) would represent the outcome of a legally mandated roadworthiness, safety, or emissions inspection. This document catalogs:

1. **Inspection types** required per jurisdiction (safety, emissions, combined roadworthiness)
2. **Data fields** on the standard inspection certificate or pass document
3. **Inspection frequency / intervals**
4. **Cross-jurisdictional comparison** of common data points

The goal is to identify the canonical data set for a `VehicleInspectionCredential` that could be:
- Issued by an authorized inspection station (the issuer DID)
- Held by the vehicle owner (wallet / telematics system)
- Presented to law enforcement, registration authorities, or border agents
- Referenced by the `VehicleRegistrationCredential` or a future `VehicleComplianceCredential`

---

## 1. United States

### 1.1 Inspection Landscape

The US has no federal vehicle inspection mandate. Programs are entirely state-run and fall into three types:

| Type | Description | States with mandate |
|------|-------------|-------------------|
| **Safety inspection** | Brakes, lights, tires, steering, windshield, emissions equipment | ~17 states + DC |
| **OBD/Emissions inspection** | On-board diagnostics readiness check (OBD-II port scan) | ~30 states (full or partial) |
| **Combined safety + emissions** | Single station performs both | TX, NY, PA, NJ, VA, others |

States with **no** mandatory periodic inspection: AL, AK, AZ, AR, CO, FL, HI (safety only on registration), ID, IA, KY, LA, MI, MN, MS, MT, ND, OK, OR, SD, TN, WA, WI, WY.

### 1.2 Standard Inspection Certificate / Sticker Data Fields

Fields that appear on state inspection certificates and OBD-II inspection reports:

| Field | Description | Notes |
|-------|-------------|-------|
| **Vehicle Identification Number (VIN)** | 17-character VIN | Present on all state programs |
| **License plate number** | State registration plate | Required |
| **Vehicle year / make / model** | Basic vehicle description | Required |
| **Odometer reading** | Mileage at time of inspection | Required in most states; used to detect rollback |
| **Inspection date** | Date test was performed | Required |
| **Certificate expiration date** | Date by which next inspection is due | Required (typically 1 year; TX = 1 year; VA = 2 years) |
| **Inspection station identifier** | State-assigned station number / name | Required |
| **Inspector / technician ID** | State-licensed inspector number | Required |
| **Overall result** | PASS / FAIL / CONDITIONAL PASS | Required |
| **Items inspected** | Checklist of safety/emissions components tested | Required (varies by state program) |
| **Failure reasons** | Specific item(s) that caused a failure | Required on failures |
| **OBD-II readiness monitors** | Pass/Fail per monitor (e.g., catalyst, O2 sensor, EVAP) | Emissions-only states |
| **OBD-II DTC codes** | Diagnostic Trouble Codes triggering failure | Emissions programs |
| **Re-inspection eligibility date** | Earliest date for free or discounted retest | Some states |
| **Repair cost waiver threshold** | Dollar limit triggering emissions waiver | Some states (e.g., CA, NY) |
| **Certificate / sticker number** | Unique document identifier | Required (anti-counterfeiting) |

### 1.3 Inspection Frequency by State (Selected)

| State | Safety | Emissions | Interval | Notes |
|-------|--------|-----------|----------|-------|
| **California** | No | Yes (Smog Check) | Every 2 years | Required on registration renewal; exempt: new cars (first 6 years), EVs, diesel pre-1998 |
| **New York** | Yes | Yes (OBD) | Annual | Both combined at inspection station |
| **Texas** | Yes | Yes (OBD in 17 counties) | Annual | Single sticker replaces both since 2015 |
| **Pennsylvania** | Yes | Yes (OBD in 25 counties) | Annual | |
| **New Jersey** | No | Yes (OBD) | Every 2 years (private); annual (commercial) | |
| **Virginia** | Yes | No | Annual | Statewide safety only; emissions check removed 2020 |
| **Maryland** | Yes | Yes (OBD) | Every 2 years | |
| **Illinois** | No | Yes (OBD — Chicago metro) | Every 2 years | |
| **Colorado** | No | Yes (OBD — Denver metro) | Annual | |
| **Massachusetts** | Yes | Yes (OBD) | Annual | |
| **Maine** | Yes | No | Annual | Includes emissions equipment check |
| **New Hampshire** | Yes | No | Annual | |
| **Rhode Island** | Yes | No | Every 2 years | |
| **District of Columbia** | Yes | Yes (OBD) | Every 2 years | |
| **Hawaii** | Yes | No | Annual | Safety only |
| **Missouri** | No | Yes (KC/St. Louis metro) | Annual | |
| **North Carolina** | Yes | Yes (OBD — 48 counties) | Annual | |
| **Georgia** | No | Yes (OBD — Atlanta metro) | Annual | |
| **Vermont** | Yes | No | Annual | |
| **Wisconsin** | No | Yes (Milwaukee, Sheboygan) | Annual | |

**Resources:**
- [Vehicle Inspection Requirements by State — Bumper.com](https://bumper.com/car-guides/vehicle-inspection-requirements-by-state/)
- [State Emissions Testing Requirements — EPA](https://www.epa.gov/state-and-local-transportation/programs-reduce-mobile-source-air-pollution#Inspection)
- [OBD-II Inspection — California BAR](https://www.bar.ca.gov/smog-check-program)
- [Vehicle Safety Inspection — Virginia DMV](https://www.dmv.virginia.gov/vehicles/vehicle-safety-inspection)

---

## 2. Canada

### 2.1 Inspection Landscape

Like the US, Canada has no federal vehicle inspection mandate for passenger vehicles. Each province operates its own program. Commercial vehicles are governed by a mix of provincial programs and federal National Safety Code (NSC) standards.

| Inspection Type | Description |
|-----------------|-------------|
| **Safety Standards Certificate (SSC)** | Required when transferring ownership or bringing a vehicle into compliance; certifies roadworthiness at that point in time |
| **Annual / periodic safety inspection** | Required by some provinces for older vehicles or on a rolling basis |
| **Emissions / AirCare** | Historically required in BC (retired 2014) and ON (retired 2019); currently limited programs |
| **Commercial Vehicle Inspection Program (CVIP)** | NSC-based periodic inspection for commercial vehicles in all provinces |

### 2.2 Safety Standards Certificate (SSC) Data Fields

The SSC is the closest Canadian analogue to a US safety inspection certificate. Province-specific certificates share a common core:

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

| Province / Territory | Program | Interval | Emissions |
|----------------------|---------|----------|-----------|
| **Alberta** | Private Vehicle Inspection (for used vehicle registration transfer) | On transfer of ownership | No ongoing emissions program |
| **British Columbia** | Inspection for registration transfer; AirCare retired 2014 | On transfer; fleet vehicles annual | No emissions program (AirCare retired) |
| **Manitoba** | Annual safety inspection (older vehicles); SGI-equivalent | Annual for vehicles >7 years | No mandatory emissions |
| **New Brunswick** | Annual Motor Vehicle Inspection (MVI) | Annual | No mandatory emissions |
| **Newfoundland & Labrador** | Annual Vehicle Inspection (AVI) | Annual | No mandatory emissions |
| **Northwest Territories** | Annual inspection | Annual | No |
| **Nova Scotia** | Annual Motor Vehicle Inspection | Annual | No mandatory emissions |
| **Nunavut** | Annual inspection | Annual | No |
| **Ontario** | Safety Standards Certificate (on sale/import); Drive Clean retired 2019 | On transfer; commercial annual | No ongoing emissions (Drive Clean retired) |
| **Prince Edward Island** | Annual inspection | Annual | No |
| **Québec** | SAAQ Mandatory Vehicle Inspection; periodic for >10-year-old vehicles | Every 2 years for vehicles ≥10 years | No mandatory emissions |
| **Saskatchewan** | Safety inspection on sale/import; SGI inspection stations | On transfer; commercial annual | No |
| **Yukon** | Annual inspection | Annual | No |

**Resources:**
- [Safety Standards Certificate — Ontario MTO](https://www.ontario.ca/page/get-safety-standards-certificate)
- [Private Vehicle Inspection Program — Alberta Transportation](https://www.alberta.ca/private-vehicle-inspection-program)
- [Motor Vehicle Inspection — Nova Scotia](https://novascotia.ca/sns/rmv/inspection/)
- [Vehicle Inspection — Quebec SAAQ](https://saaq.gouv.qc.ca/en/vehicle-registration/vehicle-inspection/)
- [Mandatory Vehicle Inspection — BC CVSEonline](https://cvse.ca/)

---

## 3. European Union

### 3.1 Roadworthiness Testing Framework

EU vehicle roadworthiness testing is harmonized under **Directive 2014/45/EU** (periodic roadworthiness tests for motor vehicles and their trailers). This replaced a patchwork of national programs with a common minimum standard while allowing member states to exceed the floor.

All EU member states must:
- Test vehicles at defined intervals
- Issue a **roadworthiness certificate** (or equivalent national document)
- Maintain an electronic register of test results
- Apply a **roadworthiness test sticker** or equivalent marking to the vehicle

Known nationally as:
| Country | Name |
|---------|------|
| Germany | **HU** (Hauptuntersuchung) + AU (Abgasuntersuchung for emissions) — TÜV, DEKRA, GTÜ stations |
| France | **Contrôle Technique (CT)** |
| Spain | **ITV** (Inspección Técnica de Vehículos) |
| Italy | **Revisione** |
| Netherlands | **APK** (Algemene Periodieke Keuring) |
| Belgium | **Contrôle Technique / Technische Controle** |
| Sweden | **Kontrollbesiktning** (Opus, BESIKTA) |
| Poland | **Badanie Techniczne** |
| Czech Republic | **STK** (Stanice Technické Kontroly) |
| Austria | **Pickerl** (§57a test) |
| Ireland | **NCT** (National Car Test) |
| United Kingdom (post-Brexit) | **MOT** (Ministry of Transport test) — aligns with EU standards but is no longer covered by 2014/45/EU |

### 3.2 EU Roadworthiness Certificate Data Fields

Directive 2014/45/EU Annex II specifies the minimum content of the **roadworthiness test report**:

| Field | Description |
|-------|-------------|
| **Vehicle Identification Number (VIN)** | 17-character VIN (mandatory per Annex II) |
| **Vehicle registration number** | National plate identifier |
| **Vehicle make / model / type** | From registration records |
| **Vehicle category** | EU type-approval category (M1, M2, N1, etc.) |
| **First registration date / year of manufacture** | Used to determine test interval |
| **Odometer reading** | Mileage at time of test |
| **Test date** | Date the test was performed |
| **Certificate validity date** | Expiry of the test result (period varies by vehicle age and category — see 3.3) |
| **Testing centre identifier** | Authorised test station name and national ID |
| **Inspector identifier** | Name/ID of the qualified inspector |
| **Overall assessment** | PASSED / MINOR DEFICIENCIES (pass) / MAJOR DEFICIENCY (fail) / DANGEROUS DEFICIENCY (fail, vehicle grounded) |
| **Defect category** | MINOR / MAJOR / DANGEROUS — per Annex I taxonomy |
| **Defect items** | Specific systems inspected and their outcomes (brakes, steering, lighting, tyres, emissions equipment, bodywork, etc.) |
| **Emissions test result** | Exhaust gas opacity, lambda value, CO/HC levels (where applicable) |
| **Test report number** | Unique identifier for this test |
| **Country of test** | ISO 3166-1 alpha-2 country code |
| **Language** | National language; some member states include EN |

**Defect classification (Annex I — Directive 2014/45/EU):**

| Class | Definition | Effect on vehicle |
|-------|------------|-------------------|
| **Minor** | Small technical deficiency with no significant effect on vehicle safety | Pass; repair recommended |
| **Major** | Deficiency that may adversely affect vehicle safety or disadvantage other road users | Fail; vehicle may be driven to repair facility |
| **Dangerous** | Direct and immediate risk to road safety or serious impact on the environment | Fail; vehicle must not be used on public roads |

### 3.3 Test Intervals by EU Vehicle Category (Directive 2014/45/EU, Article 5)

| Vehicle Category | Description | Test Schedule |
|-----------------|-------------|---------------|
| **M1 (passenger cars up to 8 passengers)** | New vehicles exempt for first 4 years; then every 2 years; then annual after 10 years | 4 years → 2 years → annual |
| **M1 (taxis/hire)** | Commercial passenger vehicles | Annual from year 1 |
| **M2 / M3 (minibuses, buses/coaches)** | Vehicles with >8 passenger seats | Annual |
| **N1 (light commercial ≤3.5t)** | Vans, light trucks | 4 years → 2 years → annual |
| **N2 / N3 (HGV >3.5t)** | Lorries, heavy trucks | Annual (initial: 1 year from registration) |
| **O3 / O4 (heavy trailers >3.5t)** | | Annual |
| **L-category (motorcycles, mopeds)** | Member state discretion; most require periodic test | Varies |

> Member states may apply more frequent intervals; above is the EU minimum floor.

**Resources:**
- [Directive 2014/45/EU — EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014L0045)
- [Roadworthiness Package — European Commission](https://transport.ec.europa.eu/transport-modes/road/road-safety/vehicles/roadworthiness_en)
- [Periodic Roadworthiness Tests — EUR-Lex Summary](https://eur-lex.europa.eu/EN/legal-content/summary/periodic-roadworthiness-tests-for-motor-vehicles.html)
- [MOT Test — UK DVSA](https://www.gov.uk/getting-an-mot)

---

## 4. Japan

### 4.1 Shaken (車検) — Vehicle Inspection

Japan operates one of the world's most rigorous mandatory vehicle inspection systems, known as **Shaken** (車検, *sha-ken* = "vehicle inspection"). It is administered by the Ministry of Land, Infrastructure, Transport and Tourism (MLIT) and performed at designated inspection facilities (民間車検場 *minkan shaken-jō*) or government-operated inspection offices (陸運局).

### 4.2 Shaken Certificate Data Fields

| Field | Description |
|-------|-------------|
| **Vehicle Identification Number (VIN / frame number)** | Japanese VIN or chassis number (車台番号) |
| **License plate number** | Japanese registration plate (ナンバープレート) |
| **Vehicle type / model code** | Type-approval category and model designation |
| **Engine displacement / fuel type** | For tax and environmental classification |
| **Vehicle weight** | Gross vehicle mass (for weight-based tax) |
| **First registration date** | Date of first registration in Japan |
| **Inspection date** | Date test was performed |
| **Certificate expiration date (有効期限)** | Date by which next Shaken must occur |
| **Inspection station name / number** | Designated facility identifier |
| **Inspector / recognized garage ID** | MLIT-licensed mechanic (指定整備工場) ID |
| **Overall result** | Pass — certificate issued; Fail — listed defects |
| **Odometer reading** | Mileage recorded at test |
| **Emissions test result** | CO, HC, NOx, opacity (diesel) levels measured against MLIT standards |
| **Inspection sticker (車検シール)** | Windshield sticker: expiry month/year + certificate number |
| **Weight tax payment confirmation** | 自動車重量税 — paid at time of Shaken; receipt attached to certificate |
| **Compulsory insurance (Jibaiseki) confirmation** | Mandatory third-party insurance (自動車損害賠償責任保険) must be valid; confirmed at Shaken |

### 4.3 Shaken Intervals

| Vehicle Type | Age | Interval |
|-------------|-----|----------|
| **Passenger car (private)** | New (first Shaken) | 3 years after first registration |
| **Passenger car (private)** | Subsequent | Every 2 years |
| **Passenger car (commercial / taxi)** | All | Every 1 year |
| **Light motor vehicle (軽自動車)** | New | 3 years |
| **Light motor vehicle** | Subsequent | Every 2 years |
| **Motorcycle (≥250cc)** | New | 3 years |
| **Motorcycle** | Subsequent | Every 2 years |
| **Trucks / buses (commercial)** | All | Every 1 year |

**Resources:**
- [Shaken (車検) Overview — MLIT Japan](https://www.mlit.go.jp/jidosha/jidosha_fr7_000007.html)
- [Japan Vehicle Inspection — JVIA](https://www.jvia.or.jp/)
- [Shaken Explained — Japan Times](https://www.japantimes.co.jp/)

---

## 5. South Korea

### 5.1 Vehicle Inspection Program

South Korea's mandatory vehicle inspection is administered by the **Korea Transportation Safety Authority (TS, 한국교통안전공단)**. It covers both safety and emissions.

### 5.2 Korean Inspection Certificate Data Fields

| Field | Description |
|-------|-------------|
| **Vehicle registration number** | Korean plate (차량번호) |
| **Vehicle Identification Number (VIN)** | Chassis number (차대번호) |
| **Vehicle make / model** | Korean or international designation |
| **Engine type / fuel** | Gasoline, diesel, LPG, electric, hybrid |
| **Inspection date** | Date of test |
| **Certificate validity date** | Expiry of inspection |
| **Inspection station name / ID** | TS-designated station or authorized private garage |
| **Inspector ID** | Certified inspection technician |
| **Overall result** | Pass (합격) / Conditional Pass / Fail (불합격) |
| **Safety inspection items** | Brakes, lights, steering, tires, suspension (specific items per TS checklist) |
| **Emissions test result** | CO, HC, NOx levels; smoke opacity (diesel); OBD readiness |
| **Inspection report number** | Unique document number |

### 5.3 Inspection Intervals

| Vehicle Type | Interval |
|-------------|----------|
| **Passenger car** | New: 4 years; then every 2 years |
| **Passenger car (>5 years)** | Annual |
| **Commercial vehicle / bus / taxi** | Annual |
| **Motorcycle** | Every 3 years initially; then every 2 years |

**Resources:**
- [Korea Transportation Safety Authority (TS)](https://www.ts2020.kr/)
- [Vehicle Inspection — TS English Portal](https://www.ts2020.kr/eng/)

---

## 6. China

### 6.1 Vehicle Inspection Program

China's mandatory inspection system is administered by the **Ministry of Public Security (公安部)** and carried out through authorized inspection stations (机动车检验机构) accredited by the **Certification and Accreditation Administration (CNCA)**. China integrates safety, emissions, and technical compliance into a single inspection.

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
| **Inspection station name / accreditation number** | Station name + CNCA-issued code |
| **Inspector / technician ID** | Certified inspector identifier |
| **Overall result** | Pass (合格) / Fail (不合格) |
| **Safety inspection items** | Brakes, steering, lights, tires, windshield, horn, mirror, etc. |
| **Emissions test result** | OBD check + tailpipe measurement; China 6b standard |
| **Annual inspection mark (年检标志)** | Sticker affixed to license plate after passing |

### 6.3 Inspection Intervals

| Vehicle Type | Interval |
|-------------|----------|
| **Private passenger car (≤6 years old)** | Every 2 years |
| **Private passenger car (7–15 years old)** | Annual |
| **Private passenger car (>15 years old)** | Every 6 months (approaching forced retirement) |
| **Commercial passenger vehicle (taxi, bus)** | Annual (new: 2 years until 5 years; then annual) |
| **Commercial freight vehicle** | Annual |
| **Motorcycle** | Annual |

**Resources:**
- [Vehicle Inspection — China MPS](https://www.mps.gov.cn/)
- [Vehicle Inspection Standards — GB/T 21861](https://std.samr.gov.cn/)
- [China Vehicle Inspection Overview — CATARC](http://www.catarc.ac.cn/)

---

## 7. India

### 7.1 Fitness Certificate Program

India's vehicle inspection framework is governed by the **Motor Vehicles Act, 1988** and the **Central Motor Vehicles Rules, 1989**, administered at the state level through **State Transport Departments** and **Vehicle Inspection & Certification Centres (VICC)**. The 2019 Motor Vehicles (Amendment) Act introduced automated testing for commercial vehicles; private vehicles largely rely on RTO-based inspection.

**National Automated Testing Stations (ATS):** The Ministry of Road Transport and Highways (MoRTH) has been rolling out a network of ATS for commercial vehicles to replace manual inspection.

### 7.2 Fitness Certificate Data Fields

| Field | Description |
|-------|-------------|
| **Vehicle Registration Number** | State registration plate |
| **Vehicle Identification Number (VIN / Chassis Number)** | As per RC book |
| **Engine number** | As per RC book |
| **Vehicle make / model / type** | Per registration certificate |
| **Category** | LMV, HMV, transport, non-transport |
| **Fuel type** | Petrol, diesel, CNG, LPG, electric |
| **Gross Vehicle Weight (GVW)** | For commercial vehicles |
| **Inspection date** | Date of test |
| **Certificate validity date** | For transport vehicles: annual; non-transport: see below |
| **Inspection centre / RTO name** | Regional Transport Office or authorized test centre |
| **Inspector / MVI designation** | Motor Vehicle Inspector (government) or ATS technician |
| **Overall result** | Fit / Unfit |
| **Defects found** | Itemized list on failure |
| **Emissions test result** | PUC (Pollution Under Control) certificate number and expiry |
| **Fitness certificate number** | Unique FC document number |

> **PUC (Pollution Under Control) Certificate:** A separate emissions-only credential; required for all motor vehicles in India. Data fields: registration number, fuel type, test date, expiry date, CO/HC/smoke opacity levels, testing centre, test equipment ID.

### 7.3 Inspection Intervals

| Vehicle Category | New Vehicle | Subsequent |
|-----------------|-------------|------------|
| **Non-transport vehicle (private car/motorcycle)** | No periodic inspection required until 15 years; then annual inspection at ATS or RTO | Annual after 15 years |
| **Transport vehicle (taxi, goods, bus)** | Annual from registration | Annual |
| **Construction equipment / special purpose** | Annual | Annual |

**Resources:**
- [Fitness Certificate — Parivahan Portal (MoRTH)](https://parivahan.gov.in/)
- [Motor Vehicles (Amendment) Act 2019 — MoRTH](https://morth.nic.in/)
- [Automated Testing Stations — MoRTH](https://morth.nic.in/automated-testing-station)
- [PUC Certificate Information — CPCB](https://cpcb.nic.in/)

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
| Odometer reading | ✓ | ✓ | ✓ | ✓ | — | ✓ | — |
| Emissions test result | ✓ (varies) | ✓ (limited) | ✓ | ✓ | ✓ | ✓ | ✓ (PUC) |
| Defect items / failure reasons | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Defect severity classification | — | — | ✓ (Minor/Major/Dangerous) | — | — | — | — |
| Certificate / report number | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Vehicle category / type-approval class | — | — | ✓ (M/N/L) | ✓ | — | ✓ | ✓ |
| First registration date | — | — | ✓ | ✓ | ✓ | ✓ | — |
| Fuel type | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Insurance validity confirmation | — | — | — | ✓ (Jibaiseki) | — | — | — |
| Weight (GVW) | Commercial | Commercial | Commercial | ✓ | — | ✓ | ✓ |
| OBD-II monitor readiness | ✓ (where OBD) | — | ✓ | — | ✓ | ✓ | — |
| Emissions standard reference | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 9. Proposed `VehicleInspectionCredential` Core Schema

Following the design pattern from `~/Documents/poi-credential/README.md`, a `VehicleInspectionCredential` would:

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
| `defectSeverity` | EU | MINOR / MAJOR / DANGEROUS per 2014/45/EU Annex I |
| `vehicleCategory` | EU, JP, CN, IN | M1/N1/L-category; Japanese type code |
| `weightTaxReceipt` | JP | 自動車重量税 payment confirmation |
| `jibaisekiConfirmation` | JP | Mandatory insurance validity at Shaken |
| `pucCertificateNumber` | IN | Separate emissions sub-credential reference |
| `obdMonitorStatus` | US, KR, CN | Per-monitor readiness bitmap |
| `repairCostWaiver` | US | Emissions waiver threshold exceeded flag |
| `reInspectionDeadline` | US, CA | Deadline for free retest after failure |

---

## 10. Key Regulatory References

| Jurisdiction | Authority | Key Instrument |
|-------------|-----------|----------------|
| USA | State DMVs; EPA (emissions) | State vehicle inspection statutes; 40 CFR Part 85 (EPA I/M) |
| Canada | Provincial transport ministries | Motor Vehicle Act (each province); NSC Standard 11 (commercial) |
| EU | European Commission DG MOVE | Directive 2014/45/EU (roadworthiness) |
| Germany | KBA, TÜV/DEKRA/GTÜ | StVZO §29; AU emissions per §47a |
| France | DREAL | Arrêté du 18 juin 1991 (Contrôle Technique) |
| UK (post-Brexit) | DVSA | The Road Vehicles (Construction and Use) Regulations 1986; MOT scheme |
| Japan | MLIT | Road Vehicles Act (道路運送車両法) |
| South Korea | TS | Motor Vehicle Management Act (자동차관리법) |
| China | MPS, CNCA | GB 21861-2014 (safety); GB 18285-2018 (petrol emissions); GB 3847-2018 (diesel) |
| India | MoRTH | Motor Vehicles Act 1988; CMVR 1989; AIS standards |

---

*Research compiled from public regulatory sources, transport ministry publications, and official legal texts. Inspection requirements, intervals, and data fields are subject to change; verify with the applicable transport authority for current requirements.*

---

## 11. Inspection Data Points Mapped to COVESA VSS

This section maps individual inspection pass/fail criteria to COVESA Vehicle Signal Specification (VSS) signal paths. Source: `vehicle_signal_specification202512` (December 2025 release), read from local vspec files at `~/doc/covesa/vehicle_signal_specification202512/spec/`.

**Key caveats:**
- VSS signals describe *live sensor readings* from a running or recently stopped vehicle. Inspection criteria are *point-in-time pass/fail thresholds* — the mapping below identifies which VSS signal feeds the criterion, not that the criterion is directly encoded in VSS.
- The `Vehicle.OBD.*` branch is **deprecated as of VSS v5.0** and scheduled for removal in v6.0. The canonical replacements are in `Vehicle.Diagnostics.*` and `Vehicle.Powertrain.CombustionEngine.*`. Both paths are shown where applicable.
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

**Inspection use:** TPMS is a mandatory system check in the US (FMVSS 138), EU (R64), Japan (Shaken), and Korea. The credential can record live kPa values at time of inspection alongside the vehicle-reported `IsPressureLow` status.

#### Tire Temperature

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.RubberTemperature` | sensor | °C | Tire rubber temperature (v5.0+ replacement for deprecated `.Temperature`) |
| `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.AirTemperature` | sensor | °C | Internal air temperature |

**Source vspec:** `spec/Chassis/Wheel.vspec`

#### Tire Tread Depth — VSS Gap

> **Gap:** COVESA VSS (as of December 2025) has **no signal for tire tread depth** (mm remaining) or tread wear indicators. The spec provides `Tire.Pressure`, `Tire.IsPressureLow`, `Tire.RubberTemperature`, and `Tire.AirTemperature` — but no `Tire.TreadDepth` or `Tire.TreadWearIndicator`.
>
> **Implication for inspection credential:** Tread depth (the most commonly failed tire item — minimum 1.6 mm EU/US, 1.6 mm CA, 1.6 mm JP) must be captured as a **custom extension field** in the credential until VSS adds a tread depth signal. Proposed path: `Vehicle.Chassis.Axle.RowN.Wheel.*.Tire.TreadDepth` (unit: mm).
>
> A VSS PR or overlay would be the right place to introduce this. The FMS overlay at `~/doc/sdv/fleet-management/spec/overlay/fms.vspec` may be worth checking for commercial-vehicle precedent.

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
| ~~`Vehicle.OBD.Status.IsMILOn`~~ | *(deprecated v5.0)* | boolean | Malfunction Indicator Light state — use replacement below |
| ~~`Vehicle.OBD.Status.DTCCount`~~ | *(deprecated v5.0)* | — | Replaced by `Vehicle.Diagnostics.DTCCount` |

> **MIL state gap:** `Vehicle.OBD.Status.IsMILOn` is deprecated but has **no direct replacement in Vehicle.Diagnostics.*` as of December 2025**. Implementations bridging to OBD inspection systems should treat a non-zero `DTCCount` as a proxy for MIL-on for credential purposes until a `Vehicle.Diagnostics.IsMILOn` signal is introduced.

**Source vspec:** `spec/Vehicle/Diagnostics.vspec`, `spec/OBD/OBD.vspec`

#### OBD-II Readiness Monitors

OBD-II readiness monitors are the primary emissions pass/fail gate in US, Canada (some provinces), Korea, and China. VSS does not have native `ReadinessMonitor.*` signals in the main spec — they remain in the deprecated `Vehicle.OBD.*` branch which maps OBD PIDs directly.

| Relevant OBD PIDs (via deprecated VSS path) | Monitor |
|---------------------------------------------|---------|
| PID 01 / 41 `DriveCycleStatus` | Catalyst, O2 Sensor, EVAP, EGR, Secondary Air monitors |
| `Vehicle.OBD.O2WR.Sensor[N].Lambda` | Wide-band lambda (air-fuel equivalence ratio) |
| `Vehicle.OBD.CommandedEGR` / `EGRError` | EGR system commanded position and error |
| `Vehicle.OBD.CommandedEVAP` / `EVAPVaporPressure` | EVAP system status |
| `Vehicle.OBD.Catalyst.Bank1.Temperature1` / `Temperature2` | Catalyst brick temperature — proxy for catalyst efficiency |

**For a credential:** The cleanest approach is to record the raw readiness monitor bitmask (from PID 01/41) as a `uint16` field `obdReadinessBitmask` alongside individual per-monitor `PASS`/`NOT_READY`/`INCOMPLETE` strings. This avoids VSS path dependency on the deprecated OBD branch while preserving full information.

#### ICE Exhaust Gas — Tailpipe Measurement

Standard tailpipe gas analyser measurements are **not directly available as VSS sensor signals** — they are measured externally by the inspection station's analyser equipment, not reported by the vehicle ECU. However, VSS has relevant supporting signals:

| VSS Signal Path | Type | Unit | Description | Inspection relevance |
|-----------------|------|------|-------------|----------------------|
| `Vehicle.Powertrain.CombustionEngine.EngineOil.Temperature` | sensor | °C | Engine oil temperature | Confirms warm engine (required for valid emissions test) |
| `Vehicle.Powertrain.CombustionEngine.EngineCoolant.Temperature` | sensor | °C | Coolant temperature | Warm-up verification |
| `Vehicle.Powertrain.CombustionEngine.Speed` | sensor | rpm | Engine RPM | Test must be at idle / 2500 rpm depending on protocol |
| `Vehicle.OBD.O2WR.Sensor[N].Lambda` *(deprecated v5.0)* | sensor | ratio | Lambda (air-fuel equivalence) — proxy for combustion efficiency | High lambda deviation = rich/lean misfire |
| `Vehicle.OBD.ShortTermFuelTrim1` / `LongTermFuelTrim1` *(deprecated v5.0)* | sensor | percent | Short/long-term fuel correction | Sustained trim deviation indicates catalyst or injector fault |

**Conclusion:** The tailpipe CO, HC, NOx, and smoke opacity values reported on an inspection certificate come from the analyser, not the vehicle. These are **inspector-measured fields** and should be encoded as direct credential data points (e.g. `co_ppm`, `hc_ppm`, `opacity_pct`) rather than VSS signal references.

#### Diesel Particulate Filter (DPF)

| VSS Signal Path | Type | Unit | Description |
|-----------------|------|------|-------------|
| `Vehicle.Powertrain.CombustionEngine.DieselParticulateFilter.InletTemperature` | sensor | °C | DPF upstream temperature |
| `Vehicle.Powertrain.CombustionEngine.DieselParticulateFilter.OutletTemperature` | sensor | °C | DPF downstream temperature |
| `Vehicle.Powertrain.CombustionEngine.DieselParticulateFilter.DeltaPressure` | sensor | Pa | Pressure drop across filter — high ΔP indicates blockage or failed regeneration |

**Inspection use:** EU Directive 2014/45/EU Annex II explicitly includes particulate filter integrity for diesel M1 vehicles. DPF delta-pressure is the primary sensor-based indicator of filter condition alongside smoke opacity measurement.

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

For BEVs and PHEVs, emissions inspection shifts to battery health and EV system integrity. Several jurisdictions (EU under 2025 Battery Regulation, CA AB 2785, Korea) are implementing or piloting SoH-based checks.

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
| `Vehicle.Body.Lights.Brake.IsOn` *(via BrakeLights.vspec)* | sensor | Brake lights active |
| `Vehicle.Body.Lights.Brake.IsDefect` | sensor | Brake light defect |

**Source vspec:** `spec/Body/StaticLights.vspec`, `spec/Body/BrakeLights.vspec`, `spec/Body/Body.vspec`

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

### 11.9 VSS Gap Summary — Fields Needed in Inspection Credential with No VSS Coverage

The following inspection data points have **no corresponding VSS signal** in the December 2025 release and must be carried as credential-specific fields or covered by a VSS extension/overlay:

| Inspection Item | Gap | Suggested credential field | Priority |
|----------------|-----|---------------------------|----------|
| **Tire tread depth** | No VSS signal | `tire.treadDepth_mm` per wheel | High — failed in every jurisdiction |
| **Headlight aim / alignment** | Inspector-measured only (optical tester) | `lighting.beamAim.result` (PASS/FAIL) | High |
| **Tailpipe CO ppm** | Analyser-measured; not from ECU | `emissions.co_ppm` | High |
| **Tailpipe HC ppm** | Analyser-measured | `emissions.hc_ppm` | High |
| **Tailpipe NOx ppm** | Analyser-measured | `emissions.nox_ppm` | High |
| **Diesel smoke opacity (%)** | Analyser-measured | `emissions.opacity_pct` | High |
| **OBD readiness monitor bitmap** | In deprecated OBD branch only | `emissions.obdReadinessBitmask` (uint16) | Medium |
| **MIL (Check Engine Light) state** | Deprecated OBD branch; no v5.0+ replacement | `emissions.isMILOn` (boolean) | Medium — critical for US/KR/CN I/M |
| **Suspension geometry (camber, toe, caster)** | No VSS signal | `suspension.alignment.result` (PASS/FAIL) | Medium |
| **Brake efficiency (%) / deceleration rate** | Rollerbrake tester output | `brakes.efficiency_pct` per axle | Medium |
| **Structural integrity / bodywork** | Visual inspection only | `bodywork.result` (PASS/FAIL) | Low (not automatable) |
| **Weight tax / GVW confirmation** (Japan) | Administrative | `weight.gvw_kg`, `weight.taxPaidConfirmed` | Japan-specific |

---

### 11.10 VSS Signal Snapshot Pattern for Inspection Credential

Following the `VSSSnapshot` pattern established in `~/Documents/poi-credential/README.md` for the FNOL credential, an inspection evidence block would look like:

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
      "treadDepth_mm": 6.2
    },
    "row1Right": {
      "pressure": { "signal": "Vehicle.Chassis.Axle.Row1.Wheel.Right.Tire.Pressure", "value": 228, "unit": "kPa" },
      "treadDepth_mm": 5.9
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
- `spec/Vehicle/Diagnostics.vspec` — DTC count/list (v5.0+ canonical paths)
- `spec/OBD/OBD.vspec` — OBD PID mappings (deprecated v5.0, removal planned v6.0)
