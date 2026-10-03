# -*- coding: utf-8 -*-
"""Gera `dados/guia.js` a partir das pesquisas + `dias.py`.

    python fonte/build.py

Falha (e diz onde) se um lugar citado no dia a dia nao existir na pesquisa, ou
se o pedaco do nome casar com mais de um lugar. E' o que impede o roteiro de
apontar para um restaurante que saiu da lista.
"""
import json, pathlib, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = pathlib.Path(__file__).parent
PESQ = AQUI / "pesquisa"
SAIDA = AQUI.parent / "dados" / "guia.js"
sys.path.insert(0, str(AQUI))
from dias import DIAS, FORA, DICAS  # noqa: E402

CAMBIO = 5.95
CIDADES = [("madri", "Madri"), ("roma", "Roma"), ("verona", "Verona"),
           ("innsbruck", "Innsbruck"), ("viena", "Viena"), ("budapeste", "Budapeste")]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").lower()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", sem_acento(s)).strip("-")[:48]


def item(cidade, tipo, d, origem):
    return {
        "id": f"{cidade}-{slug(d.get('nome'))}", "cidade": cidade, "tipo": tipo, "nome": d.get("nome"),
        "categoria": d.get("tipo") or "", "bairro": d.get("bairro") or "", "endereco": d.get("endereco") or "",
        "lat": d.get("lat"), "lng": d.get("lng"), "pedir": d.get("pedir") or "",
        "preco": d.get("preco_pp_eur") or d.get("preco_eur") or "", "horario": d.get("horario") or "",
        "fecha": d.get("fecha_em") or "", "reserva": d.get("reserva") or "", "dica": d.get("dica") or "",
        "tempo": d.get("tempo_visita") or "", "confianca": d.get("confianca") or "", "origem": origem,
        "fonte": d.get("fonte") or "",
    }


def lugares():
    rm = json.load(open(PESQ / "roma-madri.json", encoding="utf-8"))
    oc = json.load(open(PESQ / "outras-cidades.json", encoding="utf-8"))
    nome_cid = {"Roma": "roma", "Madri": "madri"}
    out = {k: [] for k, _ in CIDADES}
    for a in rm["atracoes"]:
        out[nome_cid[a["cidade"]]].append(item(nome_cid[a["cidade"]], "ver", a, "pesquisa"))
    for l in rm["lugares"]:
        # o que a pesquisa marcou como "atracao (ver 'atracoes')" ja esta la
        if "(ver" in (l.get("tipo") or ""):
            continue
        c = nome_cid[l["cidade"]]
        origem = {"lista": "sua lista", "mapa": "seu mapa"}.get(l.get("origem"), "pesquisa")
        tipo = "ver" if l.get("nome") in ("Trastevere", "Campo de' Fiori", "El Rastro") else "comer"
        if tipo == "ver" and any(x["nome"] == l["nome"] for x in out[c]):
            continue
        out[c].append(item(c, tipo, l, origem))
    mapa = {"Verona": "verona", "Innsbruck": "innsbruck", "Viena": "viena", "Budapeste": "budapeste"}
    extras = {}
    for cd in oc["cidades"]:
        c = mapa[cd["cidade"]]
        for a in cd["atracoes"]:
            out[c].append(item(c, "ver", a, "sugestão"))
        for l in cd["comer"]:
            out[c].append(item(c, "comer", l, "sugestão"))
        extras[c] = {"transporte": cd.get("transporte", []), "observacoes": cd.get("observacoes", [])}
    # A LISTA DE VIENA DO LUCAS: o que ja existia na pesquisa so ganha o selo
    # "sua lista"; o que e' novo entra como item proprio.
    vl = PESQ / "viena-lista.json"
    if vl.exists():
        ja = {"Stephansplatz": "Catedral de Santo Estêvão", "Hofburg:": "Museu Sisi", "Demel": "Demel",
              "Palácio de Schönbrunn": "Schönbrunn", "Belvedere": "Belvedere"}
        for l in json.load(open(vl, encoding="utf-8"))["lugares"]:
            chave = next((k for k in ja if l["nome"].startswith(k)), None)
            if chave:
                for x in out["viena"]:
                    if ja[chave] in x["nome"]: x["origem"] = "sua lista"
                continue
            out["viena"].append(item("viena", l["tipo"], l, "sua lista"))
    # MAIS RESTAURANTES EM MADRI (pesquisa de 30/09/2026), cada um com o seu
    # "slot" — o momento do roteiro em que ele cabe
    mr = PESQ / "madri-restaurantes.json"
    if mr.exists():
        for l in json.load(open(mr, encoding="utf-8"))["lugares"]:
            l = {**l, "pedir": l.get("o_que_pedir") or l.get("pedir")}
            it = item("madri", "comer", l, "sugestão")
            it["slot"] = l.get("slot")
            out["madri"].append(it)
    # MATCHA DA CAMILA: entram nos lugares de Madri e no dia sugerido
    mj = PESQ / "matcha.json"
    if mj.exists():
        for l in json.load(open(mj, encoding="utf-8"))["lugares"]:
            it = item("madri", "comer" if l.get("categoria") != "extra" else "ver", l, "lista da Camila")
            it.update(matcha="extra" if l.get("categoria") == "extra" else True, dia=l.get("dia_sugerido"),
                      porque=l.get("por_que") or "", instagram=l.get("instagram") or "")
            out["madri"].append(it)
    # ids unicos
    for c, l in out.items():
        vistos = {}
        for x in l:
            n = vistos.get(x["id"], 0)
            vistos[x["id"]] = n + 1
            if n:
                x["id"] += f"-{n+1}"
    return out, extras


def resolve(lista, ref, onde):
    r = sem_acento(ref)
    exatos = [x for x in lista if sem_acento(x["nome"]) == r]
    achados = exatos or [x for x in lista if r in sem_acento(x["nome"])]
    if len(achados) != 1:
        nomes = [x["nome"] for x in achados] or ["(nenhum)"]
        raise SystemExit(f"ERRO {onde}: '{ref}' casou com {len(achados)}: {nomes}")
    return achados[0]["id"]


def main():
    lug, extras = lugares()
    dias, erros = [], []
    for d in DIAS:
        blocos = []
        for quando, texto, refs in d["blocos"]:
            ids = []
            for r in refs:
                # dia de deslocamento: o lugar pode ser da cidade de onde se sai
                try:
                    ids.append(resolve(lug[d["cidade"]], r, f"{d['data']} {quando}"))
                except SystemExit as e:
                    todos = [x for v in lug.values() for x in v]
                    try:
                        ids.append(resolve(todos, r, f"{d['data']} {quando} (todas as cidades)"))
                    except SystemExit:
                        erros.append(str(e))
            blocos.append({"quando": quando, "texto": texto, "ids": ids})
        dias.append({**{k: v for k, v in d.items() if k != "blocos"}, "blocos": blocos})
    if erros:
        raise SystemExit("\n".join(erros))
    # bloco "Matcha da Camila" no dia sugerido de cada lugar
    por_dia = {}
    for x in lug["madri"]:
        if x.get("matcha") and x.get("dia"):
            por_dia.setdefault(x["dia"], []).append(x)
    for d in dias:
        l = por_dia.get(d["data"])
        if not l:
            continue
        nomes = [x for x in l if x["matcha"] is True]
        extra = [x for x in l if x["matcha"] == "extra"]
        if nomes:
            d["blocos"].append({"quando": "Matcha da Camila", "ids": [x["id"] for x in nomes],
                "texto": "Perto do caminho de hoje. " + '<a href="matcha.html">Todos os matchas</a>'})
        if extra:
            d["blocos"].append({"quando": "Extra", "ids": [x["id"] for x in extra],
                "texto": "Cabine de fotos de €5, perto do caminho de hoje."})
    # "Mais opções": os restaurantes novos de Madri entram logo DEPOIS do bloco
    # do mesmo momento (almoço depois do almoço), não no fim do dia
    SLOTS = {"chegada": ("Abertos depois da meia-noite", "Se bater fome"), "almoco": ("Mais opções de almoço", "Almoço"),
             "jantar": ("Mais opções de jantar", "Noite"), "lanche": ("Lanche antes do aeroporto", "Tarde")}
    grupos = {}
    for x in lug["madri"]:
        if x.get("slot"):
            grupos.setdefault(x["slot"], []).append(x)
    for slot, l in grupos.items():
        tipo, dm_ = slot.split("-")
        data = f"2027-{dm_[3:5]}-{dm_[0:2]}"
        rotulo, depois = SLOTS[tipo]
        d = next((d for d in dias if d["data"] == data), None)
        if not d:
            print("  aviso: slot sem dia:", slot); continue
        curto = lambda s: (s or "").split(";")[0].split(",")[0][:55]
        bloco = {"quando": rotulo, "ids": [x["id"] for x in l],
                 "texto": "; ".join(f"<b>{x['nome'].split(' (')[0]}</b>" + (f": {curto(x['pedir'])}" if x["pedir"] else "") for x in l) + "."}
        pos = next((i for i, b in enumerate(d["blocos"]) if b["quando"].startswith(depois)), None)
        if pos is None and tipo == "almoco":
            pos = next((i for i, b in enumerate(d["blocos"]) if b["quando"] == "Manhã"), None)
        d["blocos"].insert(pos + 1 if pos is not None else len(d["blocos"]), bloco)

    futebol = json.load(open(PESQ / "futebol.json", encoding="utf-8")) if (PESQ / "futebol.json").exists() else None
    # posts de referência (TikTok etc.) por cidade: entram incorporados, nunca copiados
    refs = json.load(open(PESQ / "referencias.json", encoding="utf-8")) if (PESQ / "referencias.json").exists() else {}

    transporte = {}
    tj = PESQ / "transporte.json"
    if tj.exists():
        transporte = {c["chave"]: c for c in json.load(open(tj, encoding="utf-8"))["cidades"]}

    fora = {}
    for c, itens in FORA.items():
        fora[c] = []
        for ref, motivo in itens:
            try:
                fora[c].append({"id": resolve(lug[c], ref, f"fora {c}"), "motivo": motivo})
            except SystemExit as e:
                print("  aviso:", e)
    usados = {i for d in dias for b in d["blocos"] for i in b["ids"]}

    # fotos: o prefixo mais longo do id que estiver em fotos.ARTIGO
    from fotos import ARTIGO
    fotos = json.load(open(PESQ / "fotos.json", encoding="utf-8")) if (PESQ / "fotos.json").exists() else {}
    com_foto = 0
    for l in lug.values():
        for x in l:
            pref = max((k for k in ARTIGO if x["id"].startswith(k)), key=len, default=None)
            f = fotos.get(ARTIGO[pref]) if pref else None
            if f:
                x["foto"] = f; com_foto += 1

    # METRO: estacoes do OpenStreetMap; varios nos por estacao viram um ponto so
    import math
    def hav(a, b):
        la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
        h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
        return 2*6371000*math.asin(math.sqrt(h))
    estacoes = {}
    for c in ("madri", "roma", "viena", "budapeste"):
        arq = PESQ / f"metro-{c}.json"
        if not arq.exists(): continue
        grupos = {}
        for e in json.load(open(arq, encoding="utf-8"))["elements"]:
            n = e.get("tags", {}).get("name")
            if n: grupos.setdefault(n, []).append((e["lat"], e["lon"]))
        estacoes[c] = [[n, round(sum(p[0] for p in ps)/len(ps), 6), round(sum(p[1] for p in ps)/len(ps), 6)] for n, ps in grupos.items()]
    # Verona e Innsbruck nao tem metro: a referencia e' a estacao de trem
    estacoes["verona"] = [["Verona Porta Nuova (trem)", 45.4290, 10.9828]]
    estacoes["innsbruck"] = [["Innsbruck Hauptbahnhof (trem)", 47.2633, 11.4008]]
    for c, l in lug.items():
        for x in l:
            if x.get("lat") and estacoes.get(c) and c not in ("verona", "innsbruck"):
                d, nome = min((hav((x["lat"], x["lng"]), (e[1], e[2])), e[0]) for e in estacoes[c])
                minutos = round(d * 1.3 / 80)
                if minutos <= 15:
                    x["metro"] = {"nome": nome, "min": max(1, minutos)}

    trens = json.load(open(PESQ / "trens.json", encoding="utf-8"))
    voos = None
    if (PESQ / "voos.json").exists():
        voos = json.load(open(PESQ / "voos.json", encoding="utf-8"))

    dados = {"cambio": CAMBIO, "cidades": CIDADES, "lugares": lug, "extras": extras, "dias": dias,
             "fora": fora, "usados": sorted(usados), "estacoes": estacoes, "dicas": DICAS, "transporte": transporte, "futebol": futebol, "refs": refs, "trens": trens, "voos": voos}
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text("// gerado por fonte/build.py — nao edite a mao\nwindow.GUIA = "
                     + json.dumps(dados, ensure_ascii=False) + ";\n", encoding="utf-8")
    tot = sum(len(v) for v in lug.values())
    print(f"ok: {len(dias)} dias, {tot} lugares, {com_foto} com foto, {len(usados)} citados no dia a dia, voos={'sim' if voos else 'ainda nao'}"
          f" -> {SAIDA.name} ({SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
