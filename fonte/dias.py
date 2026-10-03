# -*- coding: utf-8 -*-
"""O DIA A DIA do guia — escrito a mao, conferido contra os dias de fechamento.

Cada bloco cita lugares por um PEDACO DO NOME (`refs`). O `build.py` casa esse
pedaco com a pesquisa da cidade e FALHA se nao achar ou se achar mais de um —
assim um lugar renomeado na pesquisa nao some do roteiro em silencio.

Regras que moldaram a ordem (todas da pesquisa de 30/09/2026):
  - Domingo 21/02 em Roma: Vaticano, Testaccio, CasaManco, Suppli Roma,
    Roscioli, Peroni e Formula 1 fecham. Trapizzino, Emma e Da Fortunata abrem.
  - Segunda 22/02: Galleria Borghese e Castel Sant'Angelo fecham -> Roma Antiga.
  - Terca 23/02: Il Grottino fecha. Retirada dos ingressos da audiencia do Papa
    e' terca 15h-19h no Portao de Bronze -> Vaticano na terca.
  - Innsbruck: museu do Telhado de Ouro fecha segunda no inverno -> domingo.
  - Viena: Kunsthistorisches e Schnitzelwirt fecham segunda.
  - Budapeste: Sinagoga fecha sabado e fecha cedo sexta -> quinta.
  - Madri: Rastro e a Euromania do 100 Montaditos (tudo a 1 euro) so domingo
    07/03. Troca da guarda do Palacio Real quarta e sabado 11h-14h -> sab 20/02.
    Segunda 08/03 (Dia da Mulher): marchas no centro a noite -> sair 17h30.
"""

DIAS = [
  dict(data="2027-02-18", cidade="madri", titulo="Voo e chegada", noite="Madri",
    blocos=[
      ("Dia", "CA898: Guarulhos 08:25 → Madri 22:35 (T1).", []),
      ("Do aeroporto", "<b>Táxi</b> na saída, pedindo carro para 5; ou <b>Uber</b> no estacionamento, subindo a rampa à direita.", []),
      ("Se bater fome", "Tudo fechado: peçam no Uber Eats no caminho. Perto de Sol, a San Ginés não fecha.", ["San Ginés"]),
    ]),
  dict(data="2027-02-19", cidade="madri", titulo="Retiro, Letras e o Prado de graça", noite="Madri",
    blocos=[
      ("Manhã", "Retiro → Puerta de Alcalá → Cibeles. Suba ao mirante do CentroCentro.", ["Retiro", "Puerta de Alcalá", "Cibeles"]),
      ("Almoço", "Tapas no balcão, no Barrio de las Letras.", ["Cervecería Cervantes"]),
      ("Tarde", "Letras a pé. Às 17h30, fila do Prado: <b>grátis das 18h às 20h</b>.", ["Acid Café", "Prado"]),
      ("Noite", "Gambas al ajillo perto de Sol.", ["Casa del Abuelo"]),
    ]),
  dict(data="2027-02-20", cidade="madri", titulo="Gran Vía de manhã, Palácio e Madri dos Áustrias", noite="Madri",
    blocos=[
      ("Manhã", "<b>Gran Vía é de dia</b>: Primark, Zara e o terraço do Corte Inglés. Lojas abrem às 10h.", ["Gran Vía (+", "Callao — terraço"]),
      ("Meio-dia", "Palácio Real antes das 13h: <b>troca da guarda aos sábados, 11h–14h</b>.", ["Palacio Real", "Sabatini", "Almudena"]),
      ("Almoço", "Às 14h, na Cava Baja (La Latina). O Botín pede reserva com semanas.", ["Taberna La Concha", "Botín"]),
      ("Tarde", "Calle Mayor → Plaza Mayor → Sol, petiscando no San Miguel.", ["Puerta del Sol", "Mercado de San Miguel"]),
      ("Pôr do sol (opcional)", "Debod às ~18h50; voltem pelo Palácio, não pela Gran Vía.", ["Templo de Debod"]),
      ("Noite", "Jantar em La Latina ou Huertas.", ["Casa del Abuelo"]),
    ]),
  dict(data="2027-02-21", cidade="roma", titulo="Voo para Roma e o centro a pé", noite="Roma",
    blocos=[
      ("Manhã", "Iberia 08:45 → Fiumicino 11:10. Até o centro, <b>táxi de €55 fixo</b> (peçam de 6–7 lugares).", []),
      ("Atenção", "<b>Domingo muita coisa fecha</b>: hoje é dia de rua e praça.", []),
      ("Tarde", "Panteão, Navona e Trevi. <b>A Trevi cobra €2 das 9h às 22h</b>; depois é grátis.", ["Panteão", "Piazza Navona", "Gelateria del Teatro", "Trevi"]),
      ("Noite", "Pizza ou massa perto do Panteão; as duas abrem domingo.", ["Emma", "Fortunata"]),
      ("Opcional", "Lazio × Napoli no Olímpico (data provisória).", ["Stadio Olimpico"]),
    ]),
  dict(data="2027-02-22", cidade="roma", titulo="Roma Antiga", noite="Roma",
    blocos=[
      ("Manhã", "Coliseu às 8h30, depois Fórum e Palatino. Contem 4–5 horas.", ["Coliseu"]),
      ("Almoço", "Ao lado do Coliseu; reservem para 5.", ["Taverna dei Quaranta"]),
      ("Tarde", "Circo Massimo, terraço do Vittoriano e sorvete em Monti.", ["Circo Massimo", "Vittoriano", "Fatamorgana"]),
      ("Noite", "Pizza romana em Testaccio (fecha terça).", ["Il Grottino"]),
      ("Por que hoje", "Borghese e Castel Sant'Angelo fecham na segunda.", []),
    ]),
  dict(data="2027-02-23", cidade="roma", titulo="Vaticano e Prati", noite="Roma",
    blocos=[
      ("Manhã", "Museus Vaticanos no 1º horário, depois São Pedro e a cúpula.", ["Museus Vaticanos", "Basílica de São Pedro"]),
      ("Almoço", "Pizza al taglio a 10 min dos Museus.", ["Pizzarium", "Panificio Bonci"]),
      ("Tarde", "Castel Sant'Angelo e sorvete em Prati. Vão à audiência? Retirem os ingressos hoje, 15h–19h.", ["Audiência", "Castel Sant'Angelo", "Gracchi"]),
      ("Noite", "San Lorenzo: pizzarias baratas, sem reserva.", ["Formula 1", "L'Economica"]),
    ]),
  dict(data="2027-02-24", cidade="roma", titulo="Papa, Testaccio e Trastevere", noite="Roma",
    blocos=[
      ("Manhã (opcional)", "Audiência do Papa. <b>São Pedro fica fechada até ela acabar.</b>", ["Audiência"]),
      ("Almoço", "Mercado de Testaccio até 13h.", ["Mercato di Testaccio", "CasaManco"]),
      ("Tarde", "Trastevere a pé, com supplì e sorvete.", ["Trastevere", "Supplì Roma", "Alla Scala", "Fiordiluna"]),
      ("Noite", "Jantar em Trastevere (reservem); trapizzino de saideira.", ["Rugantino", "Da Vittorio", "Trapizzino"]),
    ]),
  dict(data="2027-02-25", cidade="roma", titulo="Borghese, Spagna e o centro das compras", noite="Roma",
    blocos=[
      ("Manhã", "Borghese às 9h (<b>reserva obrigatória</b>), Pincio e Piazza del Popolo.", ["Galleria Borghese", "Sensorio"]),
      ("Almoço", "Schiacciata na Via del Corso.", ["Via del Corso"]),
      ("Tarde", "Spagna e tiramisù; Campo de' Fiori e Roscioli.", ["Piazza di Spagna", "Pompi", "Campo de' Fiori", "Roscioli"]),
      ("Noite", "Cervejaria perto da Trevi; reservem para 5.", ["Peroni"]),
    ]),
  dict(data="2027-02-26", cidade="verona", titulo="Trem para Verona", noite="Verona",
    blocos=[
      ("Manhã", "Italo 8956: Roma 08:20 → Verona 11:38. Centro a 20 min a pé.", []),
      ("Tarde", "Arena, Giulietta (<b>horário marcado</b>), Erbe e Torre dei Lamberti no fim do dia.", ["Arena", "Giulietta", "Piazza delle Erbe e", "Lamberti"]),
      ("Noite", "Menu fixo no al Duca, ou pizza barata.", ["al Duca", "Du de Cope"]),
    ]),
  dict(data="2027-02-27", cidade="verona", titulo="Bate-volta a Veneza", noite="Verona",
    blocos=[
      ("Dia", "Trem para Veneza (~1h25, €11–14 o trecho). Taxa de acesso: confirmem em janeiro.", ["Veneza"]),
      ("Alternativa", "Ficar em Verona: Castelvecchio, San Zeno e o Castel San Pietro no pôr do sol.", ["Castelvecchio", "San Zeno", "Castel San Pietro"]),
      ("Noite", "Jantar em Verona (o Pompiere pede reserva).", ["Al Pompiere", "Sottoriva"]),
    ]),
  dict(data="2027-02-28", cidade="innsbruck", titulo="Alpes pelo Brenner", noite="Innsbruck",
    blocos=[
      ("Manhã", "Railjet 88: Verona 09:01 → Innsbruck 12:32, pelos Alpes.", []),
      ("Tarde", "Telhado de Ouro hoje (<b>fecha segunda</b>), Hofburg e a Maria-Theresien-Strasse.", ["Telhado de Ouro", "Hofburg Innsbruck", "Maria-Theresien"]),
      ("Noite", "Comida tirolesa; reservem para 5.", ["Gasthaus Goldenes", "Stiftskeller"]),
    ]),
  dict(data="2027-03-01", cidade="viena", titulo="Nordkette e trem para Viena", noite="Viena",
    blocos=[
      ("Manhã", "Malas no guarda-volumes e manhã livre no centro. Voltem até 11h45.", []),
      ("Tarde", "Railjet: Innsbruck 13:58 → Viena 18:32.", []),
      ("Noite", "O schnitzel maior que o prato.", ["Figlmüller"]),
    ]),
  dict(data="2027-03-02", cidade="viena", titulo="Kipferl, Schönbrunn e a Prefeitura no gelo", noite="Viena",
    blocos=[
      ("Café da manhã", "Kipferl, o avô do croissant, às 7h30. Ao lado: o Monumento contra a Guerra e o Fascismo e a Ópera.", ["Joseph Brot", "Mahnmal", "Wiener Staatsoper (Ópera"]),
      ("Manhã", "U4 até Schönbrunn: palácio às 8h30 e a Gloriette.", ["Schönbrunn"]),
      ("Almoço", "Naschmarkt.", ["Naschmarkt"]),
      ("Tarde", "Café Sperl e Kunsthistorisches (ou o MuseumsQuartier).", ["Sperl", "Kunsthistorisches", "MuseumsQuartier"]),
      ("Fim de tarde", "Prefeitura iluminada e a <b>pista de gelo</b> da Rathausplatz, até as 22h.", ["Eistraum", "Wiener Rathaus"]),
      ("Jantar", "<b>Kaiserschmarrn</b>, a sobremesa do imperador; reservem o Landtmann.", ["Landtmann", "Heindl"]),
    ]),
  dict(data="2027-03-03", cidade="viena", titulo="Klimt e o centro imperial", noite="Viena",
    blocos=[
      ("Manhã", "Belvedere às 9h: O Beijo, de Klimt.", ["Belvedere"]),
      ("11h", "Karlskirche, a 15 min a pé.", ["Karlskirche"]),
      ("Almoço", "Sanduichinhos vienenses; Kipferl de forno a lenha ao lado.", ["Trzesniewski", "Gragger"]),
      ("13h", "Stephansdom, Graben e mais um croissant para comparar.", ["Catedral de Santo Estêvão", "Graben", "Felber"]),
      ("15h", "Peterskirche: <b>órgão grátis às 15h</b>. Depois, o Kohlmarkt.", ["Peterskirche", "Kohlmarkt"]),
      ("15h45", "Museu Sisi (horário marcado). Contem 1h30–2h.", ["Museu Sisi"]),
      ("Lanche", "Demel, até 19h.", ["Demel"]),
      ("Noite", "Adega medieval ou a roda-gigante; Buchteln no Hawelka. O trem sai 07:40.", ["Zwölf-Apostelkeller", "Riesenrad", "Hawelka"]),
      ("Opcional", "Visita grátis à Prefeitura só às 13h, com inscrição: troca com a Stephansdom.", ["Wiener Rathaus"]),
    ]),
  dict(data="2027-03-04", cidade="budapeste", titulo="Trem para Budapeste e o bairro judeu", noite="Budapeste",
    blocos=[
      ("Manhã", "Railjet: Viena 07:40 → Budapest-Keleti 10:35.", []),
      ("Tarde", "Sinagoga hoje (<b>fecha sábado</b>), bairro judeu e o mirante da Basílica.", ["Sinagoga", "Szimpla", "Basílica de Santo Estêvão"]),
      ("Noite", "Cruzeiro no Danúbio e jantar barato.", ["Cruzeiro", "Frici Papa"]),
      ("Dinheiro", "Paguem em florim (HUF) e recusem a conversão na maquininha.", []),
    ]),
  dict(data="2027-03-05", cidade="budapeste", titulo="Parlamento, Buda e os banhos", noite="Budapeste",
    blocos=[
      ("Manhã", "Parlamento (reservado), Sapatos no Danúbio e a Ponte das Correntes.", ["Parlamento", "Sapatos"]),
      ("Almoço", "Mercado Central: lángos no andar de cima.", ["Mercado Central", "Retró Lángos", "Kisharang"]),
      ("Tarde", "Funicular ao Castelo, Bastião e Matias; banhos Széchenyi no fim do dia.", ["Castelo de Buda", "Bastião", "Igreja de Matias", "Széchenyi"]),
      ("Noite", "Goulash.", ["Hungarikum"]),
    ]),
  dict(data="2027-03-06", cidade="madri", titulo="Voo de volta a Madri", noite="Madri",
    blocos=[
      ("Manhã", "Iberia 11:10 → Madri 14:30. Saiam às 8h30, de Bolt XL ou táxi.", []),
      ("Tarde", "Táxi até a hospedagem e recolham as malas.", []),
      ("Noite", "Jantar leve em La Latina ou Lavapiés.", ["San Fernando"]),
    ]),
  dict(data="2027-03-07", cidade="madri", titulo="Rastro, montaditos a €1 e Toledo", noite="Madri",
    blocos=[
      ("Manhã", "El Rastro, a feira gigante de domingo (9h–15h).", ["El Rastro"]),
      ("Almoço", "<b>Domingo, quase tudo a €1</b> no 100 Montaditos, colado ao Rastro.", ["100 Montaditos"]),
      ("Tarde", "Toledo (33 min de trem, comprem antes) ou tarde livre.", ["Toledo"]),
      ("Noite", "Tortilla em Tetuán.", ["Mercado de San Leopoldo", "Casa Dani"]),
    ]),
  dict(data="2027-03-08", cidade="madri", titulo="Último dia e voo para casa", noite=None,
    blocos=[
      ("Manhã", "Malas guardadas, Reina Sofía (Guernica) e compras.", ["Museo Reina Sofía", "Corte Inglés Preciados +"]),
      ("Tarde", "Palácio Real grátis para brasileiros, 16h–18h, se as malas já estiverem com vocês.", ["Palacio Real"]),
      ("Noite", "<b>Saiam às 17h</b>, de táxi: marchas do Dia da Mulher no centro. CA897 às 22:30.", []),
    ]),
]

# O que fica de fora do dia a dia, mas esta na lista do Lucas: aparece na pagina
# da cidade com o motivo.
FORA = {
  "roma": [
    ("Tiramisù di Forattini", "Fica em Torrenova, ~45 min de metrô C do centro. O Pompi (25/02) é a alternativa central."),
    ("Trattoria Guerra", "Nomentano, fora do caminho e com ~15 lugares. Vale se sobrar uma noite."),
    ("Grano, Frutta e Farina", "Campo Marzio: encaixa no dia 25/02, perto da Piazza di Spagna."),
    ("Il Pastaio", "Perto da Piazza Navona: encaixa no dia 21/02 ou 25/02."),
    ("I Caruso", "Perto da Via XX Settembre; talvez feche domingo. Encaixa no dia 23/02 a caminho de San Lorenzo."),
    ("San Crispino", "Pode ter fechado; confiram no Google Maps antes."),
    ("Maddalena", "A outra unidade do All'Antico Vinaio, ao lado do Panteão (21/02)."),
    ("Porta Maggiore", "Perto de San Lorenzo: dá para passar no dia 23/02 à noite."),
  ],
  "madri": [
    ("Kitchen 154", "Mercado de Vallehermoso (Chamberí). Fecha segunda e terça."),
    ("Hundred", "Hambúrguer em Chueca. Horário não confirmado."),
  ],
}


# DICAS DE QUEM JA FOI — palavras do Lucas, da viagem de fevereiro de 2026.
DICAS = {
  "madri": [
    "No aeroporto, dá para pedir táxi na saída para quantas pessoas precisar.",
    "Para pegar Uber: na rampa à direita, antes de sair para a rua, subam até o estacionamento.",
    "Chegando de noite, vai estar tudo fechado. Vejam algo perto ou peçam pelo Uber Eats.",
    "O metrô é barato, tranquilo e tem muitas linhas. Um cartão só serve para todo mundo.",
    "Tem muitos lockers (guarda-volumes) espalhados pela cidade.",
    "O Rastro, no domingo, é uma feira gigantesca que conecta quase a cidade inteira.",
    "A cidade é rápida de atravessar a pé: olhando em volta, quando você vê, já atravessou.",
    "O vento é frio nessa época.",
    "A Gran Vía é de manhã e à tarde (Primark etc.). À noite a região é movimentada demais para ficar dando bobeira.",
    "O tour do Santiago Bernabéu não compensa: caro demais para levar todo mundo.",
  ],
}
