// Abas "Comprar" e "Cidades" do guia. Enxuto de propósito: uma linha por item,
// o número que importa em destaque, o detalhe só ao tocar.
// Usa G, HOSP, NOME, eur, brl, esc (definidos no index.html).

// ---------- custos ----------
const ATRACOES = [
  ["Madri","Palácio Real",18],["Madri","Prado (grátis 18h–20h)",0],["Madri","Trem ida e volta a Toledo",30],
  ["Roma","Coliseu + Fórum + Palatino",20],["Roma","Museus Vaticanos",25],["Roma","Cúpula de São Pedro",10],["Roma","Galleria Borghese",17],["Roma","Panteão",7],["Roma","Trevi (perto da fonte)",2],["Roma","Castel Sant'Angelo",16],
  ["Verona","Arena",12],["Verona","Casa di Giulietta",12],["Verona","Torre dei Lamberti",6],["Verona","Trem ida e volta a Veneza",26],
  ["Innsbruck","Hofburg",15],["Innsbruck","Nordkette",50.4],
  ["Viena","Schönbrunn",42],["Viena","Belvedere",23],["Viena","Kunsthistorisches",22],["Viena","Museu Sisi",20],["Viena","Torre da Stephansdom",8],["Viena","Patinação na Rathausplatz",10.5],
  ["Budapeste","Parlamento",35],["Budapeste","Banhos Széchenyi",37],
];
const VOOS_BRL = 2845 + 3449;
function custos(){
  let hosp = 0; HOSP.forEach(c => { const e = c.itens.filter(x => x.escolha && x.tipo==="airbnb"); if (e.length) hosp += Math.min(...e.map(x=>x.total)); });
  hosp += 150 * G.cambio; // taxa turística de Roma
  const trens = (159.80 + 125 + 124.50 + 80.60) * G.cambio;
  const atr = ATRACOES.reduce((s,a) => s + a[2], 0) * 5 * G.cambio;
  // bilhete mais barato em cada cidade + aeroportos sempre de táxi/Uber (Madri 4×€33, Roma €55, Budapeste ~€35)
  const loc = (Object.values(G.transporte||{}).reduce((s,t) => s + (t.recomendado?.total_5_eur || 0), 0) + 4*33 + 55 + 35) * G.cambio;
  const total = hosp + trens + atr + loc + VOOS_BRL;
  return {hosp, trens, atr, loc, voos:VOOS_BRL, total};
}

// ---------- o que comprar, e quando ----------
// [quando, rótulo curto da data, status, [[título, linha de baixo, preço, detalhe]]]
const COMPRAS = [
  ["Agora", "já", "ja", [
    ["Hospedagens", "com cancelamento grátis", "~R$ 16 mil", `Airbnb bom mais barato em cada parada, já com a taxa de Roma. <a href="hospedagens.html">Ver as opções</a>`],
    ["Trem Roma → Verona", "Italo 8956 · sex 26/02 · 08:20", "€159,80", "Tarifa Italo Friends: os 5 na mesma reserva. Troca com taxa até 72h antes; não reembolsa."],
    ["Alertas de preço dos voos", "Madri → Roma e Budapeste → Madri", "", "Iberia, em 2 reservas: 3 Basic + 2 Optimal (as 2 malas despachadas)."]]],
  ["15/10", "15 out", "br", [
    ["3 trens na Áustria e Hungria", "Verona → Innsbruck → Viena → Budapeste", "~€330", "Abrem quando o horário de 2027 entrar no sistema. Tarifa Sparschiene: a mais barata, e a primeira que acaba."]]],
  ["Até 15/12", "até 15 dez", "br", [
    ["Voos internos", "Iberia 08:45 · Iberia 11:10", "~R$ 6.300", "Janela mais barata: 15/10 a 29/12. Mala de mão para os 5 e 2 despachadas."]]],
  ["Dezembro", "dez", "br", [
    ["Museus Vaticanos", "ter 23/02 · primeiro horário", "€25/p", "Abrem ~2 meses antes. Só no site oficial."],
    ["Galleria Borghese", "qui 25/02 · 9h", "€17/p", "Reserva obrigatória."]]],
  ["~20/01", "20 jan", "br", [
    ["Audiência do Papa", "qua 24/02", "grátis", "Pedido ~1 mês antes; retirada na terça, 15h–19h."],
    ["Seguro viagem e ETIAS", "os 5", "€20/p", "ETIAS só se já estiver valendo."],
    ["Datas dos jogos de futebol", "Serie A e LaLiga", "", `Saem entre meados de janeiro e fevereiro. <a href="futebol.html">Jogos</a>`]]],
  ["23/01", "23 jan", "br", [
    ["Coliseu", "seg 22/02 · 8h30", "€20/p", "Vendas abrem 30 dias antes, às 5h de Brasília."]]],
  ["Fevereiro", "fev", "vi", [
    ["Parlamento, Giulietta e Széchenyi", "horário marcado", "", "1–2 semanas antes."],
    ["Restaurantes para 5", "8 reservas", "", "Emma, Taverna dei Quaranta, Il Grottino, Rugantino, Peroni, Al Pompiere, Stiftskeller, Landtmann."]]],
  ["Na viagem", "viagem", "vi", [
    ["Schönbrunn e Belvedere", "Viena", "", "Horário marcado, 1–3 dias antes."]]],
];

// ---------- voos e trens ----------
// [trecho, dia, como, horário, total, à venda?, detalhe]
const TRECHOS = [
  ["Madri → Roma", "dom 21/02", "Iberia", "08:45 → 11:10", "R$ 2.845", true, "Em 2 reservas: 3 Basic + 2 Optimal. A Air Europa das 12:40 sai uns R$ 700 mais barata (malas estimadas)."],
  ["Roma → Verona", "sex 26/02", "Italo 8956", "08:20 → 11:38", "€159,80", true, "Italo Friends. Plano B: Frecciarossa 8506, 08:50 → 12:08, €199,50."],
  ["Verona → Innsbruck", "dom 28/02", "Railjet 88", "09:01 → 12:32", "~€90–160", false, "Comparem ÖBB e Trenitalia, e olhem a 1ª classe: na referência saiu mais barata."],
  ["Innsbruck → Viena", "seg 01/03", "Railjet", "13:58 → 18:32", "~€125", false, "Ou 12:56 → 17:32. Evitem o das 12:42, que passa pela Alemanha (€753)."],
  ["Viena → Budapeste", "qui 04/03", "Railjet", "07:40 → 10:35", "~€81", false, "Confiram que termina em Budapest-Keleti."],
  ["Budapeste → Madri", "sáb 06/03", "Iberia", "11:10 → 14:30", "R$ 3.449", true, "Em 2 reservas: 3 Basic + 2 Optimal."],
];
const AEROPORTOS = [["Madri","táxi ~€33 por carro · Uber no estacionamento"],["Roma","táxi €55 fixo · peçam de 6–7 lugares"],["Budapeste","Bolt XL ou Főtaxi · ~€35"]];

function renderComprar(){
  const c = custos();
  const ja = COMPRAS.filter(g => g[2]==="ja").reduce((s,g)=>s+g[3].length, 0);
  const prox = COMPRAS.find(g => g[2]!=="ja");
  document.getElementById("c-kpi").innerHTML = `
    <div class="k t"><small>Total da viagem, para os 5</small><b>${brl(c.total).replace(/\.\d{3}$/, m => m)}</b><small>${brl(c.total/5)} por pessoa · sem comida</small></div>
    <div class="k"><small>Dá para comprar já</small><b>${ja} itens</b></div>
    <div class="k"><small>Próxima data</small><b>${prox[0]}</b></div>`;
  const ck = {ja:"✓", br:"!", vi:"•"};
  document.getElementById("c-proximas").innerHTML = COMPRAS.map(([q, curta, st, itens]) => `
    <div class="grupo ${st}"><b>${q}</b></div>
    <div class="lista">${itens.map(([t,s,p,d]) => `<details class="it"><summary><span class="ck ${st}">${ck[st]}</span><span class="tx"><b>${t}</b><small>${s}</small></span><span class="pr num">${p}</span></summary><p class="det">${d}</p></details>`).join("")}</div>`).join("");
  document.getElementById("c-trechos").innerHTML = `<div class="lista">${TRECHOS.map(([t,dia,como,h,tot,venda,d]) => `
      <details class="it"><summary><span class="ico">${/Iberia/.test(como)?"✈":"🚆"}</span><span class="tx"><b>${t}</b><small>${dia} · ${como} · ${h}</small></span><span class="pr num">${tot}<em class="${venda?"ok":"br"}">${venda?"à venda":"abre ~15/10"}</em></span></summary><p class="det">${d}</p></details>`).join("")}</div>
    <h3 class="sub-h">Aeroportos</h3><div class="lista">${AEROPORTOS.map(([c,t]) => `<div class="it simples"><span class="tx"><b>${c}</b><small>${t}</small></span></div>`).join("")}</div>`;
  const linhas = [["Hospedagem","18 noites, Airbnb bom mais barato",c.hosp],["Voos internos","com as bagagens",c.voos],["Trens","4 trechos",c.trens],["Ingressos","todos os da lista",c.atr],["Metrô, ônibus e táxis","inclui aeroportos",c.loc]];
  document.getElementById("c-custos").innerHTML = `<div class="lista">${linhas.map(([n,s,v]) => `<div class="it simples"><span class="tx"><b>${n}</b><small>${s}</small></span><span class="pr num">${brl(v)}</span></div>`).join("")}</div>
    <details class="cartao" style="margin-top:10px"><summary style="cursor:pointer;font-weight:600">Ingressos, por pessoa</summary><div class="lista-orc num">${ATRACOES.map(([cid,n,v]) => `<div class="linha-orc"><span class="n">${n} <span class="fraco">· ${cid}</span></span><span>${v?eur(v):"grátis"}</span></div>`).join("")}</div></details>`;
  document.querySelectorAll("#c-seg button").forEach(b => b.onclick = () => {
    document.querySelectorAll("#c-seg button").forEach(x => x.classList.toggle("on", x===b));
    ["proximas","trechos","custos"].forEach(p => document.getElementById("c-"+p).hidden = p !== b.dataset.p);
  });
}

// ---------- cidades ----------
const RESUMO = {madri:"Retiro, Prado, Palácio, Rastro", roma:"Coliseu, Vaticano, Trastevere", verona:"Arena e Veneza", innsbruck:"Alpes e Nordkette", viena:"Schönbrunn, Klimt, cafés", budapeste:"Parlamento e banhos"};
function renderCidades(){
  const n = {madri:0}; G.dias.forEach(d => n[d.cidade] = (n[d.cidade]||0) + 1);
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
