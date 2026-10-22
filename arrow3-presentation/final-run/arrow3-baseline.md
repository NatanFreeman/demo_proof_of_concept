## A3-BMC-SSS-030_RevA_Battle_Management_Center_Specification.docx

A3-BMC-SSS-030, RevA, Battle Management Center Specification

| **BMC-ENG-005** | The BMC shall complete engagement planning and transmit the engagement command to the selected launcher within 2.0 s of the operator engagement order.        | T          | SRS-TL-002         |
| **BMC-ENG-020** | The BMC shall transmit in-flight target updates (IFTU) to each interceptor in flight at not less than 4 Hz, in WGS-84 ECEF coordinates, per A3-ICD-120 Rev C. | T          | SRS-NAV-002        |
| **BMC-TIM-002** | The BMC master clock shall be GPS-disciplined and shall distribute system time to all segments with an accuracy of ±1 µs.                                     | T          | SRS-TIM-001        |
| **BMC-NAV-004** | The BMC shall perform all engagement computations and exchange all state vectors in WGS-84 ECEF.                                                              | I          | SRS-NAV-002        |
| **BMC-CYB-010** | All BMC tactical messages shall be authenticated and encrypted per the program cryptographic plan.                                                            | T          | SRS-IF-003         |
| **BMC-RAM-012** | The BMC shall achieve an inherent availability of at least 0.99 with hot-standby redundancy.                                                                  | A          | SRS-RAM-001        |

## A3-ENV-050_RevB_Environmental_and_RAM_Requirements.docx

A3-ENV-050, RevB, Environmental and RAM Requirements

| **ENV-TMP-001** | All field-deployed equipment, including the all-up round in its canister, shall operate at ambient temperatures from −33 °C to +55 °C. | T          | SRS-ENV-002        |
| **ENV-TMP-002** | Non-operating (storage and transport) temperature range shall be −40 °C to +71 °C.                                                     | T          | SRS-ENV-001        |
| **ENV-HUM-003** | Equipment shall withstand humidity per MIL-STD-810H Method 507.6, Procedure II.                                                        | T          | SRS-ENV-001        |
| **ENV-SND-004** | Equipment shall withstand blowing sand and dust per MIL-STD-810H Method 510.7.                                                         | T          | SRS-ENV-001        |
| **ENV-VIB-005** | Transport vibration shall be per MIL-STD-810H Method 514.8, Category 4 (truck transportation).                                         | T          | SRS-ENV-001        |
| **ENV-EMC-010** | All segments shall meet MIL-STD-461G requirements CE102, CS101, CS114, RE102 and RS103 as tailored in Annex B.                         | T          | SRS-EMC-001        |
| **RAM-004** | Interceptor (all-up round) captive-carry MTBF, powered in the canister on the launcher, shall be at least 2,000 h. | A          | SRS-RAM-004        |
| **RAM-005** | Launcher MTBF shall be at least 1,200 h.                                                                           | A          | SRS-RAM-004        |
| **RAM-006** | FCR MTBCF shall be at least 500 h.                                                                                 | A          | SRS-RAM-004        |
| **RAM-010** | Interceptor storage life in the sealed canister shall be at least 15 years.                                        | A          | SRS-RAM-010        |

## A3-FCR-SSS-020_RevB_Fire_Control_Radar_Specification.docx

A3-FCR-SSS-020, RevB, Fire Control Radar Specification

| **FCR-TRK-010** | The FCR shall maintain tracks on all threats within its coverage as specified in A3-SRS-001-CA.                                  | T          | SRS-TL-003         |
| **FCR-TRK-012** | The FCR shall report target track state vectors to the BMC at not less than 10 Hz per engaged track, in WGS-84 ECEF coordinates. | T          | SRS-NAV-002        |
| **FCR-TIM-003** | Track messages shall carry a time tag accurate to ±1 µs of system time.                                                          | T          | SRS-TIM-001        |
| **FCR-IF-001**  | All FCR–BMC data exchange shall conform to A3-ICD-120 Rev C.                                                                     | I          | SRS-IF-002         |
| **FCR-ENV-001** | The FCR shall meet A3-ENV-050 Rev B for field-deployed equipment.                                                                | T          | SRS-ENV-001        |
| **FCR-EMC-002** | The FCR shall meet MIL-STD-461G, tailored per A3-ENV-050 Rev B.                                                                  | T          | SRS-EMC-001        |
| **FCR-RAM-004** | The FCR mean time between critical failures (MTBCF) shall be at least 500 h.                                                     | A          | SRS-RAM-004        |

## A3-ICD-110_RevC_Interceptor-Launcher_ICD.docx

A3-ICD-110, RevC, Interceptor-Launcher ICD

This ICD defines the interface between the Arrow 3 all-up round (AUR: interceptor in its canister) and the launcher canister cell. Both the Interceptor Segment and the Launcher Segment shall comply with it.
| **IF-MEC-001** | The canister outer envelope and attachment points shall conform to drawing A3-LCH-DWG-2210 Rev D. | I          | SRS-IF-001         |
| **IF-MEC-002** | The mass of the loaded canister (all-up round) shall not exceed 1,350 kg.                         | I          | SRS-IF-001         |
| **IF-MEC-003** | The centre of gravity of the AUR shall lie within the envelope of A3-LCH-DWG-2210 Rev D, sheet 4. | A          | IF-MEC-001         |
| **IF-PWR-001** | The launcher shall supply 28 VDC (MIL-STD-1275E) to each canister cell through umbilical connector J1.                                                         | T          | SRS-PWR-002        |
| **IF-PWR-003** | The current drawn by one AUR from the launcher supply shall not exceed 12 A continuous in any pre-launch state, including IMU run-up and thermal conditioning. | T          | SRS-PWR-002        |
| **IF-PWR-004** | Inrush current at power application shall not exceed 20 A for more than 50 ms.                                                                                 | T          | IF-PWR-003         |
| **IF-CON-005** | Umbilical connector J1 shall be MIL-DTL-38999 Series III, shell size 25, 61 contacts; pin allocation per Table 3.                                              | I          | —                  |
| **IF-DAT-001** | Data between the Launcher Control Unit and the AUR shall be exchanged over a dual-redundant MIL-STD-1553B bus (Bus A / Bus B). The LCU shall be bus controller; the interceptor shall be remote terminal RT 05. | T          | SRS-IF-001         |
| **IF-DAT-004** | The message set shall be as defined in Table 4: PTL (Prepare-to-Launch), STS (status), ALN (transfer alignment), TGT (pre-launch target data), LCH (launch) and ABT (abort).                                    | I          | IF-DAT-001         |
| **IF-NAV-006** | Pre-launch target data (message TGT) shall be expressed in WGS-84 ECEF coordinates per SRS-NAV-002.                                                                                                             | I          | SRS-NAV-002        |
| **IF-SEQ-006** | The interceptor shall report READY (message STS, bit 0) within 3.0 s of receiving PTL.                                                                        | T          | SRS-TL-002         |
| **IF-SEQ-007** | The launcher shall not issue LCH before READY. If READY is not received within 3.5 s of PTL, the LCU shall declare HANG-FIRE and select the next canister.    | T          | SRS-SAF-002        |
| **IF-TIM-010** | The LCU shall distribute system time to the AUR by 1553B time-tag message plus a 1 PPS discrete; the interceptor shall align its time reference within ±1 µs. | T          | SRS-TIM-001        |

## A3-LCH-SSS-040_RevB_Launcher_Segment_Specification.docx

A3-LCH-SSS-040, RevB, Launcher Segment Specification

| **LCH-MOB-001** | The launcher shall be transportable on public roads without special permits when stowed.                                            | D          | Logistics concept  |
| **LCH-MEC-014** | The erector shall be rated for loaded canisters (all-up rounds) of up to 1,350 kg per cell, with a structural safety factor of 1.5. | A          | IF-MEC-002         |
| **LCH-MEC-016** | The erector shall raise the canister pack from stowed to launch elevation in not more than 60 s.                                    | T          | —                  |
| **LCH-PWR-020** | The launcher shall be capable of autonomous operation from its own generator for at least 24 h.                                                    | D          | —                  |
| **LCH-PWR-021** | The PDU shall supply 28 VDC (MIL-STD-1275E) to each of the six canister cells, limited to 12 A continuous per cell by electronic circuit breakers. | T          | IF-PWR-003         |
| **LCH-DAT-010** | The LCU shall act as MIL-STD-1553B bus controller on one dual-redundant bus per canister cell.                                                              | T          | IF-DAT-001         |
| **LCH-DAT-012** | The LCU shall exchange engagement commands and status with the BMC per A3-ICD-120 Rev C.                                                                    | T          | SRS-IF-002         |
| **LCH-TL-003**  | The LCU shall issue PTL to the selected canister within 3.0 s of receiving a valid engagement command, and shall issue LCH within 50 ms of receiving READY. | T          | SRS-TL-002         |
| **LCH-TIM-005** | The LCU shall distribute system time to each canister cell within ±1 µs of the BMC master clock.                                                            | T          | SRS-TIM-001        |
| **LCH-ENV-030** | The launcher shall operate at ambient temperatures from −33 °C to +55 °C.                   | T          | SRS-ENV-002        |
| **LCH-ENV-031** | The launcher shall meet the transport shock and vibration requirements of A3-ENV-050 Rev B. | T          | SRS-ENV-001        |
| **LCH-SAF-040** | The launcher shall provide the launcher-controlled ignition inhibit required by SRS-SAF-002. | D          | SRS-SAF-002        |

## A3-SRS-001_RevC_System_Requirements_Specification.docx

A3-SRS-001, RevC, System Requirements Specification

| **SRS-TL-001** | The weapon system shall launch the first interceptor within 8.0 s of the engagement order issued by the BMC operator (system reaction time).                                                                                                                                                                                                    | T          | Mission need MN-04 |
| **SRS-TL-002** | The system reaction time of SRS-TL-001 shall be allocated sequentially: BMC engagement planning (operator order to engagement command at the launcher) ≤ 2.0 s; launcher preparation (engagement command to PTL issued) ≤ 3.0 s; interceptor pre-launch preparation (PTL received to READY reported) ≤ 3.0 s. The launcher issues LCH on READY. | A          | SRS-TL-001         |
| **SRS-TL-003** | The system shall support simultaneous engagement of multiple threats; the number of simultaneous engagements is specified in A3-SRS-001-CA.                                                                                                                                                                                                     | D          | Mission need MN-05 |
| **SRS-TIM-001** | All segments shall maintain a common system time, disciplined to GPS by the BMC master clock, synchronised within ±1 µs of the master clock.                                           | T          | SRS-TL-001         |
| **SRS-NAV-002** | All target state vectors and launch parameters exchanged between segments shall be expressed in WGS-84 Earth-Centred, Earth-Fixed (ECEF) coordinates, in metres and metres per second. | I          | NGA.STND.0036      |
| **SRS-PWR-001** | Field equipment shall operate from 28 VDC power with the characteristics of MIL-STD-1275E.                                                                                                  | T          | —                  |
| **SRS-PWR-002** | The launcher shall supply all interceptor pre-launch power through the umbilical defined in A3-ICD-110; the interceptor shall not draw more than the per-canister allocation of A3-ICD-110. | A          | SRS-PWR-001        |
| **SRS-IF-001** | The interceptor–launcher interface shall conform to A3-ICD-110 Rev C.                        | I          | —                  |
| **SRS-IF-002** | Data interfaces between BMC, FCR and launchers shall conform to A3-ICD-120 Rev C.            | I          | —                  |
| **SRS-IF-003** | All tactical messages shall be authenticated; encryption per the program cryptographic plan. | T          | Security CONOPS    |
| **SRS-ENV-001** | All field-deployed equipment shall meet the environmental requirements of A3-ENV-050 Rev B.                                                 | T          | —                  |
| **SRS-ENV-002** | All field-deployed equipment shall operate at ambient temperatures from −33 °C to +55 °C, with solar loading per MIL-STD-810H Method 505.7. | T          | SRS-ENV-001        |
| **SRS-EMC-001** | All segments shall meet MIL-STD-461G, tailored per A3-ENV-050 Rev B.                                                                        | T          | —                  |
| **SRS-RAM-001** | The weapon system operational availability (Ao) shall be at least 0.95.                                                  | A          | —                  |
| **SRS-RAM-004** | Segment reliability allocations shall be as defined in A3-ENV-050 Rev B, Section 4.                                      | A          | SRS-RAM-001        |
| **SRS-RAM-010** | The interceptor shall have a storage life of at least 15 years in its sealed canister, with periodic built-in test only. | A          | Logistics concept  |
| **SRS-SAF-001** | A system safety program shall be conducted per MIL-STD-882E.                                                                     | I          | —                  |
| **SRS-SAF-002** | Rocket motor ignition shall require at least two independent inhibits to be removed, one of which is controlled by the launcher. | D          | SRS-SAF-001        |
