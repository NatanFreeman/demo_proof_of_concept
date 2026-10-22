**ARROW 3 WEAPON SYSTEM**

**Interceptor Segment Specification**

Two-stage interceptor and exo-atmospheric kill vehicle — draft for Preliminary Design Review

| **Document number** | A3-INT-SSS-010                                  |
|---------------------|-------------------------------------------------|
| **Revision**        | A                                               |
| **Date**            | 20 October 2026                                 |
| **Status**          | Draft for PDR — submitted for consistency check |
| **Prepared by**     | Interceptor Integrated Product Team             |
| **Classification**  | UNCLASSIFIED // FICTITIOUS DEMONSTRATION DATA   |

**Revision history**

| **Rev** | **Date**    | **Description**                           | **CCB ref.** |
|---------|-------------|-------------------------------------------|--------------|
| **A**   | 20 Oct 2026 | First issue for Preliminary Design Review | —            |

**Approvals**

| **Role**                     | **Organisation**          | **Signature** | **Date**    |
|------------------------------|---------------------------|---------------|-------------|
| **Interceptor Segment lead** | Interceptor IPT           | e-signed      | 20 Oct 2026 |
| **Chief Systems Engineer**   | Weapon System Engineering | pending       | —           |

# 1. Scope

This specification defines the requirements of the Arrow 3 Interceptor Segment: the two-stage interceptor, the exo-atmospheric kill vehicle and the canister, delivered together as the all-up round (AUR).

*Kinematic and lethality performance is specified in the classified annex A3-SRS-001-CA.*

# 2. Applicable documents

| **Document**      | **Title**                                               | **Rev** |
|-------------------|---------------------------------------------------------|---------|
| **A3-SRS-001**    | System Requirements Specification                       | C       |
| **A3-ICD-110**    | Interceptor–Launcher Interface Control Document         | B       |
| **A3-ICD-120**    | BMC–FCR–Launcher Data Interface Control Document        | A       |
| **A3-ENV-050**    | Environmental and RAM Requirements                      | B       |
| **MIL-STD-461F**  | Control of Electromagnetic Interference Characteristics | F       |
| **MIL-STD-1275E** | 28 VDC Electrical Systems in Military Vehicles          | E       |

# 3. Requirements

*Verification methods: A = Analysis, I = Inspection, D = Demonstration, T = Test.*

## 3.1 General and physical

| **Req. ID**     | **Requirement**                                                                                                      | **Verif.** | **Parent / trace** |
|-----------------|----------------------------------------------------------------------------------------------------------------------|------------|--------------------|
| **INT-GEN-001** | The interceptor shall be a two-stage, solid-propellant vehicle carrying an exo-atmospheric hit-to-kill kill vehicle. | I          | A3-SRS-001 §1.1    |
| **INT-PHY-002** | The mass of the all-up round, including the canister, shall not exceed 1,450 kg.                                     | I          | A3-ICD-110         |
| **INT-PHY-003** | The canister envelope shall conform to drawing A3-LCH-DWG-2210 Rev D.                                                | I          | IF-MEC-001         |

## 3.2 Electrical

| **Req. ID**     | **Requirement**                                                                                                                            | **Verif.** | **Parent / trace** |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------|------------|--------------------|
| **INT-PWR-010** | The interceptor shall operate from launcher-supplied 28 VDC power with the characteristics of MIL-STD-1275E.                               | T          | SRS-PWR-001        |
| **INT-PWR-012** | During pre-launch (IMU run-up and thermal conditioning) the interceptor shall draw not more than 18 A continuous from the launcher supply. | T          | SRS-PWR-002        |
| **INT-PWR-014** | Internal thermal batteries shall be activated on receipt of the LCH command and shall power the interceptor for the whole flight.          | T          | —                  |

## 3.3 Data and timing

| **Req. ID**     | **Requirement**                                                                                                                                              | **Verif.** | **Parent / trace** |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|--------------------|
| **INT-DAT-020** | The interceptor shall exchange pre-launch data with the launcher over a dual-redundant Gigabit Ethernet (1000BASE-T) link, the interceptor acting as server. | T          | A3-ICD-110         |
| **INT-DAT-022** | In-flight target update messages shall be decoded per A3-ICD-120 Rev A.                                                                                      | I          | A3-ICD-120         |
| **INT-TIM-031** | The interceptor shall report READY within 6.0 s of receiving the Prepare-to-Launch (PTL) command.                                                            | T          | SRS-TL-002         |
| **INT-TIM-035** | The interceptor time reference shall be synchronised to system time within ±10 µs.                                                                           | T          | SRS-TIM-001        |

## 3.4 Navigation and guidance

| **Req. ID**     | **Requirement**                                                                                                                               | **Verif.** | **Parent / trace** |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------|--------------------|
| **INT-NAV-040** | Pre-launch target data and in-flight target updates shall be received and processed in Earth-Centred Inertial coordinates (ECI, J2000 epoch). | I          | SRS-NAV-002        |
| **INT-NAV-042** | The inertial measurement unit shall be aligned before launch by transfer alignment from the launcher (message ALN).                           | T          | IF-DAT-004         |

## 3.5 Environment and EMC

| **Req. ID**     | **Requirement**                                                                     | **Verif.** | **Parent / trace** |
|-----------------|-------------------------------------------------------------------------------------|------------|--------------------|
| **INT-ENV-050** | The all-up round shall operate at ambient temperatures from −20 °C to +50 °C.       | T          | SRS-ENV-002        |
| **INT-ENV-052** | Non-operating (storage and transport) temperature range shall be −40 °C to +71 °C.  | T          | ENV-TMP-002        |
| **INT-EMC-060** | The interceptor shall meet MIL-STD-461F requirements CE102, CS114, RE102 and RS103. | T          | SRS-EMC-001        |

## 3.6 Reliability and safety

| **Req. ID**     | **Requirement**                                                                                             | **Verif.** | **Parent / trace** |
|-----------------|-------------------------------------------------------------------------------------------------------------|------------|--------------------|
| **INT-RAM-070** | The captive-carry MTBF of the all-up round, powered on the launcher, shall be at least 1,500 h.             | A          | RAM-004            |
| **INT-RAM-072** | The interceptor shall have a storage life of at least 10 years in its sealed canister.                      | A          | SRS-RAM-010        |
| **INT-SAF-080** | Rocket motor ignition shall require two independent inhibits to be removed, one controlled by the launcher. | D          | SRS-SAF-002        |
| **INT-CYB-090** | All messages received by the interceptor shall be authenticated before use.                                 | T          | SRS-IF-003         |

# 4. Notes

This draft is submitted for the PDR data package. Segment-level changes since the concept phase: Ethernet replaces the legacy data bus to support faster alignment transfer; the guidance team prefers inertial coordinates for in-flight updates.

| **Acronym** | **Meaning**                                |
|-------------|--------------------------------------------|
| **AUR**     | All-up round (interceptor in its canister) |
| **BMC**     | Battle Management Center                   |
| **CCB**     | Configuration Control Board                |
| **ECEF**    | Earth-Centred, Earth-Fixed                 |
| **FCR**     | Fire Control Radar                         |
| **ICD**     | Interface Control Document                 |
| **IFTU**    | In-flight target update                    |
| **LCU**     | Launcher Control Unit                      |
| **MTBF**    | Mean time between failures                 |
| **PTL**     | Prepare-to-Launch command                  |
| **RT**      | Remote terminal (MIL-STD-1553B)            |
| **TBR**     | To be reviewed                             |
