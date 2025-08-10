import os
from datetime import datetime
import json

RAW_DATA_PATH = os.path.join("data", "raw", "cafe_sales_dirty.csv")
PROCESSED_DATA_DIR = os.path.join("data", "processed")
REPORTS_DIR = os.path.join("reports")

def ensure_directories():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

def get_versioned_filename(base_name: str, ext: str = ".csv") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{ts}{ext}"

def save_processed_data(df, base_name="cafe_sales_cleaned"):
    ensure_directories()
    filename = get_versioned_filename(base_name, ".csv")
    path = os.path.join(PROCESSED_DATA_DIR, filename)
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"✅ Processed data saved to: {path}")
    return path

def generate_report(issues, raw_shape=None, processed_shape=None, column_types=None):
    """Generate a text report of issues, shapes, and column type detection."""
    from datetime import datetime
    import os

    report_lines = []
    report_lines.append(f"Data Cleaning Report - {datetime.now()}")
    report_lines.append("=" * 50)
    if raw_shape and processed_shape:
        report_lines.append(f"Raw Shape: {raw_shape}")
        report_lines.append(f"Processed Shape: {processed_shape}")
        report_lines.append("")

    if issues:
        report_lines.append("Cleaning & Validation Issues:")
        for issue in issues:
            report_lines.append(f" - {issue}")
    else:
        report_lines.append("No cleaning or validation issues detected.")

    report_lines.append("")

    # New: Column types
    if column_types:
        report_lines.append("Detected Column Types:")
        for col, ctype in column_types.items():
            report_lines.append(f" - {col}: {ctype}")

    report_lines.append("=" * 50)

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    filename = os.path.join(
        reports_dir,
        f"data_cleaning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(filename, "w") as f:
        f.write("\n".join(report_lines))

    return filename

