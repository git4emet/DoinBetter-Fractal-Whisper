# DoinBetter-Fractal-Whisper
Self-healing Speech-to-text system.

## AET + GSOC integration (expanded)

This layer maps American Engineering Testing (AET) workflows and Gopher State One Call (GSOC/811) utilities into the Möbius observability stack so field logistics, safety, and documentation stay in sync.

### Integration goals
- **Safety-first dig planning:** Link GSOC tickets to AET geotech tasks so crews only mobilize once utility locates are validated and expiration windows are tracked.
- **Unified project context:** Merge AET lab/field data (soil borings, compaction tests, pavement cores) with GSOC ticket metadata for a single site narrative.
- **Real-time operational awareness:** Surface ticket status, locate marks, and field progress in the observability dashboard to prevent disconnects between dispatch and site reality.

### Data model additions
Use JSON-LD to normalize AET and GSOC entities into a shared graph.

- **AET entities:** `SiteInvestigation`, `FieldObservation`, `LabResult`, `MaterialSample`, `Report`.
- **GSOC entities:** `LocateRequest`, `TicketStatus`, `FacilityOwner`, `MarkingWindow`, `ExcavationPolygon`.
- **Shared links:** `siteId`, `ticketId`, `geoFence`, `scheduleWindow`, `riskLevel`.

### Flow (bootstrap → ARC4 → observability)
1. **Bootstrap:** Seed the database with AET project metadata and GSOC ticket placeholders for any planned excavation site.
2. **ARC4 hooks:** Sync GSOC ticket status updates and AET field logs into the same event stream.
3. **Observability dashboard:** Show a triangle of *risk*, *readiness*, and *progress* for every site.

### Suggested event schema (concise)
```json
{
  "siteId": "MN-4321",
  "ticketId": "GSOC-811-2024-000123",
  "status": "Marking In Progress",
  "riskLevel": "High",
  "geoFence": "polygon",
  "nextAction": "Hold excavation until marks verified"
}
```

### Operational checks
- Gate excavation start on `TicketStatus=Cleared`.
- Auto-expire tickets after the locate window and surface for renewal.
- Flag any discrepancy between GSOC maps and AET field observations.

### Roadmap hooks
- **Voice-enabled field assistant:** hands-free ticket lookup, safety confirmations, and status updates on-site.
- **Geofence integration:** alert when crews enter a site before the ticket is cleared.
- **Automated compliance reporting:** compile AET report sections with GSOC ticket timelines.
