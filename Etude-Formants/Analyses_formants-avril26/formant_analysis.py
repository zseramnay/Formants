#!/usr/bin/env python3
"""
formant_analysis.py
-------------------
Multi-method formant analysis on a collection of WAV samples.
Intended to diagnose discrepancies between specenv-based results
and the acoustic literature (e.g. trumpet F1 ~800–1200 Hz).

Methods:
  1. LPC (Linear Predictive Coding)   — pitch-independent, resonance-oriented
  2. Cepstral envelope                — variable smoothing order
  3. Energy-weighted spectral centroid (Fp)

Usage:
  python formant_analysis.py <wav_folder> [options]

  --technique   filter by technique substring (default: 'ordinario')
  --lpc-order   LPC order (default: 18, use 2+sr/1000 rule → ~20 for 44.1k)
  --cep-order   cepstral smoothing order (default: 40, 80, 160 compared)
  --fp-band     Fp centroid band in Hz, e.g. "800,2000" (default: 600,1800)
  --sr          expected sample rate (default: 44100)
  --max-freq    upper frequency limit for analysis (default: 4000 Hz)
  --output      output CSV path (default: formant_results.csv)
  --plot        show summary plots

Requirements: numpy scipy soundfile matplotlib pandas
  pip install numpy scipy soundfile matplotlib pandas
"""

import os
import sys
import argparse
import csv
import warnings
from pathlib import Path

import numpy as np
import scipy.signal as signal
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import pandas as pd

try:
    import soundfile as sf
except ImportError:
    sys.exit("soundfile not found. Install with: pip install soundfile")

# ─────────────────────────────────────────────────────────────────────────────
# Utility: parse SOL2020-style filename to extract note / dynamic / technique
# Format: instrument-technique-note-dynamic.wav  (approximate)
# ─────────────────────────────────────────────────────────────────────────────

def parse_filename(path: str) -> dict:
    """Extract metadata from SOL2020-style filename."""
    name = Path(path).stem
    parts = name.split("-")
    info = {"filename": Path(path).name, "instrument": "", "technique": "",
            "note": "", "dynamic": ""}
    if len(parts) >= 4:
        info["instrument"] = parts[0]
        info["technique"] = parts[1]
        info["note"] = parts[2]
        info["dynamic"] = parts[3]
    elif len(parts) >= 2:
        info["instrument"] = parts[0]
        info["technique"] = parts[1]
    return info


def note_to_midi(note_str: str) -> int:
    """Convert note string like 'C4', 'Bb3', 'F#5' to MIDI number."""
    note_map = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    try:
        s = note_str.strip()
        # handle flats/sharps
        if len(s) >= 2 and s[1] in ('#', 'b', 's', 'f'):
            pc = note_map.get(s[0].upper(), -1)
            acc = 1 if s[1] in ('#', 's') else -1
            octave = int(s[2:])
            return (octave + 1) * 12 + pc + acc
        else:
            pc = note_map.get(s[0].upper(), -1)
            octave = int(s[1:])
            return (octave + 1) * 12 + pc
    except Exception:
        return -1

# ─────────────────────────────────────────────────────────────────────────────
# Audio loading
# ─────────────────────────────────────────────────────────────────────────────

def load_wav_mono(path: str, target_sr: int = 44100) -> tuple[np.ndarray, int]:
    """Load WAV, mix to mono, optionally resample."""
    data, sr = sf.read(path, always_2d=True)
    mono = data.mean(axis=1)
    if sr != target_sr:
        # simple decimation / interpolation via polyphase
        from scipy.signal import resample_poly
        from math import gcd
        g = gcd(target_sr, sr)
        mono = resample_poly(mono, target_sr // g, sr // g)
        sr = target_sr
    return mono.astype(np.float64), sr


def extract_steady_segment(audio: np.ndarray, sr: int,
                            skip_attack_ms: int = 100,
                            duration_ms: int = 500) -> np.ndarray:
    """Return a steady-state segment skipping attack transient."""
    start = int(sr * skip_attack_ms / 1000)
    length = int(sr * duration_ms / 1000)
    end = start + length
    if end > len(audio):
        end = len(audio)
    seg = audio[start:end]
    if len(seg) < 512:
        return audio  # fallback: use entire file
    return seg

# ─────────────────────────────────────────────────────────────────────────────
# Method 1: LPC formant estimation
# ─────────────────────────────────────────────────────────────────────────────

def lpc_coeffs(signal_in: np.ndarray, order: int) -> np.ndarray:
    """Compute LPC coefficients via autocorrelation / Levinson-Durbin."""
    n = len(signal_in)
    # autocorrelation
    r = np.correlate(signal_in, signal_in, mode='full')
    r = r[n-1:]  # keep non-negative lags
    # Levinson-Durbin
    a = np.zeros(order + 1)
    e = r[0]
    a[0] = 1.0
    for i in range(1, order + 1):
        lam = -sum(a[j] * r[i - j] for j in range(i)) / e
        for j in range(i, 0, -1):
            a[j] = a[j] + lam * a[i - j]
        a[i] = lam
        e *= (1.0 - lam ** 2)
        if e <= 0:
            break
    return a


def lpc_formants(audio: np.ndarray, sr: int, order: int,
                 max_freq: float = 4000.0) -> list[float]:
    """
    Extract formant frequencies from LPC poles.
    Returns list of formant frequencies in Hz (sorted), below max_freq.
    """
    # pre-emphasis
    pre = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])
    # windowed frame (use entire segment)
    win = np.hanning(len(pre))
    framed = pre * win

    # LPC via scipy (more numerically stable than manual Levinson)
    # Use scipy.signal.lfilter approach: fit AR model
    # We use the autocorrelation method via toeplitz solve
    r = np.array([np.dot(framed[lag:], framed[:len(framed)-lag])
                  for lag in range(order + 1)])
    if r[0] == 0:
        return []

    R = linalg.toeplitz(r[:order])
    try:
        a = np.linalg.solve(R, -r[1:order + 1])
    except np.linalg.LinAlgError:
        return []

    # Full LPC polynomial: [1, a1, a2, ..., ap]
    poly = np.concatenate([[1.0], a])

    # Find roots
    roots = np.roots(poly)

    # Keep roots with positive imaginary part (complex conjugate pairs)
    roots = roots[np.imag(roots) >= 0]

    # Convert to frequencies
    angles = np.arctan2(np.imag(roots), np.real(roots))
    freqs = angles * (sr / (2.0 * np.pi))

    # Keep positive frequencies below max_freq
    formants = sorted([f for f in freqs if 50 < f < max_freq])
    return formants


# ─────────────────────────────────────────────────────────────────────────────
# Method 2: Cepstral envelope
# ─────────────────────────────────────────────────────────────────────────────

def cepstral_envelope(audio: np.ndarray, sr: int,
                       fft_size: int = 4096,
                       cep_order: int = 40,
                       max_freq: float = 4000.0) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute cepstral spectral envelope.
    Returns (freqs, envelope_dB).
    """
    win = np.hanning(min(fft_size, len(audio)))
    if len(audio) > fft_size:
        # average over overlapping frames
        hop = fft_size // 2
        frames = []
        for i in range(0, len(audio) - fft_size, hop):
            f = audio[i:i+fft_size] * np.hanning(fft_size)
            spec = np.abs(np.fft.rfft(f, n=fft_size)) ** 2
            frames.append(spec)
        avg_power = np.mean(frames, axis=0)
    else:
        padded = np.zeros(fft_size)
        padded[:len(audio)] = audio * win
        avg_power = np.abs(np.fft.rfft(padded, n=fft_size)) ** 2

    eps = 1e-12
    log_spec = np.log(avg_power + eps)

    # Cepstrum
    cep = np.fft.irfft(log_spec)

    # Lifter: keep only low quefrency (smooth envelope)
    liftered = np.zeros_like(cep)
    liftered[:cep_order] = cep[:cep_order]
    liftered[-cep_order+1:] = cep[-cep_order+1:]  # symmetric

    # Back to frequency domain
    envelope = np.real(np.fft.rfft(liftered))

    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)
    max_bin = int(max_freq / (sr / fft_size))

    return freqs[:max_bin], envelope[:max_bin]


def peaks_from_envelope(freqs: np.ndarray, envelope: np.ndarray,
                         min_dist_hz: float = 80.0,
                         sr: int = 44100,
                         fft_size: int = 4096) -> list[tuple[float, float]]:
    """Find peaks in cepstral envelope. Returns [(freq_hz, amplitude), ...]."""
    bin_width = sr / fft_size
    min_dist_bins = max(1, int(min_dist_hz / bin_width))
    threshold = np.max(envelope) - 30  # -30 dB relative threshold

    peak_indices, props = signal.find_peaks(
        envelope,
        height=threshold,
        distance=min_dist_bins
    )
    # Sort by prominence
    prominences = signal.peak_prominences(envelope, peak_indices)[0]
    order = np.argsort(-prominences)
    peak_indices = peak_indices[order]

    return [(freqs[i], envelope[i]) for i in peak_indices]


# ─────────────────────────────────────────────────────────────────────────────
# Method 3: Fp centroid
# ─────────────────────────────────────────────────────────────────────────────

def fp_centroid(audio: np.ndarray, sr: int,
                fft_size: int = 4096,
                band_low: float = 600.0,
                band_high: float = 1800.0) -> float:
    """
    Compute energy-weighted spectral centroid (Fp) in a given band.
    Same definition as in the Référence Formantique pipeline.
    """
    hop = fft_size // 2
    frames = []
    for i in range(0, max(1, len(audio)), hop):
        chunk = audio[i:i+fft_size]
        padded = np.zeros(fft_size)
        w = np.hanning(len(chunk))
        padded[:len(chunk)] = chunk * w
        frames.append(np.abs(np.fft.rfft(padded, n=fft_size)))
        if i + fft_size >= len(audio):
            break

    avg_amp = np.mean(frames, axis=0)
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)

    mask = (freqs >= band_low) & (freqs <= band_high)
    if not np.any(mask):
        return 0.0
    f_band = freqs[mask]
    a_band = avg_amp[mask]
    denom = np.sum(a_band)
    if denom == 0:
        return 0.0
    return float(np.sum(f_band * a_band) / denom)


# ─────────────────────────────────────────────────────────────────────────────
# Main analysis loop
# ─────────────────────────────────────────────────────────────────────────────

def analyze_file(wav_path: str, args) -> dict | None:
    """Run all three methods on a single WAV file."""
    try:
        audio, sr = load_wav_mono(wav_path, args.sr)
    except Exception as e:
        print(f"  [SKIP] {wav_path}: {e}", file=sys.stderr)
        return None

    seg = extract_steady_segment(audio, sr,
                                  skip_attack_ms=args.skip_attack,
                                  duration_ms=args.seg_duration)

    meta = parse_filename(wav_path)
    midi = note_to_midi(meta["note"])

    # ── LPC formants ──────────────────────────────────────────────────────────
    lpc_f = lpc_formants(seg, sr, order=args.lpc_order, max_freq=args.max_freq)
    # Take up to 6 formants
    lpc_f += [np.nan] * 6
    lpc_f1, lpc_f2, lpc_f3 = lpc_f[0], lpc_f[1], lpc_f[2]

    # ── Cepstral envelope (3 smoothing orders) ────────────────────────────────
    cep_peaks = {}
    for order in args.cep_orders:
        freqs_env, env = cepstral_envelope(
            seg, sr, fft_size=args.fft_size,
            cep_order=order, max_freq=args.max_freq
        )
        peaks = peaks_from_envelope(freqs_env, env,
                                     min_dist_hz=80.0,
                                     sr=sr, fft_size=args.fft_size)
        cep_peaks[order] = peaks[0][0] if peaks else np.nan

    # ── Fp centroid ───────────────────────────────────────────────────────────
    fp = fp_centroid(seg, sr, fft_size=args.fft_size,
                     band_low=args.fp_band[0],
                     band_high=args.fp_band[1])

    row = {
        "filename":   meta["filename"],
        "instrument": meta["instrument"],
        "technique":  meta["technique"],
        "note":       meta["note"],
        "dynamic":    meta["dynamic"],
        "midi":       midi,
        "lpc_F1":     round(lpc_f1, 1) if not np.isnan(lpc_f1) else "",
        "lpc_F2":     round(lpc_f2, 1) if not np.isnan(lpc_f2) else "",
        "lpc_F3":     round(lpc_f3, 1) if not np.isnan(lpc_f3) else "",
        "fp_centroid": round(fp, 1),
    }
    for order in args.cep_orders:
        v = cep_peaks[order]
        row[f"cep_F1_order{order}"] = round(v, 1) if not np.isnan(v) else ""

    return row


def collect_wav_files(folder: str, technique_filter: str) -> list[str]:
    """Recursively collect .wav files, filtered by technique substring."""
    files = []
    technique_filter = technique_filter.lower()
    for root, _, fnames in os.walk(folder):
        for fn in sorted(fnames):
            if fn.lower().endswith(".wav"):
                if technique_filter == "" or technique_filter in fn.lower():
                    files.append(os.path.join(root, fn))
    return files


# ─────────────────────────────────────────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────────────────────────────────────────

def plot_results(df: pd.DataFrame, args):
    """Plot formant values vs MIDI pitch and histogram, broken out by dynamic."""
    df_valid = df[df["midi"] > 0].copy()
    if df_valid.empty:
        print("No valid MIDI notes found for plotting.")
        return

    # ── Dynamic colour scheme ─────────────────────────────────────────────────
    # Canonical dynamic order; anything not matched goes to 'other'
    DYN_ORDER   = ["pppp", "ppp", "pp", "p", "mp", "mf", "f", "ff", "fff", "ffff"]
    DYN_COLORS  = {
        "pppp": "#a8d8ea", "ppp": "#74b9d4", "pp": "#3498db", "p": "#1a6fa8",
        "mp":   "#f1c40f", "mf": "#e67e22",
        "f":    "#e74c3c", "ff": "#c0392b", "fff": "#922b21", "ffff": "#641e16",
        "other": "#95a5a6",
    }

    # Normalise the dynamic column: strip whitespace, lowercase
    df_valid["dyn_norm"] = df_valid["dynamic"].str.strip().str.lower()
    present_dyns = [d for d in DYN_ORDER if d in df_valid["dyn_norm"].values]
    other_mask   = ~df_valid["dyn_norm"].isin(DYN_ORDER)
    if other_mask.any():
        present_dyns += ["other"]

    # Literature reference lines
    lit_refs   = {"Backus (1969)": 700, "Meyer (2009)": 800, "Giesler (1985)": 900}
    lit_colors = ["#e74c3c", "#e67e22", "#27ae60"]
    lit_styles = ["--", "-.", ":"]

    def add_lit_lines(ax):
        for (label, val), col, ls in zip(lit_refs.items(), lit_colors, lit_styles):
            ax.axhline(val, linestyle=ls, color=col, linewidth=1.2,
                       alpha=0.85, label=label)

    def scatter_by_dyn(ax, df_src, y_col):
        """Scatter plot coloured by dynamic; add per-dynamic median line."""
        for dyn in present_dyns:
            if dyn == "other":
                mask = df_src["dyn_norm"].isin(
                    df_src["dyn_norm"].unique()) & other_mask.reindex(
                    df_src.index, fill_value=False)
            else:
                mask = df_src["dyn_norm"] == dyn
            sub = df_src[mask].copy()
            vals = pd.to_numeric(sub[y_col], errors='coerce').dropna()
            if vals.empty:
                continue
            sub = sub.loc[vals.index]
            sub[y_col + "_num"] = vals
            c = DYN_COLORS.get(dyn, "#95a5a6")
            ax.scatter(sub["midi"], vals, alpha=0.65, s=28,
                       color=c, label=dyn, zorder=3)
            # median trend line per dynamic
            ds = sub.sort_values("midi")
            med = ds[y_col + "_num"].rolling(3, center=True, min_periods=1).median()
            ax.plot(ds["midi"], med, color=c, linewidth=1.5,
                    alpha=0.9, zorder=4)

    # ── Figure layout: 3 rows × 2 cols ───────────────────────────────────────
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    folder_name = Path(args.folder).name
    fig.suptitle(
        f"Formant Analysis — {folder_name}   |   technique filter: '{args.technique}'",
        fontsize=12, fontweight='bold'
    )

    # ── [0,0]  LPC F1 vs MIDI — all dynamics mixed ───────────────────────────
    ax = axes[0, 0]
    lpc_all = pd.to_numeric(df_valid["lpc_F1"], errors='coerce')
    valid_idx = lpc_all.dropna().index
    if not valid_idx.empty:
        ax.scatter(df_valid.loc[valid_idx, "midi"], lpc_all[valid_idx],
                   alpha=0.35, s=18, color='steelblue', zorder=2, label="all dynamics")
        ds = df_valid.loc[valid_idx].copy()
        ds["v"] = lpc_all[valid_idx]
        ds = ds.sort_values("midi")
        ax.plot(ds["midi"], ds["v"].rolling(7, center=True, min_periods=1).median(),
                color='navy', linewidth=2, zorder=5, label="global median")
    add_lit_lines(ax)
    ax.set_title("LPC F1 vs. MIDI — all dynamics")
    ax.set_xlabel("MIDI pitch"); ax.set_ylabel("Hz")
    ax.set_ylim(0, args.max_freq); ax.legend(fontsize=7)

    # ── [0,1]  LPC F1 vs MIDI — coloured by dynamic ──────────────────────────
    ax = axes[0, 1]
    scatter_by_dyn(ax, df_valid, "lpc_F1")
    add_lit_lines(ax)
    ax.set_title("LPC F1 vs. MIDI — by dynamic")
    ax.set_xlabel("MIDI pitch"); ax.set_ylabel("Hz")
    ax.set_ylim(0, args.max_freq)
    ax.legend(fontsize=7, ncol=2)

    # ── [1,0]  Fp centroid vs MIDI — all dynamics ─────────────────────────────
    ax = axes[1, 0]
    fp_all = pd.to_numeric(df_valid["fp_centroid"], errors='coerce')
    valid_idx = fp_all.dropna().index
    if not valid_idx.empty:
        ax.scatter(df_valid.loc[valid_idx, "midi"], fp_all[valid_idx],
                   alpha=0.35, s=18, color='darkorange', zorder=2, label="all dynamics")
        ds = df_valid.loc[valid_idx].copy()
        ds["v"] = fp_all[valid_idx]
        ds = ds.sort_values("midi")
        ax.plot(ds["midi"], ds["v"].rolling(7, center=True, min_periods=1).median(),
                color='saddlebrown', linewidth=2, zorder=5, label="global median")
    ax.axhline(1046, linestyle='-', color='#8e44ad', linewidth=1.5,
               label="Fp pipeline (1046 Hz)")
    add_lit_lines(ax)
    ax.set_title(f"Fp centroid [{args.fp_band[0]:.0f}–{args.fp_band[1]:.0f} Hz] vs. MIDI — all dynamics")
    ax.set_xlabel("MIDI pitch"); ax.set_ylabel("Hz")
    ax.legend(fontsize=7)

    # ── [1,1]  Fp centroid vs MIDI — coloured by dynamic ─────────────────────
    ax = axes[1, 1]
    scatter_by_dyn(ax, df_valid, "fp_centroid")
    ax.axhline(1046, linestyle='-', color='#8e44ad', linewidth=1.5,
               label="Fp pipeline (1046 Hz)", zorder=6)
    add_lit_lines(ax)
    ax.set_title("Fp centroid vs. MIDI — by dynamic")
    ax.set_xlabel("MIDI pitch"); ax.set_ylabel("Hz")
    ax.legend(fontsize=7, ncol=2)

    # ── [2,0]  Histogram LPC F1 — stacked by dynamic ─────────────────────────
    ax = axes[2, 0]
    bins = np.linspace(0, args.max_freq, 60)
    for dyn in present_dyns:
        if dyn == "other":
            mask = other_mask.reindex(df_valid.index, fill_value=False)
        else:
            mask = df_valid["dyn_norm"] == dyn
        vals = pd.to_numeric(df_valid.loc[mask, "lpc_F1"], errors='coerce').dropna()
        if vals.empty:
            continue
        ax.hist(vals, bins=bins, alpha=0.55, color=DYN_COLORS.get(dyn, "#95a5a6"),
                label=dyn, edgecolor='none')
    for (label, val), col, ls in zip(lit_refs.items(), lit_colors, lit_styles):
        ax.axvline(val, linestyle=ls, color=col, linewidth=1.5, label=label)
    ax.set_title("LPC F1 histogram — by dynamic")
    ax.set_xlabel("Hz"); ax.set_ylabel("Count")
    ax.legend(fontsize=7, ncol=2)

    # ── [2,1]  Box plot: LPC F1 per dynamic ──────────────────────────────────
    ax = axes[2, 1]
    box_data = []
    box_labels = []
    box_colors = []
    for dyn in present_dyns:
        if dyn == "other":
            mask = other_mask.reindex(df_valid.index, fill_value=False)
        else:
            mask = df_valid["dyn_norm"] == dyn
        vals = pd.to_numeric(df_valid.loc[mask, "lpc_F1"], errors='coerce').dropna()
        if len(vals) >= 2:
            box_data.append(vals.values)
            box_labels.append(f"{dyn}\n(n={len(vals)})")
            box_colors.append(DYN_COLORS.get(dyn, "#95a5a6"))
    if box_data:
        bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True,
                        medianprops=dict(color='white', linewidth=2))
        for patch, color in zip(bp['boxes'], box_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
    for (label, val), col, ls in zip(lit_refs.items(), lit_colors, lit_styles):
        ax.axhline(val, linestyle=ls, color=col, linewidth=1.2,
                   alpha=0.85, label=label)
    ax.set_title("LPC F1 distribution — by dynamic (boxplot)")
    ax.set_ylabel("Hz")
    ax.legend(fontsize=7)
    ax.set_ylim(0, args.max_freq)

    plt.tight_layout()
    plot_path = Path(args.output).with_suffix(".png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved: {plot_path}")
    if args.plot:
        plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# Summary statistics
# ─────────────────────────────────────────────────────────────────────────────

def print_summary(df: pd.DataFrame, args):
    print("\n" + "="*65)
    print("SUMMARY — Formant Estimates")
    print("="*65)
    print(f"  Files analyzed : {len(df)}")
    print(f"  Technique      : '{args.technique}'\n")

    cols_to_summarize = ["lpc_F1", "lpc_F2", "fp_centroid"] + \
                        [f"cep_F1_order{o}" for o in args.cep_orders]

    # Literature targets for trumpet (adjust for other instruments)
    lit = {"Backus(1969)": 700, "Meyer(2009)": 800, "Giesler(1985)": 900}

    for col in cols_to_summarize:
        vals = pd.to_numeric(df[col], errors='coerce').dropna()
        if vals.empty:
            continue
        print(f"  {col:30s}  median={vals.median():.0f} Hz  "
              f"mean={vals.mean():.0f} Hz  σ={vals.std():.0f}  "
              f"N={len(vals)}")

    print("\n  Literature reference (trumpet):")
    for src, val in lit.items():
        print(f"    {src:20s}: {val} Hz")

    print("\n  Δ (LPC F1 median vs literature):")
    lpc = pd.to_numeric(df["lpc_F1"], errors='coerce').dropna()
    if not lpc.empty:
        for src, val in lit.items():
            print(f"    vs {src:16s}: {lpc.median() - val:+.0f} Hz")
    print("="*65 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# Argument parsing and entry point
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-method formant analysis on a WAV sample collection."
    )
    parser.add_argument("folder", help="Folder containing WAV files (searched recursively)")
    parser.add_argument("--technique", default="ordinario",
                        help="Filter filenames containing this technique string (default: ordinario)")
    parser.add_argument("--lpc-order", type=int, default=18, dest="lpc_order",
                        help="LPC order (default: 18; rule of thumb: 2 + sr/1000)")
    parser.add_argument("--cep-orders", type=int, nargs="+", default=[40, 80, 160],
                        dest="cep_orders",
                        help="Cepstral smoothing orders to compare (default: 40 80 160)")
    parser.add_argument("--fp-band", type=str, default="600,1800", dest="fp_band",
                        help="Fp centroid band in Hz, e.g. '600,1800' (default)")
    parser.add_argument("--sr", type=int, default=44100,
                        help="Target sample rate (default: 44100)")
    parser.add_argument("--max-freq", type=float, default=4000.0, dest="max_freq",
                        help="Upper frequency limit for analysis (default: 4000 Hz)")
    parser.add_argument("--fft-size", type=int, default=4096, dest="fft_size",
                        help="FFT size (default: 4096)")
    parser.add_argument("--skip-attack", type=int, default=100, dest="skip_attack",
                        help="Skip first N ms (attack transient) before analysis (default: 100ms)")
    parser.add_argument("--seg-duration", type=int, default=500, dest="seg_duration",
                        help="Duration of steady-state segment to analyze in ms (default: 500ms)")
    parser.add_argument("--output", default="formant_results.csv",
                        help="Output CSV path (default: formant_results.csv)")
    parser.add_argument("--plot", action="store_true",
                        help="Show plots interactively after analysis")
    return parser.parse_args()


def main():
    args = parse_args()

    # Parse fp-band
    try:
        lo, hi = map(float, args.fp_band.split(","))
        args.fp_band = (lo, hi)
    except Exception:
        print("Error: --fp-band must be in format 'low,high' e.g. '600,1800'")
        sys.exit(1)

    args.folder = os.path.expanduser(args.folder)
    if not os.path.isdir(args.folder):
        print(f"Error: folder not found: {args.folder}")
        sys.exit(1)

    print(f"\nScanning: {args.folder}")
    print(f"Technique filter: '{args.technique}'")
    wav_files = collect_wav_files(args.folder, args.technique)
    print(f"Found {len(wav_files)} matching WAV files\n")

    if not wav_files:
        print("No files found. Check folder path and --technique filter.")
        sys.exit(1)

    results = []
    for i, wav_path in enumerate(wav_files):
        name = os.path.basename(wav_path)
        print(f"  [{i+1:4d}/{len(wav_files)}] {name}", end="")
        row = analyze_file(wav_path, args)
        if row:
            lpc_str = f"  LPC-F1={row['lpc_F1']} Hz" if row['lpc_F1'] else ""
            print(lpc_str)
            results.append(row)
        else:
            print("  [skipped]")

    if not results:
        print("No results produced.")
        sys.exit(1)

    df = pd.DataFrame(results)

    # Save CSV
    df.to_csv(args.output, index=False)
    print(f"\nResults saved: {args.output} ({len(df)} rows)")

    print_summary(df, args)

    # Always save plot; show if --plot
    plot_results(df, args)


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    main()
