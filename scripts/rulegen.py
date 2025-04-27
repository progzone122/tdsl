from pathlib import Path
import string
import json

from models import Domain

BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_PATH = BASE_DIR / "template.txt"
DOMAINS_PATH = (BASE_DIR / "../domains.json").resolve()
OUTPUT_PATH = (BASE_DIR / "../rules.txt").resolve()

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        raise
    except PermissionError:
        print(f"Error: Permission denied when reading '{file_path}'.")
        raise
    except Exception as e:
        print(f"Unexpected error when reading file '{file_path}': {e}")
        raise

def get_domains():
    try:
        domains_file = read_file(DOMAINS_PATH)
        domains_json = json.loads(domains_file)

        domains = []

        for item in domains_json:
            domain = item.get("domain")
            source = item.get("source")

            if not isinstance(domain, str):
                raise ValueError(f"Expected string for 'domain', got {type(domain)}")
            if not isinstance(source, str):  # Если source не строка, это ошибка
                raise ValueError(f"Expected string for 'source', got {type(source)}")

            domains.append(Domain(domain, source))

        return domains
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{DOMAINS_PATH}'.")
        raise
    except ValueError as e:
        print(f"Error: Invalid data format - {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while getting domains: {e}")
        raise

def append_rule(domain):
    if not isinstance(domain, Domain):
        raise ValueError(f"Expected Domain object, got {type(domain)}")

    try:
        template_content = read_file(TEMPLATE_PATH)
        template = string.Template(template_content)

        result_text = template.substitute(domain=domain.domain)

        with open(OUTPUT_PATH, "a", encoding="utf-8") as output_file:
            output_file.write(result_text)

        print(f"Successfully added new rules for domain '{domain.domain}' to rules.txt")
    except FileNotFoundError:
        print(f"Error: Template file '{TEMPLATE_PATH}' not found.")
    except PermissionError:
        print(f"Error: Permission denied when writing to '{OUTPUT_PATH}'.")
    except KeyError as e:
        print(f"Error: Missing key in template: {e}")
    except Exception as e:
        print(f"Unexpected error when appending rule for domain '{domain.domain}': {e}")
        raise

def main():
    try:
        domains = get_domains()

        # clean file
        with open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
            output_file.write("")

        for domain in domains:
            append_rule(domain)
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()