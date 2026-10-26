# Technology

## Tiered sensing
Three tiers of sensing, each used where it earns its place.
- RGB imaging (visible light, about 400–700 nm): surface condition — soiling, cracks, discolouration, vegetation, physical damage.
- Thermal imaging (long-wave infrared, about 8–14 µm): operational anomalies — hotspots, bypass-diode faults, disconnected strings, cell mismatch.
- LiDAR: terrain and site geometry, used as input to microclimate modelling (shading, drainage, dust paths, wind exposure).
- Terahertz (THz, roughly 30–300 µm): subsurface and material state — encapsulant condition, delamination, moisture, interface degradation — measured by a panel-crawling robot on modules selected by the screening tiers.

## Edge AI
Inference runs on the drone during the flight on an edge inference unit: onboard quality checks, module localisation, anomaly ranking and target selection. Only regions of interest are uplinked, so surveys produce a prioritised inspection plan and 3D terrain inputs rather than terabytes of raw imagery. Edgegenix contributes the model training and edge deployment pipeline.

## Spatiotemporally resolved digital twin (ST-Twin)
The ST-Twin is a hybrid physics-and-data model. Each module is a record: manufacturer, model, bill of materials, factory batch and lamination record, install date, string position and mounting. That record is linked to the place it lives — local environmental exposure (salt, wetting, heat, dust, hail, frost) — and to repeated inspection evidence, energy performance and maintenance history. The twin quantifies performance impacts, evaluates intervention scenarios and tests its predictions against measured outcomes, refining itself over time. Outputs: condition estimates, root-cause assessment and lifecycle decisions with explicit cost comparison.

## Evidence chain
Materials and processes → environmental exposure → condition evolution → energy losses → intervention outcomes. Field observations become lifecycle decisions, each supported by an explicit cost comparison, and every prediction stays traceable and testable.

## Workflow
Broad-area screening → targeted diagnostics → physics-informed modelling → economic optimisation. Each step adds evidence only where it can improve the next decision.
