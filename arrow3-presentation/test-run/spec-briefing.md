# Briefing: Arrow 3 Interceptor Segment Specification (A3-INT-SSS-010 Rev A)

## Overview
This document defines the requirements for the Arrow 3 Interceptor Segment, consisting of the two-stage solid-propellant interceptor, the exo-atmospheric hit-to-kill vehicle, and the canister (delivered as an All-Up Round - AUR).

## Subsystem Key Values
- **Physical**: AUR mass (including canister) ≤ 1,450 kg; two-stage solid-propellant design.
- **Electrical**: Powered by launcher 28 VDC (MIL-STD-1275E); pre-launch draw ≤ 18 A; flight powered by internal thermal batteries.
- **Data & Timing**: Dual-redundant Gigabit Ethernet (1000BASE-T) for pre-launch data; READY report within 6.0 s of PTL command; system time sync within ±10 µs.
- **Navigation & Guidance**: ECI (J2000 epoch) coordinates for target data and updates; transfer alignment from launcher.
- **Environment & EMC**: Operating temperature -20 °C to +50 °C; storage temperature -40 °C to +71 °C; compliant with MIL-STD-461F (CE102, CS114, RE102, RS103).
- **Reliability & Safety**: Captive-carry MTBF ≥ 1,500 h; storage life ≥ 10 years; dual-independent inhibits for rocket motor ignition; authenticated messaging.

## Cited Documents and Standards
- **Internal Specifications**:
    - A3-SRS-001: System Requirements Specification
    - A3-ICD-110: Interceptor–Launcher Interface Control Document
    - A3-ICD-120: BMC–FCR–Launcher Data Interface Control Document
    - A3-ENV-050: Environmental and RAM Requirements
- **Military Standards**:
    - MIL-STD-461F: Control of Electromagnetic Interference Characteristics
    - MIL-STD-1275E: 28 VDC Electrical Systems in Military Vehicles
