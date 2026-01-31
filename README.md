# Solocal - AppSec (demo portfolio)

Objectif: proposer des outils AppSec simples avec mode demo/offline.

## Contenu
- `01-scanner-sous-domaines`: OSINT crt.sh (mode offline).
- `02-validateur-jwt`: decode JWT.
- `03-bot-anti-scraping`: rate limit (mode demo).
- `04-detecteur-injection-sql`: tests basiques (mode offline).
- `05-analyseur-logs-web`: top IP 404.

## Demarrage rapide (demos)
```
cd 01-scanner-sous-domaines
python subdomains.py --input domains.sample.txt --offline

cd ../02-validateur-jwt
python jwt_decode.py --token eyJhbGciOiJub25lIn0.eyJ1c2VyIjoiZGVtbyJ9.

cd ../03-bot-anti-scraping
python app.py --demo

cd ../04-detecteur-injection-sql
python sqli_check.py --input urls.sample.txt --offline

cd ../05-analyseur-logs-web
python log_parser.py --input access.sample.log
```

## Captures conseillees
- Terminal: sous-domaines + JWT + anti-scraping + SQLi + logs.

## Dependances
Voir `requirements.txt`.

## Roadmap et suggestions
- `ROADMAP.md`
- `CODE_SUGGESTIONS.md`
