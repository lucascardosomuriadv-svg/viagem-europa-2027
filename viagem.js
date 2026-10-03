// O que já está fechado: onde dormimos cada noite e como vamos de um lugar ao outro.
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
// [data, hora, avião|trem, de → para, quem, chegada]
const TRECHOS = [
  ["2027-02-17", "", "aviao", "Vitória → São Paulo", "", ""],
  ["2027-02-18", "08:25", "aviao", "São Paulo → Madri", "Air China CA898", "22:35"],
  ["2027-02-21", "08:45", "aviao", "Madri → Roma", "Iberia", ""],
  ["2027-02-26", "08:20", "trem", "Roma → Verona", "Italo", "11:38"],
  ["2027-02-28", "09:01", "trem", "Verona → Innsbruck", "ÖBB", "12:32"],
  ["2027-03-01", "13:58", "trem", "Innsbruck → Viena", "Railjet", "18:32"],
  ["2027-03-04", "07:40", "trem", "Viena → Budapeste", "Railjet", "10:35"],
  ["2027-03-06", "11:10", "aviao", "Budapeste → Madri", "Iberia", ""],
  ["2027-03-08", "22:30", "aviao", "Madri → São Paulo", "Air China CA897", "05:30"],
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
const ICO_TRECHO = {
  aviao: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 13.5 3 11l1.5-1.5 8 1 4-4.5a2.1 2.1 0 0 1 3 3l-4.5 4 1 8L14.5 22 12 14.5"/></svg>',
  trem: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M9 21l1.5-4M15 21l-1.5-4M9 14h.01M15 14h.01"/></svg>',
};
// ordem das ideias: a lista de vocês primeiro; depois o que a pesquisa achou mais forte; depois o resto
const DE_VOCES = /sua lista|seu mapa|lista da Camila/;
const pesoIdeia = (x, usados) => DE_VOCES.test(x.origem || "") * 2 + usados.has(x.id);
const ordemIdeias = usados => (a, b) => pesoIdeia(b, usados) - pesoIdeia(a, usados);
