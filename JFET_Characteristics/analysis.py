"""
JFET Characteristics Analysis
================================
Experiment: Study of Drain and Transfer Characteristics of JFET
Institution: Tri-Chandra Multiple Campus, Kathmandu, Nepal
Class: BSc 3rd Year | Experiment No: 08 | Group: A1

Author: [Student Name]
Date: 2082/01/30 (BS) / 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy.stats import linregress
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# STYLE CONFIGURATION
# ─────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 2,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

COLORS = {
    'VGS0':   '#1f77b4',
    'VGS1':   '#ff7f0e',
    'VGS15':  '#2ca02c',
    'fit':    '#d62728',
    'theory': '#9467bd',
    'pinch':  '#8c564b',
}

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
def load_data():
    drain = pd.read_csv('data/raw_drain_characteristics.csv')
    transfer = pd.read_csv('data/raw_transfer_characteristics.csv')
    pinch = pd.read_csv('data/pinch_off_data.csv')
    return drain, transfer, pinch


# ─────────────────────────────────────────────
# JFET SHOCKLEY EQUATION
# ─────────────────────────────────────────────
def shockley(VGS, IDSS, VP):
    """ID = IDSS * (1 - VGS/VP)^2  (Shockley's equation for JFET)"""
    return IDSS * (1 - VGS / VP) ** 2


# ─────────────────────────────────────────────
# TRANSCONDUCTANCE
# ─────────────────────────────────────────────
def transconductance(VGS, IDSS, VP):
    """gm = dID/dVGS = -2*IDSS*(1 - VGS/VP) / VP"""
    return -2 * IDSS * (1 - VGS / VP) / VP


# ─────────────────────────────────────────────
# FIGURE 1: DRAIN CHARACTERISTICS
# ─────────────────────────────────────────────
def plot_drain_characteristics(drain_df, save=True):
    fig, ax = plt.subplots(figsize=(9, 6))

    vds = drain_df['VDS_V'].values
    labels = ['VGS = 0 V', 'VGS = −1 V', 'VGS = −1.5 V']
    cols   = [COLORS['VGS0'], COLORS['VGS1'], COLORS['VGS15']]
    cols_id = ['ID_mA_VGS_0V', 'ID_mA_VGS_neg1V', 'ID_mA_VGS_neg1p5V']

    for col, lbl, clr in zip(cols_id, labels, cols):
        id_ = drain_df[col].values
        ax.plot(vds, id_, 'o-', label=lbl, color=clr, markersize=5)

    # Saturation annotations
    ax.axhline(y=3.8, color=COLORS['VGS0'], linestyle='--', alpha=0.5, linewidth=1)
    ax.axhline(y=2.0, color=COLORS['VGS1'], linestyle='--', alpha=0.5, linewidth=1)
    ax.text(1, 3.95, r'$I_{DSS}$ ≈ 3.8 mA', color=COLORS['VGS0'], fontsize=9)
    ax.text(1, 2.15, r'$I_{D,sat}$ ≈ 2.0 mA', color=COLORS['VGS1'], fontsize=9)

    ax.set_xlabel(r'Drain-Source Voltage $V_{DS}$ (V)')
    ax.set_ylabel(r'Drain Current $I_D$ (mA)')
    ax.set_title('JFET N-Channel Drain (Output) Characteristics\n'
                 r'$I_D$ vs $V_{DS}$ for different $V_{GS}$')
    ax.legend(loc='center right')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5)

    # Region labels
    ax.axvspan(0, 4, alpha=0.05, color='blue')
    ax.axvspan(4, 14, alpha=0.05, color='green')
    ax.text(1.5, 4.5, 'Ohmic\nRegion', fontsize=8, color='blue', ha='center')
    ax.text(9, 4.5, 'Saturation (Active) Region', fontsize=8, color='green', ha='center')

    plt.tight_layout()
    if save:
        plt.savefig('figures/drain_characteristics.png')
    plt.show()
    print("[✓] Drain characteristics plot saved.")


# ─────────────────────────────────────────────
# FIGURE 2: TRANSFER CHARACTERISTICS + SHOCKLEY FIT
# ─────────────────────────────────────────────
def plot_transfer_characteristics(transfer_df, save=True):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    vgs = transfer_df['VGS_V'].values
    labels  = ['VDS = 12.5 V', 'VDS = 10 V', 'VDS = 9.25 V']
    cols_id = ['ID_mA_VDS_12p5V', 'ID_mA_VDS_10V', 'ID_mA_VDS_9p25V']
    clrs    = [COLORS['VGS0'], COLORS['VGS1'], COLORS['VGS15']]

    ax = axes[0]
    for col, lbl, clr in zip(cols_id, labels, clrs):
        ax.plot(vgs, transfer_df[col].values, 'o-', label=lbl, color=clr, markersize=5)

    ax.set_xlabel(r'Gate-Source Voltage $V_{GS}$ (V)')
    ax.set_ylabel(r'Drain Current $I_D$ (mA)')
    ax.set_title('JFET Transfer (Mutual) Characteristics\n'
                 r'$I_D$ vs $V_{GS}$ for different $V_{DS}$')
    ax.legend()
    ax.set_xlim(-2.2, 0.2)
    ax.set_ylim(-0.2, 10)

    # Shockley curve fit on VDS = 12.5 V data
    ax2 = axes[1]
    col = 'ID_mA_VDS_12p5V'
    id_data = transfer_df[col].values
    mask = id_data > 0
    vgs_fit = vgs[mask]
    id_fit  = id_data[mask]

    try:
        popt, pcov = curve_fit(shockley, vgs_fit, id_fit,
                               p0=[8.8, -2.0], maxfev=5000)
        IDSS_fit, VP_fit = popt
        perr = np.sqrt(np.diag(pcov))
        vgs_th = np.linspace(VP_fit, 0.1, 200)
        id_th  = shockley(vgs_th, IDSS_fit, VP_fit)
        ax2.plot(vgs_th, id_th, '-', color=COLORS['fit'],
                 label=rf'Shockley Fit: $I_{{DSS}}$={IDSS_fit:.2f} mA, $V_P$={VP_fit:.2f} V',
                 linewidth=2.5)
        print(f"\n[Shockley Fit] IDSS = {IDSS_fit:.3f} ± {perr[0]:.3f} mA")
        print(f"[Shockley Fit]   VP = {VP_fit:.3f} ± {perr[1]:.3f} V")
    except Exception as e:
        print(f"[!] Curve fit failed: {e}")

    ax2.plot(vgs, id_data, 'o', color=COLORS['VGS0'],
             label='Measured (VDS=12.5 V)', markersize=6, zorder=5)
    ax2.set_xlabel(r'Gate-Source Voltage $V_{GS}$ (V)')
    ax2.set_ylabel(r'Drain Current $I_D$ (mA)')
    ax2.set_title("Shockley's Equation Fit to Transfer Data\n"
                  r"$I_D = I_{DSS}\left(1 - \frac{V_{GS}}{V_P}\right)^2$")
    ax2.legend(fontsize=9)
    ax2.set_xlim(-2.5, 0.2)
    ax2.set_ylim(-0.2, 10)

    plt.tight_layout()
    if save:
        plt.savefig('figures/transfer_characteristics.png')
    plt.show()
    print("[✓] Transfer characteristics plot saved.")
    return IDSS_fit, VP_fit


# ─────────────────────────────────────────────
# FIGURE 3: TRANSCONDUCTANCE CURVE
# ─────────────────────────────────────────────
def plot_transconductance(IDSS, VP, save=True):
    vgs_range = np.linspace(VP, 0, 200)
    gm = transconductance(vgs_range, IDSS, VP) * 1000  # mA/V = mS

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(vgs_range, gm, color=COLORS['theory'], linewidth=2.5,
            label=r'$g_m = \frac{-2 I_{DSS}}{V_P}\left(1-\frac{V_{GS}}{V_P}\right)$')

    gm0 = abs(transconductance(0, IDSS, VP)) * 1000
    ax.axhline(y=gm0, linestyle='--', color='gray', alpha=0.6)
    ax.text(-0.1, gm0 + 0.05, rf'$g_{{m0}}$ = {gm0:.2f} mS', fontsize=9)

    ax.set_xlabel(r'Gate-Source Voltage $V_{GS}$ (V)')
    ax.set_ylabel(r'Transconductance $g_m$ (mS)')
    ax.set_title(r'JFET Transconductance $g_m$ vs $V_{GS}$')
    ax.legend()

    plt.tight_layout()
    if save:
        plt.savefig('figures/transconductance.png')
    plt.show()
    print("[✓] Transconductance plot saved.")


# ─────────────────────────────────────────────
# FIGURE 4: PINCH-OFF VOLTAGE vs VDS
# ─────────────────────────────────────────────
def plot_pinchoff(pinch_df, save=True):
    vds = pinch_df['VDS_V'].values
    vp  = pinch_df['Vp_V'].values

    slope, intercept, r, p, se = linregress(vds, vp)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(vds, vp, 'o', color=COLORS['pinch'], markersize=9,
            label='Measured $V_P$', zorder=5)
    x_line = np.linspace(6, 14, 100)
    ax.plot(x_line, slope * x_line + intercept, '--',
            color=COLORS['fit'], label=f'Linear Fit (R²={r**2:.4f})')

    ax.set_xlabel(r'Drain-Source Voltage $V_{DS}$ (V)')
    ax.set_ylabel(r'Pinch-Off Voltage $V_P$ (V)')
    ax.set_title(r'Pinch-Off Voltage $V_P$ vs $V_{DS}$')
    ax.legend()

    plt.tight_layout()
    if save:
        plt.savefig('figures/pinchoff_vs_vds.png')
    plt.show()
    print("[✓] Pinch-off plot saved.")


# ─────────────────────────────────────────────
# STATISTICAL SUMMARY
# ─────────────────────────────────────────────
def statistical_summary(transfer_df):
    print("\n" + "="*55)
    print("  STATISTICAL SUMMARY — Transfer Characteristics")
    print("="*55)
    for col in ['ID_mA_VDS_12p5V', 'ID_mA_VDS_10V', 'ID_mA_VDS_9p25V']:
        d = transfer_df[col].values
        mean = np.mean(d)
        std  = np.std(d, ddof=1)
        se   = std / np.sqrt(len(d))
        print(f"\n  {col}")
        print(f"    Mean        : {mean:.3f} mA")
        print(f"    Std Dev     : {std:.3f} mA")
        print(f"    Std Error   : {se:.3f} mA")
        print(f"    Max IDSS    : {d.max():.3f} mA")
    print("="*55)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.makedirs('figures', exist_ok=True)

    drain, transfer, pinch = load_data()

    plot_drain_characteristics(drain)
    IDSS_fit, VP_fit = plot_transfer_characteristics(transfer)
    plot_transconductance(IDSS_fit, VP_fit)
    plot_pinchoff(pinch)
    statistical_summary(transfer)

    print("\n[✓] All figures generated and saved to figures/")
