// Abas "Comprar" e "Cidades" do guia. Enxuto de propósito: uma linha por item,
// o que importa em destaque, o detalhe só ao tocar.
// Usa G, NOME, dm, esc (definidos no index.html).

// ---------- o que falta comprar ----------
// Sem total de viagem de propósito: somar tantas estimativas daria um número
// aproximado demais. Aqui é só o que falta comprar ou reservar, e quando.
const HOJE = new Date(new Date().toISOString().slice(0,10)+"T12:00:00Z");
const faltam = iso => Math.round((new Date(iso+"T12:00:00Z") - HOJE) / 86400000);
const quandoAbre = iso => { const n = faltam(iso); return n <= 0 ? "já abriu" : n === 1 ? "abre amanhã" : `abre em ${n} dias`; };

// AGORA: dá para comprar hoje. [título, linha de baixo, preço, detalhe]
const AGORA = [
  ["Hospedagens", "com cancelamento grátis", "", `Opções pesquisadas em cada cidade. <a href="hospedagens.html">Ver</a>`],
  ["Trem Roma → Verona", "Italo 8956 · sex 26/02 · 08:20", "€159,80", "Tarifa Italo Friends, os 5 na mesma reserva."],
  ["Voos Madri → Roma e Budapeste → Madri", "Iberia, em 2 reservas", "", "3 Basic + 2 Optimal (as 2 malas despachadas). Janela mais barata até ~15/12."],
  ["Seguro viagem", "os 5, Schengen", "", "Cobertura mínima de €30 mil."],
];
// INGRESSOS com reserva. [atração, cidade, dia no roteiro, abre (ISO ou null = já dá), quando abre, preço por pessoa]
const INGRESSOS = [
  ["Palácio Real", "Madri", "sáb 20/02", null, "online", "€18"],
  ["Museus Vaticanos", "Roma", "ter 23/02", "2026-12-23", "~2 meses antes", "€25"],
  ["Galleria Borghese", "Roma", "qui 25/02 · 9h", "2026-12-25", "reserva obrigatória", "€17"],
  ["Coliseu", "Roma", "seg 22/02 · 8h30", "2027-01-23", "23/01, às 5h de Brasília", "€20"],
  ["Audiência do Papa", "Roma", "qua 24/02", "2027-01-24", "pedir ~1 mês antes", "grátis"],
  ["Casa di Giulietta", "Verona", "sex 26/02", "2027-02-12", "horário marcado", "€12"],
  ["Parlamento", "Budapeste", "sex 05/03", "2027-02-19", "1–2 semanas antes", "€35"],
  ["Banhos Széchenyi", "Budapeste", "sex 05/03", "2027-02-19", "online, evita fila", "€37"],
  ["Schönbrunn", "Viena", "ter 02/03", "2027-02-27", "1–3 dias antes", "€42"],
  ["Belvedere", "Viena", "qua 03/03", "2027-02-28", "1–3 dias antes", "€23"],
  ["Museu Sisi", "Viena", "qua 03/03", "2027-02-28", "horário marcado", "€20"],
];
const NA_HORA = [["Panteão","€7"],["Trevi (perto da fonte)","€2"],["Arena di Verona","€12"],["Nordkette","€50"],["Prado, das 18h às 20h","grátis"]];
const RESTAURANTES = ["Emma · dom 21/02","Taverna dei Quaranta e Il Grottino · seg 22/02","Rugantino · qua 24/02","Peroni · qui 25/02","Al Pompiere · sáb 27/02","Stiftskeller · dom 28/02","Landtmann · ter 02/03"];

// VOOS E TRENS. [trecho, dia, como, horário, preço, à venda?, abre (ISO), detalhe]
const TRECHOS = [
  ["Madri → Roma", "dom 21/02", "Iberia", "08:45 → 11:10", "R$ 2.845", true, null, "3 Basic + 2 Optimal. A Air Europa das 12:40 sai uns R$ 700 mais barata."],
  ["Roma → Verona", "sex 26/02", "Italo 8956", "08:20 → 11:38", "€159,80", true, null, "Plano B: Frecciarossa 8506, 08:50 → 12:08, €199,50."],
  ["Verona → Innsbruck", "dom 28/02", "Railjet 88", "09:01 → 12:32", "~€90–160", false, "2026-10-15", "Comparem ÖBB e Trenitalia."],
  ["Innsbruck → Viena", "seg 01/03", "Railjet", "13:58 → 18:32", "~€125", false, "2026-10-15", "Ou 12:56 → 17:32. Evitem o das 12:42 (via Alemanha)."],
  ["Viena → Budapeste", "qui 04/03", "Railjet", "07:40 → 10:35", "~€81", false, "2026-10-15", "Confiram que termina em Budapest-Keleti."],
  ["Budapeste → Madri", "sáb 06/03", "Iberia", "11:10 → 14:30", "R$ 3.449", true, null, "3 Basic + 2 Optimal."],
];

function renderComprar(){
  const datas = [...INGRESSOS.filter(i => i[3]).map(i => i[3]), ...TRECHOS.filter(t => !t[5]).map(t => t[6])].filter(d => faltam(d) > 0).sort();
  const prox = datas[0];
  const jaDa = AGORA.length + INGRESSOS.filter(i => !i[3] || faltam(i[3]) <= 0).length;
  const oQue = prox ? [...INGRESSOS.filter(i=>i[3]===prox).map(i=>i[0]), ...TRECHOS.filter(t=>t[6]===prox).map(t=>t[0])] : [];
  document.getElementById("c-kpi").innerHTML = `
    <div class="k"><small>Dá para comprar já</small><b>${jaDa} itens</b></div>
    <div class="k"><small>Ingressos com reserva</small><b>${INGRESSOS.length}</b></div>
    <div class="k t"><small>Próxima venda que abre</small><b>${prox ? `${dm(prox)} · ${quandoAbre(prox).replace("abre ","")}` : "tudo aberto"}</b><small>${oQue.length > 2 ? oQue.length + " trens" : oQue.join(", ")}</small></div>`;
  document.getElementById("c-agora").innerHTML = `<div class="lista">${AGORA.map(([t,s,pr,d]) => `<details class="it"><summary><span class="ck ja">✓</span><span class="tx"><b>${t}</b><small>${s}</small></span><span class="pr num">${pr}</span></summary><p class="det">${d}</p></details>`).join("")}</div>`;
  const ing = [...INGRESSOS].sort((a,b) => (a[3]||"0").localeCompare(b[3]||"0"));
  document.getElementById("c-ingressos").innerHTML = `<div class="lista">${ing.map(([n,cid,dia,abre,como,pr]) => { const aberto = !abre || faltam(abre) <= 0;
      return `<div class="it linha"><span class="ck ${aberto?"ja":"br"}">${aberto?"✓":"!"}</span><span class="tx"><b>${n}</b><small>${cid} · ${dia} · ${como}</small></span><span class="pr num">${pr}<em class="${aberto?"ok":"br"}">${aberto?"já dá":quandoAbre(abre)}</em></span></div>`; }).join("")}</div>
    <h3 class="sub-h">Na hora, sem reservar</h3>
    <div class="lista">${NA_HORA.map(([n,pr]) => `<div class="it simples"><span class="tx"><b>${n}</b></span><span class="pr num">${pr}</span></div>`).join("")}</div>
    <h3 class="sub-h">Restaurantes para reservar (1–2 semanas antes)</h3>
    <div class="lista">${RESTAURANTES.map(r => `<div class="it simples"><span class="tx"><b>${r}</b></span></div>`).join("")}</div>`;
  document.getElementById("c-trechos").innerHTML = `<div class="lista">${TRECHOS.map(([t,dia,como,h,pr,venda,abre,d]) => `
      <details class="it"><summary><span class="ico">${/Iberia/.test(como)?"✈":"🚆"}</span><span class="tx"><b>${t}</b><small>${dia} · ${como} · ${h}</small></span><span class="pr num">${pr}<em class="${venda?"ok":"br"}">${venda?"à venda":quandoAbre(abre)}</em></span></summary><p class="det">${d}</p></details>`).join("")}</div>
    <h3 class="sub-h">Aeroportos (sempre táxi ou Uber)</h3><div class="lista">${[["Madri","táxi ~€33 por carro · Uber no estacionamento"],["Roma","táxi €55 fixo · peçam de 6–7 lugares"],["Budapeste","Bolt XL ou Főtaxi · ~€35"]].map(([c,t]) => `<div class="it simples"><span class="tx"><b>${c}</b><small>${t}</small></span></div>`).join("")}</div>`;
  document.querySelectorAll("#c-seg button").forEach(b => b.onclick = () => {
    document.querySelectorAll("#c-seg button").forEach(x => x.classList.toggle("on", x===b));
    ["agora","ingressos","trechos"].forEach(p => document.getElementById("c-"+p).hidden = p !== b.dataset.p);
  });
}

// ---------- cidades ----------
const RESUMO = {madri:"Retiro, Prado, Palácio, Rastro", roma:"Coliseu, Vaticano, Trastevere", verona:"Arena e Veneza", innsbruck:"Alpes e Nordkette", viena:"Schönbrunn, Klimt, cafés", budapeste:"Parlamento e banhos"};
function renderCidades(){
  const n = {}; G.dias.forEach(d => n[d.cidade] = (n[d.cidade]||0) + 1);
  document.getElementById("lista-cidades").innerHTML = G.cidades.map(([k,nome]) => {
    const l = G.lugares[k]; const capa = l.find(x => x.foto && x.tipo==="ver" && G.usados.includes(x.id)) || l.find(x=>x.foto);
    return `<a class="cidade-card" href="cidade.html?c=${k}" style="--cor:var(--${k})">${capa?`<div class="capa"><img src="${capa.foto.url}" alt="" loading="lazy"></div>`:`<div class="capa"></div>`}<b>${nome}</b><span>${RESUMO[k]} · ${n[k]||0} ${n[k]===1?"dia":"dias"}</span></a>`;
  }).join("") + [["hospedagens.html","Hospedagem","Airbnb e hotéis"],["matcha.html","Matcha da Camila","Madri"],["futebol.html","Futebol","jogos nas datas"]]
    .map(([h,t,s]) => `<a class="cidade-card extra" href="${h}"><b>${t}</b><span>${s}</span></a>`).join("");
  const CHECKS = [["Seguro viagem Schengen","mínimo €30 mil"],["ETIAS","se já estiver valendo"],["Passaporte","válido até junho/2027"],["Mesmo apartamento em Madri na ida e na volta","para guardar as malas"],["Check-in autônomo na chegada","pousamos às 22:35"],["eSIM europeu","vale nos 4 países"],["Roupa de frio de verdade","Innsbruck abaixo de zero"]];
  document.getElementById("checks").innerHTML = CHECKS.map(([t,s]) => `<li><b>${t}</b><span>${s}</span></li>`).join("");
}
renderComprar();
renderCidades();
