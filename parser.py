import toml
import os

data_path = "data"


def parse_files(data_path):
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if(file.endswith(".toml")):
                path = os.path.join(root, file)
                print("parsing file", path)
                try:
                    data = toml.load(path)
                except toml.decoder.TomlDecodeError as e:
                    print("Failed to decode: ", path, e)
            

if __name__ == "__main__":
    parse_files(data_path)

