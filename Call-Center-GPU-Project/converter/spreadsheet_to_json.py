import csv
import json
import os
from collections import OrderedDict

CSV_FILE = "data/gpu_data.csv"
OUTPUT_FOLDER = "data/batches"


def clean_value(value):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def normalize_confidence(value):
    value = clean_value(value)

    if value is None:
        return None

    return value.lower()


def normalize_availability(value):
    value = clean_value(value)

    if value is None:
        return None

    return value.lower().replace("-", "_").replace(" ", "_")


def convert_price(value):
    value = clean_value(value)

    if value is None:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def convert_quantity(value):
    value = clean_value(value)

    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return value


def convert_batch_number(value):
    value = clean_value(value)

    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def main():

    if not os.path.exists(CSV_FILE):
        print(f"FILE NOT FOUND: {CSV_FILE}")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("NO DATA FOUND IN CSV.")
        return

    batches = OrderedDict()

    for row in rows:

        batch_number = convert_batch_number(row.get("Batch"))

        if batch_number is None:
            print("ERROR: A row has a missing or invalid Batch value.")
            print(row)
            return

        if batch_number not in batches:
            batches[batch_number] = []

        record_key = (
            clean_value(row.get("Agent")),
            clean_value(row.get("Date")),
            clean_value(row.get("Retail_ID")),
            clean_value(row.get("Location")),
            clean_value(row.get("Retailer")),
            clean_value(row.get("Source"))
        )

        existing_record = None

        for record in batches[batch_number]:
            current_key = (
                record["agent"],
                record["date"],
                record["retail_id"],
                record["location"],
                record["retailer"],
                record["source"]
            )

            if current_key == record_key:
                existing_record = record
                break

        if existing_record is None:
            existing_record = {
                "agent": record_key[0],
                "date": record_key[1],
                "retail_id": record_key[2],
                "location": record_key[3],
                "retailer": record_key[4],
                "source": record_key[5],
                "products": []
            }

            batches[batch_number].append(existing_record)

        price_amount = convert_price(row.get("Price"))

        price_type = clean_value(row.get("Price_type"))

        if price_type is None:
            price_type = "Not stated"

        product = {
            "gpu_model": clean_value(row.get("GPU model")),
            "gpu_category": clean_value(row.get("GPU Category")),
            "manufacturer": clean_value(row.get("Manufacturer")),
            "variant": clean_value(row.get("Variant")),
            "price": {
                "amount": price_amount,
                "currency": "USD",
                "price_type": price_type,
                "raw": None
            },
            "availability": normalize_availability(
                row.get("Availability")
            ),
            "quantity": convert_quantity(row.get("Quantity")),
            "restock_date": clean_value(row.get("Restock_date")),
            "confidence": normalize_confidence(row.get("Confidence")),
            "evidence": clean_value(row.get("Evidence"))
        }

        existing_record["products"].append(product)

    for batch_number, records in batches.items():

        data = {
            "batch_number": batch_number,
            "records": records
        }

        output_path = os.path.join(
            OUTPUT_FOLDER,
            f"batch_{batch_number:03d}.json"
        )

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

        total_products = sum(
            len(record["products"])
            for record in records
        )

        print(f"CREATED: {output_path}")
        print(f"CALL/STORE RECORDS: {len(records)}")
        print(f"GPU RECORDS: {total_products}")
        print(f"SUCCESS: Created Batch {batch_number}.")


if __name__ == "__main__":
    main()