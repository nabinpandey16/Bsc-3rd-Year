# ⚡ 1-Bit Digital Comparator

[![Physics](https://img.shields.io/badge/Domain-Digital%20Electronics-blue?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=flat-square&logo=python)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-orange?style=flat-square&logo=jupyter)](https://jupyter.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Institution](https://img.shields.io/badge/Institution-Tri--Chandra%20Campus%2C%20TU-red?style=flat-square)](https://trc.tu.edu.np)

> **Experiment No. 01** — Physics Practical | Tri-Chandra Multiple Campus, Tribhuvan University  
> Design and verification of a 1-bit digital comparator using TTL logic ICs on a breadboard.

---

## 📌 Overview

A **1-bit digital comparator** is a combinational logic circuit that compares two single-bit binary inputs **A** and **B**, and produces three outputs:

| Output | Condition | Boolean Expression |
|--------|-----------|-------------------|
| A = B  | Inputs are equal | $\bar{A}\cdot\bar{B} + A\cdot B$ |
| A > B  | A is greater than B | $A \cdot \bar{B}$ |
| A < B  | A is less than B | $\bar{A} \cdot B$ |

The circuit was implemented using ICs **7408 (AND)**, **7404 (NOT)**, **7402 (NOR)**, and a **BC547 NPN transistor** for output indication.

---

## 🎯 Objective

- To design and construct a 1-bit digital comparator circuit on a breadboard.
- To verify the truth table experimentally by measuring output voltages for all input combinations.
- To understand the application of basic logic gates in building magnitude comparison circuits.

---

## 🔧 Apparatus Required

| Instrument | Specification | Quantity |
|-----------|--------------|----------|
| Power Supply | 5 V DC (set to 3 V) | 1 |
| IC 7408 | Quad 2-input AND gate | 1 |
| IC 7404 | Hex Inverter (NOT gate) | 1 |
| IC 7402 | Quad 2-input NOR gate | 1 |
| Transistor BC547 | NPN, general purpose | 1 |
| Resistors | 1 kΩ, 10 kΩ | 2 each |
| Breadboard | Standard 830-tie | 1 |
| Voltmeter | Range: 5 V, Least count: 0.5 V/div | 1 |
| Jumper wires | Male-to-male | As required |

---

## 📐 Theory

### Fundamental Principle

A **comparator** determines the relative magnitude of two binary numbers. For 1-bit inputs A and B, there are only 4 possible combinations (2¹ × 2¹ = 4), and each maps to exactly one of three mutually exclusive output conditions.

This functionality is foundational in digital systems — arithmetic logic units (ALUs), address decoders in memory, and data sorting circuits all rely on magnitude comparators.

### Boolean Logic Derivation

From the truth table:

**Case 1: A = B**  
A equals B when both are 0 OR both are 1:

$$Y_{A=B} = \bar{A}\cdot\bar{B} + A\cdot B$$

This is equivalent to the XNOR function:

$$Y_{A=B} = \overline{A \oplus B}$$

Implemented using: NOT + AND + NOR gates.

**Case 2: A > B**  
A is greater than B only when A = 1 and B = 0:

$$Y_{A>B} = A \cdot \bar{B}$$

Implemented using: NOT gate on B → AND gate.

**Case 3: A < B**  
A is less than B only when A = 0 and B = 1:

$$Y_{A<B} = \bar{A} \cdot B$$

Implemented using: NOT gate on A → AND gate.

### Truth Table

| A | B | A = B | A > B | A < B |
|---|---|-------|-------|-------|
| 0 | 0 |   1   |   0   |   0   |
| 0 | 1 |   0   |   0   |   1   |
| 1 | 0 |   0   |   1   |   0   |
| 1 | 1 |   1   |   0   |   0   |

### TTL Logic Voltage Levels

For TTL family ICs (74xx series):

| Level | Voltage Range |
|-------|--------------|
| Logic HIGH (1) | 2.0 V – 5.0 V |
| Logic LOW (0) | 0 V – 0.8 V |

Typical output HIGH voltage ($V_{OH,min}$) ≈ 2.4 V, which is consistent with our measured value of **2.35 ± 0.50 V**.

---

## 🔌 Experimental Setup

The comparator is built using three sub-circuits on a breadboard:

```
 A ──────┬──── NOT ────┐
         │             ├──── AND ──── Y (A>B)
 B ──────┼─────────────┘
         │
 A ──────┼─────────────┐
         │             ├──── AND ──── Y (A<B)
 B ──────┴──── NOT ────┘
         │
 A ──┬── NOT ──┬──────────────────────┐
     │         └── AND ──┐            ├── NOR ── Y (A=B)
     └──────────── AND ──┘            │
 B ──┴── NOT ──────────────── (above)─┘
```

**ICs pin configuration used:**
- 7408 (AND): Pins 1-2 → input, 3 → output (per gate)
- 7404 (NOT): Pin 1 → input, 2 → output (per gate)
- 7402 (NOR): Pins 2-3 → input, 1 → output (per gate)
- BC547: Collector to +Vcc through 10kΩ, Base through 1kΩ from gate output, Emitter to GND

---

## 📋 Procedure

1. Identify all IC pins using the 7408, 7404, 7402 datasheets. Verify $V_{CC}$ (pin 14) and GND (pin 7) connections.
2. Insert all ICs into the breadboard, ensuring sufficient spacing.
3. Connect the +3V power supply to $V_{CC}$ rails and GND to the negative rail.
4. Wire NOT gates (7404) to create $\bar{A}$ and $\bar{B}$ signals.
5. Build the AND gate sub-circuits:
   - $A \cdot \bar{B}$ → output Y (A>B)
   - $\bar{A} \cdot B$ → output Y (A<B)
   - $\bar{A} \cdot \bar{B}$ and $A \cdot B$ → both into NOR → Y (A=B)
6. Connect each output through a 1 kΩ resistor to the base of BC547.
7. Connect voltmeter between collector and GND to measure output.
8. Apply all four input combinations (A,B) = (0,0), (0,1), (1,0), (1,1) by connecting to GND or Vcc.
9. Record voltmeter readings for each output terminal in the observation table.
10. Verify results match the theoretical truth table.

---

## 👁️ Observation

**Instrument calibration:**

- 10 divisions of voltmeter = 5 V → 1 division = **0.5 V**
- Least count of voltmeter = **0.5 V/division**
- Power supply voltage = **3 V**

**Qualitative observation:**  
When the correct output condition was active (e.g., A = B when inputs matched), the voltmeter showed a clearly elevated reading (~2.35 V), while all other outputs read near 0 V. The LED/voltmeter indicator was clearly distinguishable between HIGH and LOW states.

---

## 📊 Observation Tables

### (i) For A = B Output

| A | B | Output V₀ (V) | Corrected V_c (V) |
|---|---|--------------|-------------------|
| 0 | 0 | 2.35 | 2.35 ± 0.5 |
| 0 | 1 | 0.00 | 0.00 ± 0.5 |
| 1 | 0 | 0.00 | 0.00 ± 0.5 |
| 1 | 1 | 2.35 | 2.35 ± 0.5 |

### (ii) For A > B Output

| A | B | Output V₀ (V) | Corrected V_c (V) |
|---|---|--------------|-------------------|
| 0 | 0 | 0.00 | 0.00 ± 0.5 |
| 0 | 1 | 0.00 | 0.00 ± 0.5 |
| 1 | 0 | 2.35 | 2.35 ± 0.5 |
| 1 | 1 | 0.00 | 0.00 ± 0.5 |

### (iii) For A < B Output

| A | B | Output V₀ (V) | Corrected V_c (V) |
|---|---|--------------|-------------------|
| 0 | 0 | 0.00 | 0.00 ± 0.5 |
| 0 | 1 | 2.35 | 2.35 ± 0.5 |
| 1 | 0 | 0.00 | 0.00 ± 0.5 |
| 1 | 1 | 0.00 | 0.00 ± 0.5 |

---

## 🧮 Calculations

### Error Analysis

**Instrument uncertainty (voltmeter least count):**

$$\delta V = \frac{\text{Range}}{\text{Divisions}} = \frac{5\,\text{V}}{10} = 0.5\,\text{V}$$

**Deviation of measured HIGH voltage from supply:**

$$\Delta V = |V_{supply} - V_{HIGH}| = |3.0 - 2.35| = 0.65\,\text{V}$$

$$\text{Percentage error} = \frac{0.65}{3.0} \times 100 = \mathbf{21.7\%}$$

> **Physical note:** TTL ICs have a specified minimum output HIGH voltage of ~2.4 V even at full Vcc = 5V. At Vcc = 3V, an output of 2.35 V is entirely expected and physically valid. The "error" reflects the IC's internal behavior, not a measurement mistake.

### Statistical Analysis (HIGH outputs)

All HIGH readings: {2.35, 2.35, 2.35, 2.35} V (n = 4)

$$\bar{x} = 2.35\,\text{V}$$

$$s^2 = 0\,\text{V}^2 \quad (\text{all readings identical})$$

$$s = 0\,\text{V}, \quad SE = 0\,\text{V}$$

The zero variance confirms **perfectly consistent IC output** — a hallmark of digital (discrete-state) circuits, as opposed to analog circuits where measurement fluctuation is expected.

---

## 📈 Graphical Analysis

See the [`figures/`](figures/) directory for:

- **`graph_1_output_voltages.png`** — Bar chart of measured output voltages for all input combinations, with ±0.5 V error bars on each terminal (A=B, A>B, A<B).
- **`graph_2_truth_table_heatmap.png`** — Color-coded heatmap of the truth table (green = HIGH, red = LOW) for intuitive verification.
- **`setup_diagram.png`** — Block diagram of the comparator showing gate connectivity and signal flow.

Run the full analysis:

```bash
python src/analysis.py
```

Or open the notebook:

```bash
jupyter lab notebooks/analysis.ipynb
```

---

## ✅ Results

| Quantity | Value |
|----------|-------|
| HIGH output voltage (V_OH) | **2.35 ± 0.50 V** |
| LOW output voltage (V_OL) | **0.00 ± 0.50 V** |
| Power supply (Vcc) | 3.0 V |
| Percentage deviation from Vcc | 21.7 % |
| Truth table accuracy | **4/4 (100%)** |

**All three outputs (A=B, A>B, A<B) matched the theoretical truth table for every input combination.**

---

## 💬 Discussion

The measured HIGH voltage of 2.35 V is consistent with the TTL specification for $V_{OH,min}$ ≈ 2.4 V. The small deviation (0.65 V from the 3V supply) arises from:

1. Transistor saturation voltage ($V_{CE,sat}$ ≈ 0.2–0.3 V for BC547)
2. IC internal output resistance causing a slight voltage drop
3. Current limiting resistors (1 kΩ, 10 kΩ) forming a voltage divider at the output

The voltmeter uncertainty of ±0.5 V (one division) means the readings 2.35 V and 0.0 V are well-separated (>4σ apart), so there is no ambiguity in identifying HIGH vs LOW states. The experiment reliably demonstrates that basic logic gates can implement magnitude comparison — a principle scaled up to multi-bit comparators (like the 7485 IC) in real processors.

---

## 📝 Conclusion

The 1-bit digital comparator was successfully designed and verified on a breadboard using ICs 7408, 7404, 7402, and a BC547 transistor. The circuit accurately compared all four input combinations and produced correct HIGH/LOW outputs for each of the three comparison outputs (A=B, A>B, A<B). Experimental results matched the theoretical truth table with 100% accuracy, confirming the validity of the Boolean expressions derived from the truth table. The experiment demonstrates fundamental principles of combinational digital logic and their practical implementation.

---

## ⚠️ Precautions

1. Ensure all logic gate connections follow the circuit diagram before switching on the power supply.
2. Always disconnect the power supply while assembling or modifying the circuit to avoid short circuits.
3. Avoid loose connections on the breadboard — they cause intermittent or incorrect outputs.
4. Do not exceed the rated $V_{CC}$ (5 V) for the 74xx TTL ICs to prevent damage.
5. Verify IC orientation (notch/dot marks pin 1) before inserting into the breadboard.

---

## 🔍 Sources of Error

| Error Type | Source | Impact |
|-----------|--------|--------|
| **Instrumental** | Voltmeter least count (0.5 V/div) | ±0.5 V on all readings |
| **Human** | Misreading voltmeter scale | ±0.5 V |
| **Systematic** | TTL $V_{OH}$ < $V_{CC}$ (by IC design) | 0.65 V deviation |
| **Random** | Loose breadboard connections | Occasional wrong output |
| **Environmental** | Unstable power supply voltage | Fluctuating output levels |
| **Component** | Defective or aged ICs | Incorrect logic levels |

---

## 🚀 Improvements

- Use a **regulated 5 V power supply** to operate the 74xx ICs at their rated voltage for more accurate output levels.
- Replace the voltmeter with a **digital multimeter (DMM)** for higher precision (resolution: 0.01 V vs 0.5 V).
- Use **LED indicators** alongside the voltmeter for real-time visual confirmation of logic states.
- Scale up to a **2-bit or 4-bit comparator** using IC 7485 to explore more complex digital comparison.
- Use an **oscilloscope** to capture switching transients and measure propagation delay of the logic gates.

---

## 📚 References

Boylestad, R. L., & Nashelsky, L. (2013). *Electronic devices and circuit theory* (11th ed.). Pearson.

Floyd, T. L. (2015). *Digital fundamentals* (11th ed.). Pearson.

Malvino, A. P., & Leach, D. P. (2010). *Digital principles and applications* (8th ed.). Tata McGraw-Hill.

Morris Mano, M. (2013). *Digital design* (5th ed.). Pearson.

Texas Instruments. (2004). *SN74LS08 Quadruple 2-Input AND Gates datasheet*. https://www.ti.com/lit/ds/symlink/sn74ls08.pdf

Texas Instruments. (2004). *SN74LS04 Hex Inverters datasheet*. https://www.ti.com/lit/ds/symlink/sn74ls04.pdf

Texas Instruments. (2004). *SN74LS02 Quadruple 2-Input NOR Gates datasheet*. https://www.ti.com/lit/ds/symlink/sn74ls02.pdf

Tri-Chandra Multiple Campus. (2082). *Physics practical manual — B.Sc. 3rd Year*. Tribhuvan University.

---

## 🛠️ Skills Demonstrated

- Digital logic design (combinational circuits)
- TTL IC interfacing and breadboard prototyping
- Boolean algebra and truth table analysis
- Experimental error analysis and uncertainty estimation
- Data visualization with Python (Matplotlib)
- Scientific reporting and documentation

## 🧠 Physics Concepts Learned

- Binary number representation and magnitude comparison
- Boolean algebra: AND, NOT, NOR gate operations
- TTL logic voltage levels ($V_{OH}$, $V_{OL}$, $V_{IH}$, $V_{IL}$)
- Transistor as a digital switch (BC547 in saturation/cutoff)
- Propagation delay and fan-out in TTL circuits

---

*Physics Practical Repository | Tri-Chandra Multiple Campus, Tribhuvan University, Kathmandu, Nepal*
