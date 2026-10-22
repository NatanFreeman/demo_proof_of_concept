# Management Briefing: Arrow 3 Interceptor Segment Specification (A3-INT-SSS-010 Rev A)

## Overview
This document specifies the requirements for the Arrow 3 Interceptor Segment, comprising the two-stage solid-propellant interceptor, the exo-atmospheric hit-to-kill vehicle, and the canister (together termed the All-Up Round or AUR). This draft is prepared for the Preliminary Design Review (PDR).

## Subsystem Key Values
* **General & Physical**: Two-stage solid-propellant vehicle; AUR mass (including canister) ≤ 1,450 kg.
* **Electrical**: Operates on launcher-supplied 28 VDC (MIL-STD-1275E); pre-launch current draw ≤ 18 A; powered by internal thermal batteries during flight.
* **Data & Timing**: Pre-launch data via dual-redundant Gigabit Ethernet (1000BASE-T); READY report within 6.0 s of PTL command; system time synchronization within ±10 µs.
* **Navigation & Guidance**: Uses Earth-Centred Inertial coordinates (ECI, J2000 epoch); IMU alignment via transfer from launcher.
* **Environment & EMC**: Operating temperature -20 °C to +50 °C; storage/transport temperature -40 °C to +71 °C; compliant with MIL-STD-461F (CE102, CS114, RE102, RS103).
* **Reliability & Safety**: Captive-carry MTBF ≥ 1,500 h; storage life ≥ 10 years; rocket motor ignition requires two independent inhibits.

## Cited Documents and Standards
* **Internal Specifications**:
    * A3-SRS-001 (System Requirements Specification)
    * A3-ICD-110 (Interceptor–Launcher Interface Control Document)
    * A3-ICD-120 (BMC–FCR–Launcher Data Interface Control Document)
    * A3-ENV-050 (Environmental and RAM Requirements)
    * A3-SRS-001-CA (Classified Annex for kinematics and lethality)
* **Military Standards**:
    * MIL-STD-461F (Electromagnetic Interference Characteristics)
    * MIL-STD-1275E (28 VDC Electrical Systems in Military Vehicles)
