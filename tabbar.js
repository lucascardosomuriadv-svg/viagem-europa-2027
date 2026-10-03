// A barra de abas, uma só para todas as páginas (antes cada página tinha a sua cópia e elas divergiam).
// A página diz qual aba é a dela em <body data-aba="…">; no index quem marca é a rota().
// Tudo dentro de uma função: não deixa nenhum nome solto que possa bater com os das páginas.
(function(){
  const nav = document.getElementById("tabbar"); if (!nav) return;
  const BARRA = [
    ["viagem", "Viagem", "index.html#/viagem", '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'],
    ["mapa", "Mapa", "index.html#/mapa", '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/>'],
    ["hospedagem", "Dormir", "hospedagens.html", '<path d="M3 18v-7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v7M3 15h18M3 18v2M21 18v2M7 9V6h10v3"/>'],
    ["passagens", "Passagens", "index.html#/passagens", '<path d="M10.5 13.5 3 11l1.5-1.5 8 1 4-4.5a2.1 2.1 0 0 1 3 3l-4.5 4 1 8L14.5 22 12 14.5"/>'],
    ["ingressos", "Ingressos", "index.html#/ingressos", '<path d="M4 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4zM14 6v12"/>'],
    ["comer", "Comer", "index.html#/comer", '<path d="M7 2v9a2 2 0 0 0 2 2v9M7 2v6M11 2v6M17 2c-2 2-2 6 0 8v12"/>'],
  ];
  const minha = document.body.dataset.aba || "";
  nav.innerHTML = BARRA.map(([k, nome, href, d]) =>
    `<a href="${href}" data-v="${k}" class="${k === minha ? "on" : ""}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${d}</svg>${nome}</a>`).join("");
})();
