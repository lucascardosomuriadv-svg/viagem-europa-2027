// Aba "Comer" + a ficha curta de qualquer lugar (bottom sheet).
// Ficha só com o essencial: metrô, o que pedir, quando fecha, preço. Sem dia: ainda não há roteiro.

const TIPOS = [
  ["todos", "Tudo"],
  ["restaurante", "Restaurantes"],
  ["rapido", "Rápido"],
  ["cafe", "Cafés e doces"],
  ["matcha", "Matcha"],
];
function tipoComida(x){
  if (x.matcha === true) return "matcha";
  const t = (x.categoria + " " + x.nome).toLowerCase();
  if (/gelat|sorvet|confeit|pastic|doce|tiramis|chocolat|churr|café|cafe|caffè|coffee|padaria|bakery|panific|forno|konditor|kipferl|croissant|bäck|brot|demel|sacher|kaiserschmarrn|schmarren/.test(t)) return "cafe";
  if (/taglio|pizzarium|bocadillo|montadit|lángos|langos|würstel|wurst|imbiss|sanduí|panin|schiacciata|trapizz|suppl|street|balcão|kebab|bosna|burger|hambúrg|sandwich|tostas?\b/.test(t)) return "rapido";
  return "restaurante";
}
// ícones desenhados (emoji muda de cara em cada celular)
const SVG_COMIDA = {
  restaurante:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 2v9a2 2 0 0 0 2 2v9M7 2v6M11 2v6M17 2c-2 2-2 6 0 8v12"/></svg>',
  rapido:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11a9 5 0 0 1 18 0zM3 15h18M4 15l1 4h14l1-4"/></svg>',
  cafe:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 2v3M12 2v3"/></svg>',
  matcha:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19C5 10 11 4 20 4c0 9-6 15-15 15zM5 19l8-8"/></svg>',
  extra:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="3"/><path d="M8 7l2-3h4l2 3"/><circle cx="12" cy="13.5" r="3.5"/></svg>',
  ver:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
};
const iconeComida = tp => SVG_COMIDA[tp] || SVG_COMIDA.restaurante;
const umaFrase = s => { s = (s||"").replace(/<[^>]+>/g,"").trim(); if (!s || s==="—") return ""; const m = s.match(/^.{0,90}?[.;](\s|$)/); return (m ? m[0] : s.slice(0,90)).replace(/[.;]\s*$/,""); };

// ---------- ficha ----------
function abrirFicha(id){
  const x = porId[id]; if (!x) return;
  const campo = (r,v) => v ? `<dt>${r}</dt><dd>${esc(v)}</dd>` : "";
  const gm = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(curto(x.nome) + " " + (x.endereco || NOME[x.cidade]))}`;
  const el = document.getElementById("ficha");
  el.innerHTML = `<div class="alca"></div>
    ${x.foto?`<div class="ficha-foto"><img src="${x.foto.url}" alt=""><span class="credito">Foto: ${esc(x.foto.autor)}</span></div>`:""}
    <h2>${esc(curto(x.nome))}</h2>
    <p class="fraco">${esc(NOME[x.cidade])}${x.bairro?" · "+esc(x.bairro.split(/[(/]/)[0].trim()):""}</p>
    <dl class="kv">
      ${x.metro?`<dt>Metrô</dt><dd>${esc(x.metro.nome)} · ${x.metro.min} min a pé</dd>`:""}
      ${campo(x.tipo==="comer"?"Pedir":"O que é", umaFrase(x.pedir) || (x.tipo==="ver"?umaFrase(x.dica):""))}
      ${campo("Fecha", umaFrase(x.fecha))}
      ${campo("Preço", (v => /^~?\d/.test(v) && !/€|R\$|HUF|Ft|grát/i.test(v) ? "€" + v : v)(umaFrase(x.preco)))}
    </dl>
    <div class="ficha-acoes"><a class="bt" href="${gm}" target="_blank" rel="noopener">Abrir no Google Maps</a><button type="button" class="bt sec" id="ficha-fechar">Fechar</button></div>`;
  el.hidden = false; document.getElementById("ficha-fundo").hidden = false;
  requestAnimationFrame(() => el.classList.add("on"));
  document.getElementById("ficha-fechar").onclick = fecharFicha;
}
function fecharFicha(){
  const el = document.getElementById("ficha"); el.classList.remove("on");
  document.getElementById("ficha-fundo").hidden = true;
  setTimeout(() => { el.hidden = true; }, 180);
}
document.getElementById("ficha-fundo").onclick = fecharFicha;
document.addEventListener("keydown", e => { if (e.key === "Escape" && !document.getElementById("ficha").hidden) fecharFicha(); });
// qualquer [data-ficha] na página abre a ficha
document.addEventListener("click", e => { const a = e.target.closest("[data-ficha]"); if (!a) return; e.preventDefault(); abrirFicha(a.dataset.ficha); });

// ---------- aba Comer ----------
let kCidade = null, kTipo = "todos";
function renderComer(param){
  if (param && NOME[param]) kCidade = param;
  if (!kCidade) { let c = null; try { c = sessionStorage.getItem("cidade"); } catch(e){} kCidade = NOME[c] ? c : "todas"; }
  const todos = Object.values(G.lugares).flat().filter(x => x.tipo === "comer");
  const filtro = (l, c, t) => l.filter(x => (c==="todas" || x.cidade===c) && (t==="todos" || tipoComida(x)===t));
  const cidades = [["todas","Todas"], ...G.cidades];
  document.getElementById("k-cidades").innerHTML = cidades.map(([k,n]) => `<button type="button" class="${k===kCidade?"on":""}" data-c="${k}">${n}</button>`).join("");
  document.getElementById("k-tipos").innerHTML = TIPOS.filter(([k]) => k==="todos" || filtro(todos, kCidade, k).length)
    .map(([k,n]) => `<button type="button" class="${k===kTipo?"on":""}" data-t="${k}">${n} <span>${filtro(todos, kCidade, k).length}</span></button>`).join("");
  if (!filtro(todos, kCidade, kTipo).length) kTipo = "todos";
  document.querySelectorAll("#k-cidades button").forEach(b => b.onclick = () => { kCidade = b.dataset.c; try { if (NOME[kCidade]) sessionStorage.setItem("cidade", kCidade); } catch(e){} renderComer(); });
  document.querySelectorAll("#k-tipos button").forEach(b => b.onclick = () => { kTipo = b.dataset.t; renderComer(); });
  const l = filtro(todos, kCidade, kTipo);
  document.getElementById("k-sub").textContent = `${l.length} lugares${kCidade!=="todas"?" em "+NOME[kCidade]:""}`;
  // por cidade, na ordem da viagem; dentro dela, em ordem alfabética
  const ordemCid = Object.fromEntries(G.cidades.map(([k],i) => [k,i]));
  const ord = [...l].sort((a,b) => (ordemCid[a.cidade]-ordemCid[b.cidade]) || curto(a.nome).localeCompare(curto(b.nome)));
  const grupos = []; ord.forEach(x => { const u = grupos[grupos.length-1]; if (u && u.c===x.cidade) u.l.push(x); else grupos.push({c:x.cidade, l:[x]}); });
  document.getElementById("k-lista").innerHTML = grupos.map(g => `${kCidade==="todas"?`<div class="grupo"><b>${NOME[g.c]}</b></div>`:""}
    <div class="lista">${g.l.map(x => { const tp = tipoComida(x);
      return `<button type="button" class="it linha" data-ficha="${x.id}"><span class="th ${tp}">${iconeComida(tp)}</span><span class="tx"><b>${esc(curto(x.nome))}</b><small>${esc(umaFrase(x.pedir) || umaFrase(x.categoria))}</small></span></button>`; }).join("")}</div>`).join("")
    || '<p class="fraco">Nada com esse filtro.</p>';
}
