from pathlib import Path
import zipfile
import pandas as pd


def find_fars_files(file_list):
    acc_file = next((f for f in file_list if "ACC_AUX" in f.upper()), None)
    per_file = next((f for f in file_list if "PER_AUX" in f.upper()), None)
    veh_file = next((f for f in file_list if "VEH_AUX" in f.upper()), None)
    if not acc_file or not per_file or not veh_file:
        raise ValueError("Could not find ACC_AUX, PER_AUX, and VEH_AUX in the zip file.")
    return acc_file, per_file, veh_file


def load_fars_data(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z:
        file_list = z.namelist()
        acc_file, per_file, veh_file = find_fars_files(file_list)
        acc_df = pd.read_csv(z.open(acc_file), low_memory=False)
        per_df = pd.read_csv(z.open(per_file), low_memory=False)
        veh_df = pd.read_csv(z.open(veh_file), low_memory=False)
    return acc_df, per_df, veh_df


def clean_column_names(df):
    df.columns = [col.strip().upper() for col in df.columns]
    return df


def basic_cleaning(df, name):
    df = clean_column_names(df)
    if "ST_CASE" not in df.columns:
        raise ValueError(f"ST_CASE not found in {name}")
    df = df.drop_duplicates()
    df["ST_CASE"] = pd.to_numeric(df["ST_CASE"], errors="coerce")
    df = df.dropna(subset=["ST_CASE"]).copy()
    df["ST_CASE"] = df["ST_CASE"].astype(int)
    print(f"\n{name} after basic cleaning:")
    print("Shape:", df.shape)
    print("Missing ST_CASE:", df["ST_CASE"].isna().sum())
    return df


def summarize_person_data(per_df):
    per_summary = per_df.groupby("ST_CASE").size().reset_index(name="PERSON_RECORD_COUNT")
    return per_summary


def summarize_vehicle_data(veh_df):
    veh_summary = veh_df.groupby("ST_CASE").size().reset_index(name="VEHICLE_RECORD_COUNT")
    return veh_summary


def merge_to_crash_level(acc_df, per_summary, veh_summary):
    merged_df = acc_df.merge(per_summary, on="ST_CASE", how="left")
    merged_df = merged_df.merge(veh_summary, on="ST_CASE", how="left")
    merged_df["PERSON_RECORD_COUNT"] = merged_df["PERSON_RECORD_COUNT"].fillna(0).astype(int)
    merged_df["VEHICLE_RECORD_COUNT"] = merged_df["VEHICLE_RECORD_COUNT"].fillna(0).astype(int)
    return merged_df


def main():
    repo_root = Path(__file__).resolve().parents[1]
    zip_path = repo_root / "data" / "raw" / "FARS2023NationalAuxiliaryCSV.zip"
    output_dir = repo_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    acc_df, per_df, veh_df = load_fars_data(zip_path)
    print("\nOriginal dataset shapes:")
    print("ACC_AUX:", acc_df.shape)
    print("PER_AUX:", per_df.shape)
    print("VEH_AUX:", veh_df.shape)

    acc_df = basic_cleaning(acc_df, "ACC_AUX")
    per_df = basic_cleaning(per_df, "PER_AUX")
    veh_df = basic_cleaning(veh_df, "VEH_AUX")

    per_summary = summarize_person_data(per_df)
    veh_summary = summarize_vehicle_data(veh_df)

    print("\nSummary shapes:")
    print("PER summary:", per_summary.shape)
    print("VEH summary:", veh_summary.shape)

    integrated_df = merge_to_crash_level(acc_df, per_summary, veh_summary)

    print("\nIntegrated dataset shape:")
    print(integrated_df.shape)
    print("\nFirst 5 rows:")
    print(integrated_df.head())

    acc_df.to_csv(output_dir / "acc_aux_cleaned.csv", index=False)
    per_df.to_csv(output_dir / "per_aux_cleaned.csv", index=False)
    veh_df.to_csv(output_dir / "veh_aux_cleaned.csv", index=False)
    per_summary.to_csv(output_dir / "per_summary_by_st_case.csv", index=False)
    veh_summary.to_csv(output_dir / "veh_summary_by_st_case.csv", index=False)
    integrated_df.to_csv(output_dir / "fars_integrated_crash_level.csv", index=False)

    print("\nSaved files to data/processed/")


if __name__ == "__main__":
    main()