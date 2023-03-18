# traducir
Gør det nemmere at bruge danske begreber i datalogi.

# Setup
## Podman (anbefales)
Kør

```
podman kube play kube.yaml
```

Besøg `http://localhost:1025`. Hvis man ønsker at ændre port / domæne skal man bare ændre `Caddyfile` og `kube.yaml`.

## Manuelt
Alt efter hvilken distro kan du skifte mellem apt eller dnf.
`sudo dnf install python3-waitress python3-flask python3-lxml python3-requests`
APIen klargøres med:
`python3 database-setup.py`
`waitress-serve --listen=127.0.0.1:5000 app:app`

Caddy bruges som en reverse proxy til ovenstående API og filserver til hjemmesiden. Instrukser for at installere det kan findes på https://caddyserver.com/docs/install. Alt efter hvilket domæne man har og om man vil køre det over localhost, skal man ændre `Caddyfile`. Når det er installeret, kan man køre
`(sudo) caddy run`

Man kan med fordel se på `screen`, når man ssh'er ind på serveren.

## Ressourcer
https://topdatamat.dk/ordbog.thc
http://www.klid.dk/dansk/ordlister/ordliste.html
https://imada.sdu.dk/~chdj/ordbog.php
