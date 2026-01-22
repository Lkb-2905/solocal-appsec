import argparse
import json
import urllib.request


def fetch_crtsh(domain: str) -> list:
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = resp.read().decode("utf-8")
    if not data:
        return []
    return json.loads(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="OSINT sous-domaines via crt.sh")
    parser.add_argument("--domain", required=True)
    args = parser.parse_args()

    records = fetch_crtsh(args.domain)
    names = set()
    for item in records:
        name = item.get("name_value", "")
        for entry in name.split("\n"):
            if entry.endswith(args.domain):
                names.add(entry.strip())

    for entry in sorted(names):
        print(entry)


if __name__ == "__main__":
    main()
