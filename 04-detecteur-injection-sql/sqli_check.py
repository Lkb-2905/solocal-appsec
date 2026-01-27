import argparse
import urllib.parse
import urllib.request


PAYLOADS = ["'", "\"", "' OR 1=1 --", "\" OR 1=1 --"]
OFFLINE_BASE = {"status": 200, "length": 1200}


def fetch(url: str) -> tuple:
    req = urllib.request.Request(url, headers={"User-Agent": "SQLi-Checker"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read()
    return resp.status, len(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Detecteur SQLi basique")
    parser.add_argument("--url", help="URL avec parametre ex: https://site.tld?id=1")
    parser.add_argument("--input", help="Fichier de URLs (une par ligne)")
    parser.add_argument("--offline", action="store_true", help="Mode demo sans reseau")
    args = parser.parse_args()

    targets = []
    if args.url:
        targets.append(args.url)
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            targets.extend([line.strip() for line in handle if line.strip()])
    if not targets:
        raise SystemExit("Fournissez --url ou --input.")

    for target in targets:
        if args.offline:
            base_status, base_len = OFFLINE_BASE["status"], OFFLINE_BASE["length"]
        else:
            base_status, base_len = fetch(target)
        results = []
        for payload in PAYLOADS:
            test_url = target + urllib.parse.quote(payload)
            try:
                if args.offline:
                    status = 200
                    length = base_len + (350 if "1=1" in payload else 0)
                else:
                    status, length = fetch(test_url)
                changed = (status != base_status) or (abs(length - base_len) > 200)
                results.append({"payload": payload, "status": status, "length": length, "changed": changed})
            except Exception as exc:
                results.append({"payload": payload, "error": str(exc)})

        print(f"URL: {target}")
        for item in results:
            print(item)


if __name__ == "__main__":
    main()
