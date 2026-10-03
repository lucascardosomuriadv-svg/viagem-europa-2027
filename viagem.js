// O que já está fechado: onde dormimos cada noite. Voos e trens ficam em conteudo.js (aba Passagens).
// Sem roteiro por dia (decisão do Lucas em 03/10/2026): as cidades só juntam ideias.

// [cidade, chega (ISO), sai (ISO)] — noites = sai − chega
const PARADAS = [
  ["madri", "2027-02-18", "2027-02-21"],
  ["roma", "2027-02-21", "2027-02-26"],
  ["verona", "2027-02-26", "2027-02-28"],
  ["innsbruck", "2027-02-28", "2027-03-01"],
  ["viena", "2027-03-01", "2027-03-04"],
  ["budapeste", "2027-03-04", "2027-03-06"],
  ["madri", "2027-03-06", "2027-03-08"],
];
const noites = (a, b) => Math.round((new Date(b + "T12:00:00Z") - new Date(a + "T12:00:00Z")) / 86400000);
// "21 → 26/02" ou "28/02 → 01/03"
const periodo = (a, b) => (a.slice(5, 7) === b.slice(5, 7) ? +a.slice(8) : a.slice(8, 10) + "/" + a.slice(5, 7)) + " → " + b.slice(8, 10) + "/" + b.slice(5, 7);
const estadias = c => PARADAS.filter(p => p[0] === c);
// texto curto das noites de uma cidade: "5 noites" ou "3 noites + 2 na volta"
function noitesDe(c){
  const l = estadias(c).map(p => noites(p[1], p[2]));
  if (l.length === 1) return `${l[0]} ${l[0] === 1 ? "noite" : "noites"}`;
  return `${l[0]} noites + ${l[1]} na volta`;
}
// ordem das ideias: a lista de vocês primeiro; depois o que a pesquisa achou mais forte; depois o resto
const DE_VOCES = /sua lista|seu mapa|lista da Camila/;
const pesoIdeia = (x, usados) => DE_VOCES.test(x.origem || "") * 2 + usados.has(x.id);
const ordemIdeias = usados => (a, b) => pesoIdeia(b, usados) - pesoIdeia(a, usados);
