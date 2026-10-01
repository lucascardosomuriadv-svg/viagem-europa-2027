// Conteúdo do guia (compras, voos, trens, orçamento, cidades, checklist).
// Escrito à mão; o index.html (app) só fornece os contêineres e as funções G, eur, brl, NOME, COR.

// ---------- compras ----------
const COMPRAS = [
  ["Agora", "outubro/2026", [
    `<b>Hospedagens</b> com cancelamento grátis. <a href="hospedagens.html">Opções pesquisadas por cidade</a>.`,
    `<b>Trem Roma → Verona</b> (26/02): Italo 8956, tarifa Italo Friends, <b>€159,80 para os 5</b>, todos na mesma reserva. <a href="https://www.italotreno.com" target="_blank" rel="noopener">italotreno.com</a>`,
    `<b>Alertas de preço dos voos</b> Madri → Roma (21/02) e Budapeste → Madri (06/03). Recomendação: Iberia, em 2 reservas (3 Basic + 2 Optimal). <a href="#transporte">Detalhes</a>.`
  ]],
  ["~15/10/2026", "quando o horário 2027 entrar", [
    `<b>Trens da Áustria e da Hungria</b>: Verona → Innsbruck (28/02), Innsbruck → Viena (01/03), Viena → Budapeste (04/03). Tarifa Sparschiene, a mais barata, que acaba primeiro. Hoje o sistema só vende até 12/12/2026. <a href="https://www.oebb.at" target="_blank" rel="noopener">oebb.at</a>`
  ]],
  ["Até meados de dezembro", "janela barata: 15/10 a 29/12", [
    `<b>Comprar os voos internos</b>: Iberia 08:45 Madri → Roma e Iberia 11:10 Budapeste → Madri, ~R$ 6.300 para os 5 com bagagens.`
  ]],
  ["Dezembro/2026", "~2 meses antes", [
    `<b>Museus Vaticanos</b> para 23/02: as datas abrem ~2 meses antes. Só em <a href="https://tickets.museivaticani.va" target="_blank" rel="noopener">tickets.museivaticani.va</a> (existem sites falsos).`,
    `<b>Galleria Borghese</b> para 25/02, turno das 9h: reserva obrigatória, sem venda na porta.`,
    `<b>Botín</b> em Madri, se quiserem: pede reserva com semanas de antecedência.`
  ]],
  ["~20/01/2027", "~1 mês antes", [
    `<b>Audiência do Papa</b> (quarta, 24/02): ingressos grátis pedidos à Prefeitura da Casa Pontifícia (formulário no vatican.va ou fax +39 06 6988 5863).`,
    `<b>Seguro viagem Schengen</b> e <b>ETIAS</b>, se já estiver valendo (€20 por pessoa, só no site oficial).`,
    `Conferir o calendário 2027 da <b>taxa de acesso a Veneza</b> (27/02).`,
    `<b>Futebol</b>: a Serie A marca dia e hora em meados de janeiro, e a LaLiga no fim de janeiro (para 19–22/02) e em ~10–15/02 (para 05–08/03). Na Itália, cada comprador leva no máximo 4 ingressos, então são 2 compradores para os 5. <a href="futebol.html">Jogos</a>`
  ]],
  ["23/01/2027", "às 5h de Brasília", [
    `<b>Coliseu</b> para 22/02, 8h30: as vendas abrem 30 dias antes, de manhã em Roma. Só em <a href="https://ticketing.colosseo.it" target="_blank" rel="noopener">ticketing.colosseo.it</a>.`
  ]],
  ["Fevereiro", "1–2 semanas antes", [
    `<b>Parlamento de Budapeste</b> (05/02... 05/03), <b>Casa di Giulietta</b> (26/02, horário marcado) e os <b>banhos Széchenyi</b> online.`,
    `<b>Reservas de restaurante</b> para 5: Emma (21/02), Taverna dei Quaranta e Il Grottino (22/02), Rugantino (24/02), Peroni (25/02), Al Pompiere (27/02), Stiftskeller ou Gasthaus Goldenes Dachl (28/02), Café Landtmann (02/03).`
  ]],
  ["Na viagem", "1–3 dias antes ou no dia", [
    `<b>Schönbrunn</b> e <b>Belvedere</b> em Viena: horário marcado, 1–3 dias antes.`
  ]],
];
document.getElementById("lista-compras").innerHTML = COMPRAS.map(([q,s,l]) =>
  `<li class="compra"><div class="quando num">${q}<span>${s}</span></div><ul>${l.map(x=>`<li>${x}</li>`).join("")}</ul></li>`).join("")
  .replace("(05/02... 05/03)", "(05/03)");


// ---------- voos ----------
(function(){
  const el = document.getElementById("voos");
  const v = G.voos;
  if (!v) { el.innerHTML = `<h3>Voos dentro da Europa</h3><p class="cartao" style="margin-top:12px">A pesquisa de voos com as bagagens (mala de mão para os 5 e 2 despachadas) ainda está sendo feita. Esta seção se atualiza quando ela terminar.</p>`; return; }
  const rota = (titulo, data, rec, linhas) => `<div class="trecho cartao">
    <div class="cab"><h3>${titulo}</h3><span><span class="chip ok">à venda</span> <span class="fraco num">${data}</span></span></div>
    <p class="rec">${rec}</p>
    <div class="rolagem"><table class="num"><thead><tr><th>Voo</th><th>Horário</th><th>Como fica a bagagem</th><th>Total para os 5</th><th>Preço</th></tr></thead><tbody>
      ${linhas.map(([r,v,h,bag,tot,cert]) => `<tr class="${r?"recomendado":""}"><td>${v}</td><td>${h}</td><td>${bag}</td><td><b>${tot}</b></td><td class="fraco">${cert}</td></tr>`).join("")}
    </tbody></table></div></div>`;
  el.innerHTML = `<h3>Voos dentro da Europa</h3>
    <p class="sub" style="margin-top:6px">Todos os totais já incluem a regra de vocês: <b>mala de mão de 10 kg para os 5 e mala despachada para 2</b>. Não incluem o IOF do cartão (3,5%). Pesquisa de 30/09/2026.</p>
    ${rota("Madri → Roma", "dom 21/02",
      "<b>Iberia 08:45 → 11:10</b>, pousando em Fiumicino. Na Iberia a mala de mão já vem na tarifa Basic, e a tarifa vale para a reserva inteira. Por isso o mais barato são <b>duas reservas</b>: 3 pessoas na Basic e 2 na Optimal, que inclui a mala de 23 kg (+€34 por pessoa). Se sair às 12:40 não atrapalhar, a Air Europa economiza uns R$ 700, mas o preço das 2 malas dela é estimado.",
      [[1,"Iberia","08:45 → 11:10 (ou 11:30 → 13:55)","3 Basic + 2 Optimal","R$ 2.845 (€481)","todo ao vivo"],
       [0,"Air Europa","12:40 → 15:05","mala de mão incluída; +2 malas","~R$ 2.000–2.240","malas estimadas"],
       [0,"Wizz Air","09:25 → 11:55","5 Priority + 2 malas de 20 kg","~R$ 2.180 (até R$ 4.280)","estimado (site bloqueia)"],
       [0,"Ryanair FR2436","09:35","5 Regular + 2 malas","~R$ 3.016","mala estimada"],
       [0,"Iberia","21:50 → 00:15","3 Basic + 2 Optimal","R$ 2.046","ao vivo, mas chega à meia-noite"]])}
    ${rota("Budapeste → Madri", "sáb 06/03",
      "<b>Iberia 11:10 → 14:30</b>: o preço conferido e um horário bom, com a mesma divisão (3 Basic + 2 Optimal). A Wizz só compensa se, na hora de comprar, Priority para 5 + 2 malas de 20 kg saírem por menos de ~€270 no total.",
      [[1,"Iberia","11:10 → 14:30","3 Basic + 2 Optimal","R$ 3.449","todo ao vivo"],
       [0,"Wizz Air","15:45 → 19:15","5 Priority + 2 malas de 20 kg","~R$ 2.830 (R$ 2.120–4.930)","estimado"],
       [0,"Ryanair FR5712","16:15 → 19:35","5 Regular + 2 malas","~R$ 3.210","mala estimada"],
       [0,"Ryanair FR6712","06:10","5 Regular + 2 malas","~R$ 3.150","mala estimada"]])}
    <div class="cartao" style="margin-top:16px">
      <h3>Quando comprar</h3>
      <p class="rec" style="margin-top:8px;color:var(--tinta-2)">O Google considera o preço de hoje "típico" e aponta <b>15/10 a 29/12</b> como a janela mais barata para Madri–Roma. Criem alertas de preço agora e comprem até meados de dezembro. Não deixem para o fim: 5 pessoas precisam de 5 lugares na mesma faixa barata, e um dos voos já mostrava "5 lugares restantes neste preço".</p>
      <h3 style="margin-top:14px">Armadilhas das low-cost</h3>
      <ul style="margin:8px 0 0;padding-left:18px;color:var(--tinta-2);display:grid;gap:4px">
        <li><b>Ryanair:</b> o pacote Plus inclui a mala de 20 kg mas <b>não</b> a mala de mão. Para a mala de mão é Priority ou o pacote Regular.</li>
        <li><b>Wizz:</b> o pacote WIZZ Go inclui a mala de 20 kg mas <b>não</b> a mala de mão.</li>
        <li><b>Air Europa:</b> a mala de mão é mais estreita (55×35×25). <b>ITA:</b> só 8 kg.</li>
      </ul>
    </div>`;
  window.TOTAL_VOOS_BRL = 2845 + 3449;
})();

// ---------- trens ----------
const TRENS_PT = {
  "1": {rec:"<b>Dá para comprar já.</b> Italo 8956, 08:20 → 11:38, direto, tarifa <b>Italo Friends</b> (grupo de 3 a 5 pessoas na mesma reserva): €159,80 para os 5. Troca com taxa até 72h antes; não reembolsa. Plano B: Frecciarossa 8506, 08:50 → 12:08, Super Economy €199,50. O site do Italo pode mostrar dólar porque vocês estão no Brasil: paguem em euro.", ok:true,
        destaque: o => /Friends \(Smart\)/.test(o.fare_name||"")},
  "2": {rec:"<b>Venda abre ~meados de outubro</b>, quando o horário de 2027 entrar no sistema. Railjet 88, 09:01 → 12:32, direto. Comparem ÖBB e Trenitalia: a Trenitalia vende esse mesmo trem e saiu mais barata na data de referência. Olhem também a 1ª classe, que na referência saiu mais barata que a 2ª.",
        destaque: o => /88/.test(o.train||"") && /Spar/i.test(o.fare_name||"")},
  "3": {rec:"<b>Venda abre ~meados de outubro.</b> Railjet ~13:58 → 18:32, direto (ou 12:56 → 17:32). Sparschiene na referência: ~€124,50 para os 5; a tarifa cheia seria €434. Evitem o trem das 12:42, que passa pela Alemanha e custa €753.",
        destaque: o => /13:5/.test(o.dep||"") && /Spar/i.test(o.fare_name||"")},
  "4": {rec:"<b>Venda abre ~meados de outubro.</b> Railjet ~07:40 → 10:35 (ou EuroCity 06:40 → 09:29). Sparschiene na referência: ~€80,60 para os 5; a cheia seria €266,50. Confiram que o trem termina em Budapest-Keleti.",
        destaque: o => /07:4/.test(o.dep||"") && /Spar/i.test(o.fare_name||"")},
  "4-ALT": {rec:"Só vale para o plano antigo, com bate-volta a Budapeste: ~€155 ida e volta para os 5.", destaque: () => false},
};
(function(){
  const legs = (G.trens && G.trens.legs) || [];
  document.getElementById("trens").innerHTML = legs.map(l => {
    const k = (l.leg.match(/^([\d]+(?:-ALT)?)/i)||[])[1]?.toUpperCase() || "";
    const t = TRENS_PT[k] || {rec:"", destaque:()=>false};
    const titulo = l.leg.replace(/^[\d\-A-Z]+\.\s*/,"").replace("->","→").replace("same-day return","ida e volta no mesmo dia");
    const hora = s => (s||"").match(/\d{2}:\d{2}/)?.[0] || s || "";
    return `<div class="trecho cartao">
      <div class="cab"><h3>${titulo}</h3><span>${l.sales_open ? '<span class="chip ok">à venda</span>' : '<span class="chip espera">venda abre ~meados de out/2026</span>'} <span class="fraco num">${l.date.replace(/\s*\(.*\)/,"").split("-").reverse().slice(0,2).join("/")}</span></span></div>
      <p class="rec">${t.rec}</p>
      <div class="rolagem"><table class="num"><thead><tr><th>Trem</th><th>Sai → chega</th><th>Trocas</th><th>Tarifa</th><th>Total 5 (€)</th><th>Total 5 (R$)</th><th>Dado</th></tr></thead><tbody>
        ${l.options.map(o => `<tr class="${t.destaque(o)?"recomendado":""}"><td>${o.operator||""} ${(o.train||"").replace(/\s*\(.*$/,"")}</td><td>${hora(o.dep)} → ${hora(o.arr)}</td><td>${o.changes ?? ""}</td><td>${o.fare_name||""}</td><td>${o.total_5_eur!=null?eur(o.total_5_eur):"—"}</td><td>${o.total_5_brl!=null?brl(o.total_5_brl):"—"}</td><td class="fraco">${/live/i.test(o.source||"")&&!/reference|NOT/i.test(o.source||"")?"ao vivo":"referência"}</td></tr>`).join("")}
      </tbody></table></div>
    </div>`;
  }).join("");
})();

// ---------- orçamento ----------
const ATRACOES = [
  ["Madri","Palácio Real",18],["Madri","Prado (grátis 18h–20h)",0],["Madri","Trem ida e volta a Toledo",30],
  ["Roma","Coliseu + Fórum + Palatino",20],["Roma","Museus Vaticanos",25],["Roma","Cúpula de São Pedro",10],["Roma","Galleria Borghese",17],["Roma","Panteão",7],["Roma","Trevi (perto da fonte)",2],["Roma","Castel Sant'Angelo",16],
  ["Verona","Arena",12],["Verona","Casa di Giulietta (completa)",12],["Verona","Torre dei Lamberti",6],["Verona","Trem ida e volta a Veneza",26],
  ["Innsbruck","Hofburg",15],["Innsbruck","Nordkette (Seegrube)",50.4],
  ["Viena","Schönbrunn",42],["Viena","Belvedere",23],["Viena","Kunsthistorisches",22],["Viena","Museu Sisi",20],["Viena","Torre da Stephansdom",8],["Viena","Patinação na Rathausplatz",10.5],
  ["Budapeste","Parlamento",35],["Budapeste","Banhos Széchenyi",37],
];
function orcamento(){
  const atr = ATRACOES.reduce((s,a) => s + a[2], 0) * 5 * G.cambio;
  let hosp = 0; HOSP.forEach(c => { const e = c.itens.filter(x => x.escolha && x.tipo==="airbnb"); if (e.length) hosp += Math.min(...e.map(x=>x.total)); });
  hosp += 150 * G.cambio; // taxa turística de Roma
  const trens = (159.80 + 125 + 124.50 + 80.60) * G.cambio;
  const voos = window.TOTAL_VOOS_BRL || null;
  // transporte local: o bilhete recomendado em cada cidade, já para os 5
  // + aeroportos, sempre de táxi/Uber (regra do grupo): Madri 4 × €33, Roma €55 (táxi grande), Budapeste ~€35
  const loc = (Object.values(G.transporte||{}).reduce((s,t) => s + (t.recomendado?.total_5_eur || 0), 0) + 4 * 33 + 55 + 35) * G.cambio;
  const total = hosp + trens + atr + loc + (voos || 0);
  document.getElementById("orc").innerHTML = `
    <div class="caixa"><p class="fraco">Hospedagem (Airbnb bom mais barato + taxa de Roma)</p><p class="v">${brl(hosp)}</p></div>
    <div class="caixa"><p class="fraco">Trens (4 trechos)</p><p class="v">${brl(trens)}</p><p class="fraco">1 ao vivo, 3 por referência</p></div>
    <div class="caixa"><p class="fraco">Voos internos com bagagem</p><p class="v">${voos?brl(voos):"—"}</p>${voos?"":'<p class="fraco">aguardando pesquisa</p>'}</div>
    <div class="caixa"><p class="fraco">Ingressos e passeios</p><p class="v">${brl(atr)}</p></div>
    <div class="caixa"><p class="fraco">Metrô, ônibus e aeroportos</p><p class="v">${brl(loc)}</p><p class="fraco">bilhete mais barato em cada cidade + táxis de aeroporto</p></div>
    <div class="caixa total"><p class="fraco">Total para os 5${voos?"":" (sem voos)"}</p><p class="v">${brl(total)}</p><p class="fraco">${brl(total/5)} por pessoa</p></div>`;
}
document.getElementById("lista-orc").innerHTML = ATRACOES.map(([c,n,v]) =>
  `<div class="linha-orc"><span class="n">${n} <span class="fraco">· ${c}</span></span><span>${v?eur(v):"grátis"}</span></div>`).join("");
orcamento();

// ---------- cidades ----------
const RESUMO = {madri:"Chegada e volta: Retiro, Prado, Palácio, Rastro, Toledo", roma:"5 noites: Roma Antiga, Vaticano, Trastevere, Borghese", verona:"Arena, Giulietta e bate-volta a Veneza", innsbruck:"Uma noite nos Alpes, com a Nordkette", viena:"Kipferl, Schönbrunn, Klimt, Sisi e Kaiserschmarrn", budapeste:"Parlamento, Buda e banhos termais"};
document.getElementById("lista-cidades").innerHTML = G.cidades.map(([k,n]) => {
  const l = G.lugares[k]; const c = l.filter(x=>x.tipo==="comer").length, v = l.length - c;
  const capa = l.find(x => x.foto && x.tipo==="ver" && G.usados.includes(x.id));
  return `<a class="cidade-card" href="cidade.html?c=${k}" style="--cor:${COR[k]}">${capa?`<div class="capa"><img src="${capa.foto.url}" alt="" loading="lazy"></div>`:""}<b>${n}</b><span>${RESUMO[k]}</span><span class="num">${v} para ver · ${c} para comer</span></a>`;
}).join("") + `<a class="cidade-card" href="hospedagens.html" style="--cor:var(--tinta)"><b>Hospedagem</b><span>Airbnb e hotéis pesquisados em cada parada</span></a><a class="cidade-card" href="matcha.html" style="--cor:#4d7c0f"><b>Matcha da Camila</b><span>Os lugares de matcha de Madri</span></a><a class="cidade-card" href="futebol.html" style="--cor:#15803d"><b>Futebol</b><span>Jogos nas cidades, nos dias em que vocês estão lá</span></a>`;

// ---------- checklist ----------
const CHECKS = [
  ["Hospedagens reservadas (cancelamento grátis)","A de Madri na chegada precisa de check-in autônomo à meia-noite."],
  ["Mesmo apartamento em Madri na ida e na volta","É o que permite deixar as malas grandes guardadas."],
  ["Trem Roma → Verona (Italo Friends)","Já à venda: €159,80 para os 5."],
  ["Voos Madri → Roma e Budapeste → Madri","Com mala de mão para os 5 e 2 despachadas."],
  ["Trens ÖBB (3 trechos)","Abrem ~meados de outubro."],
  ["Museus Vaticanos (23/02)","Abrem ~2 meses antes."],
  ["Galleria Borghese (25/02, 9h)","Reserva obrigatória."],
  ["Coliseu (22/02, 8h30)","Vendas abrem 23/01/2027."],
  ["Audiência do Papa (24/02)","Pedir ~1 mês antes; retirar terça 15h–19h."],
  ["Casa di Giulietta (26/02)","Horário marcado."],
  ["Parlamento de Budapeste (05/03)","1–2 semanas antes."],
  ["Restaurantes reservados","Emma, Taverna dei Quaranta, Il Grottino, Rugantino, Peroni, Al Pompiere, Stiftskeller."],
  ["Seguro viagem Schengen","Cobertura mínima de €30 mil."],
  ["ETIAS, se já estiver valendo","€20 por pessoa, só no site oficial."],
  ["Passaporte válido até junho/2027 ou depois","3 meses depois da saída."],
  ["Van reservada para a chegada em Madri","22:35, 5 pessoas e malas."],
  ["eSIM europeu","Um plano de roaming na UE vale para os 4 países."],
  ["Roupa de frio de verdade","Innsbruck abaixo de zero; Viena e Budapeste perto de 0 °C."],
];
document.getElementById("checks").innerHTML = CHECKS.map(([t,s]) => `<li><b>${t}</b><span>${s}</span></li>`).join("");
