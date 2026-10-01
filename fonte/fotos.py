# -*- coding: utf-8 -*-
"""Busca a foto de cada ponto turistico no Wikimedia Commons, com credito.

    python fonte/fotos.py

Por que Wikimedia: licenca livre (CC / dominio publico), autor e licenca vem
junto pela API, e o arquivo e' servido de upload.wikimedia.org — nada de foto
de banco de imagem ou de site de terceiro.

O mapa abaixo liga o comeco do `id` do lugar ao TITULO do artigo na Wikipedia
em ingles (o mais completo em foto). Itens que nao sao lugar (eventos,
VeronaCard) ficam sem foto de proposito. Grava `pesquisa/fotos.json`.
"""
import json, pathlib, sys, time, urllib.error, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = pathlib.Path(__file__).parent
SAIDA = AQUI / "pesquisa" / "fotos.json"
UA = {"User-Agent": "guia-viagem-europa-2027/1.0 (uso pessoal; github.com/lucascardosomuriadv-svg)"}

ARTIGO = {
  "madri-museo-del-prado": "Museo del Prado",
  "madri-palacio-real": "Royal Palace of Madrid", "madri-catedral-de-la-almudena": "Almudena Cathedral",
  "madri-jardines-de-sabatini": "Sabatini Gardens", "madri-templo-de-debod": "Temple of Debod",
  "madri-parque-del-retiro": "Buen Retiro Park", "madri-puerta-de-alcala": "Puerta de Alcalá",
  "madri-fuente-de-cibeles": "Plaza de Cibeles", "madri-gran-via": "Gran Vía (Madrid)",
  "madri-puerta-del-sol": "Plaza Mayor, Madrid", "madri-mercado-de-san-miguel": "Mercado de San Miguel",
  "madri-el-rastro": "El Rastro", "madri-tour-do-estadio": "Santiago Bernabéu Stadium",
  "madri-bate-volta-a-toledo": "Toledo, Spain",
  "roma-coliseu": "Colosseum", "roma-museus-vaticanos": "Sistine Chapel", "roma-basilica-de-sao-pedro": "St. Peter's Basilica",
  "roma-audiencia-geral": "St. Peter's Square", "roma-panteao": "Pantheon, Rome", "roma-fontana-di-trevi": "Trevi Fountain",
  "roma-galleria-borghese": "Villa Borghese", "roma-castel-sant-angelo": "Castel Sant'Angelo",
  "roma-piazza-di-spagna": "Spanish Steps", "roma-piazza-navona": "Piazza Navona", "roma-vittoriano": "Victor Emmanuel II Monument",
  "roma-circo-massimo": "Circus Maximus", "roma-porta-maggiore": "Porta Maggiore", "roma-stadio-olimpico": "Stadio Olimpico",
  "roma-trastevere": "Trastevere", "roma-campo-de-fiori": "Campo de' Fiori",
  "verona-arena": "Verona Arena", "verona-torre-dei-lamberti": "Torre dei Lamberti",
  "verona-museo-di-castelvecchio": "Castelvecchio, Verona", "verona-castel-san-pietro": "Ponte Pietra",
  "verona-piazza-delle-erbe": "Piazza delle Erbe, Verona", "verona-basilica-di-san-zeno": "Basilica of San Zeno",
  "verona-bate-volta-veneza": "Grand Canal (Venice)", "verona-bate-volta-sirmione": "Sirmione",
  "innsbruck-nordkette": "Nordkette", "innsbruck-goldenes-dachl": "Goldenes Dachl", "innsbruck-hofburg-innsbruck": "Hofburg, Innsbruck",
  "innsbruck-bergisel": "Bergisel Ski Jump", "innsbruck-maria-theresien": "Annasäule",
  "innsbruck-altstadt": "Innsbruck", "innsbruck-hofkirche": "Hofkirche, Innsbruck", "innsbruck-swarovski": "Swarovski Kristallwelten",
  "viena-palacio-de-schonbrunn": "Schönbrunn Palace", "viena-belvedere": "Belvedere, Vienna", "viena-hofburg": "Hofburg",
  "viena-catedral-de-santo-estevao": "St. Stephen's Cathedral, Vienna", "viena-kunsthistorisches": "Maria-Theresien-Platz",
  "viena-naschmarkt": "Naschmarkt", "viena-wiener-staatsoper": "Vienna State Opera", "viena-visita-guiada-a-staatsoper": "Vienna State Opera",
  "viena-prater": "Wiener Riesenrad", "viena-albertina": "Albertina", "viena-karlskirche": "Karlskirche", "viena-museumsquartier": "Museumsquartier",
  "budapeste-parlamento": "Hungarian Parliament Building", "budapeste-castelo-de-buda": "Buda Castle",
  "budapeste-bastiao-dos-pescadores": "Fisherman's Bastion", "budapeste-igreja-de-matias": "Matthias Church",
  "budapeste-basilica-de-santo-estevao": "St. Stephen's Basilica", "budapeste-banhos-szechenyi": "Széchenyi thermal bath",
  "budapeste-banhos-rudas": "Rudas Baths", "budapeste-mercado-central": "Great Market Hall (Budapest)",
  "budapeste-cruzeiro-noturno": "Széchenyi Chain Bridge", "budapeste-szimpla-kert": "Szimpla Kert",
  "budapeste-sapatos-na-margem": "Shoes on the Danube Bank", "budapeste-praca-dos-herois": "Heroes' Square (Budapest)",
  "budapeste-sinagoga-da-rua-dohany": "Dohány Street Synagogue",
}
# acrescimos que vem de outras pesquisas (lista de Viena do Lucas etc.)
EXTRA = AQUI / "pesquisa" / "fotos-extra.json"
if EXTRA.exists():
    ARTIGO.update(json.load(open(EXTRA, encoding="utf-8")))


def api(base, **p):
    p.update(format="json", formatversion="2")
    url = base + "?" + urllib.parse.urlencode(p)
    for tentativa in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            espera = int(e.headers.get("Retry-After") or 0) or 5 * (tentativa + 1)
            print(f"  429, esperando {espera}s"); time.sleep(espera)
    raise SystemExit("Wikimedia continua limitando; rode de novo depois")


def limpa(html):
    import re
    return re.sub(r"<[^>]+>", "", html or "").strip()


def main():
    feitos = json.load(open(SAIDA, encoding="utf-8")) if SAIDA.exists() else {}
    titulos = sorted(set(ARTIGO.values()) - set(feitos))
    arquivo_de = {}
    for i in range(0, len(titulos), 20):
        lote = titulos[i:i+20]
        q = api("https://en.wikipedia.org/w/api.php", action="query", prop="pageimages", piprop="name",
                titles="|".join(lote), redirects=1)["query"]
        alias = {n["from"]: n["to"] for n in q.get("normalized", [])}
        alias.update({n["from"]: n["to"] for n in q.get("redirects", [])})
        por = {pg["title"]: pg for pg in q["pages"]}
        for t in lote:
            alvo = alias.get(alias.get(t, t), alias.get(t, t))
            pg = por.get(alvo)
            if pg and "pageimage" in pg: arquivo_de[t] = pg["pageimage"]
            else: print("  sem foto:", t)
        time.sleep(1)
    arqs = sorted(set(arquivo_de.values()))
    meta = {}
    for i in range(0, len(arqs), 20):
        lote = arqs[i:i+20]
        q = api("https://commons.wikimedia.org/w/api.php", action="query", prop="imageinfo",
                iiprop="url|extmetadata", iiurlwidth="800", titles="|".join("File:" + a for a in lote))["query"]
        alias = {n["to"]: n["from"] for n in q.get("normalized", [])}
        for pg in q["pages"]:
            if "imageinfo" not in pg: continue
            ii = pg["imageinfo"][0]; md = ii.get("extmetadata", {})
            nome = pg["title"].removeprefix("File:").replace(" ", "_")
            meta[nome] = {"url": ii.get("thumburl") or ii["url"], "pagina": ii.get("descriptionurl"),
                          "autor": limpa(md.get("Artist", {}).get("value"))[:80] or "Wikimedia Commons",
                          "licenca": limpa(md.get("LicenseShortName", {}).get("value")) or "ver página"}
        time.sleep(1)
    for t, a in arquivo_de.items():
        m = meta.get(a.replace(" ", "_"))
        if m: feitos[t] = m
        else: print("  arquivo fora do Commons:", t, a)
    SAIDA.write_text(json.dumps(feitos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(feitos)} fotos em {SAIDA.name}")


if __name__ == "__main__":
    main()
