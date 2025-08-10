from src.data_loader import load_data
from src.data_cleaner import clean_data
from src.data_validator import validate_data
from src.utils import save_processed_data, generate_report, RAW_DATA_PATH
from src.config_loader import load_cleaning_config
from src.advanced_cleaner import apply_custom_rules, advanced_imputation
from src.column_type_detector import detect_column_types
from src.llm_suggestions import get_llm_suggestions


def main():
    print("🚀 Starting Data Cleaning Agent...\n")

    # 1️⃣ Load cleaning configuration
    try:
        config = load_cleaning_config()
        print("✅ Cleaning configuration loaded.")
    except FileNotFoundError:
        print("⚠️ No cleaning configuration file found. Using defaults.")
        config = {}

    # 2️⃣ Load raw dataset
    try:
        df_raw = load_data(RAW_DATA_PATH)
        print(f"✅ Raw data loaded: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns.")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return

    raw_shape = df_raw.shape

    # 3️⃣ Apply custom cleaning rules from config
    df_custom = apply_custom_rules(df_raw, config)
    print("✅ Custom cleaning rules applied.")

    # 4️⃣ Apply advanced imputations
    df_imputed = advanced_imputation(df_custom, config)
    print("✅ Advanced imputation completed.")

    # 5️⃣ Automatic cleaning
    df_clean, cleaning_issues = clean_data(df_imputed)
    print("✅ Automatic cleaning completed.")

    # 6️⃣ Validate cleaned data
    validation_issues = validate_data(df_clean)
    print("✅ Validation completed.")

    # 7️⃣ Detect column types
    column_types = detect_column_types(df_clean)

    # 8️⃣ Print cleaning & validation summaries
    print("\n📊 Cleaning summary:")
    if cleaning_issues:
        for issue in cleaning_issues:
            print(f" - {issue}")
    else:
        print(" - No automatic cleaning actions applied.")

    print("\n🔎 Validation summary:")
    if validation_issues:
        for issue in validation_issues:
            print(f" - {issue}")
    else:
        print(" - No validation issues found.")

    # 9️⃣ AI-powered LLM suggestions (Groq)
    ai_suggestions = get_llm_suggestions(
        cleaning_summary="\n".join(cleaning_issues) if cleaning_issues else "No issues.",
        validation_summary="\n".join(validation_issues) if validation_issues else "No issues."
    )
    print("\n🤖 AI Suggestions:")
    if ai_suggestions:
        for s in ai_suggestions:
            print(f" - {s}")
    else:
        print(" - No AI suggestions available.")

    # 🔟 Save processed data and report
    processed_path = save_processed_data(df_clean)
    report_path = generate_report(
        cleaning_issues + validation_issues,
        raw_shape=raw_shape,
        processed_shape=df_clean.shape,
        column_types=column_types
    )

    print("\n🎉 Pipeline finished successfully.")
    print(f"📁 Processed file saved to: {processed_path}")
    print(f"📝 Report file saved to: {report_path}")


if __name__ == "__main__":
    main()
