import argparse
import re
from collections import Counter


LOG_RE = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<date>[^\]]+)\] "(?P<req>[^"]+)" (?P<status>\d{3})')


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyseur logs Apache/Nginx")
    parser.add_argument("--input", required=True)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()

    counter = Counter()
    with open(args.input, "r", encoding="utf-8") as handle:
        for line in handle:
            match = LOG_RE.match(line)
            if not match:
                continue
            status = match.group("status")
            if status == "404":
                counter[match.group("ip")] += 1

    for ip, count in counter.most_common(args.top):
        print(f"{ip} {count}")


if __name__ == "__main__":
    main()
