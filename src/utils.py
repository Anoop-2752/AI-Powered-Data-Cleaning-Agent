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

def generate_report(issues, raw_shape=None, processed_shape=None, base_name="data_cleaning_report"):
    ensure_directories()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = os.path.join(REPORTS_DIR, f"{base_name}_{ts}.txt")
    json_path = os.path.join(REPORTS_DIR, f"{base_name}_{ts}.json")

    lines = []
    lines.append("Data Cleaning Report")
    lines.append("="*40)
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if raw_shape:
        lines.append(f"Raw shape: {raw_shape}")
    if processed_shape:
        lines.append(f"Processed shape: {processed_shape}")
    lines.append("")
    if issues:
        lines.append("Issues / Actions:")
        for i in issues:
            lines.append(f"- {i}")
    else:
        lines.append("No issues found.")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    meta = {
        "date": datetime.now().isoformat(),
        "raw_shape": raw_shape,
        "processed_shape": processed_shape,
        "issues": issues
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"📄 Report saved to: {txt_path}")
    return txt_path
