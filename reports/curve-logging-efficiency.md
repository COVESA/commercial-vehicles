# Curve Logging: Efficient Vehicle Data That Is Also the Right Data

**COVESA Commercial and Fleet Vehicle Expert Group**
**Date:** November 2026
**Audience:** OEM connected-services and data-platform decision makers, fleet operators, insurers, maintenance providers

## Summary

Curve logging is an adaptive data-collection method, derived from the Ramer-Douglas-Peucker (RDP) line-simplification algorithm, that keeps a vehicle signal sample only when it deviates from the straight line between the points already kept by more than a per-signal tolerance (epsilon). It runs in production on Geotab GO devices, is open source under MPL-2.0, is a defined subscription filter in VISS, and is the sampling method the COVESA Fleet Management Data (FMD) sheet recommends for continuous signals. Published examples show 76 to 95 percent fewer points for speed and GPS with a bounded reconstruction error. The less obvious point, and the one this report presses, is that the points curve logging keeps are exactly the moments a fleet, insurer, OEM service or maintenance shop cares about. Efficiency and usefulness are the same selection rule.

## Related resources

- Geotab curve library (Python and Rust, MPL-2.0): <https://github.com/Geotab/curve>
- Geotab, "How the curve algorithm for GPS logging works" (Neil Cawse): <https://www.geotab.com/blog/gps-logging-curve-algorithm/>
- Geotab Developers, "GO device logging": <https://geotab.github.io/sdk/software/guides/go-device-logging/>
- Geotab white paper, "Putting fleet data quality to the test for risk management" (Mecanica closed-track test): <https://www.geotab.com/white-paper/fleet-data-quality/>
- COVESA VISS v3.2 Core, "Curve logging Filter Operation": <https://raw.githack.com/COVESA/vehicle-information-service-specification/v3.2/spec/VISSv3.2_Core.html> (W3C-hosted VISSv2 text: <https://w3c.github.io/automotive/spec/VISSv2_Core.html>)
- COVESA Fleet Management Data sheet (curve error threshold column): <https://docs.google.com/spreadsheets/d/1FMtSLhJy1REgadlnSwAqPX7r57rqdLYyw4W7ZsWyg8E>
- IETF draft, "Sampling With Purpose" (T. Guild): [draft-data-sampling-connected-vehicles.md](draft-data-sampling-connected-vehicles.md)
- Eclipse Kuksa databroker fork with VISS curvelog filter: <https://github.com/tguild/kuksa-databroker> (branch `viss-curvelog-filter`)
- Eclipse SDV Fleet Management Blueprint (Bosch/ETAS curve integration, PR #48): <https://github.com/eclipse-sdv-blueprints/fleet-management>
- Companion analyses in this folder: [VSS_Sampling_Standards_Survey.md](VSS_Sampling_Standards_Survey.md), [Data_Collection_Conventions_Assessment1.md](Data_Collection_Conventions_Assessment1.md)
- Decks (Google Slides, public): [Curve logic overview](https://docs.google.com/presentation/d/1cWnuzOzprRDikuSpbKicJ3dVMkGBQssPc4E3fuFU0HU), [CCS / W3C VISS: access control and curve logging](https://docs.google.com/presentation/d/1Z6oew3Ub9Icw5Gi-tR_QwwCkaP97qErSZAuVBqvrVDU), [Commercial Vehicle Update, Spring AMM 2024](https://docs.google.com/presentation/d/12t8N8QbB2E-CtRSHJ8uq3xFoquRqdOJSfm4KgYOy7Tg) (slide 15, how curve logging works), [VISS overview and current status](https://docs.google.com/presentation/d/1RYgy9oGLRm7t8haYbKqOQhkQZEhoEvjCPZuxbD1F-lg)
- [COVESA Commercial Vehicle BoF overview deck](https://docs.google.com/presentation/d/1zLbYQEsAZ2ULSroFDKla5FGYbS_25X5lKCUzDcCH6AM) (why fleets need standardized OEM data, pillars, use case to signal to sampling chain)
- [Commercial Vehicle Overview, COVESA Spring AMM 2024](https://docs.google.com/presentation/d/12t8N8QbB2E-CtRSHJ8uq3xFoquRqdOJSfm4KgYOy7Tg) (same core plus OEM and fleet testimonials)
- [FMD guidelines business case](fmd-guidelines-business-case.md)
- [VSS adoption indicators](vss-adoption-indicators.md)

## How it works

RDP was published in the 1970s to simplify coastlines on maps; curve logging applies it to a signal plotted against time. The device buffers raw samples, draws a straight line from the first kept point to the newest sample, and finds the buffered point furthest from that line. If that distance exceeds epsilon, the point is kept and the two sub-segments are checked the same way; if not, everything between the endpoints is dropped. Geotab's implementation measures vertical distance for scalar signals, so epsilon is expressed in the signal's own units (km/h, V, degrees C), and perpendicular distance for GPS, where both axes share units.

```
speed (km/h)
 100 |          x x x x x x x x x x          <- cruising: all dropped
     |        x                     x        <- kept: start/end of plateau
  60 |      x                         x
     |    x                             x    <- kept: braking knee
  20 |  x                                 x x x x
     |x_____________________________________________ time
       ^                     ^           ^
     kept                  kept        kept
```

Two properties matter. First, the error is bounded: a signal reconstructed by linear interpolation between kept points is within epsilon of the original at every instant. Second, the reference is the interpolated path, not the last transmitted value. A conventional deadband (OPC UA, LwM2M, BACnet, IEC 61850) retransmits every step of a slow ramp; curve logging sends a ramp as two points and still catches a spike that returns to baseline. The survey of 34 standards in this folder found no other collection trigger that works this way.

## Efficiency evidence

| Source | Signal | Epsilon | Result |
|---|---|---|---|
| Geotab curve README | Speed | 4 km/h | 1,116 points to 148 (over 85 percent reduction) |
| Geotab curve README | GPS | perpendicular | 625 points to 23 (over 95 percent reduction) |
| Bosch/ETAS, Eclipse SDV Fleet Blueprint, 2024 (reported in the IETF draft) | Speed, ~1 Hz delivery route | 3.8 km/h (FMD) | about 76 percent reduction, "retaining the critical changes and trend of the data" |
| Kuksa fork benchmark (Guild, 2026) | Speed, 472 samples at 1 Hz | 3.8 km/h | 91 points kept, 81 percent reduction, full 0.07 to 90.7 km/h range preserved |
| Geotab/Mecanica white paper, 2022 | Speed and position vs. 100 Hz RTK logger | production settings | curve-based logging "most efficient" and comparable to the reference logger; Mecanica's CEO is quoted that the logic can "cut data volume by 30%" while maintaining quality |

The spread is the point: reduction depends on how much actually happens. A highway cruise compresses to almost nothing; stop-and-go delivery keeps more. Fixed-interval logging spends the same bandwidth either way. Fewer points mean less cellular traffic, smaller ingestion and storage, and cheaper queries, and the saving compounds with bit-level compression downstream, since curve logging reduces points rather than bits per point.

## Threshold crossing is the event

The compression story understates the case. A kept point is, by definition, a moment when the signal stopped doing what a straight line predicted. That is also the definition of something a data consumer wants to know about.

- **Speed and position for trip reconstruction.** A vehicle at 100 km/h covers 28 m per second. A 30-second ping misses the corner, draws the route through a building and under-reports mileage, as the Geotab blog illustrates. Curve-logged GPS keeps the turn because the turn is the deviation; a fleet gets accurate routes and distance, an insurer gets the braking and cornering profile, with fewer records than the ping.
- **Harsh braking.** A braking event lasts one to two seconds. At 15-second sampling it disappears between samples; at 1 Hz fixed rate it may still be clipped. With a 3.8 km/h epsilon, the onset, the knee and the stop are the three points that cannot be interpolated away, so the event record is the event itself. Insurers and safety programs get the signal with no separate "event detector" to tune.
- **Coolant temperature excursion.** FMD suggests a 4 degree C epsilon with a periodic heartbeat. A warm engine at steady temperature produces heartbeat points only. The moment temperature climbs off its trend, points appear, and the slope of those points tells the maintenance provider whether it is a hill or a failing thermostat, before a fault code is set.
- **Battery state of charge and voltage.** A 1 percent epsilon on EV state of charge yields a discharge curve whose kept points fall exactly where consumption changes (grade, HVAC, fast charge). On 12 V systems, a 0.894 V epsilon with a 30-second heartbeat tracks the slow decline of an ageing battery over weeks, and a tighter "partial RDP" tolerance during the five-second cranking burst preserves the sawtooth that predicts starter failure while still shedding most of the 100 Hz samples.

The consumer's requirement is expressed in one number, in physical units they already understand, and the same number is what makes the stream cheap. There is no second-order loss of fidelity hidden in an aggregate, as there is with averaging or downsampling.

## How it fits the standards

- **VSS** names and types the signals (`Vehicle.Speed`, `Vehicle.Powertrain.TractionBattery.StateOfCharge.Current`), so epsilons attach to shared identifiers, not vendor fields.
- **VISS** (W3C VISSv2, now COVESA VISS v3.2) defines `curvelog` as a subscription filter with `maxerr` (the epsilon) and `bufsize`; any VISS client can request a curve-logged stream without a proprietary API. Support is optional in the spec, an argument for OEMs to implement it.
- **FMD** recommends "smart/curve logic" for continuous signals, links to the Geotab library, and carries a "Curve error threshold when applicable" column with the per-signal values used above.
- **The IETF draft** argues that no single fixed sampling regime satisfies every consumer and positions curve logging with per-signal epsilons as the open answer.
- **Proposed VSS metadata** ([Data_Collection_Conventions_Assessment1.md](Data_Collection_Conventions_Assessment1.md)) would record `curve_epsilon`, `curve_algorithm` and min/max interval in signal catalogs, so the collection contract travels with the data model.

## Implementation options for an OEM

1. **Edge library in the telematics unit or zonal controller.** Vendor the Rust crate from github.com/Geotab/curve (MPL-2.0, embedded-friendly) and run it per signal with FMD epsilons. This is how GO devices and the Eclipse SDV Fleet Blueprint work.
2. **Databroker filter.** Apply curve logging at the in-vehicle signal broker so every subscriber receives a compressed stream. The Kuksa fork above implements the VISS `curvelog` filter in Rust against the same crate, with integration tests on 1 Hz and 50 Hz datasets; COVESA's VISSR reference server has a Go implementation.
3. **Cloud-side thinning.** Workable for existing full-rate pipelines, but it forfeits the bandwidth saving.

In every case epsilon should be configurable per signal and per campaign, with a heartbeat interval so consumers can tell "nothing changed" from "no data".

## Conclusion

Curve logging lets an OEM move fewer bytes and store less, and the evidence is public and reproducible. The stronger reason to adopt it is that the bytes it moves are the ones that carry meaning: the brake, the turn, the temperature climb, the charge dip. The method is open source with an MPL-2.0 patent grant, specified in VISS, recommended by FMD, and running in production at fleet scale. For an OEM building connected services for fleets, insurers and maintenance partners, it is the rare choice that lowers cost and raises product quality at the same time.
