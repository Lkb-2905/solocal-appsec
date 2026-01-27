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


OFFLINE_RESULTS = {
    "example.com": ["www.example.com", "api.example.com"],
    "pagesjaunes.fr": ["www.pagesjaunes.fr", "m.pagesjaunes.fr"],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="OSINT sous-domaines via crt.sh")
    parser.add_argument("--domain", help="Domaine cible")
    parser.add_argument("--input", help="Fichier de domaines (un par ligne)")
    parser.add_argument("--offline", action="store_true", help="Mode demo sans reseau")
    args = parser.parse_args()

    domains = []
    if args.domain:
        domains.append(args.domain)
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            domains.extend([line.strip() for line in handle if line.strip()])
    if not domains:
        raise SystemExit("Fournissez --domain ou --input.")

    for domain in domains:
        if args.offline:
            names = OFFLINE_RESULTS.get(domain, [f"www.{domain}"])
        else:
            records = fetch_crtsh(domain)
            names = set()
            for item in records:
                name = item.get("name_value", "")
                for entry in name.split("\n"):
                    if entry.endswith(domain):
                        names.add(entry.strip())
            names = sorted(names)
        for entry in names:
            print(entry)


if __name__ == "__main__":
    main()
