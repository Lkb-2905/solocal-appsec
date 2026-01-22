import argparse
import base64
import json


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def main() -> None:
    parser = argparse.ArgumentParser(description="Decodeur JWT (sans verification)")
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    parts = args.token.split(".")
    if len(parts) < 2:
        raise SystemExit("JWT invalide (format).")

    header = json.loads(b64url_decode(parts[0]).decode("utf-8"))
    payload = json.loads(b64url_decode(parts[1]).decode("utf-8"))
    print("Header:")
    print(json.dumps(header, ensure_ascii=True, indent=2))
    print("Payload:")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
