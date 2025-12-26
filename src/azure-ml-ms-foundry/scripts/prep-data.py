
import argparse
import csv
import glob
import os
import shutil
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def get_data(path):
    import os, glob, tempfile, shutil, csv
    from pathlib import Path

    p = Path(path)
    if p.is_dir():
        candidates = sorted(p.glob("*.csv"))
        if not candidates:
            raise FileNotFoundError(f"No CSV files in: {p}")
        p = candidates[0]

    # copy to local temp to avoid mount read(nbytes) issues
    fd, tmp = tempfile.mkstemp(suffix=p.suffix or ".csv"); os.close(fd)
    shutil.copyfile(str(p), tmp)

    # detect delimiter (fallback to comma)
    try:
        with open(tmp, "r", encoding="utf-8", errors="ignore") as f:
            sample = f.read(20000)
        sep = csv.Sniffer().sniff(sample, delimiters=[",",";","\t","|"]).delimiter
    except Exception:
        sep = ","

    # robust read with python engine
    try:
        df = pd.read_csv(tmp, engine="python", sep=sep)
    except UnicodeDecodeError:
        df = pd.read_csv(tmp, engine="python", sep=sep, encoding="latin-1")

    print(f"Preparing {len(df)} rows of data")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # simple NA drop; extend with domain-specific cleaning if needed
    before = df.shape[0]
    df = df.dropna()
    print(f"[DEBUG] clean_data: dropped {before - df.shape[0]} rows with NA")
    return df


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    # Handle common column name variants (Pima Indians dataset vs your names)
    alias_groups = {
        "Pregnancies": ["Pregnancies"],
        "Glucose": ["Glucose", "PlasmaGlucose"],
        "BloodPressure": ["BloodPressure", "DiastolicBloodPressure"],
        "SkinThickness": ["SkinThickness", "TricepsThickness"],
        "Insulin": ["Insulin", "SerumInsulin"],
        "BMI": ["BMI"],
        "DiabetesPedigreeFunction": ["DiabetesPedigreeFunction", "DiabetesPedigree"],
        # Add "Age" if you want to scale it too
    }

    # Pick whichever alias exists in df
    cols_to_scale = []
    for canonical, aliases in alias_groups.items():
        for a in aliases:
            if a in df.columns:
                cols_to_scale.append(a)
                break

    if not cols_to_scale:
        raise ValueError("None of the expected numeric columns were found to scale.")

    # Coerce to numeric
    for c in cols_to_scale:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Drop rows that became NaN in any scaled column
    before = df.shape[0]
    df = df.dropna(subset=cols_to_scale)
    print(f"[DEBUG] normalize_data: coerced to numeric; dropped {before - df.shape[0]} rows with non-numeric values in {cols_to_scale}")

    scaler = MinMaxScaler()
    df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
    print(f"[DEBUG] normalized columns: {cols_to_scale}")
    return df


def main(args):
    df = get_data(args.input_data)
    print(f"Preparing {len(df)} rows of data")

    cleaned = clean_data(df)
    normalized = normalize_data(cleaned)

    out_dir = Path(args.output_data)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "diabetes.csv"
    normalized.to_csv(out_path, index=False)
    print(f"[INFO] wrote: {out_path} rows={len(normalized)}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", required=True, type=str)
    parser.add_argument("--output_data", required=True, type=str)
    return parser.parse_args()


if __name__ == "__main__":
    print("start main")
    print("\n\n" + "*" * 60)
    args = parse_args()
    main(args)
    print("*" * 60 + "\n\n")
