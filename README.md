# ChillAir d.o.o. — web stranica

Statična web stranica (HTML + CSS + malo JS-a), bez ovisnosti i bez kolačića. Fontovi su lokalno u `assets/fonts`.

## Uređivanje
Sadržaj i podaci firme nalaze se u `tools/build.py` (blok `FIRMA` na vrhu). Nakon izmjene:

```bash
python3 tools/build.py
```

Skripta ponovno generira sve `.html` datoteke, `sitemap.xml` i `robots.txt`.

### Za popuniti prije objave


- domena (`domena`) i poštanski broj (`grad`)

## Objava na GitHub Pages
Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)`.
Za vlastitu domenu dodajte datoteku `CNAME` s nazivom domene (npr. `chillair.hr`).

## Kontakt obrazac
Stranica nema poslužitelj, pa obrazac otvara e-mail program posjetitelja s pripremljenom porukom.
Za slanje izravno sa stranice može se spojiti servis poput Formspree ili Web3Forms.
