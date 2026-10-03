// Aba Mapa: um mapa só para a viagem inteira.
// De longe aparecem as cidades e o caminho; de perto (zoom >= Z_PERTO), os lugares de cada cidade.
// A folha embaixo acompanha o que está na tela: a viagem toda ou a cidade que está no centro do mapa.
const CENTRO = {madri:[40.4168,-3.7038],roma:[41.9028,12.4964],verona:[45.4384,10.9916],innsbruck:[47.2672,11.3925],viena:[48.2082,16.3738],budapeste:[47.4979,19.0402]};
const Z_PERTO = 11;
// onde o nome fica em relação ao ponto (b = embaixo, c = em cima, d = à direita, e = à esquerda): as cidades do meio são vizinhas
const LADO = {madri:"b", roma:"d", verona:"e", innsbruck:"e", viena:"c", budapeste:"b"};
// os dois voos saem em arco, cada um para um lado, para não passarem por cima das cidades do trem
const CURVA = {"madri>roma":-.18, "budapeste>madri":.1};
// fundo com relevo de longe e nome de rua de perto
const FUNDO = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}";
const ICO_PERNA = {
  aviao: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 13.5 3 11l1.5-1.5 8 1 4-4.5a2.1 2.1 0 0 1 3 3l-4.5 4 1 8L14.5 22 12 14.5"/></svg>',
  trem: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="3" width="12" height="14" rx="3"/><path d="M6 11h12M9.5 17 8 21M14.5 17l1.5 4M10 14h.01M14 14h.01"/></svg>',
};
let mapa, mCid = null, mTipo = "tudo", mPinos = {}, mLug, mCids, mRota, mSelos = [];

const mDist = (a,b) => { const r=Math.PI/180, X=(b[1]-a[1])*r*Math.cos((a[0]+b[0])/2*r), Y=(b[0]-a[0])*r; return Math.sqrt(X*X+Y*Y)*6371000; };
const mLista = c => ideias(c).filter(x => x.lat && x.tipo !== "info" && (mTipo==="tudo" || x.tipo===mTipo));
const mCor = x => x.tipo==="comer" ? "#c2410c" : "#1d4ed8";
const mCalmo = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
// cada deslocamento entre duas paradas, com o voo ou trem que está na aba Passagens
function mTrechos(){
  return PARADAS.slice(0,-1).map((p,i) => { const a = p[0], b = PARADAS[i+1][0];
    const v = PASSAGENS.find(x => x[0]===p[2] && x[4]===`${NOME[a]} → ${NOME[b]}`) || [];
    return {a, b, dia:p[2], sai:v[1]||"", chega:v[2]||"", tipo:v[3]||"trem"}; });
}
const mQuando = t => `${t.tipo==="aviao"?"avião":"trem"} · ${sem(t.dia)} ${dm(t.dia)}${t.sai?` · ${t.sai}${t.chega?" → "+t.chega:""}`:""}`;
// curva suave entre dois pontos; k diz o quanto e para que lado ela abre
function mArco(a, b, k){
  const cs = Math.cos((a[0]+b[0])/2*Math.PI/180), ax = a[1]*cs, bx = b[1]*cs;
  const cx = (ax+bx)/2 - (b[0]-a[0])*k, cy = (a[0]+b[0])/2 + (bx-ax)*k, pts = [];
  for (let i=0; i<=32; i++){ const t = i/32, u = 1-t; pts.push([u*u*a[0]+2*u*t*cy+t*t*b[0], (u*u*ax+2*u*t*cx+t*t*bx)/cs]); }
  return pts;
}

function mapaInicia(){
  mapa = L.map("m-mapa", {zoomControl:false, minZoom:3, maxZoom:18, zoomSnap:.25, maxBounds:[[24,-28],[64,44]], maxBoundsViscosity:.7});
  L.control.zoom({position:"bottomright", zoomInTitle:"Aproximar", zoomOutTitle:"Afastar"}).addTo(mapa);
  L.tileLayer(FUNDO, {attribution:"Esri, HERE, Garmin, OpenStreetMap", maxZoom:18}).addTo(mapa);
  // o caminho
  mRota = L.layerGroup().addTo(mapa);
  mTrechos().forEach(t => {
    const voo = t.tipo === "aviao", A = CENTRO[t.a], B = CENTRO[t.b];
    const pts = voo ? mArco(A, B, CURVA[`${t.a}>${t.b}`] || .15) : [A, B];
    if (!voo) L.polyline(pts, {color:"#fff", weight:7, opacity:.75, interactive:false}).addTo(mRota);
    L.polyline(pts, {color:"#101828", weight: voo ? 3.5 : 3, dashArray: voo ? "1 8" : null, lineCap:"round", interactive:false}).addTo(mRota);
    const texto = `<b>${NOME[t.a]} → ${NOME[t.b]}</b><br>${mQuando(t)}`;
    L.polyline(pts, {weight:24, opacity:0}).addTo(mRota).bindPopup(texto);
    const meio = pts.length > 2 ? pts[pts.length >> 1] : [(A[0]+B[0])/2, (A[1]+B[1])/2];
    mSelos.push({A, B, m: L.marker(meio, {icon: L.divIcon({className:"", html:`<div class="selo">${ICO_PERNA[t.tipo]}</div>`, iconSize:[22,22], iconAnchor:[11,11]})}).bindPopup(texto)});
  });
  // as cidades (de longe) e os lugares (de perto)
  mCids = L.layerGroup(); mLug = L.layerGroup();
  G.cidades.forEach(([c, nome]) => {
    const n = PARADAS.map((p,i) => p[0]===c ? i+1 : 0).filter(Boolean).join("·");
    const html = `<div class="cid lado-${LADO[c]}" style="--c:${HEX[c]}"><span class="cid-p">${n}</span><span class="cid-t"><b>${nome}</b><small>${noitesDe(c).replace(" na volta","")}</small></span></div>`;
    L.marker(CENTRO[c], {icon: L.divIcon({className:"", html, iconSize:[0,0]}), title:nome, zIndexOffset:500})
      .addTo(mCids).on("click", () => mapaIr(c, true));
  });
  mapaPinos();
  mapa.on("zoomend", mapaZoom);
  mapa.on("moveend", mapaOnde);
}
// os pinos de todas as cidades, numerados na ordem da lista de cada uma
function mapaPinos(){
  mLug.clearLayers(); mPinos = {};
  G.cidades.forEach(([c]) => {
    const ls = mLista(c), pts = ls.map(x => [x.lat, x.lng]);
    (G.estacoes[c]||[]).forEach(([n,la,lo]) => {
      if (pts.some(p => mDist(p,[la,lo]) < 600) || ["verona","innsbruck"].includes(c))
        L.marker([la,lo],{icon:L.divIcon({className:"",html:'<div class="pin-m">M</div>',iconSize:[18,18],iconAnchor:[9,9]})}).addTo(mLug).bindTooltip(n);
    });
    ls.forEach((x,k) => {
      mPinos[x.id] = L.marker([x.lat,x.lng],{zIndexOffset:1000,icon:L.divIcon({className:"",html:`<div class="pin" style="background:${mCor(x)}">${k+1}</div>`,iconSize:[28,28],iconAnchor:[14,14]})})
        .addTo(mLug).bindPopup(`<b>${esc(curto(x.nome))}</b><br><a href="#" data-ficha="${x.id}">Detalhes</a>`)
        .on("click", () => mapaMarca(x.id));
    });
  });
}
function mapaMarca(id){ document.querySelectorAll("#m-lista .it").forEach(b => b.classList.toggle("on", b.dataset.id===id)); }
// troca cidades por lugares conforme o zoom; na rua o caminho some (a linha só liga centro a centro);
// o selo do avião/trem só aparece quando o trecho tem espaço para ele
function mapaZoom(){
  const z = mapa.getZoom(), perto = z >= Z_PERTO;
  mapa[perto ? "addLayer" : "removeLayer"](mLug); mapa[perto ? "removeLayer" : "addLayer"](mCids);
  mapa[z > Z_PERTO + 1 ? "removeLayer" : "addLayer"](mRota);
  mSelos.forEach(s => { const cabe = !perto && mapa.latLngToLayerPoint(s.A).distanceTo(mapa.latLngToLayerPoint(s.B)) > 84; mapa[cabe ? "addLayer" : "removeLayer"](s.m); });
}
// depois de arrastar ou dar zoom: qual cidade está no centro? (nenhuma = a viagem toda)
function mapaOnde(){
  mapaZoom();
  let c = null;
  if (mapa.getZoom() >= Z_PERTO){ const m = mapa.getCenter(); let perto = 12e4;
    for (const k in CENTRO){ const d = mDist([m.lat, m.lng], CENTRO[k]); if (d < perto){ perto = d; c = k; } } }
  if (c === mCid) return;
  mCid = c; if (c) guardaCidade(c);
  mapaFolha(); mapaEndereco();
}
function mapaEndereco(){ if (location.hash.startsWith("#/mapa")) history.replaceState(null, "", "#/mapa" + (mCid ? "/"+mCid : "")); }
// leva o mapa para uma cidade (ou para a viagem toda, sem cidade)
function mapaIr(c, anima){
  mCid = c || null; if (c) guardaCidade(c);
  mapaFolha(); mapaEndereco(); mapa.closePopup();
  // numa cidade o zoom nunca fica abaixo de Z_PERTO, senão os lugares não apareceriam
  const voa = anima && !mCalmo(), ir = (pts, o) => { const t = mapa._getBoundsCenterZoom(L.latLngBounds(pts), o), z = c ? Math.max(t.zoom, Z_PERTO) : t.zoom;
    voa ? mapa.flyTo(t.center, z, {duration:1.1}) : mapa.setView(t.center, z, {animate:false}); };
  if (!c) return ir(Object.values(CENTRO), {paddingTopLeft:[38,86], paddingBottomRight:[44,64]});
  // enquadra o centro da cidade; bate-voltas (Veneza, Swarovski, Toledo) continuam marcados, fora do quadro
  const pts = mLista(c).map(x => [x.lat, x.lng]).filter(p => mDist(p, CENTRO[c]) < 7000);
  ir(pts.length > 1 ? pts : [CENTRO[c], CENTRO[c]], {paddingTopLeft:[30,70], paddingBottomRight:[30,50], maxZoom: pts.length > 1 ? 15 : 13});
}
// a folha: as paradas da viagem ou os lugares da cidade
function mapaFolha(){
  const c = mCid, nav = document.getElementById("m-cidades"), lista = document.getElementById("m-lista"), tipos = document.getElementById("m-tipos");
  document.documentElement.style.setProperty("--cor", c ? HEX[c] : "#b45309");
  nav.innerHTML = [["","Viagem toda"], ...G.cidades].map(([k,n]) => `<button type="button" class="${k===(c||"")?"on":""}" data-c="${k}">${n}</button>`).join("");
  nav.querySelectorAll("button").forEach(b => b.onclick = () => mapaIr(b.dataset.c || null, true));
  const on = nav.querySelector(".on"); if (on) nav.scrollLeft = on.offsetLeft - (nav.clientWidth - on.offsetWidth) / 2;
  tipos.hidden = !c;
  if (!c){
    const tr = mTrechos();
    document.getElementById("m-titulo").textContent = "A viagem toda";
    document.getElementById("m-sub").textContent = `${G.cidades.length} cidades · ${PARADAS.reduce((s,p) => s + noites(p[1],p[2]), 0)} noites`;
    lista.innerHTML = PARADAS.map(([k,a,b],i) => { const n = noites(a,b);
      return `<button type="button" class="it" data-c="${k}"><span class="n" style="background:${HEX[k]}">${i+1}</span><span><b>${NOME[k]}</b><small>${n} ${n===1?"noite":"noites"} · ${periodo(a,b)}</small></span></button>`
        + (tr[i] ? `<p class="perna">${ICO_PERNA[tr[i].tipo]}${mQuando(tr[i])}</p>` : ""); }).join("");
    lista.querySelectorAll(".it").forEach(b => b.onclick = () => { mapaIr(b.dataset.c, true); scrollTo({top:0, behavior:"smooth"}); });
    return;
  }
  const todos = ideias(c).filter(x => x.lat && x.tipo !== "info"), conta = t => todos.filter(x => t==="tudo" || x.tipo===t).length, ls = mLista(c);
  tipos.innerHTML = [["tudo","Tudo"],["ver","Para ver"],["comer","Para comer"]]
    .map(([k,n]) => `<button type="button" class="${k===mTipo?"on":""}" data-t="${k}">${n} <span>${conta(k)}</span></button>`).join("");
  tipos.querySelectorAll("button").forEach(b => b.onclick = () => { mTipo = b.dataset.t; if (mapa) mapaPinos(); mapaFolha(); });
  document.getElementById("m-titulo").textContent = NOME[c];
  document.getElementById("m-sub").textContent = `${noitesDe(c)} · ${ls.length} ${ls.length===1?"lugar":"lugares"} no mapa`;
  lista.innerHTML = ls.map((x,k) =>
    `<button type="button" class="it" data-id="${x.id}"><span class="n" style="background:${mCor(x)}">${k+1}</span><span><b>${esc(curto(x.nome))}</b><small>${esc(umaFrase(x.pedir) || umaFrase(x.categoria) || umaFrase(x.dica))}</small></span></button>`).join("")
    || '<p class="fraco">Nada no mapa com esse filtro.</p>';
  lista.querySelectorAll(".it").forEach(b => b.onclick = () => { const x = porId[b.dataset.id]; if (!mapa) return;
    mapa.flyTo([x.lat,x.lng], 16, {duration:.5, animate:!mCalmo()}); mPinos[x.id].openPopup(); mapaMarca(x.id); scrollTo({top:0, behavior:"smooth"}); });
}
// c = cidade pedida no endereço. Sem cidade: a viagem toda na primeira vez; depois, o mapa fica onde foi deixado.
function renderMapa(c){
  if (!window.L){ mCid = c; mapaFolha(); return; }
  const novo = !mapa;
  if (novo) mapaInicia();
  mapa.invalidateSize();
  if (c || novo) mapaIr(c, false); else mapaFolha();
  mapaZoom();
}
