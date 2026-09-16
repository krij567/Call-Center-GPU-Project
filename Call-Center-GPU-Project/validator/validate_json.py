import json
import os
import sys
from jsonschema import validate, ValidationError


SCHEMA_FILE = "schema/gpu_extraction.schema.json"
BATCH_FOLDER = "data/batches"


def main():
    try:
        # Load schema
        with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
            schema = json.load(file)

        # Find all JSON batch files
        batch_files = sorted(
            filename
            for filename in os.listdir(BATCH_FOLDER)
            if filename.endswith(".json")
        )

        if not batch_files:
            print("NO JSON BATCHES FOUND.")
            sys.exit(1)

        all_valid = True

        # Validate each batch
        for filename in batch_files:

            json_path = os.path.join(BATCH_FOLDER, filename)

            try:
                with open(json_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                validate(instance=data, schema=schema)

                print(f"VALID: {filename}")

            except ValidationError as error:
                print(f"INVALID: {filename}")
                print(f"Problem: {error.message}")
                all_valid = False

            except json.JSONDecodeError as error:
                print(f"INVALID JSON: {filename}")
                print(error)
                all_valid = False

        # Final result
        if all_valid:
            print("ALL BATCHES VALID.")
        else:
            print("ONE OR MORE BATCHES ARE INVALID.")
            sys.exit(1)

    except FileNotFoundError as error:
        print("FILE NOT FOUND:")
        print(error.filename)
        sys.exit(1)


if __name__ == "__main__":
    main()