import datetime
import os
import toml

data_path = "data"
mandatory_fields = ["title", "url", "modified_date", "category"]

def parse_files(data_path):
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if(file.endswith(".toml")):
                path = os.path.join(root, file)
                print("parsing file", path)
                try:
                    data = toml.load(path)
                except toml.decoder.TomlDecodeError as e:
                    print(f"ERROR: {path} failed to decode: {e}")
                    continue
                    
                # Check mandatory fields
                missing_fields = []
                for field in mandatory_fields:
                    if field not in data:
                        missing_fields.append(field)
                if missing_fields:
                    print(f"ERROR: {path} is missing fields {', '.join(missing_fields)}")
                    # skip rest of processing for this file
                    continue

                # Check that the modified_date is a valid date
                try:
                    last_modified = datetime.datetime.fromisoformat(data['modified_date'])
                except ValueError:
                    print(f"ERROR: {path} invalid modified_date field")
                    continue


if __name__ == "__main__":
    parse_files(data_path)

