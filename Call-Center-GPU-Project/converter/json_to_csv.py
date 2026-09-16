
import csv
import json
import os

BATCH_FOLDER = "data/batches"
OUTPUT_FILE = "data/analysis_data.csv"


def main():

    if not os.path.exists(BATCH_FOLDER):
        print(f"FOLDER NOT FOUND: {BATCH_FOLDER}")
        return

    batch_files = sorted(
        filename
        for filename in os.listdir(BATCH_FOLDER)
        if filename.endswith(".json")
    )

    if not batch_files:
        print("NO JSON BATCHES FOUND.")
        return

    rows = []

    for filename in batch_files:

        json_path = os.path.join(BATCH_FOLDER, filename)

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        batch_number = data.get("batch_number")

        for record in data.get("records", []):

            for product in record.get("products", []):

                price = product.get("price", {})

                row = {
                    "Batch": batch_number,
                    "Agent": record.get("agent"),
                    "Date": record.get("date"),
                    "Retail_ID": record.get("retail_id"),
                    "Location": record.get("location"),
                    "Retailer": record.get("retailer"),
                    "GPU model": product.get("gpu_model"),
                    "GPU Category": product.get("gpu_category"),
                    "Manufacturer": product.get("manufacturer"),
                    "Variant": product.get("variant"),
                    "Price": price.get("amount"),
                    "Currency": price.get("currency"),
                    "Price_type": price.get("price_type"),
                    "Availability": product.get("availability"),
                    "Quantity": product.get("quantity"),
                    "Restock_date": product.get("restock_date"),
                    "Source": record.get("source"),
                    "Confidence": product.get("confidence"),
                    "Evidence": product.get("evidence")
                }

                rows.append(row)

    fieldnames = [
        "Batch",
        "Agent",
        "Date",
        "Retail_ID",
        "Location",
        "Retailer",
        "GPU model",
        "GPU Category",
        "Manufacturer",
        "Variant",
        "Price",
        "Currency",
        "Price_type",
        "Availability",
        "Quantity",
        "Restock_date",
        "Source",
        "Confidence",
        "Evidence"
    ]

    os.makedirs("data", exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"CREATED: {OUTPUT_FILE}")
    print(f"BATCH FILES: {len(batch_files)}")
    print(f"GPU RECORDS: {len(rows)}")


if __name__ == "__main__":
    main()
