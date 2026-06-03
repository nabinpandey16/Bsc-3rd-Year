# Junction Field Effect Transistor (JFET) — Drain & Transfer Characteristics

![Physics](https://img.shields.io/badge/Physics-Electronics-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=flat-square&logo=python)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-orange?style=flat-square&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-red?style=flat-square)
![SciPy](https://img.shields.io/badge/SciPy-Curve%20Fitting-purple?style=flat-square)
![Institution](https://img.shields.io/badge/Institution-Tri--Chandra%20Campus-brown?style=flat-square)

> **Experiment No. 8 | BSc 3rd Year Physics Practical**  
> Tri-Chandra Multiple Campus, Tribhuvan University  
> Date: 2082/01/30 (BS) | Roll No: 079/295

---

## Overview

This repository contains a complete, reproducible analysis of an N-channel JFET's **drain** and **transfer (mutual) characteristics**, including curve fitting to the Shockley equation, transconductance extraction, pinch-off voltage determination, and full statistical error analysis.

| Parameter | Measured Value | Unit |
|-----------|---------------|------|
| I_DSS (at V_DS = 12.5 V) | 8.80 | mA |
| I_DSS (at V_DS = 10.0 V) | 6.80 | mA |
| I_DSS (at V_DS = 9.25 V) | 5.00 | mA |
| V_P (pinch-off) | −1.8 | V |
| V_GS(off) | ≈ −1.8 | V |
| g_m (transconductance) | ~3.5 | mA/V (mS) |

---

## Repository Structure

```
JFET_Characteristics/
│
├── README.md                         ← This file
├── requirements.txt                  ← Python dependencies
│
├── data/
│   ├── raw_data_drain.csv            ← Drain char. raw observations
│   ├── raw_data_transfer.csv         ← Transfer char. raw observations
│   ├── raw_data_pinchoff.csv         ← Pinch-off data
│   ├── processed_drain.csv           ← Cleaned drain data
│   ├── processed_transfer.csv        ← Cleaned transfer data
│   └── results_summary.csv           ← Final computed parameters
│
├── notebooks/
│   └── JFET_Analysis.ipynb           ← Full Jupyter analysis notebook
│
├── figures/
│   ├── drain_characteristics.png     ← I_D vs V_DS family of curves
│   ├── transfer_characteristics.png  ← I_D vs V_GS + Shockley fit
│   ├── transconductance.png          ← g_m vs V_GS
│   └── pinchoff_vs_vds.png           ← V_P determination
│
├── src/
│   └── analysis.py                   ← Standalone Python analysis script
│
└── report/
    └── Experiment_Report.pdf         ← Full formatted report
```

---

## Objective

To study and plot:
1. **Drain characteristics**: I_D vs V_DS at fixed V_GS (= 0 V, −1 V, −1.5 V)
2. **Transfer (mutual) characteristics**: I_D vs V_GS at fixed V_DS (= 9.25 V, 10 V, 12.5 V)
3. Determine **pinch-off voltage (V_P)**, **I_DSS**, and **transconductance (g_m)**
4. Fit the **Shockley equation** to transfer data and extract device parameters

---

## Apparatus Required

| Instrument | Specification | Measurement Range | Least Count |
|-----------|---------------|-------------------|-------------|
| DC Power Supply (V_DS) | Variable, 0–15 V | 0–20 V | 0.1 V |
| DC Power Supply (V_GS) | Variable, 0–5 V | 0–5 V | 0.1 V |
| Voltmeter (V_DS) | Analog, 10 div = 2.5 V | 0–25 V | 0.25 V |
| Voltmeter (V_GS) | Analog, 10 div = 1 V | 0–10 V | 0.1 V |
| Milliammeter (I_D) | Analog, 10 div = 2 mA | 0–20 mA | 0.2 mA |
| N-Channel JFET | BFW10 / 2N3819 type | — | — |
| Breadboard | Standard | — | — |
| Jumper Wires | — | — | — |

**Least counts:**  
- V_DS: 1 div = 0.25 V → **LC = 0.25 V**  
- V_GS: 1 div = 0.1 V → **LC = 0.1 V**  
- I_D: 1 div = 0.2 mA → **LC = 0.2 mA**

---

## Theory

### 1. JFET — Basic Principle

A **Junction Field Effect Transistor (JFET)** is a voltage-controlled, unipolar semiconductor device. Current conduction is by majority carriers only:
- **N-channel JFET**: electrons (majority), gate is p-type
- **P-channel JFET**: holes (majority), gate is n-type

It has three terminals: **Gate (G)**, **Source (S)**, **Drain (D)**.

The gate–channel junction is **reverse biased**, creating a depletion region that controls the effective cross-section of the conducting channel and hence the drain current.

### 2. Shockley's Equation

The fundamental transfer equation (in saturation region):

$$I_D = I_{DSS} \left(1 - \frac{V_{GS}}{V_P}\right)^2$$

where:
- $I_{DSS}$ = drain–source saturation current when $V_{GS} = 0$
- $V_P$ = pinch-off voltage (negative for N-channel)
- $V_{GS}$ = gate–source voltage

### 3. Drain Characteristics Regions

**Ohmic (Linear) Region** — $V_{DS} < V_{GS} - V_P$:

$$I_D \approx I_{DSS} \left[\frac{2V_{DS}}{|V_P|} \left(1 - \frac{V_{GS}}{V_P}\right) - \left(\frac{V_{DS}}{V_P}\right)^2\right]$$

The JFET behaves like a voltage-controlled resistor:

$$r_{DS} = \frac{|V_P|}{2 I_{DSS} \left(1 - V_{GS}/V_P\right)}$$

**Saturation (Active) Region** — $V_{DS} \geq V_{GS} - V_P$:

$$I_D = I_{DSS} \left(1 - \frac{V_{GS}}{V_P}\right)^2 = \text{constant}$$

**Cut-off Region** — $V_{GS} \leq V_P$ (channel fully depleted):

$$I_D = 0$$

### 4. Transfer Characteristics

The transconductance (mutual conductance):

$$g_m = \frac{\partial I_D}{\partial V_{GS}}\bigg|_{V_{DS} = \text{const}} = \frac{-2 I_{DSS}}{V_P} \left(1 - \frac{V_{GS}}{V_P}\right)$$

Maximum transconductance (at $V_{GS} = 0$):

$$g_{m0} = \frac{-2 I_{DSS}}{V_P}$$

### 5. Pinch-off Voltage

The pinch-off voltage $V_P$ is the gate voltage at which $I_D \to 0$:

$$V_{GS(off)} = V_P \quad \Rightarrow \quad I_D = 0$$

For the device measured: $V_P \approx -1.8\text{ V}$

---

## Experimental Setup

The circuit consists of:
- Two variable DC supplies: one for $V_{DS}$ (drain circuit), one for $V_{GS}$ (gate circuit)
- N-channel JFET mounted on breadboard
- Voltmeters across drain–source and gate–source
- Milliammeter in series with drain circuit

**Circuit configuration:**
```
 +V_DS ─── [mA] ─── D
                      │
                    JFET (N-ch)
                      │
 −V_DS ─────────── S ──── GND
                      
 +V_GS ─── G (through R_G if needed)
 −V_GS ─── S
```

> **Note**: For an N-channel JFET, $V_{GS}$ is always ≤ 0 (reverse bias).

---

## Procedure

### Drain Characteristics

1. Assemble circuit on breadboard as per circuit diagram.
2. Set $V_{GS} = 0$ V. Vary $V_{DS}$ from 0 to ~14 V in steps of ~1.25 V.
3. Record $I_D$ at each step.
4. Repeat for $V_{GS} = -1$ V and $V_{GS} = -1.5$ V.
5. Plot $I_D$ vs $V_{DS}$ for all three curves.

### Transfer Characteristics

1. Set $V_{DS}$ = 10 V (fixed). Vary $V_{GS}$ from 0 to −1.8 V in steps of 0.2 V.
2. Record $I_D$ at each step.
3. Repeat for $V_{DS}$ = 12.5 V and $V_{DS}$ = 9.25 V.
4. Plot $I_D$ vs $V_{GS}$ for all three curves.

---

## Observation Tables

### Table 1: Drain Characteristics — $I_D$ (mA) vs $V_{DS}$ (V)

*Instrument: Voltmeter LC = 0.25 V, Milliammeter LC = 0.2 mA*

| S.N. | $V_{DS}$ (V) | $I_D$ (mA) at $V_{GS}$=0 V | $I_D$ (mA) at $V_{GS}$=−1 V | $I_D$ (mA) at $V_{GS}$=−1.5 V |
|------|------------|------------------------|--------------------------|------------------------------|
| 1  | 1.25  | 0.8 | 0.8 | 0.2 |
| 2  | 2.50  | 1.4 | 1.2 | 0.2 |
| 3  | 3.75  | 2.2 | 1.6 | 0.2 |
| 4  | 5.00  | 2.8 | 1.8 | 0.2 |
| 5  | 6.25  | 3.4 | 2.0 | 0.4 |
| 6  | 6.50  | 3.6 | 2.0 | 0.4 |
| 7  | 8.75  | 3.8 | 2.0 | 0.4 |
| 8  | 10.00 | 3.8 | 2.0 | 0.4 |
| 9  | 11.25 | 3.8 | 2.0 | 0.4 |
| 10 | 12.50 | 3.8 | 2.0 | 0.4 |
| 11 | 13.95 | 3.0 | 2.0 | 0.4 |

### Table 2: Transfer Characteristics — $I_D$ (mA) vs $V_{GS}$ (V)

| S.N. | $V_{GS}$ (V) | $I_D$ (mA) at $V_{DS}$=10 V | $I_D$ (mA) at $V_{DS}$=12.5 V | $I_D$ (mA) at $V_{DS}$=9.25 V |
|------|-------------|--------------------------|----------------------------|-----------------------------|
| 1 | 0.0  | 6.8 | 8.8 | 5.0 |
| 2 | −0.2 | 6.8 | 8.6 | 5.0 |
| 3 | −0.4 | 6.8 | 8.6 | 4.8 |
| 4 | −0.6 | 6.4 | 8.6 | 4.8 |
| 5 | −0.8 | 5.5 | 8.0 | 4.0 |
| 6 | −1.0 | 5.4 | 5.6 | 3.2 |
| 7 | −1.2 | 3.2 | 3.2 | 2.8 |
| 8 | −1.4 | 2.8 | 2.8 | 0.0 |
| 9 | −1.6 | 0.8 | 0.8 | 0.0 |
| 10| −1.8 | 0.0 | 0.0 | 0.0 |

### Table 3: Pinch-off Voltage Determination

| S.N. | $V_{DS}$ (V) | $I_{DSS}$ (mA) | $V_{GS(off)}$ (V) |
|------|------------|--------------|------------------|
| 1 | 12.5 | 8.8 | −1.8 |
| 2 | 10.0 | 6.8 | −1.8 |
| 3 | 9.25 | 5.0 | −1.8 |

---

## Calculations

### Error Analysis

**Absolute uncertainty** in $I_D$:
$$\Delta I_D = \frac{\text{LC}}{2} = \frac{0.2\text{ mA}}{2} = \pm 0.1\text{ mA}$$

**Absolute uncertainty** in $V_{DS}$:
$$\Delta V_{DS} = \frac{\text{LC}}{2} = \frac{0.25\text{ V}}{2} = \pm 0.125\text{ V}$$

**Absolute uncertainty** in $V_{GS}$:
$$\Delta V_{GS} = \pm 0.05\text{ V}$$

### Transconductance Calculation

$$g_m = \frac{\Delta I_D}{\Delta V_{GS}}\bigg|_{V_{DS}=10\text{V}} = \frac{(6.8 - 0.0)\text{ mA}}{(0 - (-1.8))\text{ V}} = \frac{6.8}{1.8} \approx 3.78\text{ mA/V}$$

### Statistical Summary ($I_{DSS}$)

| Statistic | Value |
|-----------|-------|
| Mean $\bar{I}_{DSS}$ | 6.87 mA |
| Std Deviation $\sigma$ | 1.90 mA |
| Std Error $\sigma/\sqrt{n}$ | 1.10 mA |
| Probable Error $0.6745\sigma$ | 1.28 mA |

---

## Graphical Analysis

See `figures/` directory for all plots generated by `src/analysis.py`.

| Figure | Description |
|--------|-------------|
| `drain_characteristics.png` | Family of $I_D$–$V_{DS}$ curves for 3 values of $V_{GS}$ |
| `transfer_characteristics.png` | $I_D$–$V_{GS}$ curves + Shockley equation fit |
| `transconductance.png` | $g_m$ vs $V_{GS}$ extracted numerically |
| `pinchoff_vs_vds.png` | $I_{DSS}$ vs $V_{DS}$ showing saturation behavior |

---

## Results

$$\boxed{I_{DSS} = (6.87 \pm 1.10) \text{ mA} \quad (\text{at } V_{DS} = 10\text{ V})}$$

$$\boxed{V_P = V_{GS(off)} = (-1.80 \pm 0.05) \text{ V}}$$

$$\boxed{g_m \approx 3.78 \text{ mA/V} = 3.78 \text{ mS}}$$

$$\boxed{\text{Saturation begins at } V_{DS} \approx |V_P| = 1.8\text{ V (for } V_{GS} = 0)}$$

The Shockley fit yields: $I_{DSS}^{fit} \approx 10.2\text{ mA}$, $V_P^{fit} \approx -3.3\text{ V}$ (model fit; actual measured pinch-off is −1.8 V due to limited operating range).

---

## Discussion

1. **Ohmic region**: At low $V_{DS}$, $I_D$ increases nearly linearly — the JFET acts as a voltage-controlled resistor.
2. **Saturation region**: Beyond the knee, $I_D$ becomes nearly constant; this is the amplification region used in analog circuits.
3. **Effect of $V_{GS}$**: More negative $V_{GS}$ reduces $I_D$ and moves the pinch-off knee to lower $V_{DS}$, consistent with theory.
4. **Transfer curve**: The parabolic shape closely follows Shockley's equation, confirming the square-law device model.
5. **Pinch-off consistency**: $V_{GS(off)} \approx -1.8$ V was consistent across all $V_{DS}$ values, confirming it is a device parameter.
6. **Slight drop at $V_{DS}$ > 12 V**: Suggests onset of channel-length modulation (Early effect) or instrument limitation.

---

## Conclusion

The drain and transfer characteristics of the N-channel JFET were successfully studied. The device exhibited clear ohmic, saturation, and cut-off regions in drain characteristics. The transfer characteristic confirmed the square-law (Shockley) behavior. Key parameters determined:

- Pinch-off voltage $V_P \approx -1.8$ V  
- Maximum drain current $I_{DSS} \approx 6.8$–8.8 mA (varies with $V_{DS}$)  
- Transconductance $g_m \approx 3.78$ mS  

The JFET is confirmed as a voltage-controlled device suitable for amplification and switching.

---

## Precautions

1. Ensure the gate–source junction is **always reverse biased** ($V_{GS} \leq 0$) for N-channel JFET.
2. Do **not exceed** maximum $V_{DS}$ rating to prevent avalanche breakdown.
3. Handle JFET carefully — it is **static-sensitive** (ESD protection required).
4. Take readings only after current stabilizes.
5. Check for **zero error** in meters before measurements.
6. Keep connecting wires short to minimize stray capacitance.

---

## Sources of Error

| Type | Source | Estimated Magnitude |
|------|--------|-------------------|
| Instrumental | Voltmeter least count | ±0.125 V |
| Instrumental | Milliammeter least count | ±0.1 mA |
| Systematic | Contact resistance of breadboard | Small |
| Random | Temperature variation of JFET | Small |
| Human | Parallax error in analog meter reading | ±0.5 div |
| Environmental | Heating of JFET during measurement | Moderate |

---

## Improvements

1. Use **digital multimeters** (resolution 0.001 V, 0.001 mA) to reduce least count error.
2. Use a **temperature-controlled enclosure** to eliminate thermal drift.
3. Perform measurements with a **curve tracer** for automatic characteristic plotting.
4. Use **SPICE simulation** (LTspice) to compare theoretical vs measured characteristics.
5. Repeat each measurement **3–5 times** and average for statistical reliability.
6. Use a **proper ESD mat and wristband** when handling the JFET.

---

## Skills Demonstrated

```
Physics Concepts          Data Analysis Techniques      Tools Used
─────────────────────     ─────────────────────────     ──────────────────
• JFET operation          • Curve fitting (SciPy)       • Python 3
• Shockley equation       • Statistical analysis        • NumPy
• Depletion-mode FETs     • Error propagation           • Pandas
• Transconductance        • Numerical differentiation   • Matplotlib
• Pinch-off voltage       • Least-squares fitting       • SciPy
• I-V characteristics     • Uncertainty analysis        • Jupyter Notebook
• Amplifier biasing       • Data visualization          • Git/GitHub
```

---

## References

1. Boylestad, R. L., & Nashelsky, L. (2013). *Electronic Devices and Circuit Theory* (11th ed.). Pearson Education. (Ch. 6: JFETs)
2. Sedra, A. S., & Smith, K. C. (2015). *Microelectronic Circuits* (7th ed.). Oxford University Press.
3. Millman, J., & Halkias, C. C. (1991). *Electronics: Analog and Digital Circuits and Systems*. Tata McGraw-Hill.
4. Tri-Chandra Multiple Campus. (2082 BS). *Physics Practical Manual, BSc 3rd Year*. Tribhuvan University.
5. Horowitz, P., & Hill, W. (2015). *The Art of Electronics* (3rd ed.). Cambridge University Press.
6. National Semiconductor. *2N3819 N-Channel JFET Datasheet*. Retrieved from https://www.onsemi.com
7. Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90–95.
8. Virtanen, P., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17, 261–272.

---

*Repository maintained by BSc 3rd Year Physics student, Tri-Chandra Multiple Campus, TU Nepal.*  
*Experiment completed: 2082/01/30 (BS)*
