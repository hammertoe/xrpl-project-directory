import datetime
import os
import sys
import toml

data_path = "data"
mandatory_fields = ["title", "url", "modified_date", "category"]

def parse_files(data_path):
    failed_files = []
    successful_files = []
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if(file.endswith(".toml")):
                path = os.path.join(root, file)
                print("parsing file", path)
                try:
                    data = toml.load(path)
                except toml.decoder.TomlDecodeError as e:
                    print(f"ERROR: {path} failed to decode: {e}")
                    failed_files.append(path)
                    continue
                    
                # Check mandatory fields
                missing_fields = []
                for field in mandatory_fields:
                    if field not in data:
                        missing_fields.append(field)
                if missing_fields:
                    print(f"ERROR: {path} is missing fields {', '.join(missing_fields)}")
                    failed_files.append(path)
                    # skip rest of processing for this file
                    continue

                # Check that the modified_date is a valid date
                try:
                    last_modified = datetime.datetime.fromisoformat(data['modified_date'])
                except ValueError:
                    print(f"ERROR: {path} invalid modified_date field")
                    failed_files.append(path)
                    continue

                # If we reach here our file has been validated successfully
                successful_files.append(path)

    return successful_files, failed_files


if __name__ == "__main__":
    successful_files, failed_files = parse_files(data_path)

    print()
    print(f"Sucessfully parsed {len(successful_files)} files.")
    print(f"Failed files: {len(failed_files)}.")

    # Return non-zero error code to signal to other processes
    if failed_files:
        sys.exit(1)
