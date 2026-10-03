// Aba "Comprar" do guia.
// Comprar = AGENDA (jeito A, escolhido pelo Lucas em 01/10/2026): o que falta
// comprar ou reservar, mês a mês, dizendo EXATAMENTE o que comprar, com botão
// para o site oficial e lembrete no calendário do celular. Sem total da viagem.
// Usa G, NOME, dm, esc (definidos no index.html).

const HOJE = new Date(new Date().toISOString().slice(0,10)+"T12:00:00Z");
const faltam = iso => Math.round((new Date(iso+"T12:00:00Z") - HOJE) / 86400000);
const MES = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
const MES3 = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];

// [data em que dá para comprar (ISO, null = já), hora do lembrete (Brasília), título, o que comprar, site, rótulo do site, quando é na viagem]
const AGENDA = [
  [null, null, "Hospedagens", "7 estadias, com cancelamento grátis", "hospedagens.html", "Ver opções", ""],
  [null, null, "Trem Roma → Verona", "5 bilhetes · Italo 8956 · sex 26/02 · 08:20 · tarifa Italo Friends · €159,80", "https://www.italotreno.com", "Site do Italo", ""],
  [null, null, "Voos Madri → Roma e Budapeste → Madri", "Iberia dom 21/02 08:45 e sáb 06/03 11:10 · em 2 reservas: 3 Basic + 2 Optimal (as 2 malas)", "https://www.iberia.com", "Iberia", "mais barato até 15/12"],
  [null, null, "Palácio Real de Madri", "5 ingressos · ~€18 cada", "https://tickets.patrimonionacional.es", "Site oficial", ""],
  [null, null, "Seguro viagem", "os 5 · Schengen, mínimo €30 mil de cobertura", "", "", ""],
  ["2026-10-15", "09:00", "3 trens na Áustria e Hungria", "5 bilhetes Sparschiene em cada: RJ 88 dom 28/02 09:01 · Railjet seg 01/03 13:58 · Railjet qui 04/03 07:40", "https://www.oebb.at", "Site da ÖBB", "data prevista; confiram no dia"],
  ["2026-12-01", "09:00", "Lembrete: voos Iberia", "Se ainda não compraram, comprem até 15/12 (janela mais barata)", "https://www.iberia.com", "Iberia", ""],
  ["2026-12-23", "09:00", "Museus Vaticanos", "5 ingressos · primeiro horário do dia", "https://tickets.museivaticani.va", "Site oficial", "abre ~2 meses antes da visita"],
  ["2026-12-25", "09:00", "Galleria Borghese", "5 ingressos · turno das 9h", "https://galleriaborghese.beniculturali.it", "Site oficial", "reserva obrigatória"],
  ["2027-01-15", "09:00", "Datas dos jogos de futebol", "Lazio × Napoli e os outros: dia e hora saem a partir de meados de janeiro", "futebol.html", "Jogos", ""],
  ["2027-01-20", "09:00", "ETIAS", "os 5 · €20 cada, só se já estiver valendo", "https://travel-europe.europa.eu/etias_en", "Site oficial", ""],
  ["2027-01-23", "04:50", "Coliseu", "5 ingressos · a venda abre às 5h de Brasília, 30 dias antes da visita", "https://ticketing.colosseo.it", "Site oficial", "esgota rápido"],
  ["2027-01-24", "09:00", "Audiência do Papa", "pedido grátis para 5 · é às quartas: qua 24/02 é a única em Roma", "https://www.vatican.va/various/prefettura/index_it.html", "Prefeitura", ""],
  ["2027-02-07", "09:00", "Restaurantes para 5", "Os que forem escolhidos. Para mesa de 5, reservar sempre", "", "", ""],
  ["2027-02-12", "09:00", "Casa di Giulietta", "5 ingressos · horário marcado", "https://museiverona.com", "Site oficial", ""],
  ["2027-02-19", "09:00", "Parlamento de Budapeste", "5 ingressos · visita guiada", "https://jegymester.hu/parlament", "Site oficial", ""],
  ["2027-02-19", "09:00", "Banhos Széchenyi", "5 ingressos · Fast Track", "https://www.szechenyibath.hu", "Site oficial", ""],
  ["2027-02-27", "09:00", "Schönbrunn", "5 ingressos Palace Ticket · primeiro horário", "https://www.schoenbrunn.at", "Site oficial", ""],
  ["2027-02-28", "09:00", "Belvedere e Museu Sisi", "5 + 5 ingressos · horário marcado", "https://www.belvedere.at", "Belvedere", ""],
];
const NA_HORA = "Panteão €7 · Trevi €2 · Arena €12 · Prado grátis das 18h às 20h";

// lembrete: arquivo .ics com alarme, que o celular abre direto no calendário
function ics(data, hora, titulo, texto, site){
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
function baixarLembrete(i){
  const [data, hora, titulo, texto, site] = AGENDA[i];
  const url = URL.createObjectURL(new Blob([ics(data, hora, titulo, texto, site)], {type:"text/calendar"}));
  const a = document.createElement("a"); a.href = url; a.download = `lembrete-${titulo.toLowerCase().replace(/[^a-z0-9]+/g,"-")}.ics`;
  document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
}

function renderComprar(){
  const itens = AGENDA.map((x,i) => ({i, data:x[0], hora:x[1], titulo:x[2], oque:x[3], site:x[4], rot:x[5], obs:x[6], ja: !x[0] || faltam(x[0]) <= 0}));
  const futuros = itens.filter(x => !x.ja).sort((a,b) => a.data.localeCompare(b.data));
  const prox = futuros[0];
  document.getElementById("c-topo").innerHTML = prox
    ? `<div class="proxima"><small>Próxima ação · ${faltam(prox.data) === 1 ? "amanhã" : `faltam ${faltam(prox.data)} dias`}</small><b>${dm(prox.data)} · ${esc(prox.titulo)}</b></div>` : "";
  const ev = x => `<div class="ev"><div class="dt ${x.ja?"ja":""}">${x.ja?`<b>✓</b><small>já</small>`:`<b>${+x.data.slice(8)}</b><small>${MES3[+x.data.slice(5,7)-1]}</small>`}</div>
    <div class="ev-c"><h3>${esc(x.titulo)}</h3><p>${esc(x.oque)}</p>${!x.ja ? `<span class="f">faltam ${faltam(x.data)} dias${x.obs?" · "+esc(x.obs):""}</span>` : (x.obs?`<span class="f">${esc(x.obs)}</span>`:"")}
      <div class="bts">${x.site?`<a class="bt p" href="${x.site}" ${/^https/.test(x.site)?'target="_blank" rel="noopener"':""}>${esc(x.rot)}</a>`:""}${!x.ja?`<button type="button" class="bt" data-lembrete="${x.i}">Lembrete</button>`:""}</div></div></div>`;
  const grupos = []; futuros.forEach(x => { const k = x.data.slice(0,7); const u = grupos[grupos.length-1]; if (u && u.k===k) u.l.push(x); else grupos.push({k, l:[x]}); });
  document.getElementById("c-agenda").innerHTML =
    `<div class="mes">Já dá para comprar</div>${itens.filter(x=>x.ja).map(ev).join("")}`
    + grupos.map(g => `<div class="mes">${MES[+g.k.slice(5,7)-1]}</div>${g.l.map(ev).join("")}`).join("")
    + `<div class="mes">Na hora, sem reservar</div><p class="na-hora">${NA_HORA}</p>`;
  document.querySelectorAll("[data-lembrete]").forEach(b => b.onclick = () => baixarLembrete(+b.dataset.lembrete));
}

renderComprar();
