import csv
import os
from collections import Counter


INPUT_FILE = "data/analysis_data.csv"
OUTPUT_FILE = "data/analysis_report.txt"


def normalize_gpu_model(model):
    if not model:
        return model

    model = model.strip()

    replacements = {
        "GeForce RTX": "RTX",
        "Radeon RX": "RX"
    }

    for old, new in replacements.items():
        if model.startswith(old):
            model = model.replace(old, new, 1)
            break

    return model


def main():

    if not os.path.exists(INPUT_FILE):
        print(f"FILE NOT FOUND: {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("NO DATA FOUND.")
        return

    lines = []

    lines.append("=" * 50)
    lines.append("CALL CENTER GPU DATA ANALYSIS")
    lines.append("=" * 50)

    # Total GPU records
    lines.append("")
    lines.append(f"Total GPU records: {len(rows)}")

    # Unique retailers
    retailers = {
        row["Retail_ID"]
        for row in rows
        if row["Retail_ID"]
    }

    lines.append(f"Total retailers/stores: {len(retailers)}")

    # Availability
    availability = Counter(
        row["Availability"]
        for row in rows
        if row["Availability"]
    )

    lines.append("")
    lines.append("AVAILABILITY")

    for status, count in availability.items():
        lines.append(f"{status}: {count}")

    # Prices
    prices = []

    for row in rows:
        try:
            price = float(row["Price"])
            prices.append(price)
        except (ValueError, TypeError):
            pass

    lines.append("")
    lines.append("PRICE")

    if prices:
        average_price = sum(prices) / len(prices)

        lines.append(f"Average price: ${average_price:,.2f}")
        lines.append(f"Lowest price: ${min(prices):,.2f}")
        lines.append(f"Highest price: ${max(prices):,.2f}")
    else:
        lines.append("No valid prices found.")

    # GPU models
    models = Counter(
        normalize_gpu_model(row["GPU model"])
        for row in rows
        if row["GPU model"]
    )

    lines.append("")
    lines.append("MOST REPORTED GPU MODELS")

    for model, count in models.most_common(10):
        lines.append(f"{model}: {count}")

    # Manufacturers
    manufacturers = Counter(
        row["Manufacturer"]
        for row in rows
        if row["Manufacturer"]
    )

    lines.append("")
    lines.append("MANUFACTURERS")

    for manufacturer, count in manufacturers.most_common():
        lines.append(f"{manufacturer}: {count}")

    # Confidence
    confidence = Counter(
        row["Confidence"]
        for row in rows
        if row["Confidence"]
    )

    lines.append("")
    lines.append("CONFIDENCE")

    for level, count in confidence.items():
        lines.append(f"{level}: {count}")

    lines.append("")
    lines.append("=" * 50)
    lines.append("ANALYSIS COMPLETE")
    lines.append("=" * 50)

    report = "\n".join(lines)

    print(report)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nREPORT SAVED: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()