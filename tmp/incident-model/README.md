# COVESA S2DM — Generic Incident Data Model

A generic vehicle incident data model following the
[COVESA S2DM](https://github.com/COVESA/s2dm) (Simplified Semantic Data Modeling)
approach using GraphQL SDL.

## Purpose

Defines a reusable base model for incident reporting across fleet and
commercial vehicle operations. The generic model is designed to be
**extended** by specializations for specific incident types.

## File Structure

```
incident-model/
├── Incident.graphql               # Root generic incident type
├── Incident_Classification.graphql # Category + type + detection method
├── Incident_Enums.graphql         # All shared enumerations
├── Incident_Location.graphql      # WGS84 location with context
├── Incident_Party.graphql         # Involved parties (vehicle, person, org)
├── Incident_Evidence.graphql      # Evidence + telematics snapshot
├── Incident_Response.graphql      # Actions taken + insurance claim
└── specializations/
    ├── VehicleTheft.graphql       # Theft-specific extension (TODO)
    ├── UnsafeDriving.graphql      # Unsafe driving extension (TODO)
    └── AccidentReport.graphql     # Collision report extension (TODO)
```

## Design Principles

- **Generic base, specific extensions**: `Incident` captures what is
  common to all incidents; specializations add domain-specific fields
  using GraphQL `extend type` or new linked types.
- **VSS-aligned signals**: `IncidentTelematicsSnapshot` field names and
  units follow COVESA VSS signal paths where applicable.
- **Open classification**: `IncidentClassification.type` is a `String`
  rather than a fixed enum, allowing each specialization to define its
  own type enum without modifying the base model.
- **Modular composition**: Each sub-domain (location, party, evidence,
  response) is in its own file, following the S2DM modular pattern.

## Planned Specializations

| Type | Category | Key Added Fields |
|---|---|---|
| `VehicleTheft` | THEFT | **Complete** — 7 use cases (THEFT01-07): identification, location/movement, intrusion detection, key auth, lost mode/alarm, security sensors, vehicle state |
| `UnsafeDriving` | UNSAFE_DRIVING | behavior type, threshold exceeded, rule violated |
| `AccidentReport` | ACCIDENT | collision type, conditions, injuries, damage |

## S2DM Directives Used

| Directive | Usage |
|---|---|
| `@range(min, max)` | Constrain numeric fields (lat/lon, heading, fuel level) |
| `@cardinality(min, max)` | Define collection size expectations |
| `@noDuplicates` | Prevent duplicate entries in lists |
| `@metadata(vssType, comment)` | Mark signal types (sensor/actuator/attribute) |

## References

- [COVESA S2DM](https://github.com/COVESA/s2dm)
- [COVESA VSS](https://github.com/COVESA/vehicle_signal_specification)
- COVESA Commercial and Fleet Vehicles Expert Group
