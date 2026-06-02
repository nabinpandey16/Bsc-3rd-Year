"""
1-Bit Digital Comparator — Analysis Script
Tri-Chandra Multiple Campus, Tribhuvan University
Experiment No. 01 | Physics Practical
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
POWER_SUPPLY_V   = 3.0        # V
VOLTMETER_RANGE  = 5.0        # V (10 divisions)
DIVISION_VALUE   = 0.5        # V per division (least count)
HIGH_THRESHOLD   = 2.35       # V — measured HIGH output
LOW_THRESHOLD    = 0.0        # V — measured LOW output
UNCERTAINTY      = 0.5        # V (one division)
VCC              = 5.0        # V (IC supply)

# ─────────────────────────────────────────
# DATA
# ─────────────────────────────────────────
truth_table = pd.DataFrame({
    "A": [0, 0, 1, 1],
    "B": [0, 1, 0, 1],
    "A=B (theory)": [1, 0, 0, 1],
    "A>B (theory)": [0, 0, 1, 0],
    "A<B (theory)": [0, 1, 0, 0],
    "V_AeqB (V)":   [2.35, 0.0, 0.0, 2.35],
    "V_AgtB (V)":   [0.0, 0.0, 2.35, 0.0],
    "V_AltB (V)":   [0.0, 2.35, 0.0, 0.0],
})

truth_table["V_AeqB ± δV"] = truth_table["V_AeqB (V)"].apply(
    lambda v: f"{v:.2f} ± {UNCERTAINTY}" if v > 0 else f"0.00 ± {UNCERTAINTY}"
)
truth_table["V_AgtB ± δV"] = truth_table["V_AgtB (V)"].apply(
    lambda v: f"{v:.2f} ± {UNCERTAINTY}" if v > 0 else f"0.00 ± {UNCERTAINTY}"
)
truth_table["V_AltB ± δV"] = truth_table["V_AltB (V)"].apply(
    lambda v: f"{v:.2f} ± {UNCERTAINTY}" if v > 0 else f"0.00 ± {UNCERTAINTY}"
)

# ─────────────────────────────────────────
# PLOT 1 — Output Voltage Bar Chart
# ─────────────────────────────────────────
def plot_output_voltages(save_path="figures/graph_1_output_voltages.png"):
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
    fig.suptitle("1-Bit Digital Comparator — Measured Output Voltages",
                 fontsize=14, fontweight='bold', y=1.02)

    input_labels = ["A=0,B=0", "A=0,B=1", "A=1,B=0", "A=1,B=1"]
    colors       = ["#2ecc71", "#e74c3c", "#3498db", "#f39c12"]
    outputs      = ["V_AeqB (V)", "V_AgtB (V)", "V_AltB (V)"]
    titles       = ["Output: A = B", "Output: A > B", "Output: A < B"]
    uncertainties = [UNCERTAINTY] * 4

    for ax, col, title in zip(axes, outputs, titles):
        bars = ax.bar(input_labels, truth_table[col], color=colors,
                      edgecolor="black", linewidth=0.8, width=0.55)
        ax.errorbar(input_labels, truth_table[col],
                    yerr=uncertainties, fmt='none', color='black',
                    capsize=5, linewidth=1.5, label="Uncertainty (±0.5 V)")
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel("Input Combination (A, B)", fontsize=10)
        ax.set_ylabel("Output Voltage (V)", fontsize=10)
        ax.set_ylim(0, 3.5)
        ax.axhline(y=HIGH_THRESHOLD, color='gray', linestyle='--',
                   linewidth=1, alpha=0.7, label=f"HIGH = {HIGH_THRESHOLD} V")
        ax.legend(fontsize=8)
        ax.tick_params(axis='x', rotation=15)
        ax.grid(axis='y', alpha=0.3)

        for bar, val in zip(bars, truth_table[col]):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width()/2,
                        val + 0.08, f"{val:.2f} V",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.show()


# ─────────────────────────────────────────
# PLOT 2 — Logic Level Heatmap (Truth Table Visual)
# ─────────────────────────────────────────
def plot_truth_table_heatmap(save_path="figures/graph_2_truth_table_heatmap.png"):
    fig, ax = plt.subplots(figsize=(8, 5))

    data_matrix = np.array([
        truth_table["A=B (theory)"].values,
        truth_table["A>B (theory)"].values,
        truth_table["A<B (theory)"].values,
    ], dtype=float)

    im = ax.imshow(data_matrix, cmap="RdYlGn", aspect="auto",
                   vmin=0, vmax=1, interpolation='nearest')

    ax.set_xticks(range(4))
    ax.set_xticklabels(["A=0,B=0", "A=0,B=1", "A=1,B=0", "A=1,B=1"],
                       fontsize=11)
    ax.set_yticks(range(3))
    ax.set_yticklabels(["A = B", "A > B", "A < B"], fontsize=12, fontweight='bold')
    ax.set_title("Truth Table — Logic Output Heatmap\n(Green = HIGH, Red = LOW)",
                 fontsize=13, fontweight='bold')

    for i in range(3):
        for j in range(4):
            val = int(data_matrix[i, j])
            label = "HIGH\n(1)" if val == 1 else "LOW\n(0)"
            ax.text(j, i, label, ha='center', va='center',
                    fontsize=11, fontweight='bold',
                    color='white' if val == 1 else 'black')

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("Logic Level", fontsize=10)
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(["LOW (0)", "HIGH (1)"])

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.show()


# ─────────────────────────────────────────
# PLOT 3 — Circuit Setup Diagram (Matplotlib)
# ─────────────────────────────────────────
def plot_setup_diagram(save_path="figures/setup_diagram.png"):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')

    ax.set_title("1-Bit Digital Comparator — Block Diagram",
                 fontsize=14, fontweight='bold', pad=15)

    def draw_gate(ax, x, y, label, color='#3498db'):
        rect = mpatches.FancyBboxPatch((x-0.4, y-0.25), 0.8, 0.5,
                                        boxstyle="round,pad=0.05",
                                        linewidth=1.5, edgecolor='black',
                                        facecolor=color, alpha=0.85)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center',
                fontsize=8, fontweight='bold', color='white')

    def draw_box(ax, x, y, w, h, label, color='#ecf0f1'):
        rect = mpatches.FancyBboxPatch((x, y), w, h,
                                        boxstyle="round,pad=0.1",
                                        linewidth=2, edgecolor='#2c3e50',
                                        facecolor=color)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h/2, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='#2c3e50')

    # Inputs
    ax.annotate('', xy=(1.5, 5.5), xytext=(0.5, 5.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.annotate('', xy=(1.5, 1.5), xytext=(0.5, 1.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.text(0.3, 5.5, "A", ha='center', va='center', fontsize=14,
            fontweight='bold', color='#e74c3c')
    ax.text(0.3, 1.5, "B", ha='center', va='center', fontsize=14,
            fontweight='bold', color='#3498db')

    # NOT gates
    draw_gate(ax, 2.0, 5.5, "NOT\n(7404)", color='#8e44ad')
    draw_gate(ax, 2.0, 1.5, "NOT\n(7404)", color='#8e44ad')

    # AND gates for outputs
    draw_gate(ax, 4.5, 5.5, "AND\n(7408)", color='#27ae60')
    draw_gate(ax, 4.5, 3.5, "AND\n(7408)", color='#27ae60')
    draw_gate(ax, 4.5, 1.5, "AND\n(7408)", color='#27ae60')

    # NOR for A=B
    draw_gate(ax, 6.5, 3.5, "NOR\n(7402)", color='#e67e22')

    # Output boxes
    draw_box(ax, 8.0, 5.0, 1.5, 0.8, "A > B", '#e74c3c')
    draw_box(ax, 8.0, 3.1, 1.5, 0.8, "A = B", '#27ae60')
    draw_box(ax, 8.0, 1.2, 1.5, 0.8, "A < B", '#3498db')

    # Connection lines (simplified)
    ax.plot([2.4, 3.5, 3.5, 4.1], [5.5, 5.5, 5.5, 5.5], 'k-', lw=1.2)
    ax.plot([2.4, 3.5, 3.5, 4.1], [1.5, 1.5, 1.5, 1.5], 'k-', lw=1.2)
    ax.plot([4.9, 7.4, 7.4, 8.0], [5.5, 5.5, 5.4, 5.4], 'k-', lw=1.2)
    ax.plot([4.9, 6.1], [3.5, 3.5], 'k-', lw=1.2)
    ax.plot([6.9, 8.0], [3.5, 3.5], 'k-', lw=1.2)
    ax.plot([4.9, 7.4, 7.4, 8.0], [1.5, 1.5, 1.6, 1.6], 'k-', lw=1.2)

    # IC labels
    ax.text(5.0, 0.5, "ICs Used: 7408 (AND) · 7404 (NOT) · 7402 (NOR)",
            ha='center', va='center', fontsize=9, style='italic',
            color='#7f8c8d',
            bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))

    ax.text(9.0, 6.5, f"Vcc = +{VCC} V", ha='center', fontsize=10,
            color='#c0392b', fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.show()


# ─────────────────────────────────────────
# ERROR ANALYSIS
# ─────────────────────────────────────────
def error_analysis():
    print("\n" + "="*55)
    print("  ERROR ANALYSIS — 1-Bit Digital Comparator")
    print("="*55)

    measured_high   = HIGH_THRESHOLD          # V
    theoretical_max = VCC                     # V (ideal HIGH = Vcc)
    
    abs_error  = abs(theoretical_max - measured_high)
    rel_error  = abs_error / theoretical_max
    pct_error  = rel_error * 100

    print(f"\n  Measured HIGH output voltage : {measured_high:.2f} V")
    print(f"  Theoretical HIGH (Vcc)       : {theoretical_max:.2f} V")
    print(f"  Instrument uncertainty       : ±{UNCERTAINTY:.2f} V")
    print(f"\n  Absolute error  = |{theoretical_max} - {measured_high}|")
    print(f"                  = {abs_error:.2f} V")
    print(f"\n  Relative error  = {abs_error:.2f} / {theoretical_max:.2f}")
    print(f"                  = {rel_error:.4f}")
    print(f"\n  Percentage error = {pct_error:.2f} %")
    print(f"\n  Note: Discrepancy is due to transistor saturation")
    print(f"        voltage and IC internal resistance (expected).")
    print("="*55)

    return {
        "measured_HIGH": measured_high,
        "theoretical_HIGH": theoretical_max,
        "absolute_error": abs_error,
        "relative_error": rel_error,
        "percentage_error": pct_error,
        "uncertainty": UNCERTAINTY
    }


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.makedirs("figures", exist_ok=True)

    print("Generating plots...")
    plot_output_voltages()
    plot_truth_table_heatmap()
    plot_setup_diagram()

    results = error_analysis()

    print("\n  All figures saved to /figures/")
    print("  Analysis complete.\n")
