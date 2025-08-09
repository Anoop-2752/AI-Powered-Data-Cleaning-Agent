from src.data_loader import load_data
from src.data_cleaner import clean_data
from src.data_validator import validate_data
from src.utils import save_processed_data, generate_report, RAW_DATA_PATH

def main():
    print("🚀 Starting Data Cleaning Agent...\n")

    # 1. Load raw data
    try:
        df_raw = load_data(RAW_DATA_PATH)
    except FileNotFoundError as e:
        print(str(e))
        return

    raw_shape = df_raw.shape

    # 2. Clean data (returns cleaned df and list of applied fixes)
    df_clean, cleaning_issues = clean_data(df_raw)

    # 3. Validate cleaned data (returns list of issues)
    validation_issues = validate_data(df_clean)

    # 4. Print summary to console
    print("\n📊 Cleaning summary:")
    if cleaning_issues:
        for i in cleaning_issues:
            print(f" - {i}")
    else:
        print(" - No automatic cleaning actions applied.")

    print("\n🔎 Validation summary:")
    if validation_issues:
        for v in validation_issues:
            print(f" - {v}")
    else:
        print(" - No validation issues found.")

    # 5. Save processed data and report
    processed_path = save_processed_data(df_clean)
    report_path = generate_report(
        issues=cleaning_issues + validation_issues,
        raw_shape=raw_shape,
        processed_shape=df_clean.shape
    )

    print("\n🎉 Pipeline finished.")
    print(f"Processed file: {processed_path}")
    print(f"Report file: {report_path}")

if __name__ == "__main__":
    main()
