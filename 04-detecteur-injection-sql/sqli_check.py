import argparse
import urllib.parse
import urllib.request


PAYLOADS = ["'", "\"", "' OR 1=1 --", "\" OR 1=1 --"]


def fetch(url: str) -> tuple:
    req = urllib.request.Request(url, headers={"User-Agent": "SQLi-Checker"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read()
    return resp.status, len(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Detecteur SQLi basique")
    parser.add_argument("--url", required=True, help="URL avec parametre ex: https://site.tld?id=1")
    args = parser.parse_args()

    base_status, base_len = fetch(args.url)
    results = []
    for payload in PAYLOADS:
        test_url = args.url + urllib.parse.quote(payload)
        try:
            status, length = fetch(test_url)
            changed = (status != base_status) or (abs(length - base_len) > 200)
            results.append({"payload": payload, "status": status, "length": length, "changed": changed})
        except Exception as exc:
            results.append({"payload": payload, "error": str(exc)})

    for item in results:
        print(item)


if __name__ == "__main__":
    main()
