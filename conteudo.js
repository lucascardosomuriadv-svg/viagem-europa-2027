// Abas "Passagens" e "Ingressos" (antes eram uma só, "Comprar").
// Passagens = cada voo e trem, na ordem da viagem, com a situação da compra.
// Ingressos = atrações que pedem ingresso ou reserva, na ordem em que a venda abre.
// Hospedagem tem a sua aba; seguro e ETIAS ficam em "Antes de ir", na aba Viagem. Sem total da viagem.
// Usa G, NOME, dm, sem, esc (index.html).

const HOJE = new Date(new Date().toISOString().slice(0,10)+"T12:00:00Z");
const faltam = iso => Math.round((new Date(iso+"T12:00:00Z") - HOJE) / 86400000);
const MES = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
const MES3 = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];

// lembrete: arquivo .ics com alarme, que o celular abre direto no calendário
function ics(data, hora, titulo, texto, site){
  if (site && !/^(https?|mailto):/.test(site)) site = new URL(site, location.href).href;   // link relativo vira completo
  const [h, m] = (hora || "09:00").split(":").map(Number);
  // Brasília = UTC−3, sem horário de verão
  const ini = new Date(Date.UTC(+data.slice(0,4), +data.slice(5,7)-1, +data.slice(8,10), h + 3, m));
  const fim = new Date(ini.getTime() + 30*60000);
  const f = d => d.toISOString().replace(/[-:]/g,"").replace(/\.\d{3}/,"");
  const limpa = s => String(s).replace(/[,;\\]/g, m => "\\" + m).replace(/\n/g, "\\n");
  return ["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Europa 2027//PT","BEGIN:VEVENT",
    `UID:${data}-${titulo.replace(/\W+/g,"")}@europa2027`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(ini)}`, `DTEND:${f(fim)}`,
    `SUMMARY:${limpa("Comprar: " + titulo)}`, `DESCRIPTION:${limpa(texto + (site ? "\n" + site : ""))}`, site && /^https/.test(site) ? `URL:${site}` : "",
    "BEGIN:VALARM","ACTION:DISPLAY","TRIGGER:-PT10M",`DESCRIPTION:${limpa(titulo)}`,"END:VALARM","END:VEVENT","END:VCALENDAR"].filter(Boolean).join("\r\n");
}
function baixarLembrete(data, hora, titulo, texto, site){
  const url = URL.createObjectURL(new Blob([ics(data, hora, titulo, texto, site)], {type:"text/calendar"}));
  const a = document.createElement("a"); a.href = url; a.download = `lembrete-${titulo.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g,"-")}.ics`;
  document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
}
const proximaAcao = (dataISO, titulo) => `<div class="proxima"><small>Próxima ação · ${faltam(dataISO) === 1 ? "amanhã" : `faltam ${faltam(dataISO)} dias`}</small><b>${dm(dataISO)} · ${esc(titulo)}</b></div>`;

// ---------- PASSAGENS ----------
// [dia, sai, chega, avião|trem, trecho, companhia, situação (comprada|comprar|abre), dia em que a venda abre, o que comprar, site, rótulo]
const PASSAGENS = [
  ["2027-02-17", "", "", "aviao", "Vitória → São Paulo", "", "comprar", null, "Os 5, na véspera do voo para Madri", "https://www.google.com/travel/flights", "Buscar voo"],
  ["2027-02-18", "08:25", "22:35", "aviao", "São Paulo → Madri", "Air China CA898", "comprada", null, "2 malas despachadas por pessoa", "", ""],
  ["2027-02-21", "08:45", "", "aviao", "Madri → Roma", "Iberia", "comprar", null, "3 Basic + 2 Optimal (as 2 malas despachadas) · mais barato até 15/12", "https://www.iberia.com", "Iberia"],
  ["2027-02-26", "08:20", "11:38", "trem", "Roma → Verona", "Italo 8956", "comprar", null, "5 bilhetes na tarifa Italo Friends · €159,80 os 5", "https://www.italotreno.com", "Site do Italo"],
  ["2027-02-28", "09:01", "12:32", "trem", "Verona → Innsbruck", "ÖBB RJ 88", "abre", "2026-10-15", "5 bilhetes Sparschiene · a data da abertura é prevista, confiram no dia", "https://www.oebb.at", "Site da ÖBB"],
  ["2027-03-01", "13:58", "18:32", "trem", "Innsbruck → Viena", "ÖBB Railjet", "abre", "2026-10-15", "5 bilhetes Sparschiene", "https://www.oebb.at", "Site da ÖBB"],
  ["2027-03-04", "07:40", "10:35", "trem", "Viena → Budapeste", "ÖBB Railjet", "abre", "2026-10-15", "5 bilhetes Sparschiene", "https://www.oebb.at", "Site da ÖBB"],
  ["2027-03-06", "11:10", "", "aviao", "Budapeste → Madri", "Iberia", "comprar", null, "3 Basic + 2 Optimal (as 2 malas despachadas) · mais barato até 15/12", "https://www.iberia.com", "Iberia"],
  ["2027-03-08", "22:30", "05:30", "aviao", "Madri → São Paulo", "Air China CA897", "comprada", null, "2 malas despachadas por pessoa", "", ""],
  ["2027-03-09", "", "", "aviao", "São Paulo → Vitória", "", "comprar", null, "Os 5, depois do pouso em São Paulo às 05:30", "https://www.google.com/travel/flights", "Buscar voo"],
];
function renderPassagens(){
  const itens = PASSAGENS.map((p,i) => ({i, dia:p[0], sai:p[1], chega:p[2], tipo:p[3], trecho:p[4], cia:p[5], sit:p[6], abre:p[7], oque:p[8], site:p[9], rot:p[10]}));
  // venda que já abriu passa a "comprar agora"
  itens.forEach(x => { if (x.sit === "abre" && faltam(x.abre) <= 0) x.sit = "comprar"; });
  const n = s => itens.filter(x => x.sit === s).length;
  document.getElementById("p-sub").textContent = `${itens.length} trechos · ${n("comprada")} comprados · ${n("comprar")} para comprar agora`;
  const prox = itens.filter(x => x.sit === "abre").sort((a,b) => a.abre.localeCompare(b.abre))[0];
  document.getElementById("p-topo").innerHTML = prox ? proximaAcao(prox.abre, `abre a venda dos ${n("abre")} trens da ÖBB`) : "";
  const chip = x => x.sit === "comprada" ? `<span class="chip ok">Comprada</span>` : x.sit === "comprar" ? `<span class="chip espera">Comprar agora</span>` : `<span class="chip">Venda abre em ${dm(x.abre)}</span>`;
  document.getElementById("p-lista").innerHTML = itens.map(x => `<div class="ev"><div class="dt ${x.sit==="comprada"?"ja":""}"><b>${+x.dia.slice(8)}</b><small>${MES3[+x.dia.slice(5,7)-1]}</small></div>
    <div class="ev-c"><h3>${esc(x.trecho)}</h3>
      <p>${sem(x.dia)} ${dm(x.dia)}${x.sai?` · ${x.sai}${x.chega?" → "+x.chega:""}`:""} · ${x.tipo==="trem"?"trem":"avião"}${x.cia?" · "+esc(x.cia):""}</p>
      <p>${esc(x.oque)}</p><p class="sit">${chip(x)}</p>
      ${x.sit!=="comprada" && (x.site || x.sit==="abre") ? `<div class="bts">${x.site?`<a class="bt p" href="${x.site}" target="_blank" rel="noopener">${esc(x.rot)}</a>`:""}${x.sit==="abre"?`<button type="button" class="bt" data-lp="${x.i}">Lembrete</button>`:""}</div>` : ""}</div></div>`).join("");
  document.querySelectorAll("[data-lp]").forEach(b => b.onclick = () => { const p = PASSAGENS[+b.dataset.lp]; baixarLembrete(p[7], "09:00", `trem ${p[4]}`, `${p[8]} · ${p[5]} · ${dm(p[0])} ${p[1]}`, p[9]); });
}

// ---------- INGRESSOS ----------
// [dia em que dá para comprar (ISO, null = já), hora do lembrete (Brasília), título, o que comprar, site, rótulo do site, observação]
// Sem dia de visita: ainda não há roteiro. A data é a da primeira janela de venda para os dias em que estaremos na cidade.
const INGRESSOS = [
  [null, null, "Palácio Real de Madri", "5 ingressos · ~€18 cada · grátis de segunda a quinta, das 16h às 18h", "https://tickets.patrimonionacional.es", "Site oficial", ""],
  ["2026-12-23", "09:00", "Museus Vaticanos", "5 ingressos · primeiro horário do dia", "https://tickets.museivaticani.va", "Site oficial", "abre ~2 meses antes da visita"],
  ["2026-12-25", "09:00", "Galleria Borghese", "5 ingressos · turno das 9h", "https://galleriaborghese.cultura.gov.it", "Site oficial", "reserva obrigatória"],
  ["2027-01-15", "09:00", "Jogos de futebol", "As datas e os horários saem a partir de meados de janeiro", "futebol.html", "Ver os jogos", ""],
  ["2027-01-23", "04:50", "Coliseu", "5 ingressos · a venda abre às 5h de Brasília, 30 dias antes da visita", "https://ticketing.colosseo.it", "Site oficial", "esgota rápido"],
  ["2027-01-24", "09:00", "Audiência do Papa", "pedido grátis para 5, por e-mail à Prefeitura da Casa Pontifícia · é às quartas: qua 24/02 é a única em Roma", "mailto:ordinanze@pontificalisdomus.va", "Pedir por e-mail", ""],
  ["2027-02-12", "09:00", "Casa di Giulietta", "5 ingressos · horário marcado", "https://museiverona.com", "Site oficial", ""],
  ["2027-02-19", "09:00", "Parlamento de Budapeste", "5 ingressos · visita guiada", "https://jegymester.hu/parlament", "Site oficial", ""],
  ["2027-02-19", "09:00", "Banhos Széchenyi", "5 ingressos · Fast Track", "https://www.szechenyibath.hu", "Site oficial", ""],
  ["2027-02-27", "09:00", "Schönbrunn", "5 ingressos Palace Ticket · primeiro horário", "https://www.schoenbrunn.at", "Site oficial", ""],
  ["2027-02-28", "09:00", "Belvedere", "5 ingressos · horário marcado", "https://www.belvedere.at", "Site oficial", ""],
  ["2027-02-28", "09:00", "Museu Sisi (Hofburg)", "5 ingressos · horário marcado", "https://www.sisimuseum-hofburg.at", "Site oficial", ""],
];
const NA_HORA = "Panteão €7 · Trevi €2 · Arena de Verona €12 · Prado grátis das 18h às 20h";
function renderIngressos(){
  const itens = INGRESSOS.map((x,i) => ({i, data:x[0], hora:x[1], titulo:x[2], oque:x[3], site:x[4], rot:x[5], obs:x[6], ja: !x[0] || faltam(x[0]) <= 0}));
  const futuros = itens.filter(x => !x.ja).sort((a,b) => a.data.localeCompare(b.data));
  document.getElementById("c-topo").innerHTML = (futuros[0] ? proximaAcao(futuros[0].data, futuros[0].titulo) : "")
    + `<a class="atalho" href="futebol.html">Jogos de futebol nas datas da viagem ›</a>`;
  const ev = x => `<div class="ev"><div class="dt ${x.ja?"ja":""}">${x.ja?`<b>✓</b><small>já</small>`:`<b>${+x.data.slice(8)}</b><small>${MES3[+x.data.slice(5,7)-1]}</small>`}</div>
    <div class="ev-c"><h3>${esc(x.titulo)}</h3><p>${esc(x.oque)}</p>${!x.ja ? `<span class="f">faltam ${faltam(x.data)} dias${x.obs?" · "+esc(x.obs):""}</span>` : (x.obs?`<span class="f">${esc(x.obs)}</span>`:"")}
      <div class="bts">${x.site?`<a class="bt p" href="${x.site}" ${/^https/.test(x.site)?'target="_blank" rel="noopener"':""}>${esc(x.rot)}</a>`:""}${!x.ja?`<button type="button" class="bt" data-li="${x.i}">Lembrete</button>`:""}</div></div></div>`;
  const grupos = []; futuros.forEach(x => { const k = x.data.slice(0,7); const u = grupos[grupos.length-1]; if (u && u.k===k) u.l.push(x); else grupos.push({k, l:[x]}); });
  const jas = itens.filter(x => x.ja);
  document.getElementById("c-agenda").innerHTML =
    (jas.length ? `<div class="mes">Já dá para comprar</div>${jas.map(ev).join("")}` : "")
    + grupos.map(g => `<div class="mes">${MES[+g.k.slice(5,7)-1]}</div>${g.l.map(ev).join("")}`).join("")
    + `<div class="mes">Na hora, sem reservar</div><p class="na-hora">${NA_HORA}</p>`;
  document.querySelectorAll("[data-li]").forEach(b => b.onclick = () => { const x = INGRESSOS[+b.dataset.li]; baixarLembrete(x[0], x[1], x[2], x[3], x[4]); });
}
