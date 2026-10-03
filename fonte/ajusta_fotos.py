# -*- coding: utf-8 -*-
"""Ajustes nas fotos das atrações depois da conferência no olho (03/10/2026).

    python fonte/atracoes.py      (busca tudo de novo)
    python fonte/ajusta_fotos.py  (reaplica estes ajustes)
    python fonte/build.py

A busca automática acerta quase sempre a foto principal; a segunda às vezes vem ruim
(pintura antiga, gravura, detalhe, foto escura, outro lugar). Aqui fica a lista do que foi
tirado ou trocado. Chave: nome da atração nova, ou começo do id do lugar antigo.
"""
import json, pathlib, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = pathlib.Path(__file__).parent
PESQ = AQUI / "pesquisa"
sys.path.insert(0, str(AQUI))
import atracoes

# segunda foto ruim: fica só a principal
SEM2 = {
 "Madrid Río", "Bate-volta Segóvia", "Terrazza del Pincio", "Museus Capitolinos", "Termas de Caracalla", "Gianicolo (mirante)", "Pirâmide de Céstio",
 "Largo di Torre Argentina", "Ilha Tiberina", "Fontana delle Tartarughe", "Cripta dos Capuchinhos", "Bate-volta Tivoli (Villa d'Este)", "Duomo de Verona",
 "Giardino Giusti", "Casa di Romeo", "Bate-volta Pádua (Capela Scrovegni)", "Bate-volta Vicenza", "Patscherkofel", "Bate-volta Hall in Tirol",
 "Bate-volta Seefeld", "Secession", "Mozarthaus", "Haus der Musik", "Kahlenberg (mirante)", "Via Mazzini", "Bate-volta Bratislava", "Ponte das Correntes",
 "Museu de Etnografia", "Várkert Bazár", "Estação Nyugati", "Mirante Erzsébet", "Bate-volta Szentendre",
 "madri-bate-volta-a-toledo", "madri-gran-via", "roma-piazza-di-spagna", "verona-arena", "verona-bate-volta-veneza", "innsbruck-altstadt", "viena-hofburg",
 "viena-wiener-staatsoper", "viena-visita-guiada", "budapeste-banhos-rudas", "budapeste-cruzeiro-noturno", "budapeste-praca-dos-herois", "madri-plaza-de-espana",
 "madri-edificio-metropolis", "madri-mirante-do-hotel-riu", "madri-malasana", "madri-cava-baja", "madri-casa-del-libro", "madri-museo-reina-sofia",
 "madri-alcala-de-henares",
}
# a principal já é uma foto de dentro: sem etiqueta "por fora / por dentro"
SEMROT = {"Museo Arqueológico Nacional", "Estação fantasma de Chamberí", "Galleria Sciarra", "Cripta dos Capuchinhos", "Bate-volta Pádua (Capela Scrovegni)", "roma-museus-vaticanos"}
# principal errada ou fraca: busca outra
TROCA1 = {
 "Centrale Montemartini": "Centrale Montemartini", "Stadtpark (Strauss dourado)": "Johann Strauss Denkmal Stadtpark Wien", "Via Mazzini": "Via Mazzini Verona",
 "Jardim das Laranjeiras (Giardino degli Aranci)": "Giardino degli Aranci Roma", "Praça da Liberdade": "Szabadság tér Budapest", "Gozsdu Udvar": "Gozsdu udvar Budapest",
 "verona-casa-di-giulietta": "Casa di Giulietta Verona balcone",
}
# principal cuja miniatura não baixou na conferência: se o endereço não responder, busca outra
CONFERE1 = {"Donauturm": "Donauturm Wien", "Avenida Andrássy": "Andrássy út Budapest", "Ilha Margarida": "Margitsziget Budapest", "Hospital na Rocha": "Sziklakórház Budapest"}
# segunda que não mostra o que interessa: busca outra (termo, etiqueta)
TROCA2 = {
 "Biblioteca Nacional (Prunksaal)": ("Prunksaal Nationalbibliothek Wien", "por dentro"), "Círculo de Bellas Artes (terraço)": ("Círculo de Bellas Artes azotea", ""),
 "Estação de Atocha (jardim tropical)": ("Atocha jardín tropical", "por dentro"), "Biblioteca Szabó Ervin": ("Szabó Ervin Könyvtár olvasóterem", "por dentro"),
 "madri-palacio-real": ("Palacio Real de Madrid Salón del Trono", "por dentro"), "roma-galleria-borghese": ("Galleria Borghese interior", "por dentro"),
 "viena-palacio-de-schonbrunn": ("Schönbrunn Große Galerie", "por dentro"), "viena-catedral-de-santo-estevao": ("Stephansdom Wien Innenraum", "por dentro"),
 "viena-kunsthistorisches": ("Kunsthistorisches Museum Wien Stiegenhaus", "por dentro"), "budapeste-banhos-szechenyi": ("Széchenyi fürdő medence", ""),
}


def responde(url):
    try:
        req = urllib.request.Request(url, headers=atracoes.UA, method="HEAD")
        return urllib.request.urlopen(req, timeout=30).status == 200
    except Exception:
        return False


def ajusta(chave, fotos, log):
    if chave in TROCA1 or (chave in CONFERE1 and not responde(fotos[0]["url"])):
        termo = TROCA1.get(chave) or CONFERE1[chave]
        f = atracoes.busca(termo, fora=tuple(x["url"] for x in fotos)); time.sleep(0.7)
        if f: fotos[0] = dict(f, rot=fotos[0].get("rot", "")); log.append((chave, "principal", f["url"]))
        else: print("  sem resultado para a principal de", chave)
    if chave in SEM2: del fotos[1:]
    if chave in TROCA2:
        termo, rot = TROCA2[chave]
        f = atracoes.busca(termo, fora=tuple(x["url"] for x in fotos)); time.sleep(0.7)
        if f:
            del fotos[1:]; fotos.append(dict(f, rot=rot)); log.append((chave, "segunda", f["url"]))
        else: print("  sem resultado para a segunda de", chave)
    if chave in SEMROT or len(fotos) == 1 or not any(x.get("rot") == "por dentro" for x in fotos[1:]):
        for x in fotos: x["rot"] = ""
    elif fotos[1].get("rot") == "por dentro": fotos[0]["rot"] = "por fora"
    return fotos


def main():
    log = []
    p = PESQ / "atracoes-extra.json"; novas = json.load(open(p, encoding="utf-8"))
    for l in novas.values():
        for a in l: a["fotos"] = ajusta(a["nome"], a["fotos"], log)
    p.write_text(json.dumps(novas, ensure_ascii=False, indent=1), encoding="utf-8")
    p = PESQ / "fotos-avulsas.json"; velhas = json.load(open(p, encoding="utf-8"))
    for k in velhas: velhas[k] = ajusta(k, velhas[k], log)
    # fotos escolhidas à mão entre candidatas (valem sobre a busca): pesquisa/fotos-escolhidas.json
    esc = json.load(open(PESQ / "fotos-escolhidas.json", encoding="utf-8")) if (PESQ / "fotos-escolhidas.json").exists() else {}
    for chave, fotos in esc.items():
        if chave in velhas: velhas[chave] = fotos
        for l in novas.values():
            for a in l:
                if a["nome"] == chave: a["fotos"] = fotos
    (PESQ / "atracoes-extra.json").write_text(json.dumps(novas, ensure_ascii=False, indent=1), encoding="utf-8")
    p.write_text(json.dumps(velhas, ensure_ascii=False, indent=1), encoding="utf-8")
    (PESQ / "fotos-trocadas.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(log), "fotos trocadas:"); [print("  ", c, "|", q) for c, q, _ in log]


if __name__ == "__main__":
    main()
