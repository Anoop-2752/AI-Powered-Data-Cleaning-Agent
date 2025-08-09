from src.data_loading import load_raw_data
from src.data_cleaning import clean_data
from src.data_validation import validate_data
from src.utils import save_processed_data, generate_report

def main():
    print("🚀 Starting Data Cleaning Agent...\n")

    df_raw = load_raw_data()
    if df_raw is None:
        return

    df_clean = clean_data(df_raw)
    issues = validate_data(df_clean)

    if issues:
        print("\n⚠️ Validation Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n✅ No validation issues found.")

    processed_path = save_processed_data(df_clean)
    generate_report(issues)

if __name__ == "__main__":
    main()
