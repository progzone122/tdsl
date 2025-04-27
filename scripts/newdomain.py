from pathlib import Path
import argparse
import json

from models import Domain
from rulegen import read_file

BASE_DIR = Path(__file__).resolve().parent

DOMAINS_PATH = (BASE_DIR / "../domains.json").resolve()

def append_domain(domain, source):
    try:
        domains_file = read_file(DOMAINS_PATH)
        domains_json = json.loads(domains_file)

        if source is None:
            source = "[SOURCE]"

            new_domain = Domain(domain, source)
            domains_json.append(new_domain.to_dict())

            with open(DOMAINS_PATH, 'w', encoding='utf-8') as file:
                json.dump(domains_json, file, ensure_ascii=False, indent=4)

            print(f"Successfully appended domain: {domain} with source: {source} to {DOMAINS_PATH}.")

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{DOMAINS_PATH}'.")
        raise
    except ValueError as e:
        print(f"Error: Invalid data format - {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while appending domain: {e}")
        raise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str)
    parser.add_argument('--source', type=str, default=None)

    try:
        args = parser.parse_args()

        append_domain(args.domain, args.source)

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()