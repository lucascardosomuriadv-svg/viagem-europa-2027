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
from dias import DIAS, FORA  # noqa: E402

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
    fora = {}
    for c, itens in FORA.items():
        fora[c] = []
        for ref, motivo in itens:
            try:
                fora[c].append({"id": resolve(lug[c], ref, f"fora {c}"), "motivo": motivo})
            except SystemExit as e:
                print("  aviso:", e)
    usados = {i for d in dias for b in d["blocos"] for i in b["ids"]}

    trens = json.load(open(PESQ / "trens.json", encoding="utf-8"))
    voos = None
    if (PESQ / "voos.json").exists():
        voos = json.load(open(PESQ / "voos.json", encoding="utf-8"))

    dados = {"cambio": CAMBIO, "cidades": CIDADES, "lugares": lug, "extras": extras, "dias": dias,
             "fora": fora, "usados": sorted(usados), "trens": trens, "voos": voos}
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text("// gerado por fonte/build.py — nao edite a mao\nwindow.GUIA = "
                     + json.dumps(dados, ensure_ascii=False) + ";\n", encoding="utf-8")
    tot = sum(len(v) for v in lug.values())
    print(f"ok: {len(dias)} dias, {tot} lugares, {len(usados)} citados no dia a dia, voos={'sim' if voos else 'ainda nao'}"
          f" -> {SAIDA.name} ({SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
