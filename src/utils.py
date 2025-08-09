import os
from datetime import datetime

RAW_DATA_PATH = os.path.join("data", "raw", "cafe_sales_dirty.csv")
PROCESSED_DATA_DIR = os.path.join("data", "processed")
REPORTS_DIR = "reports"

def ensure_directories():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

def get_versioned_filename(filename):
    base, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}{ext}"

def save_processed_data(df, filename="cafe_sales_cleaned.csv"):
    ensure_directories()
    versioned_name = get_versioned_filename(filename)
    file_path = os.path.join(PROCESSED_DATA_DIR, versioned_name)
    df.to_csv(file_path, index=False)
    print(f"✅ Processed data saved to: {file_path}")
    return file_path

def generate_report(issues, filename="report.txt"):
    ensure_directories()
    file_path = os.path.join(REPORTS_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:  # ✅ Added encoding
        if issues:
            f.write("⚠️ Validation Issues Found:\n")
            for issue in issues:
                f.write(f"- {issue}\n")
        else:
            f.write("✅ No validation issues found.\n")
    print(f"📄 Report saved to: {file_path}")
    return file_path

