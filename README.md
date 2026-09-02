# Spectroscopy Data Analyzer

A Python-based automation tool for processing raw UV-Vis spectrophotometer data collected from TiO2/PDMS thin-film coating samples.

## Purpose

Raw transmittance spectra collected from spectrophotometers often contain instrumental noise, missing (NaN) readings, and physically impossible values (transmittance below 0% or above 100%). Manually cleaning this data in Excel or OriginLab is error-prone and difficult to reproduce across multiple samples. This tool automates that pipeline to ensure consistent, reproducible, and auditable data processing for materials characterization workflows.

## What it does

1. **Load raw data** - reads a CSV file exported from the spectrophotometer (wavelength vs. transmittance).
2. **Physical bounds check** - flags and logs any transmittance values below 0% or above 100%, then clips them to a physically valid range.
3. **Missing data handling** - detects NaN/unreadable values and fills them using linear interpolation, logging how many points were affected.
4. **Noise smoothing** - applies a Savitzky-Golay filter (scipy.signal.savgol_filter) to remove high-frequency instrumental noise while preserving the underlying spectral trend.
5. **Visualization** - overlays raw (semi-transparent) and filtered (opaque) spectra in a single publication-ready, high-resolution .png figure.
6. **Export** - writes the cleaned, filtered dataset to a new .csv file ready for archiving or further analysis.

## Installation

    git clone https://github.com/erenA4/Spectroscopy-Data-Analyzer.git
    cd Spectroscopy-Data-Analyzer
    python -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r requirements.txt

## Usage

Place your raw spectrophotometer CSV file in the project directory, then run:

    python analiz.py

Outputs:
- temizlenmis_spektro_verisi.csv - cleaned, filtered dataset
- spektro_sonucu.png - raw vs. filtered spectrum comparison plot

## Filter parameters

WINDOW_LENGTH and POLY_ORDER in analiz.py control the Savitzky-Golay filter. These should be chosen relative to the spectral point spacing of your instrument.

## Limitations

- Out-of-range values are clipped after logging; this does not distinguish between sensor noise and genuine baseline drift.
- No automated unit tests are currently included.
- Filter parameters are not yet auto-selected based on data resolution.

## Tech stack

- pandas, NumPy - data cleaning and interpolation
- SciPy - noise smoothing
- Matplotlib - visualization
